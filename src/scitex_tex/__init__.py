#!/usr/bin/env python3
"""scitex-tex — LaTeX helpers (export, preview, vector formatting) — standalone."""

__version__ = "0.1.0"

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
