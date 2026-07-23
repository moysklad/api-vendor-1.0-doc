---
name: check-doc-links
description: Build this project's documentation and verify links in the generated site. Use when working in api-vendor-1.0-doc and the user asks to check documentation links, validate internal anchors, validate external URLs, or run a LinksChecker-style check.
---

# Check Doc Links

## Workflow

Build the documentation first, then run the checker from the repository root:

```bash
bundle exec middleman build
python3 scripts/check-doc-links.py --site-dir build
```

By default, the script checks external `http://` and `https://` links too.
Use `--skip-external` for a fast local pass.

The script performs the check against the generated HTML:

1. Scan all HTML files under `build/`.
2. Validate `href` values and in-page anchors.
3. Resolve internal links against the generated files.
4. Check external `http://` and `https://` links with HTTP requests.

## Link Check Semantics

Treat `href` values as follows:

- Missing or blank `href`: `LINK_HREF_ABSENT_OR_BLANK`.
- `#anchor`: validate against ids on page headings (`h1` through `h6`).
- Relative paths and `http://docs.local/...` links: resolve against the built `build/` output and validate the optional fragment as `INTERNAL_LINK_BROKEN`.
- Absolute `http://` or `https://` URLs to other hosts: perform an HTTP request and report non-2xx/3xx responses as `EXTERNAL_LINK_BROKEN`.
- Skip `mailto:`, `tel:`, `javascript:`, `data:`, and non-HTTP(S) schemes.

## Options

Use script options when needed:

```bash
python3 scripts/check-doc-links.py --site-dir build --verbose-check
python3 scripts/check-doc-links.py --site-dir build --verbose-found
python3 scripts/check-doc-links.py --site-dir build --show-content
```

If external HTTP access fails because of sandbox restrictions, rerun the same command with the required approval/escalation.

## Reporting

Summarize the result with:

- Which site directory was checked.
- Total links checked.
- Any errors, grouped by error kind and URL/link markup.
