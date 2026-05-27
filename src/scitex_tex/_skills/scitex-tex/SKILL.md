---
name: scitex-tex
description: |
  [WHAT] LaTeX helpers — `export_tex` (writer dict → .tex), `compile_tex` (pdflatex/lualatex/xelatex with multi-pass), `preview` (LaTeX string → matplotlib Figure), `to_vec` (string → LaTeX \overrightarrow form).
  [WHEN] Use to compile manuscripts from SciTeX writer objects, render quick math previews, or convert labels to LaTeX vector notation.
  [HOW] `import scitex_tex; scitex_tex.compile_tex("paper.tex")` returns a `CompileResult`; `scitex_tex.preview([r"$x^2$"])` returns a matplotlib `Figure`.
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

LaTeX helpers — `export_tex(doc, path)` serializes a SciTeX writer dict to .tex, `compile_tex(path)` runs pdflatex/xelatex/lualatex with multi-pass and optional bibtex support, `preview(tex_strings)` renders a matplotlib Figure from LaTeX strings, `to_vec(label)` wraps a string in `\overrightarrow{\mathrm{...}}` with automatic rendering fallback. Drop-in replacement for hand-rolled `subprocess.run(['pdflatex', ...])` chains.

## Index

- [01_installation.md](01_installation.md) — pip install and verify
- [02_quick-start.md](02_quick-start.md) — compile + preview a .tex in 30 seconds
- [03_python-api.md](03_python-api.md) — `export_tex`, `compile_tex`, `preview`, `to_vec`, `CompileResult`
