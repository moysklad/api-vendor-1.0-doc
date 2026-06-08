---
name: check-doc-links
description: Run this project's Docker Compose documentation server and verify links on the local documentation page. Use when working in api-vendor-1.0-doc and the user asks to start the docs, open http://localhost:4567, check documentation links, validate internal anchors, validate external URLs, or run a LinksChecker-style check.
---

# Check Doc Links

## Workflow

Run the bundled script from the repository root:

```bash
python3 .codex/skills/check-doc-links/scripts/check_doc_links.py
```

The script performs the full workflow:

1. Probe `http://localhost:4567`.
2. If the page is not reachable, run Docker Compose in detached mode.
3. Wait until the documentation responds.
4. Try to open `http://localhost:4567` in the system browser.
5. Download the page and check links in the same spirit as `LinksChecker.java`.

## Link Check Semantics

Treat `href` values as follows:

- Missing or blank `href`: `LINK_HREF_ABSENT_OR_BLANK`.
- `#anchor`: validate against ids on page headings (`h1` through `h6`), matching the original Java checker.
- Absolute `http://` or `https://` URL: perform an HTTP request and report non-2xx/3xx responses as `EXTERNAL_LINK_BROKEN`.
- Same-host absolute links to `localhost:4567`: fetch the page and validate the optional fragment as `INTERNAL_LINK_BROKEN`.
- Relative paths: resolve against `http://localhost:4567`, fetch the page, and validate the optional fragment as `INTERNAL_LINK_BROKEN`.
- Skip `mailto:`, `tel:`, `javascript:`, `data:`, and non-HTTP(S) schemes.

## Options

Use script options when needed:

```bash
python3 .codex/skills/check-doc-links/scripts/check_doc_links.py --verbose-found --verbose-check
python3 .codex/skills/check-doc-links/scripts/check_doc_links.py --no-open
python3 .codex/skills/check-doc-links/scripts/check_doc_links.py --timeout 180
```

If Docker or external HTTP access fails because of sandbox restrictions, rerun the same command with the required approval/escalation. Opening the browser can also require approval in managed environments; if browser opening is blocked, report the URL and continue the link check.

## Reporting

Summarize the result with:

- Whether Docker Compose was already serving the page or had to be started.
- Whether the browser open step succeeded or was skipped/blocked.
- Total links checked.
- Any errors, grouped by error kind and URL/link markup.
