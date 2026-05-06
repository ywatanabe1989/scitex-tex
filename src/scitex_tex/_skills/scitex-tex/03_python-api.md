---
description: |
  [TOPIC] Public Python API of scitex-tex
  [DETAILS] `export_tex`, `compile_tex`, `preview`, `to_vec`, and the `CompileResult` dataclass.
tags: [scitex-tex-python-api]
---

# Python API

```python
import scitex_tex
```

## `compile_tex(path, *, engine="pdflatex") -> CompileResult`

Compiles a `.tex` file with bibtex-rerun handling. Returns a
`CompileResult` (dataclass) with `pdf_path`, `success`, `log`,
`warnings`. `engine` may be `"pdflatex"` or `"xelatex"`.

## `export_tex(doc, path) -> None`

Serialize a SciTeX writer document object to `.tex` at `path`.

## `preview(pdf_path, *, out=None) -> str`

Render page 1 of `pdf_path` to a PNG (Pillow-based). Writes to `out`
when given, otherwise alongside the PDF. Returns the PNG path.

## `to_vec(...)`

Convert vector graphics (SVG/PDF) to a LaTeX-ready format suitable for
`\includegraphics`.

## `CompileResult`

```python
@dataclass
class CompileResult:
    pdf_path: str
    success: bool
    log: str
    warnings: list[str]
```

## See also

- [01_installation.md](01_installation.md)
- [02_quick-start.md](02_quick-start.md)
