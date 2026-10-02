#!/usr/bin/env python3
"""Build hash-redirect-map.json and point Markdown links at react-doc-engine routes."""

import json
import re
import subprocess
import sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD_ROOT = ROOT / "md"
CONFIG_PATH = ROOT / "config.json"
MAP_PATH = ROOT / "hash-redirect-map.json"
SLUGIFY = ROOT.parent / "react-doc-engine" / "node_modules" / "slugify" / "slugify.js"
DOC_TITLE = "Документация разработчика решений для Каталога решений МойСклад"
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FENCE_RE = re.compile(r"^```")
LINK_RE = re.compile(r"(?<!!)\]\(#([^)\s]+)\)")
IMAGE_RE = re.compile(r"(!\[[^\]]*\]\()(?!https?:|/)(?!\./)(images/)")


def normalize(text):
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", "", text))).strip()


def transform_markdown_path_to_url(file_name):
    normalized = file_name.removeprefix("./").removesuffix(".md")
    if normalized.startswith("_"):
        normalized = normalized[1:]
    normalized = re.sub(r"/_+", "/", normalized)
    return normalized.replace("_", "-")


def slugify_many(texts):
    script = (
        "const slugify=require(process.argv[1]);"
        "let data='';process.stdin.on('data',c=>data+=c);"
        "process.stdin.on('end',()=>{for (const line of data.split('\\n').slice(0,-1))"
        "console.log(slugify(line,{lower:true,strict:true}));});"
    )
    completed = subprocess.run(
        ["node", "-e", script, str(SLUGIFY)],
        input="".join(f"{text}\n" for text in texts),
        text=True,
        check=True,
        capture_output=True,
    )
    return completed.stdout.splitlines()


def production_headings(html_path):
    html = Path(html_path).read_text(encoding="utf-8", errors="replace")
    matches = re.findall(
        r"<h([1-6])[^>]*\bid=[\"']([^\"']+)[\"'][^>]*>(.*?)</h\1>",
        html,
        flags=re.I | re.S,
    )
    return [
        {"level": int(level), "id": heading_id, "text": normalize(text)}
        for level, heading_id, text in matches
    ]


def new_headings():
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    files = []
    for folder in config:
        for child in folder["children"]:
            relative = child["folderPath"].removeprefix("./")
            if relative not in files:
                files.append(relative)
    headings = []
    for relative in files:
        in_fence = False
        for line in (MD_ROOT / relative).read_text(encoding="utf-8").splitlines():
            if FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            match = HEADING_RE.match(line)
            if match:
                headings.append({
                    "file": relative,
                    "url": transform_markdown_path_to_url(relative),
                    "level": len(match.group(1)),
                    "text": normalize(match.group(2)),
                })
    slugs = slugify_many(heading["text"] for heading in headings)
    if len(slugs) != len(headings):
        raise SystemExit("Slugify returned an unexpected number of headings")
    for heading, slug in zip(headings, slugs):
        heading["anchor"] = f"{heading['level']}-{slug}"
        heading["route"] = f"#/{heading['url']}#{heading['anchor']}"
    return headings


def align(old_headings, current_headings):
    mapping = []
    new_index = 0
    for old in old_headings:
        if old["text"] == DOC_TITLE:
            mapping.append((old, current_headings[0]))
            continue
        while new_index < len(current_headings):
            current = current_headings[new_index]
            if current["text"] == old["text"]:
                mapping.append((old, current))
                new_index += 1
                break
            previous = current_headings[new_index - 1] if new_index else None
            if previous and current["text"] == previous["text"]:
                new_index += 1
                continue
            raise SystemExit(
                "Cannot align headings:\n"
                f"old: {old['id']} | {old['text']}\n"
                f"new: {current['file']} | {current['text']}"
            )
        else:
            raise SystemExit(f"No new heading for old id {old['id']}: {old['text']}")
    return mapping


def rewrite_markdown(route_by_old_id):
    unresolved = []
    for path in MD_ROOT.rglob("*.md"):
        rewritten = []
        in_fence = False
        changed = False
        for line in path.read_text(encoding="utf-8").splitlines():
            if FENCE_RE.match(line):
                in_fence = not in_fence
                rewritten.append(line)
                continue
            if not in_fence:
                def replace(match):
                    anchor = match.group(1)
                    if anchor.startswith("/"):
                        return match.group(0)
                    route = route_by_old_id.get(anchor)
                    if route is None:
                        unresolved.append(f"{path.relative_to(ROOT)}: #{anchor}")
                        return match.group(0)
                    return f"]({route})"

                updated = LINK_RE.sub(replace, line)
                updated = IMAGE_RE.sub(r"\1./\2", updated)
                changed = changed or updated != line
                rewritten.append(updated)
            else:
                rewritten.append(line)
        if changed:
            path.write_text("\n".join(rewritten) + "\n", encoding="utf-8")
    return unresolved


def heading_routes():
    return {heading["route"] for heading in new_headings()}


def check():
    route_map = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    routes = heading_routes()
    missing_targets = [f"{old} -> {new}" for old, new in route_map.items() if new not in routes]
    old_links = []
    broken_links = []
    for path in MD_ROOT.rglob("*.md"):
        in_fence = False
        for line in path.read_text(encoding="utf-8").splitlines():
            if FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for match in LINK_RE.finditer(line):
                anchor = match.group(1)
                if anchor.startswith("/"):
                    route = f"#{anchor}"
                    if route not in routes:
                        broken_links.append(f"{path.relative_to(ROOT)}: {route}")
                else:
                    old_links.append(f"{path.relative_to(ROOT)}: #{anchor}")
    errors = []
    if missing_targets:
        errors.append("Redirect targets missing:\n" + "\n".join(missing_targets[:20]))
    if old_links:
        errors.append("Old internal links remain:\n" + "\n".join(old_links[:20]))
    if broken_links:
        errors.append("Broken new links:\n" + "\n".join(broken_links[:20]))
    if errors:
        raise SystemExit("\n\n".join(errors))
    print(f"ok redirects={len(route_map)} headings={len(routes)}")


def build(html_path):
    mapping = align(production_headings(html_path), new_headings())
    route_by_old_id = {old["id"]: current["route"] for old, current in mapping}
    MAP_PATH.write_text(json.dumps(route_by_old_id, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    unresolved = rewrite_markdown(route_by_old_id)
    if unresolved:
        raise SystemExit("Unresolved internal links:\n" + "\n".join(unresolved))
    check()


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--check":
        check()
        return
    if len(sys.argv) != 2:
        raise SystemExit("Usage: build_hash_redirect_map.py HTML | --check")
    build(sys.argv[1])


if __name__ == "__main__":
    main()
