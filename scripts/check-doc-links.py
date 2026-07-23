#!/usr/bin/env python3
"""Check documentation links in the built Middleman site."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urljoin, urlparse, urlsplit, urlunsplit
from urllib.request import Request, urlopen


SITE_ORIGIN = "http://docs.local"
LOCAL_HOSTS = {"docs.local", "localhost", "127.0.0.1", "::1"}
IGNORED_SCHEMES = {"mailto", "tel", "javascript", "data"}
IGNORED_EXTERNAL_PREFIXES = (
    ("api.moysklad.ru", "/api/remap/1.2"),
    ("apps-api.moysklad.ru", "/api/vendor/1.0"),
)
REQUEST_HEADERS = {
    "User-Agent": "doc-link-checker/1.0",
    "Accept": "*/*",
    "Accept-Encoding": "gzip",
}

LINK_RE = re.compile(r"<\s*a\b.*?</a\s*>", re.IGNORECASE | re.DOTALL)
HEADER_RE = re.compile(r"<\s*h[1-6]\b.*?>", re.IGNORECASE | re.DOTALL)
HREF_RE = re.compile(r"\bhref\s*=\s*([\"'])(.*?)\1", re.IGNORECASE | re.DOTALL)
ID_RE = re.compile(r"\bid\s*=\s*([\"'])(.*?)\1", re.IGNORECASE | re.DOTALL)


@dataclass
class CheckError:
    kind: str
    link: str
    detail: Optional[str] = None

    def __str__(self) -> str:
        if self.detail:
            return f"CheckError{{kind={self.kind}, link='{self.link}', detail='{self.detail}'}}"
        return f"CheckError{{kind={self.kind}, link='{self.link}'}}"


@dataclass
class Page:
    file_path: Path
    url: str
    content: str
    header_ids: Set[str]


@dataclass
class ExternalLinkResult:
    ok: bool
    detail: Optional[str]
    final_url: Optional[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check links in the built documentation site.")
    parser.add_argument("--site-dir", default="build", help="Path to the built documentation output.")
    parser.add_argument("--link-timeout", type=int, default=12, help="Seconds per external HTTP request.")
    parser.add_argument(
        "--skip-external",
        action="store_true",
        help="Skip checks for external http/https links.",
    )
    parser.add_argument("--verbose-found", action="store_true")
    parser.add_argument("--verbose-check", action="store_true")
    parser.add_argument("--show-content", action="store_true")
    return parser.parse_args()


def log(message: str) -> None:
    print(message, flush=True)


def encode_url_for_request(url: str) -> str:
    parts = urlsplit(url)
    if not parts.scheme:
        return quote(url, safe="/%:@!$&'()*+,;=?#[]")

    netloc = parts.netloc
    if parts.hostname:
        try:
            host = parts.hostname.encode("idna").decode("ascii")
        except UnicodeError:
            host = parts.hostname

        if ":" in host and not host.startswith("["):
            host = f"[{host}]"
        if parts.port:
            host = f"{host}:{parts.port}"

        userinfo = ""
        if parts.username:
            userinfo = quote(parts.username, safe="")
            if parts.password:
                userinfo += ":" + quote(parts.password, safe="")
            userinfo += "@"
        netloc = userinfo + host

    path = quote(parts.path, safe="/%:@!$&'()*+,;=")
    query = quote(parts.query, safe="/%:@!$&'()*+,;=?")
    fragment = quote(parts.fragment, safe="/%:@!$&'()*+,;=?")
    return urlunsplit((parts.scheme, netloc, path, query, fragment))


def request_url(url: str, timeout: int) -> Tuple[bool, Optional[str], Optional[str]]:
    request = Request(encode_url_for_request(url), headers=REQUEST_HEADERS)
    try:
        with urlopen(request, timeout=timeout) as response:
            status = getattr(response, "status", 200)
            if 200 <= status < 400:
                return True, None, response.geturl()
            return False, f"HTTP {status}", response.geturl()
    except HTTPError as error:
        final_url = getattr(error, "url", url)
        if 300 <= error.code < 400:
            return True, None, final_url
        return False, f"HTTP {error.code}: {error.reason}", final_url
    except (URLError, TimeoutError, OSError, UnicodeError) as error:
        return False, str(error), url


def iter_links(content: str) -> Iterable[str]:
    for match in LINK_RE.finditer(content):
        yield match.group(0)


def extract_value(markup: str, pattern: re.Pattern[str]) -> Optional[str]:
    match = pattern.search(markup)
    if not match:
        return None
    return match.group(2)


def has_attr(markup: str, name: str, value: str) -> bool:
    pattern = re.compile(rf"\b{name}\s*=\s*([\"']){re.escape(value)}\1", re.IGNORECASE | re.DOTALL)
    return pattern.search(markup) is not None


def has_class(markup: str, class_name: str) -> bool:
    class_value = extract_value(markup, re.compile(r"\bclass\s*=\s*([\"'])(.*?)\1", re.IGNORECASE | re.DOTALL))
    if class_value is None:
        return False
    classes = class_value.split()
    return class_name in classes


def is_intentional_placeholder_link(link: str, href: Optional[str]) -> bool:
    if href == "#":
        return has_attr(link, "id", "nav-button") or re.search(
            r"\bdata-language-name\s*=",
            link,
            re.IGNORECASE | re.DOTALL,
        ) is not None

    if href == "":
        return has_class(link, "toc-h1") and has_class(link, "toc-link")

    return False


def parse_header_ids(content: str) -> Set[str]:
    header_ids: Set[str] = set()
    duplicates: Set[str] = set()

    for header in HEADER_RE.finditer(content):
        markup = header.group(0)
        match = ID_RE.search(markup)
        if match is None:
            raise RuntimeError(f"Broken header (id not found): {markup}")

        header_id = match.group(2)
        if header_id in header_ids:
            duplicates.add(header_id)
        header_ids.add(header_id)

    if duplicates:
        duplicate_list = ", ".join(sorted(duplicates))
        raise RuntimeError(f"There are duplicate ids in some header(s): {duplicate_list}")

    return header_ids


def find_html_files(site_dir: Path) -> List[Path]:
    return sorted(path for path in site_dir.rglob("*.html") if path.is_file())


def page_url_for_file(file_path: Path, site_dir: Path) -> str:
    relative_path = file_path.relative_to(site_dir).as_posix()
    if relative_path == "index.html":
        return f"{SITE_ORIGIN}/"
    if relative_path.endswith("/index.html"):
        return f"{SITE_ORIGIN}/{relative_path[:-10]}"
    return f"{SITE_ORIGIN}/{relative_path}"


def load_page(file_path: Path, site_dir: Path, cache: Dict[Path, Page]) -> Page:
    if file_path in cache:
        return cache[file_path]

    content = file_path.read_text(encoding="utf-8", errors="replace")
    page = Page(
        file_path=file_path,
        url=page_url_for_file(file_path, site_dir),
        content=content,
        header_ids=parse_header_ids(content),
    )
    cache[file_path] = page
    return page


def fragment_exists(fragment: str, header_ids: Set[str]) -> bool:
    return fragment in header_ids or unquote(fragment) in header_ids


def resolve_local_file(site_dir: Path, url: str) -> Optional[Path]:
    parsed = urlparse(url)
    raw_path = unquote(parsed.path or "/")
    trimmed_path = raw_path.lstrip("/")

    candidates: List[Path] = []
    if not trimmed_path:
        candidates.append(site_dir / "index.html")
    else:
        base = site_dir / trimmed_path
        candidates.append(base)

        if trimmed_path.endswith("/"):
            stripped = trimmed_path.rstrip("/")
            candidates.append(site_dir / stripped / "index.html")
            candidates.append(site_dir / f"{stripped}.html")
        elif base.suffix != ".html":
            candidates.append(site_dir / f"{trimmed_path}.html")
            candidates.append(site_dir / trimmed_path / "index.html")

    seen: Set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.is_file():
            return candidate

    return None


def is_internal_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and (parsed.hostname or "").lower() in LOCAL_HOSTS


def is_intentional_external_reference(url: str) -> bool:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    path = parsed.path.rstrip("/")

    for ignored_host, ignored_prefix in IGNORED_EXTERNAL_PREFIXES:
        if host == ignored_host and (path == ignored_prefix or path.startswith(ignored_prefix + "/")):
            return True

    return False


def check_external_link(
    url: str,
    link: str,
    timeout: int,
    external_cache: Dict[str, ExternalLinkResult],
) -> Optional[CheckError]:
    if is_intentional_external_reference(url):
        return None

    if url in external_cache:
        result = external_cache[url]
    else:
        ok, error, final_url = request_url(url, timeout)
        result = ExternalLinkResult(ok=ok, detail=error, final_url=final_url)
        external_cache[url] = result

    if result.ok:
        return None

    detail = result.detail
    if result.final_url and result.final_url != url:
        detail = f"{detail}; final_url={result.final_url}"
    return CheckError("EXTERNAL_LINK_BROKEN", link, detail)


def check_internal_link(
    url: str,
    link: str,
    site_dir: Path,
    page_cache: Dict[Path, Page],
) -> Optional[CheckError]:
    parsed = urlparse(url)
    fragment = parsed.fragment
    target_file = resolve_local_file(site_dir, url)

    if target_file is None:
        return CheckError("INTERNAL_LINK_BROKEN", link, f"target page not found: {parsed.path or '/'}")

    try:
        target_page = load_page(target_file, site_dir, page_cache)
    except Exception as error:
        return CheckError("INTERNAL_LINK_BROKEN", link, str(error))

    if fragment and not fragment_exists(fragment, target_page.header_ids):
        return CheckError("INTERNAL_ANCHOR_BROKEN", link, fragment)

    return None


def check_links_for_page(
    page: Page,
    site_dir: Path,
    args: argparse.Namespace,
    page_cache: Dict[Path, Page],
    external_cache: Dict[str, ExternalLinkResult],
) -> Tuple[List[CheckError], int, int]:
    links = list(iter_links(page.content))
    if args.show_content:
        print(f"[{page.file_path.relative_to(site_dir)}] content:")
        print(page.content)
    if args.verbose_found:
        print(f"[{page.file_path.relative_to(site_dir)}] links={len(links)}")
        for link in links:
            print(link)

    errors: List[CheckError] = []
    skipped = 0

    for link in links:
        error: Optional[CheckError] = None
        href = extract_value(link, HREF_RE)

        if href is None or href.strip() == "":
            href = "" if href is not None else None
            if not is_intentional_placeholder_link(link, href):
                error = CheckError("LINK_HREF_ABSENT_OR_BLANK", link)
        else:
            href = href.strip()
            parsed_href = urlparse(href)

            if parsed_href.scheme.lower() in IGNORED_SCHEMES:
                skipped += 1
            elif href.startswith("#"):
                fragment = href[1:]
                if is_intentional_placeholder_link(link, href):
                    skipped += 1
                elif not fragment_exists(fragment, page.header_ids):
                    error = CheckError("INTERNAL_ANCHOR_BROKEN", link, fragment)
            else:
                absolute_url = urljoin(page.url, href)
                parsed_absolute = urlparse(absolute_url)

                if parsed_absolute.scheme not in {"http", "https"}:
                    skipped += 1
                elif is_internal_url(absolute_url):
                    error = check_internal_link(absolute_url, link, site_dir, page_cache)
                elif args.skip_external:
                    skipped += 1
                else:
                    error = check_external_link(absolute_url, link, args.link_timeout, external_cache)

        if args.verbose_check:
            print(link + " - " + (str(error) if error else "OK"))

        if error:
            errors.append(error)

    return errors, len(links), skipped


def main() -> int:
    args = parse_args()
    site_dir = Path(args.site_dir)

    if not site_dir.exists():
        raise RuntimeError(f"Site directory does not exist: {site_dir}")
    if not site_dir.is_dir():
        raise RuntimeError(f"Site path is not a directory: {site_dir}")

    pages = find_html_files(site_dir)
    if not pages:
        raise RuntimeError(f"No HTML files found under: {site_dir}")

    log("Check links in " + str(site_dir))
    page_cache: Dict[Path, Page] = {}
    external_cache: Dict[str, ExternalLinkResult] = {}
    errors: List[CheckError] = []
    total_links = 0
    skipped = 0

    for page_file in pages:
        page = load_page(page_file, site_dir, page_cache)
        page_errors, page_links, page_skipped = check_links_for_page(
            page,
            site_dir,
            args,
            page_cache,
            external_cache,
        )
        errors.extend(page_errors)
        total_links += page_links
        skipped += page_skipped

    log(f"Checked pages: {len(pages)}")
    log(f"Checked links: total={total_links}, skipped={skipped}, errors={len(errors)}")

    if not errors:
        print("There is no errors found")
        return 0

    print("ERRORS FOUND: " + str(len(errors)))
    for error in errors:
        print(error)
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr)
        sys.exit(130)
    except Exception as error:
        print("ERROR: " + str(error), file=sys.stderr)
        sys.exit(2)
