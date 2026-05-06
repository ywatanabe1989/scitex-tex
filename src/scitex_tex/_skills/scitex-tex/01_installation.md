---
description: |
  [TOPIC] Installing scitex-tex
  [DETAILS] pip install (standalone vs umbrella), required system LaTeX toolchain, and how to verify the install.
tags: [scitex-tex-installation]
---

# Installation

## pip install

```bash
pip install scitex-tex
```

Requires Python >= 3.9 plus a working LaTeX toolchain on `PATH`
(`pdflatex` or `xelatex`, `bibtex`). On Debian/Ubuntu:

```bash
sudo apt install texlive-latex-extra texlive-bibtex-extra
```

## Standalone vs umbrella

`scitex-tex` is a standalone package, but it is also part of the
[scitex umbrella](https://pypi.org/project/scitex/):

```python
# Standalone — pip install scitex-tex
import scitex_tex
scitex_tex.compile_tex("paper.tex")

# Umbrella — pip install scitex
import scitex
scitex.tex.compile_tex("paper.tex")
```

`pip install scitex-tex` alone does **not** expose the `scitex`
namespace. Install both for both paths
(`pip install scitex scitex-tex` or `pip install scitex[tex]`).

## Verify

```bash
scitex-tex --version
```

```python
import scitex_tex
print(scitex_tex.__version__)
```

## See also

- [02_quick-start.md](02_quick-start.md)
- [03_python-api.md](03_python-api.md)
