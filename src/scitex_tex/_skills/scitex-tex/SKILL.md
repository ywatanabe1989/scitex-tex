---
name: scitex-tex
description: |
  [WHAT] LaTeX helpers — `export_tex`, `compile_tex` (pdflatex/xelatex with bibtex-rerun handling), `preview` (first-page PNG), `to_vec` (vector→LaTeX).
  [WHEN] Use to compile manuscripts from SciTeX writer objects, render quick previews, or convert figures to LaTeX-ready vector format.
  [HOW] `import scitex_tex; scitex_tex.compile_tex("paper.tex")` returns a `CompileResult`; `scitex_tex.preview("paper.pdf")` writes a PNG of page 1.
primary_interface: python
interfaces:
  python: 2
  cli: 1
  mcp: 0
  skills: 2
  hook: 0
  http: 0
canonical-location: scitex-tex/src/scitex_tex/_skills/scitex-tex/SKILL.md
tags: [scitex-tex]
---

> **Interfaces:** Python ⭐⭐ · CLI ⭐ · MCP — · Skills ⭐⭐ · Hook — · HTTP —

# scitex-tex

LaTeX helpers — `export_tex(doc, path)` serializes a SciTeX writer object to .tex, `compile_tex(path)` runs pdflatex/xelatex with retry-on-error, `preview(path)` renders a PNG snapshot of the first page, `to_vec(...)` converts vector graphics to LaTeX-ready format. Drop-in replacement for hand-rolled `subprocess.run(['pdflatex', ...])` chains with bibtex-rerun handling.

## Index

- [01_installation.md](01_installation.md) — pip install and verify
- [02_quick-start.md](02_quick-start.md) — compile + preview a .tex in 30 seconds
- [03_python-api.md](03_python-api.md) — `export_tex`, `compile_tex`, `preview`, `to_vec`, `CompileResult`
