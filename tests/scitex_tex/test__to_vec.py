#!/usr/bin/env python3
# Time-stamp: "2026-05-18 22:51:00 (ywatanabe)"
# File: ./tests/scitex_tex/test__to_vec.py

"""Tests for to_vec function — converts strings to LaTeX vector notation.

Test-quality rules (PA-307 / STX-TQ001-007):
- Descriptive names (≥3 word-tokens after `test_`)
- AAA marker comments
- One assertion per test
"""

import os

import pytest

from scitex_tex import to_vec
from scitex_tex._to_vec import FALLBACK_AVAILABLE, safe_to_vec, vector_notation


# =============================================================================
# to_vec — raw LaTeX output (enable_fallback=False)
# =============================================================================


class TestToVecWithoutFallback:
    """Tests for to_vec with enable_fallback=False (raw LaTeX output)."""

    def test_to_vec_basic_two_letter_label_emits_overrightarrow_mathrm(self):
        # Arrange
        v_str = "AB"
        # Act
        result = to_vec(v_str, enable_fallback=False)
        # Assert
        assert result == r"\overrightarrow{\mathrm{AB}}"

    def test_to_vec_single_lower_letter_emits_overrightarrow_mathrm(self):
        # Arrange
        v_str = "v"
        # Act
        result = to_vec(v_str, enable_fallback=False)
        # Assert
        assert result == r"\overrightarrow{\mathrm{v}}"

    def test_to_vec_single_letter_x_emits_overrightarrow_mathrm(self):
        # Arrange
        v_str = "x"
        # Act
        result = to_vec(v_str, enable_fallback=False)
        # Assert
        assert result == r"\overrightarrow{\mathrm{x}}"

    def test_to_vec_numeric_two_digit_string_emits_overrightarrow_mathrm(self):
        # Arrange
        v_str = "12"
        # Act
        result = to_vec(v_str, enable_fallback=False)
        # Assert
        assert result == r"\overrightarrow{\mathrm{12}}"

    def test_to_vec_numeric_zero_string_emits_overrightarrow_mathrm(self):
        # Arrange
        v_str = "0"
        # Act
        result = to_vec(v_str, enable_fallback=False)
        # Assert
        assert result == r"\overrightarrow{\mathrm{0}}"

    def test_to_vec_empty_string_returns_empty_string(self):
        # Arrange
        v_str = ""
        # Act
        result = to_vec(v_str, enable_fallback=False)
        # Assert
        assert result == ""

    @pytest.mark.parametrize(
        "v_str,expected",
        [
            ("v_1", r"\overrightarrow{\mathrm{v_1}}"),
            ("PQ", r"\overrightarrow{\mathrm{PQ}}"),
            ("A'", r"\overrightarrow{\mathrm{A'}}"),
        ],
    )
    def test_to_vec_special_input_emits_expected_overrightarrow_form(
        self, v_str, expected
    ):
        # Arrange
        v_input = v_str
        # Act
        result = to_vec(v_input, enable_fallback=False)
        # Assert
        assert result == expected

    @pytest.mark.parametrize(
        "v_str,expected",
        [
            ("velocity", r"\overrightarrow{\mathrm{velocity}}"),
            ("F_net", r"\overrightarrow{\mathrm{F_net}}"),
        ],
    )
    def test_to_vec_multi_character_label_emits_expected_overrightarrow_form(
        self, v_str, expected
    ):
        # Arrange
        v_input = v_str
        # Act
        result = to_vec(v_input, enable_fallback=False)
        # Assert
        assert result == expected

    @pytest.mark.parametrize(
        "v_str,expected",
        [
            ("αβ", r"\overrightarrow{\mathrm{αβ}}"),
            ("∇φ", r"\overrightarrow{\mathrm{∇φ}}"),
        ],
    )
    def test_to_vec_unicode_input_emits_expected_overrightarrow_form(
        self, v_str, expected
    ):
        # Arrange
        v_input = v_str
        # Act
        result = to_vec(v_input, enable_fallback=False)
        # Assert
        assert result == expected

    @pytest.mark.parametrize(
        "v_str,expected",
        [
            ("A B", r"\overrightarrow{\mathrm{A B}}"),
            (" CD ", r"\overrightarrow{\mathrm{ CD }}"),
        ],
    )
    def test_to_vec_input_with_spaces_emits_expected_overrightarrow_form(
        self, v_str, expected
    ):
        # Arrange
        v_input = v_str
        # Act
        result = to_vec(v_input, enable_fallback=False)
        # Assert
        assert result == expected

    @pytest.mark.parametrize(
        "v_str,expected",
        [
            ("$x$", r"\overrightarrow{\mathrm{$x$}}"),
            ("a&b", r"\overrightarrow{\mathrm{a&b}}"),
            ("x^2", r"\overrightarrow{\mathrm{x^2}}"),
        ],
    )
    def test_to_vec_input_with_latex_special_chars_emits_unescaped_form(
        self, v_str, expected
    ):
        # Arrange
        v_input = v_str
        # Act
        result = to_vec(v_input, enable_fallback=False)
        # Assert
        assert result == expected

    @pytest.mark.parametrize(
        "v_str,expected",
        [
            ("{AB}", r"\overrightarrow{\mathrm{{AB}}}"),
            ("a{b}c", r"\overrightarrow{\mathrm{a{b}c}}"),
        ],
    )
    def test_to_vec_input_with_braces_emits_expected_overrightarrow_form(
        self, v_str, expected
    ):
        # Arrange
        v_input = v_str
        # Act
        result = to_vec(v_input, enable_fallback=False)
        # Assert
        assert result == expected

    def test_to_vec_backslash_command_input_emits_overrightarrow_form(self):
        # Arrange
        v_str = r"\vec"
        # Act
        result = to_vec(v_str, enable_fallback=False)
        # Assert
        assert result == r"\overrightarrow{\mathrm{\vec}}"

    def test_to_vec_input_with_newline_preserves_newline_in_output(self):
        # Arrange
        v_str = "A\nB"
        # Act
        result = to_vec(v_str, enable_fallback=False)
        # Assert
        assert result == "\\overrightarrow{\\mathrm{A\nB}}"

    @pytest.mark.parametrize(
        "v_str,expected",
        [
            ("r", r"\overrightarrow{\mathrm{r}}"),
            ("F", r"\overrightarrow{\mathrm{F}}"),
            ("r_0", r"\overrightarrow{\mathrm{r_0}}"),
        ],
    )
    def test_to_vec_physics_notation_emits_expected_overrightarrow_form(
        self, v_str, expected
    ):
        # Arrange
        v_input = v_str
        # Act
        result = to_vec(v_input, enable_fallback=False)
        # Assert
        assert result == expected

    def test_to_vec_output_contains_overrightarrow_command_substring(self):
        # Arrange
        v_str = "PQ"
        # Act
        result = to_vec(v_str, enable_fallback=False)
        # Assert
        assert r"\overrightarrow" in result

    def test_to_vec_output_contains_mathrm_command_substring(self):
        # Arrange
        v_str = "PQ"
        # Act
        result = to_vec(v_str, enable_fallback=False)
        # Assert
        assert r"\mathrm" in result

    def test_to_vec_output_contains_braced_label_substring(self):
        # Arrange
        v_str = "PQ"
        # Act
        result = to_vec(v_str, enable_fallback=False)
        # Assert
        assert "{PQ}" in result

    def test_to_vec_one_hundred_char_label_renders_full_label_in_output(self):
        # Arrange
        long_str = "A" * 100
        # Act
        result = to_vec(long_str, enable_fallback=False)
        # Assert
        assert result == rf"\overrightarrow{{\mathrm{{{long_str}}}}}"

    def test_to_vec_punctuation_only_input_emits_overrightarrow_form(self):
        # Arrange
        v_str = "_-_-_"
        # Act
        result = to_vec(v_str, enable_fallback=False)
        # Assert
        assert result == r"\overrightarrow{\mathrm{_-_-_}}"

    def test_to_vec_six_digit_label_emits_overrightarrow_form(self):
        # Arrange
        v_str = "123456"
        # Act
        result = to_vec(v_str, enable_fallback=False)
        # Assert
        assert result == r"\overrightarrow{\mathrm{123456}}"


# =============================================================================
# to_vec — fallback enabled (default behaviour)
# =============================================================================


class TestToVecWithFallback:
    """Tests for to_vec with enable_fallback=True (default behavior)."""

    def test_to_vec_fallback_default_preserves_label_text_in_output(self):
        # Arrange
        v_str = "AB"
        # Act
        result = to_vec(v_str)
        # Assert
        condition = (
            ("AB" in result or "⃗" in result)
            if FALLBACK_AVAILABLE
            else (result == r"\overrightarrow{\mathrm{AB}}")
        )
        assert condition

    def test_to_vec_fallback_empty_string_returns_empty_string(self):
        # Arrange
        v_str = ""
        # Act
        result = to_vec(v_str)
        # Assert
        assert result == ""

    def test_to_vec_fallback_preserves_content_label_substring(self):
        # Arrange
        v_str = "XYZ"
        # Act
        result = to_vec(v_str)
        # Assert
        assert "X" in result or "XYZ" in result

    def test_to_vec_fallback_strategy_unicode_returns_combining_arrow_form(
        self,
    ):
        # Arrange
        v_str = "AB"
        expected = "AB⃗" if FALLBACK_AVAILABLE else r"\overrightarrow{\mathrm{AB}}"
        # Act
        result = to_vec(v_str, fallback_strategy="unicode")
        # Assert
        assert result == expected

    def test_to_vec_fallback_strategy_plain_returns_vec_function_form(self):
        # Arrange
        v_str = "AB"
        expected = "vec(AB)" if FALLBACK_AVAILABLE else r"\overrightarrow{\mathrm{AB}}"
        # Act
        result = to_vec(v_str, fallback_strategy="plain")
        # Assert
        assert result == expected


# =============================================================================
# to_vec — consistency / type
# =============================================================================


class TestToVecConsistency:
    """Tests for consistent behavior of to_vec."""

    def test_to_vec_two_identical_calls_produce_identical_output(self):
        # Arrange
        input_str = "XY"
        # Act
        result1 = to_vec(input_str, enable_fallback=False)
        result2 = to_vec(input_str, enable_fallback=False)
        # Assert
        assert result1 == result2

    def test_to_vec_call_returns_expected_overrightarrow_for_xy(self):
        # Arrange
        input_str = "XY"
        # Act
        result = to_vec(input_str, enable_fallback=False)
        # Assert
        assert result == r"\overrightarrow{\mathrm{XY}}"

    def test_to_vec_two_letter_label_returns_str_instance(self):
        # Arrange
        input_str = "AB"
        # Act
        result = to_vec(input_str, enable_fallback=False)
        # Assert
        assert isinstance(result, str)

    def test_to_vec_empty_input_returns_str_instance(self):
        # Arrange
        input_str = ""
        # Act
        result = to_vec(input_str)
        # Assert
        assert isinstance(result, str)

    def test_to_vec_simple_input_returns_str_instance(self):
        # Arrange
        input_str = "test"
        # Act
        result = to_vec(input_str)
        # Assert
        assert isinstance(result, str)

    def test_to_vec_label_ab_output_starts_with_overrightarrow(self):
        # Arrange
        input_str = "AB"
        # Act
        result = to_vec(input_str, enable_fallback=False)
        # Assert
        assert result.startswith(r"\overrightarrow")

    def test_to_vec_label_bc_output_starts_with_overrightarrow(self):
        # Arrange
        input_str = "BC"
        # Act
        result = to_vec(input_str, enable_fallback=False)
        # Assert
        assert result.startswith(r"\overrightarrow")

    def test_to_vec_concatenated_expression_contains_overrightarrow_ab(self):
        # Arrange
        vec_ab = to_vec("AB", enable_fallback=False)
        vec_bc = to_vec("BC", enable_fallback=False)
        # Act
        latex_expr = f"{vec_ab} + {vec_bc}"
        # Assert
        assert r"\overrightarrow{\mathrm{AB}}" in latex_expr

    def test_to_vec_concatenated_expression_contains_overrightarrow_bc(self):
        # Arrange
        vec_ab = to_vec("AB", enable_fallback=False)
        vec_bc = to_vec("BC", enable_fallback=False)
        # Act
        latex_expr = f"{vec_ab} + {vec_bc}"
        # Assert
        assert r"\overrightarrow{\mathrm{BC}}" in latex_expr


# =============================================================================
# safe_to_vec
# =============================================================================


class TestSafeToVec:
    """Tests for safe_to_vec function (always fallback-enabled)."""

    def test_safe_to_vec_basic_label_preserves_content_in_output(self):
        # Arrange
        v_str = "AB"
        # Act
        result = safe_to_vec(v_str)
        # Assert
        condition = (
            ("AB" in result or "⃗" in result)
            if FALLBACK_AVAILABLE
            else (result == r"\overrightarrow{\mathrm{AB}}")
        )
        assert condition

    def test_safe_to_vec_unicode_strategy_returns_combining_arrow_form(self):
        # Arrange
        v_str = "AB"
        expected = "AB⃗" if FALLBACK_AVAILABLE else r"\overrightarrow{\mathrm{AB}}"
        # Act
        result = safe_to_vec(v_str, fallback_strategy="unicode")
        # Assert
        assert result == expected

    def test_safe_to_vec_plain_strategy_returns_vec_function_form(self):
        # Arrange
        v_str = "AB"
        expected = (
            "vec(AB)" if FALLBACK_AVAILABLE else r"\overrightarrow{\mathrm{AB}}"
        )
        # Act
        result = safe_to_vec(v_str, fallback_strategy="plain")
        # Assert
        assert result == expected

    def test_safe_to_vec_empty_input_returns_empty_string(self):
        # Arrange
        v_str = ""
        # Act
        result = safe_to_vec(v_str)
        # Assert
        assert result == ""


# =============================================================================
# vector_notation alias
# =============================================================================


class TestVectorNotationAlias:
    """Tests for vector_notation alias of to_vec."""

    def test_vector_notation_is_same_object_as_to_vec(self):
        # Arrange
        alias = vector_notation
        # Act
        same = alias is to_vec
        # Assert
        assert same

    def test_vector_notation_returns_same_output_as_to_vec_for_label_ab(self):
        # Arrange
        input_str = "AB"
        # Act
        result = vector_notation(input_str, enable_fallback=False)
        # Assert
        assert result == r"\overrightarrow{\mathrm{AB}}"


# =============================================================================
# FALLBACK_AVAILABLE flag
# =============================================================================


class TestFallbackAvailability:
    """Tests for fallback availability flag handling."""

    def test_fallback_available_module_constant_is_bool_instance(self):
        # Arrange
        flag = FALLBACK_AVAILABLE
        # Act
        is_bool = isinstance(flag, bool)
        # Assert
        assert is_bool

    def test_to_vec_disable_fallback_returns_raw_latex_form_for_test_label(
        self,
    ):
        # Arrange
        v_str = "test"
        # Act
        result = to_vec(v_str, enable_fallback=False)
        # Assert
        assert result == r"\overrightarrow{\mathrm{test}}"


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])

# EOF
