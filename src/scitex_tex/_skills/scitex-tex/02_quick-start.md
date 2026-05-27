---
description: |
  [TOPIC] First scitex-tex compile in 30 seconds
  [DETAILS] Compile a .tex file to PDF with multi-pass handling; render LaTeX previews via matplotlib.
tags: [scitex-tex-quick-start]
---

# Quick Start

## Compile

```python
import scitex_tex

result = scitex_tex.compile_tex("paper.tex")
print(result.pdf_path, result.success, result.warnings)
```

`compile_tex` runs `pdflatex` (or `xelatex`/`lualatex`/`latexmk` if requested)
with multi-pass handling so cross-refs and citations resolve. Returns a
`CompileResult` with `pdf_path`, `success`, `stdout`, `stderr`, `errors`,
`warnings`.

## Preview LaTeX strings

```python
fig = scitex_tex.preview([r"$\sum_{i=1}^N x_i$", r"$\alpha + \beta$"])
fig.savefig("preview.png")
```

Renders LaTeX strings via matplotlib — no system TeX installation needed.
Returns a `matplotlib.figure.Figure` that you can display in a notebook or
save to disk.

## See also

- [03_python-api.md](03_python-api.md)
