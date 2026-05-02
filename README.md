# scitex-tex

<p align="center">
  <a href="https://scitex.ai">
    <img src="docs/scitex-logo-blue-cropped.png" alt="SciTeX" width="400">
  </a>
</p>

<p align="center"><b>LaTeX helpers — export to .tex, compile to PDF, preview images, vector formatting.</b></p>

<p align="center">
  <a href="https://scitex-tex.readthedocs.io/">Full Documentation</a> · <code>pip install scitex-tex</code>
</p>

<!-- scitex-badges:start -->
<p align="center">
  <a href="https://pypi.org/project/scitex-tex/"><img src="https://img.shields.io/pypi/v/scitex-tex.svg" alt="PyPI"></a>
  <a href="https://pypi.org/project/scitex-tex/"><img src="https://img.shields.io/pypi/pyversions/scitex-tex.svg" alt="Python"></a>
  <a href="https://github.com/ywatanabe1989/scitex-tex/actions/workflows/test.yml"><img src="https://github.com/ywatanabe1989/scitex-tex/actions/workflows/test.yml/badge.svg" alt="Tests"></a>
  <a href="https://github.com/ywatanabe1989/scitex-tex/actions/workflows/install-test.yml"><img src="https://github.com/ywatanabe1989/scitex-tex/actions/workflows/install-test.yml/badge.svg" alt="Install Test"></a>
  <a href="https://codecov.io/gh/ywatanabe1989/scitex-tex"><img src="https://codecov.io/gh/ywatanabe1989/scitex-tex/graph/badge.svg" alt="Coverage"></a>
  <a href="https://scitex-tex.readthedocs.io/en/latest/"><img src="https://readthedocs.org/projects/scitex-tex/badge/?version=latest" alt="Docs"></a>
  <a href="https://www.gnu.org/licenses/agpl-3.0"><img src="https://img.shields.io/badge/license-AGPL_v3-blue.svg" alt="License: AGPL v3"></a>
</p>
<!-- scitex-badges:end -->

---

## Installation

```bash
pip install scitex-tex
```

## Quick Start

```python
import scitex_tex as tx

# Convert a SciTeX-style writer doc → .tex
tx.export_tex(doc, "manuscript.tex")

# Compile .tex → .pdf (returns CompileResult)
result = tx.compile_tex("manuscript.tex")

# Render a snippet to a preview image
tx.preview(r"$\sum_{i=1}^N x_i$", "preview.png")

# Format a numeric value with sig-fig rules
tx.to_vec(1.234e-3, sig_figs=3)
```

## 1 Interfaces

<details open>
<summary><strong>Python API</strong></summary>

<br>

```python
import scitex_tex as tx

# Export — writer doc → .tex string + file
tx.export_tex(doc, "manuscript.tex")

# Compile — .tex → .pdf via pdflatex/xelatex; returns CompileResult
res = tx.compile_tex("manuscript.tex")
print(res.pdf_path, res.log)

# Preview — render a snippet to a PNG
tx.preview(r"$\frac{1}{2}\sum x_i$", "preview.png")

# Vector formatting helpers
tx.to_vec(1.234e-3, sig_figs=3)
```

</details>

## Status

Standalone fork of `scitex.tex`. Only dep is matplotlib (for preview rendering).
The umbrella package's `scitex.tex` import path is preserved via a
`sys.modules`-alias bridge.

## Part of SciTeX

`scitex-tex` is part of [**SciTeX**](https://scitex.ai). Install via
the umbrella with `pip install scitex[tex]` to use as
`scitex.tex` (Python) or `scitex tex ...` (CLI).

>Four Freedoms for Research
>
>0. The freedom to **run** your research anywhere — your machine, your terms.
>1. The freedom to **study** how every step works — from raw data to final manuscript.
>2. The freedom to **redistribute** your workflows, not just your papers.
>3. The freedom to **modify** any module and share improvements with the community.
>
>AGPL-3.0 — because we believe research infrastructure deserves the same freedoms as the software it runs on.

## License

AGPL-3.0-only (see [LICENSE](./LICENSE)).

---

<p align="center">
  <a href="https://scitex.ai" target="_blank"><img src="docs/scitex-icon-navy-inverted.png" alt="SciTeX" width="40"/></a>
</p>
