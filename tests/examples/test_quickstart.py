#!/usr/bin/env python3
"""Compile-only smoke test for examples/quickstart.py.

Runs `py_compile` to confirm the example parses on the supported Python
versions. Heavier behavioral coverage belongs in tests/integration/.
"""

import py_compile
from pathlib import Path

EXAMPLE = Path(__file__).resolve().parents[2] / "examples" / "quickstart.py"


def test_quickstart_example_file_exists_on_disk():
    # Arrange
    example_path = EXAMPLE
    # Act
    is_file = example_path.is_file()
    # Assert
    assert is_file, f"missing example: {example_path}"


def test_quickstart_example_compiles_to_pyc_at_requested_path(tmp_path):
    # Arrange
    example_path = str(EXAMPLE)
    out_pyc = tmp_path / "quickstart.pyc"
    # Act
    pyc_path = py_compile.compile(
        example_path, cfile=str(out_pyc), doraise=True
    )
    # Assert
    assert pyc_path == str(out_pyc)


# EOF
