#!/usr/bin/env python3
# Time-stamp: "2026-05-18 22:51:00 (ywatanabe)"
# File: ./tests/scitex_tex/test__preview.py

"""Real-integration tests for tex._preview module.

The previous version of this file was pure mock theater: every test
patched `scitex.plt.subplots` and then asserted on the resulting Mock
calls. The whole content was already `@pytest.mark.skip`-ed as stale
post-figrecipe drift, so per the SciTeX no-mocks rule
(`02_package_12_no-mocks.md`, "Honest delete > dishonest rewrite") we
delete the mock-shaped tests and replace them with a small set of
real integration tests that drive the actual `preview()` function
against a real Matplotlib backend.

Test-quality rules (PA-307 / STX-TQ001-007):
- Descriptive names (≥3 word-tokens after `test_`)
- AAA marker comments
- One assertion per test
"""

import pytest

matplotlib = pytest.importorskip("matplotlib")
matplotlib.use("Agg")  # Non-interactive backend for headless test runs

# `scitex_tex._preview` imports `from scitex_plt import subplots` at
# call time. Skip the entire module if scitex-plt is not available
# (e.g. minimal CI env).
pytest.importorskip("scitex_plt")

from matplotlib.figure import Figure  # noqa: E402

from scitex_tex._preview import FALLBACK_AVAILABLE, preview  # noqa: E402


# =============================================================================
# preview — real Matplotlib backend, no mocks
# =============================================================================


class TestPreviewReturnType:
    """Tests asserting preview returns a real matplotlib Figure."""

    def test_preview_single_latex_string_returns_real_matplotlib_figure(self):
        # Arrange
        tex_strings = ["x^2"]
        # Act
        fig = preview(tex_strings, enable_fallback=False)
        # Assert
        assert isinstance(fig, Figure)

    def test_preview_multiple_latex_strings_returns_real_matplotlib_figure(
        self,
    ):
        # Arrange
        tex_strings = ["x^2", r"\sum_{i=1}^n i", r"\frac{a}{b}"]
        # Act
        fig = preview(tex_strings, enable_fallback=False)
        # Assert
        assert isinstance(fig, Figure)

    def test_preview_with_fallback_enabled_returns_real_matplotlib_figure(self):
        # Arrange
        tex_strings = ["x^2"]
        # Act
        fig = preview(tex_strings)
        # Assert
        assert isinstance(fig, Figure)

    def test_preview_single_string_input_is_auto_wrapped_into_list(self):
        # Arrange
        single_tex = "x^2"
        # Act
        fig = preview(single_tex, enable_fallback=False)
        # Assert
        assert isinstance(fig, Figure)


# =============================================================================
# preview — axes / figure layout
# =============================================================================


class TestPreviewFigureLayout:
    """Tests asserting preview produces the expected axes layout."""

    def test_preview_single_entry_input_produces_figure_with_one_axes(self):
        # Arrange
        tex_strings = ["x^2"]
        # Act
        fig = preview(tex_strings, enable_fallback=False)
        # Assert
        assert len(fig.axes) == 1

    def test_preview_three_entry_input_produces_figure_with_three_axes(self):
        # Arrange
        tex_strings = ["x^2", r"\alpha", r"\beta"]
        # Act
        fig = preview(tex_strings, enable_fallback=False)
        # Assert
        assert len(fig.axes) == 3

    def test_preview_five_entry_input_produces_figure_with_five_axes(self):
        # Arrange
        tex_strings = ["a", "b", "c", "d", "e"]
        # Act
        fig = preview(tex_strings, enable_fallback=False)
        # Assert
        assert len(fig.axes) == 5

    def test_preview_three_entry_input_scales_figure_height_to_nine_inches(
        self,
    ):
        # Arrange
        tex_strings = ["x^2", r"\alpha", r"\beta"]
        # Act
        fig = preview(tex_strings, enable_fallback=False)
        # Assert
        assert fig.get_size_inches()[1] == pytest.approx(9.0)

    def test_preview_one_entry_input_scales_figure_height_to_three_inches(
        self,
    ):
        # Arrange
        tex_strings = ["x^2"]
        # Act
        fig = preview(tex_strings, enable_fallback=False)
        # Assert
        assert fig.get_size_inches()[1] == pytest.approx(3.0)


# =============================================================================
# preview — text rendering content
# =============================================================================


def _all_text_strings_on_figure(fig):
    """Collect every Text artist's string from every Axes on the figure."""
    out = []
    for ax in fig.axes:
        for t in ax.texts:
            out.append(t.get_text())
    return out


class TestPreviewTextContent:
    """Tests asserting preview writes expected text artists."""

    def test_preview_emits_raw_label_as_one_axis_text_artist(self):
        # Arrange
        tex_strings = ["MYLABEL"]
        # Act
        fig = preview(tex_strings, enable_fallback=False)
        texts = _all_text_strings_on_figure(fig)
        # Assert
        assert "MYLABEL" in texts

    def test_preview_emits_dollar_wrapped_label_as_second_text_artist(self):
        # Arrange
        tex_strings = ["MYLABEL"]
        # Act
        fig = preview(tex_strings, enable_fallback=False)
        texts = _all_text_strings_on_figure(fig)
        # Assert
        assert "$MYLABEL$" in texts

    def test_preview_already_dollar_wrapped_string_is_not_double_wrapped(self):
        # Arrange
        tex_strings = ["$x^2$"]
        # Act
        fig = preview(tex_strings, enable_fallback=False)
        texts = _all_text_strings_on_figure(fig)
        # Assert
        assert "$$x^2$$" not in texts

    def test_preview_emits_two_text_artists_per_input_string(self):
        # Arrange
        tex_strings = ["x^2"]
        # Act
        fig = preview(tex_strings, enable_fallback=False)
        texts = _all_text_strings_on_figure(fig)
        # Assert
        assert len(texts) == 2


# =============================================================================
# FALLBACK_AVAILABLE flag
# =============================================================================


class TestFallbackAvailability:
    """Tests for the FALLBACK_AVAILABLE module-level flag."""

    def test_fallback_available_module_constant_is_bool_instance(self):
        # Arrange
        flag = FALLBACK_AVAILABLE
        # Act
        is_bool = isinstance(flag, bool)
        # Assert
        assert is_bool


if __name__ == "__main__":
    import os

    pytest.main([os.path.abspath(__file__)])

# EOF
