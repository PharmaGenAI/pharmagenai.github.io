# Open Pharma Plugins business documentation

Business-first documentation and fictional examples for
[Open Pharma Plugins](https://github.com/PharmaGenAI/open-pharma-plugins).

## Local preview

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/check_content.py
.venv/bin/python scripts/check_workflows.py
.venv/bin/mkdocs build --strict
.venv/bin/python scripts/check_local_links.py --site-dir site
.venv/bin/mkdocs serve
```

Release-sensitive display data is pinned in `docs/assets/data/release.json`. The plugin repository remains
canonical for package versions, installation, releases, and technical behavior.

Release synchronization is review-gated. See [docs/operations/release-sync.md](docs/operations/release-sync.md)
for the repository-dispatch payload and the narrow credential contract.
