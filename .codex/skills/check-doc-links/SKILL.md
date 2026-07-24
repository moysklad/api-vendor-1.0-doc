---
name: check-doc-links
description: Build this project's documentation and verify links in the generated site. Use when working in api-vendor-1.0-doc and the user asks to check documentation links, validate internal anchors, validate external URLs, or run a LinksChecker-style check.
---

# Check Doc Links

## Workflow

Build the documentation first, then run the checker from the repository root:

```bash
docker compose build
docker compose run --rm app bundle exec middleman build
python3 scripts/check-doc-links.py --site-dir build
```

The project uses an old Ruby/Bundler stack, so local builds should run in the
Docker image defined by `Dockerfile` (Ruby 2.5.9). The GitHub Actions workflow
may use its own Ruby setup.

By default, the script checks external `http://` and `https://` links too.
Use `--skip-external` for a fast local pass.
Manually verified external URLs unavailable from the CI network can be added
to `scripts/check-doc-links-allowlist.txt`; they are reported as `INFO` and do
not fail CI.
API endpoint references such as `https://api.moysklad.ru/api/remap/1.2` and
`https://apps-api.moysklad.ru/api/vendor/1.0` are treated as documentation
references and skipped from external HTTP validation.

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
