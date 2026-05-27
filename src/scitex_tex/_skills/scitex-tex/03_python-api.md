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

## `export_tex(writer_doc, output_path, *, ...) -> Path`

Serialize a SciTeX writer document dict to `.tex` at `output_path`.
Also handles image export, BibTeX generation, and journal-specific presets
(IEEE, Elsevier, Springer, APS, MDPI, ACM).

Parameters:
- `writer_doc` — dict with `blocks`, `metadata`, `references`, `images`
- `output_path` — path for the output `.tex` file
- `document_class` — LaTeX document class (default `"article"`)
- `packages` — additional LaTeX packages
- `preamble` — extra preamble content
- `image_dir` — directory for extracted images
- `export_images` — whether to export embedded images (default True)
- `journal_preset` — one of `"ieee"`, `"elsevier"`, `"springer"`, `"aps"`, `"mdpi"`, `"acm"`
- `use_bibtex` — generate a `.bib` file (default False)

Returns the `Path` to the written `.tex` file.

## `compile_tex(tex_path, *, output_dir=None, compiler="pdflatex", runs=2, clean=True, timeout=120) -> CompileResult`

Compile a `.tex` file to PDF with multi-pass handling.

Parameters:
- `tex_path` — path to the `.tex` file
- `output_dir` — output directory for the PDF (default: same as tex file)
- `compiler` — `"pdflatex"`, `"xelatex"`, `"lualatex"`, or `"latexmk"`
- `runs` — number of compilation passes (default 2; ignored for `latexmk`)
- `clean` — remove auxiliary files after compilation (default True)
- `timeout` — timeout in seconds per pass (default 120)

Returns a `CompileResult` dataclass.

## `preview(tex_str_list, *, enable_fallback=True) -> matplotlib.figure.Figure`

Render a list of LaTeX strings to a matplotlib Figure. Each string gets
its own subplot showing both the raw text and the LaTeX-rendered version.
No system TeX installation required — uses matplotlib's math rendering
with optional fallback mechanisms.

Parameters:
- `tex_str_list` — list of LaTeX strings (a single string is auto-wrapped)
- `enable_fallback` — whether to enable LaTeX fallback (default True)

Returns a `matplotlib.figure.Figure`.

## `to_vec(v_str, *, enable_fallback=True, fallback_strategy="auto") -> str`

Convert a string to LaTeX vector notation (`\overrightarrow{\mathrm{...}}`)
with automatic fallback if LaTeX rendering fails.

Parameters:
- `v_str` — the label to wrap (e.g., `"AB"`, `"v"`, `"F_net"`)
- `enable_fallback` — whether to enable fallback mechanisms (default True)
- `fallback_strategy` — `"auto"`, `"mathtext"`, `"unicode"`, `"plain"`

Returns a LaTeX-ready string.

## `CompileResult`

```python
@dataclass
class CompileResult:
    success: bool                          # Whether compilation succeeded
    pdf_path: Path | None                  # Path to generated PDF
    exit_code: int                         # Process exit code
    stdout: str                            # Compiler stdout
    stderr: str                            # Compiler stderr
    log_content: str                       # Raw .log file content
    errors: list[str]                      # Parsed error messages
    warnings: list[str]                    # Parsed warning messages
```

## See also

- [01_installation.md](01_installation.md)
- [02_quick-start.md](02_quick-start.md)
