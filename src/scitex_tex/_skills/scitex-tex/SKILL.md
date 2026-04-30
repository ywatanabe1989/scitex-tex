---
name: scitex-tex
description: LaTeX helpers — `export_tex(doc, path)` serializes a SciTeX writer object to .tex, `compile_tex(path)` runs pdflatex/xelatex with retry-on-error, `preview(path)` renders a PNG snapshot of the first page, `to_vec(...)` converts vector graphics to LaTeX-ready format. Drop-in replacement for hand-rolled `subprocess.run(['pdflatex', ...])` chains with bibtex-rerun handling.
primary_interface: python
interfaces:
  python: 2
  cli: 1
  mcp: 0
  skills: 2
  hook: 0
  http: 0
canonical-location: scitex-tex/src/scitex_tex/_skills/scitex-tex/SKILL.md
tags: [scitex-tex, scitex-package]
---

> **Interfaces:** Python ⭐⭐ · CLI ⭐ · MCP — · Skills ⭐⭐ · Hook — · HTTP —

# scitex-tex

LaTeX helpers — `export_tex(doc, path)` serializes a SciTeX writer object to .tex, `compile_tex(path)` runs pdflatex/xelatex with retry-on-error, `preview(path)` renders a PNG snapshot of the first page, `to_vec(...)` converts vector graphics to LaTeX-ready format. Drop-in replacement for hand-rolled `subprocess.run(['pdflatex', ...])` chains with bibtex-rerun handling.

See README.md and the package's public `__init__.py` for the full
function list. This skill leaf exists so agents discover the package
exists and roughly what shape it has — refer to the source for
signatures.
