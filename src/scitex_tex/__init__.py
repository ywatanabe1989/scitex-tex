#!/usr/bin/env python3
"""scitex-tex — LaTeX helpers (export, preview, vector formatting) — standalone."""

try:
    from importlib.metadata import version as _v, PackageNotFoundError
    try:
        __version__ = _v("scitex-tex")
    except PackageNotFoundError:
        __version__ = "0.0.0+local"
    del _v, PackageNotFoundError
except ImportError:  # pragma: no cover — only on ancient Pythons
    __version__ = "0.0.0+local"
from ._export import CompileResult, compile_tex, export_tex
from ._preview import preview
from ._to_vec import to_vec

__all__ = [
    "export_tex",
    "compile_tex",
    "CompileResult",
    "preview",
    "to_vec",
]
