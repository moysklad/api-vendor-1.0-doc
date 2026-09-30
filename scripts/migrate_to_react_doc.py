#!/usr/bin/env python3
"""One-off migration of Slate includes into react-doc-engine markdown."""

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INCLUDES = ROOT / "source" / "includes"
INCLUDE_ORDER = [
    "_1_getting_started.md",
    "_2_app_types.md",
    "_3_apps_requirements.md",
    "_4_development_and_publication.md",
    "_5.1_developer_guide_token_access_to_json_api.md",
    "_5.2_developer_guide_widgets.md",
    "_5.3_developer_guide_descriptor.md",
    "_6.1_vendor_api_1.0_authentication.md",
    "_6.2_vendor_api_1.0_processes.md",
    "_6.3_vendor_api_1.0_REST_vendorside.md",
    "_6.4_vendor_api_1.0_REST_moyskladside.md",
    "_7_developer_personal_account.md",
    "_8_changelog.md",
]

FILE_NAMES = {
    "Быстрый старт": "quick_start",
    "Как создать и опубликовать решение": "create_and_publish",
    "Порядок размещения решения в каталоге решений": "publication_order",
    "Визуальные материалы решения": "visual_materials",
    "Демо-решения": "demo_solutions",
    "Типы решений для каталога решений": "app_types",
    "Условия размещения решений": "placement_requirements",
    "Доступ по токену к JSON API": "json_api_token_access",
    "Работа с вебхуками": "webhooks",
    "Работа с дополнительными полями": "custom_fields",
    "Особенности доступа к некоторым функциям JSON API 1.2": "json_api_access_notes",
    "Окна (iframes)": "iframes",
    "Виджеты": "widgets",
    "Кастомные модальные окна": "custom_popups",
    "Контекст пользователя": "user_context",
    "Сервисы хост-окна": "host_window_services",
    "SDK для виджетов": "widget_sdk",
    "Ошибки при работе с виджетами": "widget_errors",
    "Ограничения для контента, загружаемого в виджетах": "widget_content_limits",
    "Кастомные кнопки": "custom_buttons",
    "Действия в сценариях": "scenario_actions",
    "Дескриптор решения": "solution_descriptor",
    "Примеры дескрипторов": "descriptor_examples",
    "Аутентификация взаимодействия по Vendor API": "authentication",
    "Процесс активации решения на аккаунте": "activation",
    "Процесс деактивации решения на аккаунте": "deactivation",
    "Процесс приостановки и возобновления работы решения на аккаунте": "suspend_and_resume",
    "Уведомления о дополнительных событиях": "additional_events",
    "Механизм Retry": "retry",
    "REST-эндпоинты на стороне разработчика решений": "vendor_endpoints",
    "REST-эндпоинты на стороне МоегоСклада": "moysklad_endpoints",
    "Личный кабинет разработчика": "developer_cabinet",
    "Список последних изменений": "changelog",
}
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FENCE_RE = re.compile(r"^```([A-Za-z0-9_-]+)?\s*$")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def unwrap_blockquotes(text):
    lines = text.splitlines()
    in_fence = False
    output = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if FENCE_RE.match(line):
            in_fence = not in_fence
            output.append(line)
            index += 1
            continue
        if not in_fence and (line.startswith("> ") or line == ">"):
            block = []
            while index < len(lines) and (lines[index].startswith("> ") or lines[index] == ">"):
                block.append(lines[index][2:] if lines[index].startswith("> ") else "")
                index += 1
            lookahead = index
            while lookahead < len(lines) and lines[lookahead].strip() == "":
                lookahead += 1
            fence = FENCE_RE.match(lines[lookahead]) if lookahead < len(lines) else None
            if fence and fence.group(1) in ("json", "shell"):
                output.extend(f"> {item}" if item else ">" for item in block)
            else:
                output.extend(block)
            continue
        output.append(line)
        index += 1
    return "\n".join(output) + "\n"


def convert_explicit_html_headings(text):
    lines = text.splitlines()
    in_fence = False
    converted = []
    pattern = re.compile(r"^<h([1-6]) id=\"[^\"]+\">(.*?)</h\1>$")
    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            converted.append(line)
            continue
        match = None if in_fence else pattern.match(line.strip())
        if match:
            converted.append(f"{'#' * int(match.group(1))} {match.group(2)}")
            continue
        converted.append(line)
    return "\n".join(converted) + "\n"


def rewrite_images(text):
    def replace(match):
        alt, target = match.group(1), match.group(2).strip()
        if re.fullmatch(r"[A-Za-z0-9_.-]+\.(png|jpe?g|gif|svg|webp)", target):
            target = f"images/{target}"
        return f"![{alt}]({target})"

    return IMAGE_RE.sub(replace, text)


def parse_nodes(text):
    nodes = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            nodes.append(("text", line))
            continue
        heading = None if in_fence else HEADING_RE.match(line)
        if heading:
            nodes.append(("heading", len(heading.group(1)), heading.group(2).strip()))
        else:
            nodes.append(("text", line))
    return nodes


def h2_sections(nodes):
    preamble = []
    sections = []
    current = None
    for node in nodes:
        if node[0] == "heading" and node[1] == 1:
            preamble.append(("text", f"**{node[2]}**"))
            preamble.append(("text", ""))
            continue
        if node[0] == "heading" and node[1] == 2:
            current = {"title": node[2], "nodes": []}
            sections.append(current)
            continue
        if current is None:
            preamble.append(node)
        else:
            current["nodes"].append(node)
    return preamble, sections


def render_nodes(nodes):
    rendered = []
    for node in nodes:
        if node[0] == "heading":
            rendered.append(f"{'#' * node[1]} {node[2]}")
        else:
            rendered.append(node[1])
    text = "\n".join(rendered).strip() + "\n"
    return text


def shift_page_heading(nodes, source_level, target_level):
    shifted = []
    changed = False
    for node in nodes:
        if node[0] == "heading" and not changed and node[1] == source_level:
            shifted.append(("heading", target_level, node[2]))
            changed = True
        else:
            shifted.append(node)
    return shifted


def split_h3(section):
    pages = []
    intro = []
    current = None
    for node in section["nodes"]:
        if node[0] == "heading" and node[1] == 3:
            current = {"title": node[2], "nodes": [("heading", 2, node[2])]}
            pages.append(current)
            continue
        if current is None:
            intro.append(node)
        else:
            current["nodes"].append(node)
    return intro, pages


def unique_path(directory, title, used):
    slug = FILE_NAMES.get(title)
    if not slug:
        raise SystemExit(f"No English file name for: {title}")
    candidate = f"{directory}/_{slug}.md"
    number = 2
    while candidate in used:
        candidate = f"{directory}/_{slug}_{number}.md"
        number += 1
    used.add(candidate)
    return candidate


def page_entry(title, path):
    return {"title": title, "level": 2, "folderPath": f"./{path}", "children": []}


def folder_entry(title, pages):
    return {
        "title": title,
        "level": 1,
        "folderPath": f"./{pages[0]['folderPath'].removeprefix('./')}",
        "children": pages,
    }


def write_page(path, nodes, folder_title=None, preamble=None):
    content_nodes = []
    if folder_title:
        content_nodes.append(("heading", 1, folder_title))
        content_nodes.append(("text", ""))
    if preamble:
        content_nodes.extend(preamble)
        if preamble and preamble[-1] != ("text", ""):
            content_nodes.append(("text", ""))
    content_nodes.extend(nodes)
    destination = ROOT / "md" / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_nodes(content_nodes), encoding="utf-8")


def main():
    raw = "\n".join((INCLUDES / name).read_text(encoding="utf-8") for name in INCLUDE_ORDER)
    prepared = convert_explicit_html_headings(rewrite_images(unwrap_blockquotes(raw)))
    preamble, sections = h2_sections(parse_nodes(prepared))
    by_title = {section["title"]: section for section in sections}
    if len(by_title) != len(sections):
        raise SystemExit(f"Duplicate h2 titles: {[section['title'] for section in sections]}")

    used = set()
    config = []

    getting_started_titles = [
        "Быстрый старт",
        "Как создать и опубликовать решение",
        "Порядок размещения решения в каталоге решений",
        "Визуальные материалы решения",
        "Демо-решения",
    ]
    pages = []
    for index, title in enumerate(getting_started_titles):
        section = by_title.pop(title)
        path = unique_path("getting_started", title, used)
        nodes = [("heading", 2, title), ("text", "")] + section["nodes"]
        write_page(path, nodes, "Быстрый старт" if index == 0 else None, preamble if index == 0 else None)
        pages.append(page_entry(title, path))
    config.append(folder_entry("Быстрый старт", pages))

    single_before_guides = [
        ("Типы решений для каталога решений", "app_types"),
        ("Условия размещения решений", "placement"),
    ]
    for title, directory in single_before_guides:
        section = by_title.pop(title)
        path = unique_path(directory, title, used)
        nodes = [("heading", 2, title), ("text", "")] + section["nodes"]
        write_page(path, nodes, title)
        config.append(folder_entry(title, [page_entry(title, path)]))

    split_folders = [
        ("Руководство разработчика", "developer_guide"),
        ("Vendor API 1.0", "vendor_api"),
    ]
    for title, directory in split_folders:
        section = by_title.pop(title)
        intro, h3_pages = split_h3(section)
        if not h3_pages:
            raise SystemExit(f"No h3 pages in {title}")
        pages = []
        for index, page in enumerate(h3_pages):
            path = unique_path(directory, page["title"], used)
            write_page(
                path,
                page["nodes"],
                title if index == 0 else None,
                intro if index == 0 else None,
            )
            pages.append(page_entry(page["title"], path))
        config.append(folder_entry(title, pages))

    single_after_guides = [
        ("Личный кабинет разработчика", "cabinet"),
        ("Список последних изменений", "changelog"),
    ]
    for title, directory in single_after_guides:
        section = by_title.pop(title)
        path = unique_path(directory, title, used)
        nodes = [("heading", 2, title), ("text", "")] + section["nodes"]
        write_page(path, nodes, title)
        config.append(folder_entry(title, [page_entry(title, path)]))

    if by_title:
        raise SystemExit(f"Unassigned sections: {sorted(by_title)}")

    (ROOT / "config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    image_destination = ROOT / "images"
    image_destination.mkdir(exist_ok=True)
    for image in (ROOT / "source" / "images").glob("*"):
        if image.is_file():
            shutil.copy2(image, image_destination / image.name)

    print(f"folders={len(config)} pages={sum(len(item['children']) for item in config)}")


if __name__ == "__main__":
    main()
