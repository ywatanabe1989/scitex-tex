# scitex-tex

<!-- scitex-badges:start -->
[![PyPI](https://img.shields.io/pypi/v/scitex-tex.svg)](https://pypi.org/project/scitex-tex/)
[![Python](https://img.shields.io/pypi/pyversions/scitex-tex.svg)](https://pypi.org/project/scitex-tex/)
[![Tests](https://github.com/ywatanabe1989/scitex-tex/actions/workflows/test.yml/badge.svg)](https://github.com/ywatanabe1989/scitex-tex/actions/workflows/test.yml)
[![Install Test](https://github.com/ywatanabe1989/scitex-tex/actions/workflows/install-test.yml/badge.svg)](https://github.com/ywatanabe1989/scitex-tex/actions/workflows/install-test.yml)
[![Coverage](https://codecov.io/gh/ywatanabe1989/scitex-tex/graph/badge.svg)](https://codecov.io/gh/ywatanabe1989/scitex-tex)
[![Docs](https://readthedocs.org/projects/scitex-tex/badge/?version=latest)](https://scitex-tex.readthedocs.io/en/latest/)
[![License: AGPL v3](https://img.shields.io/badge/license-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
<!-- scitex-badges:end -->


LaTeX helpers (export to .tex, compile to PDF, render preview images, vector formatting) extracted from the [SciTeX](https://github.com/ywatanabe1989/scitex-python) ecosystem as a standalone package.

## Install

```bash
pip install scitex-tex
```

## API

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

## Status

Standalone fork of `scitex.tex`. Only dep is matplotlib (for preview rendering).
The umbrella package's `scitex.tex` import path is preserved via a
`sys.modules`-alias bridge. 128/128 tests pass.

## License

AGPL-3.0-only (see [LICENSE](./LICENSE)).
