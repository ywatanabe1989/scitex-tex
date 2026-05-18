"""Smoke test: every example script under examples/ runs to completion."""

import subprocess
import sys
from pathlib import Path

import pytest

EXAMPLES = sorted(
    Path(__file__).parent.parent.joinpath("examples").glob("*.py")
)


def test_examples_directory_contains_at_least_one_script():
    # Arrange
    examples_found = EXAMPLES
    # Act
    count = len(examples_found)
    # Assert
    assert count > 0, "No example scripts found under examples/"


@pytest.mark.parametrize(
    "example_path",
    EXAMPLES,
    ids=[ex.name for ex in EXAMPLES],
)
def test_example_script_exits_zero_when_run_as_subprocess(example_path, tmp_path):
    # Arrange
    cmd = [sys.executable, str(example_path)]
    # Act
    completed = subprocess.run(
        cmd,
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
    )
    # Assert
    assert completed.returncode == 0, (
        f"{example_path.name} failed:\n"
        f"STDOUT:\n{completed.stdout}\n"
        f"STDERR:\n{completed.stderr}"
    )
