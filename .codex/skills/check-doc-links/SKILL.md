---
name: check-doc-links
description: Verify Vendor API documentation links and legacy redirects. Use when working in api-vendor-1.0-doc and the user asks to check documentation links, validate internal anchors, validate external URLs, or run a LinksChecker-style check.
---

# Check Doc Links

## Workflow

Run both checks from the repository root. The redirect check needs the same `slugify` package as GitHub Actions:

```bash
npm install --no-save --package-lock=false slugify@1.6.6
python3 scripts/build_hash_redirect_map.py --check
python3 scripts/check-doc-links.py --markdown-dir md
```

`build_hash_redirect_map.py --check` verifies internal Markdown links and entries in `hash-redirect-map.json`.

`check-doc-links.py --markdown-dir md` checks external `http://` and `https://` links in `md/`. It skips fenced code blocks. Use `--skip-external` for a fast local pass.

Manually verified external URLs unavailable from the CI network can be added to `scripts/check-doc-links-allowlist.txt`. They are reported as `INFO` and do not fail CI.

API endpoint references such as `https://api.moysklad.ru/api/remap/1.2` and `https://apps-api.moysklad.ru/api/vendor/1.0` are treated as documentation references and skipped from external HTTP validation.

Markdown formatting rules (`test:md`) run in the remap-deployer React build, not in this repository's GitHub Actions workflow.

## Built HTML

`--site-dir` checks `href` values in an already built React site. This repository does not build that site itself:

```bash
python3 scripts/check-doc-links.py --site-dir build
```

Treat `href` values as follows:

- Missing or blank `href`: `LINK_HREF_ABSENT_OR_BLANK`.
- `#anchor`: validate against `id` attributes on the target page.
- Relative paths and `http://docs.local/...` links: resolve against the built output and validate the optional fragment as `INTERNAL_LINK_BROKEN`.
- Absolute `http://` or `https://` URLs to other hosts: perform an HTTP request and report non-2xx/3xx responses as `EXTERNAL_LINK_BROKEN`.
- Skip `mailto:`, `tel:`, `javascript:`, `data:`, and non-HTTP(S) schemes.

## Options

```bash
python3 scripts/check-doc-links.py --markdown-dir md --skip-external
python3 scripts/check-doc-links.py --markdown-dir md --verbose-check
python3 scripts/check-doc-links.py --site-dir build --verbose-found
python3 scripts/check-doc-links.py --site-dir build --show-content
```

If external HTTP access fails because of sandbox restrictions, rerun the same command with the required approval.

## Reporting

Summarize the result with:

- Which command and directory were checked.
- Total links checked.
- Any errors, grouped by error kind and URL/link markup.
