---
description: |
  [TOPIC] First scitex-tex compile in 30 seconds
  [DETAILS] Compile a .tex file to PDF with bibtex-rerun handling; render a first-page PNG preview.
tags: [scitex-tex-quick-start]
---

# Quick Start

## Compile

```python
import scitex_tex

result = scitex_tex.compile_tex("paper.tex")
print(result.pdf_path, result.success, result.warnings)
```

`compile_tex` runs `pdflatex` (or `xelatex` if requested) with
bibtex-rerun handling so cross-refs and citations resolve in one call.
Returns a `CompileResult` with `pdf_path`, `success`, `log`, `warnings`.

## Preview the first page

```python
scitex_tex.preview("paper.pdf", out="preview.png")
```

Useful for embedding a current snapshot in a notebook or chat — no
need to open a PDF viewer.

## See also

- [03_python-api.md](03_python-api.md)
