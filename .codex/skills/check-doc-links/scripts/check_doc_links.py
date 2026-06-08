#!/usr/bin/env python3
import argparse
import re
import shutil
import subprocess
import sys
import time
import webbrowser
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Set, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urldefrag, urljoin, urlparse, urlsplit, urlunsplit
from urllib.request import Request, urlopen


LINK_RE = re.compile(r"<\s*a\b.*?</a\s*>", re.IGNORECASE | re.DOTALL)
HEADER_RE = re.compile(r"<\s*h([1-6])\b.*?</h\1\s*>", re.IGNORECASE | re.DOTALL)
HREF_RE = re.compile(r"\bhref\s*=\s*([\"'])(.*?)\1", re.IGNORECASE | re.DOTALL)
ID_RE = re.compile(r"\bid\s*=\s*([\"'])(.*?)\1", re.IGNORECASE | re.DOTALL)
IGNORED_SCHEMES = {"mailto", "tel", "javascript", "data"}
REQUEST_HEADERS = {
    "User-Agent": "codex-check-doc-links/1.0",
    "Accept": "*/*",
    "Accept-Encoding": "gzip",
}
CONTENT_REQUEST_HEADERS = {
    "User-Agent": REQUEST_HEADERS["User-Agent"],
    "Accept": "text/html,*/*",
}


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
    url: str
    content: str
    headers: List[str]
    header_ids: Set[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run local docs via Docker Compose and check documentation links."
    )
    parser.add_argument("--base-url", default="http://localhost:4567")
    parser.add_argument("--timeout", type=int, default=120, help="Seconds to wait for docs startup.")
    parser.add_argument("--link-timeout", type=int, default=12, help="Seconds per link HTTP request.")
    parser.add_argument("--no-open", action="store_true", help="Do not try to open the page in a browser.")
    parser.add_argument("--no-compose", action="store_true", help="Do not run Docker Compose if the page is down.")
    parser.add_argument("--show-content", action="store_true")
    parser.add_argument("--verbose-found", action="store_true")
    parser.add_argument("--verbose-check", action="store_true")
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
    request_url = encode_url_for_request(url)
    request = Request(request_url, headers=REQUEST_HEADERS)
    try:
        with urlopen(request, timeout=timeout) as response:
            status = getattr(response, "status", 200)
            if 200 <= status < 400:
                return True, None, response.geturl()
            return False, f"HTTP {status}", response.geturl()
    except HTTPError as error:
        final_url = getattr(error, "url", request_url)
        if 300 <= error.code < 400:
            return True, None, final_url
        return False, f"HTTP {error.code}: {error.reason}", final_url
    except (URLError, TimeoutError, OSError, UnicodeError) as error:
        return False, str(error), request_url


def fetch_content(url: str, timeout: int) -> str:
    request = Request(encode_url_for_request(url), headers=CONTENT_REQUEST_HEADERS)
    with urlopen(request, timeout=timeout) as response:
        raw = response.read()
        charset = response.headers.get_content_charset() or "utf-8"
        return raw.decode(charset, errors="replace")


def is_docs_reachable(base_url: str, timeout: int) -> bool:
    ok, _, _ = request_url(base_url, timeout)
    return ok


def find_compose_command() -> List[str]:
    docker = shutil.which("docker")
    if docker:
        version = subprocess.run(
            [docker, "compose", "version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if version.returncode == 0:
            return [docker, "compose"]

    docker_compose = shutil.which("docker-compose")
    if docker_compose:
        return [docker_compose]

    raise RuntimeError("Neither 'docker compose' nor 'docker-compose' is available.")


def start_compose() -> None:
    compose = find_compose_command()
    command = compose + ["up", "-d"]
    log("Starting documentation with: " + " ".join(command))
    subprocess.run(command, check=True)


def wait_for_docs(base_url: str, timeout: int) -> None:
    deadline = time.monotonic() + timeout
    last_error = "not checked"

    while time.monotonic() < deadline:
        ok, error, _ = request_url(base_url, timeout=5)
        if ok:
            return
        last_error = error or "unknown error"
        time.sleep(2)

    raise RuntimeError(f"Documentation did not become reachable at {base_url}: {last_error}")


def try_open_browser(base_url: str, no_open: bool) -> str:
    if no_open:
        return "skipped"
    try:
        return "opened" if webbrowser.open(base_url) else "failed"
    except Exception as error:
        return f"failed: {error}"


def extract_value(markup: str, pattern: re.Pattern) -> Optional[str]:
    match = pattern.search(markup)
    if not match:
        return None
    return match.group(2)


def parse_page(url: str, content: str) -> Page:
    headers = HEADER_RE.findall(content)
    header_markup = [match.group(0) for match in HEADER_RE.finditer(content)]
    header_ids: Set[str] = set()
    duplicates: Set[str] = set()

    for header in header_markup:
        header_id = extract_value(header, ID_RE)
        if header_id is None:
            raise RuntimeError(f"Broken header (id not found): {header}")
        if header_id in header_ids:
            duplicates.add(header_id)
        header_ids.add(header_id)

    if duplicates:
        duplicate_list = ", ".join(sorted(duplicates))
        raise RuntimeError(f"There are duplicate ids in some header(s): {duplicate_list}")

    return Page(url=url, content=content, headers=header_markup, header_ids=header_ids)


def same_origin(url_a: str, url_b: str) -> bool:
    left = urlparse(url_a)
    right = urlparse(url_b)
    left_port = left.port or (443 if left.scheme == "https" else 80)
    right_port = right.port or (443 if right.scheme == "https" else 80)
    return (left.scheme, left.hostname, left_port) == (right.scheme, right.hostname, right_port)


def fragment_exists(fragment: str, header_ids: Set[str]) -> bool:
    return fragment in header_ids or unquote(fragment) in header_ids


def page_without_fragment(url: str) -> str:
    return urldefrag(url).url


def load_internal_page(url: str, timeout: int, cache: Dict[str, Page]) -> Tuple[Optional[Page], Optional[str]]:
    clean_url = page_without_fragment(url)
    if clean_url in cache:
        return cache[clean_url], None

    try:
        content = fetch_content(clean_url, timeout)
        page = parse_page(clean_url, content)
        cache[clean_url] = page
        return page, None
    except Exception as error:
        return None, str(error)


def check_external_link(url: str, link: str, timeout: int) -> Optional[CheckError]:
    ok, error, final_url = request_url(url, timeout)
    if ok:
        return None
    detail = error
    if final_url and final_url != url:
        detail = f"{detail}; final_url={final_url}"
    return CheckError("EXTERNAL_LINK_BROKEN", link, detail)


def check_internal_link(
    url: str,
    link: str,
    base_url: str,
    base_page: Page,
    timeout: int,
    cache: Dict[str, Page],
) -> Optional[CheckError]:
    parsed = urlparse(url)
    fragment = parsed.fragment
    target_without_fragment = page_without_fragment(url)
    base_without_fragment = page_without_fragment(base_url)

    if target_without_fragment.rstrip("/") == base_without_fragment.rstrip("/"):
        target_page = base_page
    else:
        target_page, error = load_internal_page(url, timeout, cache)
        if error:
            return CheckError("INTERNAL_LINK_BROKEN", link, error)

    if fragment and not fragment_exists(fragment, target_page.header_ids):
        return CheckError("INTERNAL_ANCHOR_BROKEN", link, fragment)

    if not fragment and target_page is None:
        return CheckError("INTERNAL_LINK_BROKEN", link, "target page not loaded")

    return None


def iter_links(content: str) -> Iterable[str]:
    for match in LINK_RE.finditer(content):
        yield match.group(0)


def check_links(base_url: str, content: str, args: argparse.Namespace) -> Tuple[List[CheckError], int, int]:
    if args.show_content:
        print("Content: " + content)

    links = list(iter_links(content))
    log("Found links: " + str(len(links)))
    if args.verbose_found:
        for link in links:
            print(link)

    base_page = parse_page(base_url, content)
    log("Found headers: " + str(len(base_page.headers)))
    log("Found headers ids: " + str(len(base_page.header_ids)))
    if args.verbose_found:
        for header_id in sorted(base_page.header_ids):
            print(header_id)

    errors: List[CheckError] = []
    skipped = 0
    page_cache: Dict[str, Page] = {page_without_fragment(base_url): base_page}

    log("Start checking...")
    for link in links:
        error: Optional[CheckError] = None
        href = extract_value(link, HREF_RE)

        if href is None or href.strip() == "":
            error = CheckError("LINK_HREF_ABSENT_OR_BLANK", link)
        else:
            href = href.strip()
            parsed_href = urlparse(href)

            if parsed_href.scheme.lower() in IGNORED_SCHEMES:
                skipped += 1
            elif href.startswith("#"):
                fragment = href[1:]
                if not fragment_exists(fragment, base_page.header_ids):
                    error = CheckError("INTERNAL_ANCHOR_BROKEN", link, fragment)
            else:
                absolute_url = urljoin(base_url, href)
                parsed_absolute = urlparse(absolute_url)
                if parsed_absolute.scheme not in {"http", "https"}:
                    skipped += 1
                elif same_origin(base_url, absolute_url):
                    error = check_internal_link(
                        absolute_url,
                        link,
                        base_url,
                        base_page,
                        args.link_timeout,
                        page_cache,
                    )
                else:
                    error = check_external_link(absolute_url, link, args.link_timeout)

        if args.verbose_check:
            print(link + " - " + (str(error) if error else "OK"))

        if error:
            errors.append(error)

    return errors, len(links), skipped


def main() -> int:
    args = parse_args()
    base_url = args.base_url.rstrip("/")

    log("Check links in " + base_url)
    started_by_compose = False

    if is_docs_reachable(base_url, timeout=3):
        log("Documentation is already reachable.")
    elif args.no_compose:
        raise RuntimeError(f"Documentation is not reachable at {base_url} and --no-compose was set.")
    else:
        start_compose()
        started_by_compose = True
        wait_for_docs(base_url, args.timeout)

    browser_status = try_open_browser(base_url, args.no_open)
    log("Browser: " + browser_status)

    content = fetch_content(base_url, args.link_timeout)
    errors, total_links, skipped = check_links(base_url, content, args)

    log("Docs status: " + ("started_by_compose" if started_by_compose else "already_running"))
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
