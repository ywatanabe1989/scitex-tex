#!/usr/bin/env python3
# Time-stamp: "2026-05-18 22:51:00 (ywatanabe)"
# File: ./tests/scitex_tex/test__export.py

"""Comprehensive tests for tex._export module.

Test-quality rules (PA-307 / STX-TQ001-007) require every test to have:
- A descriptive name (≥3 word-tokens after `test_`)
- AAA marker comments (`# Arrange` / `# Act` / `# Assert`)
- Exactly one assertion per test (multi-asserts must be split)

PA-306 forbids `unittest.mock` / `pytest-mock` / `monkeypatch`. For the
single timeout test we use a real shell shim instead.
"""

import os
import shutil
import stat
import tempfile
from pathlib import Path

import pytest

from scitex_tex._export import (
    JOURNAL_PRESETS,
    CompileResult,
    _build_latex_document,
    _convert_caption,
    _convert_equation,
    _convert_heading,
    _convert_image,
    _convert_list_item,
    _convert_paragraph,
    _convert_reference_to_latex,
    _convert_table,
    _escape_latex,
    _generate_bibtex,
    _parse_latex_log,
    _write_images_to_dir,
    compile_tex,
    export_tex,
)


# =============================================================================
# _escape_latex
# =============================================================================


class TestEscapeLatex:
    """Tests for _escape_latex helper function."""

    def test_escape_latex_returns_empty_string_for_empty_input(self):
        # Arrange
        text_in = ""
        # Act
        result = _escape_latex(text_in)
        # Assert
        assert result == ""

    def test_escape_latex_passes_through_plain_text_without_changes(self):
        # Arrange
        text_in = "Hello World"
        # Act
        result = _escape_latex(text_in)
        # Assert
        assert result == "Hello World"

    def test_escape_latex_escapes_ampersand_with_backslash(self):
        # Arrange
        text_in = "A & B"
        # Act
        result = _escape_latex(text_in)
        # Assert
        assert result == r"A \& B"

    def test_escape_latex_escapes_percent_sign_with_backslash(self):
        # Arrange
        text_in = "100%"
        # Act
        result = _escape_latex(text_in)
        # Assert
        assert result == r"100\%"

    def test_escape_latex_escapes_dollar_sign_with_backslash(self):
        # Arrange
        text_in = "$100"
        # Act
        result = _escape_latex(text_in)
        # Assert
        assert result == r"\$100"

    def test_escape_latex_escapes_hash_pound_sign_with_backslash(self):
        # Arrange
        text_in = "Item #1"
        # Act
        result = _escape_latex(text_in)
        # Assert
        assert result == r"Item \#1"

    def test_escape_latex_escapes_underscore_with_backslash(self):
        # Arrange
        text_in = "var_name"
        # Act
        result = _escape_latex(text_in)
        # Assert
        assert result == r"var\_name"

    def test_escape_latex_escapes_curly_braces_with_backslash(self):
        # Arrange
        text_in = "{text}"
        # Act
        result = _escape_latex(text_in)
        # Assert
        assert result == r"\{text\}"

    def test_escape_latex_replaces_tilde_with_textasciitilde(self):
        # Arrange
        text_in = "~"
        # Act
        result = _escape_latex(text_in)
        # Assert
        assert "textasciitilde" in result

    def test_escape_latex_replaces_caret_with_textasciicircum(self):
        # Arrange
        text_in = "^"
        # Act
        result = _escape_latex(text_in)
        # Assert
        assert "textasciicircum" in result

    def test_escape_latex_multiple_special_chars_contains_escaped_dollar(self):
        # Arrange
        text_in = "$100 & 50%"
        # Act
        result = _escape_latex(text_in)
        # Assert
        assert r"\$" in result

    def test_escape_latex_multiple_special_chars_contains_escaped_ampersand(self):
        # Arrange
        text_in = "$100 & 50%"
        # Act
        result = _escape_latex(text_in)
        # Assert
        assert r"\&" in result

    def test_escape_latex_multiple_special_chars_contains_escaped_percent(self):
        # Arrange
        text_in = "$100 & 50%"
        # Act
        result = _escape_latex(text_in)
        # Assert
        assert r"\%" in result


# =============================================================================
# _convert_heading
# =============================================================================


class TestConvertHeading:
    """Tests for _convert_heading helper function."""

    def test_convert_heading_level_one_produces_section_command(self):
        # Arrange
        block = {"type": "heading", "level": 1, "text": "Introduction"}
        # Act
        result = _convert_heading(block)
        # Assert
        assert r"\section{Introduction}" in result

    def test_convert_heading_level_two_produces_subsection_command(self):
        # Arrange
        block = {"type": "heading", "level": 2, "text": "Methods"}
        # Act
        result = _convert_heading(block)
        # Assert
        assert r"\subsection{Methods}" in result

    def test_convert_heading_level_three_produces_subsubsection_command(self):
        # Arrange
        block = {"type": "heading", "level": 3, "text": "Data Collection"}
        # Act
        result = _convert_heading(block)
        # Assert
        assert r"\subsubsection{Data Collection}" in result

    def test_convert_heading_level_four_produces_paragraph_command(self):
        # Arrange
        block = {"type": "heading", "level": 4, "text": "Details"}
        # Act
        result = _convert_heading(block)
        # Assert
        assert r"\paragraph{Details}" in result

    def test_convert_heading_level_five_produces_subparagraph_command(self):
        # Arrange
        block = {"type": "heading", "level": 5, "text": "Note"}
        # Act
        result = _convert_heading(block)
        # Assert
        assert r"\subparagraph{Note}" in result

    def test_convert_heading_missing_level_defaults_to_section_command(self):
        # Arrange
        block = {"type": "heading", "text": "Title"}
        # Act
        result = _convert_heading(block)
        # Assert
        assert r"\section{Title}" in result

    def test_convert_heading_escapes_special_chars_in_text(self):
        # Arrange
        block = {
            "type": "heading",
            "level": 1,
            "text": "Results & Discussion",
        }
        # Act
        result = _convert_heading(block)
        # Assert
        assert r"\&" in result


# =============================================================================
# _convert_paragraph
# =============================================================================


class TestConvertParagraph:
    """Tests for _convert_paragraph helper function."""

    def test_convert_paragraph_includes_plain_text_in_output(self):
        # Arrange
        block = {"type": "paragraph", "text": "This is a paragraph."}
        # Act
        result = _convert_paragraph(block)
        # Assert
        assert "This is a paragraph." in result

    def test_convert_paragraph_wraps_bold_run_in_textbf(self):
        # Arrange
        block = {
            "type": "paragraph",
            "runs": [
                {"text": "Normal "},
                {"text": "bold", "bold": True},
                {"text": " text"},
            ],
        }
        # Act
        result = _convert_paragraph(block)
        # Assert
        assert r"\textbf{bold}" in result

    def test_convert_paragraph_passes_through_normal_run_text(self):
        # Arrange
        block = {
            "type": "paragraph",
            "runs": [
                {"text": "Normal "},
                {"text": "bold", "bold": True},
                {"text": " text"},
            ],
        }
        # Act
        result = _convert_paragraph(block)
        # Assert
        assert "Normal" in result

    def test_convert_paragraph_wraps_italic_run_in_textit(self):
        # Arrange
        block = {
            "type": "paragraph",
            "runs": [{"text": "emphasis", "italic": True}],
        }
        # Act
        result = _convert_paragraph(block)
        # Assert
        assert r"\textit{emphasis}" in result

    def test_convert_paragraph_wraps_underline_run_in_underline(self):
        # Arrange
        block = {
            "type": "paragraph",
            "runs": [{"text": "underlined", "underline": True}],
        }
        # Act
        result = _convert_paragraph(block)
        # Assert
        assert r"\underline{underlined}" in result

    def test_convert_paragraph_combined_bold_run_emits_textbf(self):
        # Arrange
        block = {
            "type": "paragraph",
            "runs": [
                {
                    "text": "styled",
                    "bold": True,
                    "italic": True,
                    "underline": True,
                }
            ],
        }
        # Act
        result = _convert_paragraph(block)
        # Assert
        assert r"\textbf" in result

    def test_convert_paragraph_combined_italic_run_emits_textit(self):
        # Arrange
        block = {
            "type": "paragraph",
            "runs": [
                {
                    "text": "styled",
                    "bold": True,
                    "italic": True,
                    "underline": True,
                }
            ],
        }
        # Act
        result = _convert_paragraph(block)
        # Assert
        assert r"\textit" in result

    def test_convert_paragraph_combined_underline_run_emits_underline(self):
        # Arrange
        block = {
            "type": "paragraph",
            "runs": [
                {
                    "text": "styled",
                    "bold": True,
                    "italic": True,
                    "underline": True,
                }
            ],
        }
        # Act
        result = _convert_paragraph(block)
        # Assert
        assert r"\underline" in result


# =============================================================================
# _convert_table
# =============================================================================


class TestConvertTable:
    """Tests for _convert_table helper function."""

    def test_convert_table_emits_begin_table_environment(self):
        # Arrange
        block = {"type": "table", "rows": [["A", "B"], ["C", "D"]]}
        # Act
        result = _convert_table(block)
        # Assert
        assert r"\begin{table}" in result

    def test_convert_table_emits_begin_tabular_environment(self):
        # Arrange
        block = {"type": "table", "rows": [["A", "B"], ["C", "D"]]}
        # Act
        result = _convert_table(block)
        # Assert
        assert r"\begin{tabular}" in result

    def test_convert_table_emits_end_tabular_environment(self):
        # Arrange
        block = {"type": "table", "rows": [["A", "B"], ["C", "D"]]}
        # Act
        result = _convert_table(block)
        # Assert
        assert r"\end{tabular}" in result

    def test_convert_table_emits_end_table_environment(self):
        # Arrange
        block = {"type": "table", "rows": [["A", "B"], ["C", "D"]]}
        # Act
        result = _convert_table(block)
        # Assert
        assert r"\end{table}" in result

    def test_convert_table_joins_first_row_cells_with_ampersand(self):
        # Arrange
        block = {"type": "table", "rows": [["A", "B"], ["C", "D"]]}
        # Act
        result = _convert_table(block)
        # Assert
        assert "A & B" in result

    def test_convert_table_joins_second_row_cells_with_ampersand(self):
        # Arrange
        block = {"type": "table", "rows": [["A", "B"], ["C", "D"]]}
        # Act
        result = _convert_table(block)
        # Assert
        assert "C & D" in result

    def test_convert_table_returns_empty_string_for_empty_rows(self):
        # Arrange
        block = {"type": "table", "rows": []}
        # Act
        result = _convert_table(block)
        # Assert
        assert result == ""

    def test_convert_table_escapes_percent_in_cell_text(self):
        # Arrange
        block = {"type": "table", "rows": [["100%", "$50"]]}
        # Act
        result = _convert_table(block)
        # Assert
        assert r"\%" in result

    def test_convert_table_escapes_dollar_in_cell_text(self):
        # Arrange
        block = {"type": "table", "rows": [["100%", "$50"]]}
        # Act
        result = _convert_table(block)
        # Assert
        assert r"\$" in result

    def test_convert_table_uses_centered_column_spec_per_column(self):
        # Arrange
        block = {"type": "table", "rows": [["A", "B", "C"]]}
        # Act
        result = _convert_table(block)
        # Assert
        assert "|c|c|c|" in result


# =============================================================================
# _convert_caption
# =============================================================================


class TestConvertCaption:
    """Tests for _convert_caption helper function."""

    def test_convert_caption_figure_emits_begin_figure(self):
        # Arrange
        block = {
            "type": "caption",
            "caption_type": "figure",
            "number": "1",
            "caption_text": "A sample figure",
        }
        # Act
        result = _convert_caption(block)
        # Assert
        assert r"\begin{figure}" in result

    def test_convert_caption_figure_emits_caption_command(self):
        # Arrange
        block = {
            "type": "caption",
            "caption_type": "figure",
            "number": "1",
            "caption_text": "A sample figure",
        }
        # Act
        result = _convert_caption(block)
        # Assert
        assert r"\caption{A sample figure}" in result

    def test_convert_caption_figure_emits_label_with_fig_prefix(self):
        # Arrange
        block = {
            "type": "caption",
            "caption_type": "figure",
            "number": "1",
            "caption_text": "A sample figure",
        }
        # Act
        result = _convert_caption(block)
        # Assert
        assert r"\label{fig:1}" in result

    def test_convert_caption_figure_emits_end_figure(self):
        # Arrange
        block = {
            "type": "caption",
            "caption_type": "figure",
            "number": "1",
            "caption_text": "A sample figure",
        }
        # Act
        result = _convert_caption(block)
        # Assert
        assert r"\end{figure}" in result

    def test_convert_caption_figure_with_image_hash_emits_includegraphics(self):
        # Arrange
        block = {
            "type": "caption",
            "caption_type": "figure",
            "number": "2",
            "caption_text": "With image",
            "image_hash": "abc123",
        }
        image_map = {"abc123": "figures/fig_1.png"}
        # Act
        result = _convert_caption(block, image_map)
        # Assert
        assert r"\includegraphics" in result

    def test_convert_caption_figure_with_image_hash_resolves_to_filename(self):
        # Arrange
        block = {
            "type": "caption",
            "caption_type": "figure",
            "number": "2",
            "caption_text": "With image",
            "image_hash": "abc123",
        }
        image_map = {"abc123": "figures/fig_1.png"}
        # Act
        result = _convert_caption(block, image_map)
        # Assert
        assert "figures/fig_1" in result

    def test_convert_caption_table_includes_table_number_prefix(self):
        # Arrange
        block = {
            "type": "caption",
            "caption_type": "table",
            "number": "1",
            "caption_text": "Sample table",
        }
        # Act
        result = _convert_caption(block)
        # Assert
        assert "Table 1" in result

    def test_convert_caption_table_includes_caption_text_body(self):
        # Arrange
        block = {
            "type": "caption",
            "caption_type": "table",
            "number": "1",
            "caption_text": "Sample table",
        }
        # Act
        result = _convert_caption(block)
        # Assert
        assert "Sample table" in result

    def test_convert_caption_generic_no_type_emits_caption_word(self):
        # Arrange
        block = {"type": "caption", "caption_text": "Some caption"}
        # Act
        result = _convert_caption(block)
        # Assert
        assert "Caption:" in result


# =============================================================================
# _convert_image
# =============================================================================


class TestConvertImage:
    """Tests for _convert_image helper function."""

    def test_convert_image_with_known_hash_emits_includegraphics(self):
        # Arrange
        block = {"type": "image", "image_hash": "hash123"}
        image_map = {"hash123": "figures/fig_1.png"}
        # Act
        result = _convert_image(block, image_map)
        # Assert
        assert r"\includegraphics" in result

    def test_convert_image_with_known_hash_resolves_to_filename(self):
        # Arrange
        block = {"type": "image", "image_hash": "hash123"}
        image_map = {"hash123": "figures/fig_1.png"}
        # Act
        result = _convert_image(block, image_map)
        # Assert
        assert "figures/fig_1" in result

    def test_convert_image_with_unknown_hash_emits_placeholder_text(self):
        # Arrange
        block = {"type": "image", "image_hash": "unknown"}
        # Act
        result = _convert_image(block, {})
        # Assert
        assert "placeholder" in result.lower()

    def test_convert_image_with_custom_width_propagates_width_argument(self):
        # Arrange
        block = {
            "type": "image",
            "image_hash": "hash123",
            "width": "0.5\\textwidth",
        }
        image_map = {"hash123": "figures/fig_1.png"}
        # Act
        result = _convert_image(block, image_map)
        # Assert
        assert "width=0.5" in result


# =============================================================================
# _convert_list_item
# =============================================================================


class TestConvertListItem:
    """Tests for _convert_list_item helper function."""

    def test_convert_list_item_emits_item_command_with_text(self):
        # Arrange
        block = {"type": "list-item", "text": "First item"}
        # Act
        result = _convert_list_item(block)
        # Assert
        assert r"\item First item" in result

    def test_convert_list_item_escapes_dollar_sign_in_text(self):
        # Arrange
        block = {"type": "list-item", "text": "Item with $100"}
        # Act
        result = _convert_list_item(block)
        # Assert
        assert r"\$" in result


# =============================================================================
# _convert_equation
# =============================================================================


class TestConvertEquation:
    """Tests for _convert_equation helper function."""

    def test_convert_equation_emits_begin_equation_environment(self):
        # Arrange
        block = {"type": "equation", "latex": "E = mc^2"}
        # Act
        result = _convert_equation(block)
        # Assert
        assert r"\begin{equation}" in result

    def test_convert_equation_includes_supplied_latex_body(self):
        # Arrange
        block = {"type": "equation", "latex": "E = mc^2"}
        # Act
        result = _convert_equation(block)
        # Assert
        assert "E = mc^2" in result

    def test_convert_equation_emits_end_equation_environment(self):
        # Arrange
        block = {"type": "equation", "latex": "E = mc^2"}
        # Act
        result = _convert_equation(block)
        # Assert
        assert r"\end{equation}" in result

    def test_convert_equation_text_fallback_still_emits_begin_equation(self):
        # Arrange
        block = {"type": "equation", "text": "x + y = z"}
        # Act
        result = _convert_equation(block)
        # Assert
        assert r"\begin{equation}" in result

    def test_convert_equation_returns_empty_string_when_no_content(self):
        # Arrange
        block = {"type": "equation"}
        # Act
        result = _convert_equation(block)
        # Assert
        assert result == ""


# =============================================================================
# _convert_reference_to_latex
# =============================================================================


class TestConvertReference:
    """Tests for _convert_reference_to_latex helper function."""

    def test_convert_reference_numbered_emits_bibitem_with_ref_key(self):
        # Arrange
        ref = {"number": 1, "text": "Author, Title, Year"}
        # Act
        result = _convert_reference_to_latex(ref)
        # Assert
        assert r"\bibitem{ref1}" in result

    def test_convert_reference_numbered_includes_author_text(self):
        # Arrange
        ref = {"number": 1, "text": "Author, Title, Year"}
        # Act
        result = _convert_reference_to_latex(ref)
        # Assert
        assert "Author" in result

    def test_convert_reference_unnumbered_emits_empty_bibitem(self):
        # Arrange
        ref = {"text": "Anonymous reference"}
        # Act
        result = _convert_reference_to_latex(ref)
        # Assert
        assert r"\bibitem{}" in result


# =============================================================================
# _generate_bibtex
# =============================================================================


class TestGenerateBibtex:
    """Tests for _generate_bibtex helper function."""

    def test_generate_bibtex_single_ref_emits_misc_entry_with_ref1_key(self):
        # Arrange
        refs = [{"number": 1, "text": "Smith, J. Paper Title. 2020"}]
        # Act
        result = _generate_bibtex(refs)
        # Assert
        assert "@misc{ref1" in result

    def test_generate_bibtex_single_ref_emits_note_field(self):
        # Arrange
        refs = [{"number": 1, "text": "Smith, J. Paper Title. 2020"}]
        # Act
        result = _generate_bibtex(refs)
        # Assert
        assert "note" in result

    def test_generate_bibtex_multiple_refs_emits_first_misc_entry(self):
        # Arrange
        refs = [
            {"number": 1, "text": "First ref"},
            {"number": 2, "text": "Second ref"},
        ]
        # Act
        result = _generate_bibtex(refs)
        # Assert
        assert "@misc{ref1" in result

    def test_generate_bibtex_multiple_refs_emits_second_misc_entry(self):
        # Arrange
        refs = [
            {"number": 1, "text": "First ref"},
            {"number": 2, "text": "Second ref"},
        ]
        # Act
        result = _generate_bibtex(refs)
        # Assert
        assert "@misc{ref2" in result


# =============================================================================
# _parse_latex_log
# =============================================================================


class TestParseLatexLog:
    """Tests for _parse_latex_log helper function."""

    def test_parse_latex_log_returns_at_least_one_error_for_undefined_sequence(
        self,
    ):
        # Arrange
        log = """
! Undefined control sequence.
l.15 \\badcommand
"""
        # Act
        errors, _warnings = _parse_latex_log(log)
        # Assert
        assert len(errors) >= 1

    def test_parse_latex_log_first_error_mentions_undefined_control_sequence(
        self,
    ):
        # Arrange
        log = """
! Undefined control sequence.
l.15 \\badcommand
"""
        # Act
        errors, _warnings = _parse_latex_log(log)
        # Assert
        assert "Undefined control sequence" in errors[0]

    def test_parse_latex_log_returns_at_least_one_warning_for_undefined_reference(
        self,
    ):
        # Arrange
        log = """
LaTeX Warning: Reference `fig:1' on page 1 undefined
"""
        # Act
        _errors, warnings = _parse_latex_log(log)
        # Assert
        assert len(warnings) >= 1

    def test_parse_latex_log_collects_overfull_hbox_into_warnings(self):
        # Arrange
        log = """
Overfull \\hbox (10.0pt too wide) in paragraph
"""
        # Act
        _errors, warnings = _parse_latex_log(log)
        # Assert
        assert any("Overfull" in w for w in warnings)

    def test_parse_latex_log_empty_input_returns_no_errors(self):
        # Arrange
        log = ""
        # Act
        errors, _warnings = _parse_latex_log(log)
        # Assert
        assert errors == []

    def test_parse_latex_log_empty_input_returns_no_warnings(self):
        # Arrange
        log = ""
        # Act
        _errors, warnings = _parse_latex_log(log)
        # Assert
        assert warnings == []


# =============================================================================
# JOURNAL_PRESETS
# =============================================================================


class TestJournalPresets:
    """Tests for JOURNAL_PRESETS configuration."""

    @pytest.mark.parametrize(
        "preset_name",
        ["article", "ieee", "elsevier", "springer", "aps", "mdpi", "acm"],
    )
    def test_journal_presets_dict_contains_expected_preset_key(
        self, preset_name
    ):
        # Arrange
        presets = JOURNAL_PRESETS
        # Act
        present = preset_name in presets
        # Assert
        assert present

    @pytest.mark.parametrize("preset_name", list(JOURNAL_PRESETS.keys()))
    def test_journal_preset_entry_defines_document_class_key(
        self, preset_name
    ):
        # Arrange
        preset = JOURNAL_PRESETS[preset_name]
        # Act
        has_key = "document_class" in preset
        # Assert
        assert has_key

    @pytest.mark.parametrize("preset_name", list(JOURNAL_PRESETS.keys()))
    def test_journal_preset_entry_defines_class_options_key(self, preset_name):
        # Arrange
        preset = JOURNAL_PRESETS[preset_name]
        # Act
        has_key = "class_options" in preset
        # Assert
        assert has_key

    @pytest.mark.parametrize("preset_name", list(JOURNAL_PRESETS.keys()))
    def test_journal_preset_entry_defines_required_packages_key(
        self, preset_name
    ):
        # Arrange
        preset = JOURNAL_PRESETS[preset_name]
        # Act
        has_key = "required_packages" in preset
        # Assert
        assert has_key

    def test_journal_preset_ieee_uses_ieeetran_document_class(self):
        # Arrange
        preset = JOURNAL_PRESETS["ieee"]
        # Act
        doc_class = preset["document_class"]
        # Assert
        assert doc_class == "IEEEtran"

    def test_journal_preset_ieee_class_options_include_conference(self):
        # Arrange
        preset = JOURNAL_PRESETS["ieee"]
        # Act
        options = preset["class_options"]
        # Assert
        assert "conference" in options


# =============================================================================
# CompileResult
# =============================================================================


class TestCompileResult:
    """Tests for CompileResult dataclass."""

    def test_compile_result_success_records_success_flag_true(self):
        # Arrange
        kwargs = dict(
            success=True,
            pdf_path=Path("/tmp/test.pdf"),
            exit_code=0,
            stdout="Output",
            stderr="",
        )
        # Act
        result = CompileResult(**kwargs)
        # Assert
        assert result.success is True

    def test_compile_result_success_records_exit_code_zero(self):
        # Arrange
        kwargs = dict(
            success=True,
            pdf_path=Path("/tmp/test.pdf"),
            exit_code=0,
            stdout="Output",
            stderr="",
        )
        # Act
        result = CompileResult(**kwargs)
        # Assert
        assert result.exit_code == 0

    def test_compile_result_success_defaults_errors_to_empty_list(self):
        # Arrange
        kwargs = dict(
            success=True,
            pdf_path=Path("/tmp/test.pdf"),
            exit_code=0,
            stdout="Output",
            stderr="",
        )
        # Act
        result = CompileResult(**kwargs)
        # Assert
        assert result.errors == []

    def test_compile_result_success_defaults_warnings_to_empty_list(self):
        # Arrange
        kwargs = dict(
            success=True,
            pdf_path=Path("/tmp/test.pdf"),
            exit_code=0,
            stdout="Output",
            stderr="",
        )
        # Act
        result = CompileResult(**kwargs)
        # Assert
        assert result.warnings == []

    def test_compile_result_failure_records_success_flag_false(self):
        # Arrange
        kwargs = dict(
            success=False,
            pdf_path=None,
            exit_code=1,
            stdout="",
            stderr="Error",
            errors=["Compile error"],
        )
        # Act
        result = CompileResult(**kwargs)
        # Assert
        assert result.success is False

    def test_compile_result_failure_keeps_none_pdf_path(self):
        # Arrange
        kwargs = dict(
            success=False,
            pdf_path=None,
            exit_code=1,
            stdout="",
            stderr="Error",
            errors=["Compile error"],
        )
        # Act
        result = CompileResult(**kwargs)
        # Assert
        assert result.pdf_path is None

    def test_compile_result_failure_keeps_compile_error_in_errors_list(self):
        # Arrange
        kwargs = dict(
            success=False,
            pdf_path=None,
            exit_code=1,
            stdout="",
            stderr="Error",
            errors=["Compile error"],
        )
        # Act
        result = CompileResult(**kwargs)
        # Assert
        assert "Compile error" in result.errors

    def test_compile_result_default_errors_list_is_empty(self):
        # Arrange
        kwargs = dict(
            success=True,
            pdf_path=None,
            exit_code=0,
            stdout="",
            stderr="",
        )
        # Act
        result = CompileResult(**kwargs)
        # Assert
        assert result.errors == []

    def test_compile_result_default_warnings_list_is_empty(self):
        # Arrange
        kwargs = dict(
            success=True,
            pdf_path=None,
            exit_code=0,
            stdout="",
            stderr="",
        )
        # Act
        result = CompileResult(**kwargs)
        # Assert
        assert result.warnings == []


# =============================================================================
# export_tex
# =============================================================================


def _minimal_doc():
    return {
        "blocks": [],
        "metadata": {},
        "references": [],
        "images": [],
    }


class TestExportTexMinimal:
    """Tests for export_tex with minimal input document."""

    def test_export_tex_returns_supplied_output_path_for_minimal_doc(
        self, tmp_path
    ):
        # Arrange
        output_path = tmp_path / "test.tex"
        # Act
        result = export_tex(_minimal_doc(), output_path)
        # Assert
        assert result == output_path

    def test_export_tex_minimal_doc_creates_file_on_disk(self, tmp_path):
        # Arrange
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(_minimal_doc(), output_path)
        # Assert
        assert output_path.exists()

    def test_export_tex_minimal_doc_writes_documentclass_article_directive(
        self, tmp_path
    ):
        # Arrange
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(_minimal_doc(), output_path)
        # Assert
        assert r"\documentclass{article}" in output_path.read_text()

    def test_export_tex_minimal_doc_writes_begin_document_marker(
        self, tmp_path
    ):
        # Arrange
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(_minimal_doc(), output_path)
        # Assert
        assert r"\begin{document}" in output_path.read_text()

    def test_export_tex_minimal_doc_writes_end_document_marker(self, tmp_path):
        # Arrange
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(_minimal_doc(), output_path)
        # Assert
        assert r"\end{document}" in output_path.read_text()


class TestExportTexMetadata:
    """Tests for export_tex with metadata."""

    def test_export_tex_with_title_metadata_writes_title_command(
        self, tmp_path
    ):
        # Arrange
        doc = _minimal_doc()
        doc["metadata"] = {"title": "Test Title", "author": "Test Author"}
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path)
        # Assert
        assert r"\title{Test Title}" in output_path.read_text()

    def test_export_tex_with_author_metadata_writes_author_command(
        self, tmp_path
    ):
        # Arrange
        doc = _minimal_doc()
        doc["metadata"] = {"title": "Test Title", "author": "Test Author"}
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path)
        # Assert
        assert r"\author{Test Author}" in output_path.read_text()

    def test_export_tex_with_metadata_writes_maketitle_command(self, tmp_path):
        # Arrange
        doc = _minimal_doc()
        doc["metadata"] = {"title": "Test Title", "author": "Test Author"}
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path)
        # Assert
        assert r"\maketitle" in output_path.read_text()


class TestExportTexBlocks:
    """Tests for export_tex with body block content."""

    def test_export_tex_with_heading_block_writes_section_command(
        self, tmp_path
    ):
        # Arrange
        doc = _minimal_doc()
        doc["blocks"] = [
            {"type": "heading", "level": 1, "text": "Introduction"}
        ]
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path)
        # Assert
        assert r"\section{Introduction}" in output_path.read_text()

    def test_export_tex_with_paragraphs_writes_first_paragraph_text(
        self, tmp_path
    ):
        # Arrange
        doc = _minimal_doc()
        doc["blocks"] = [
            {"type": "paragraph", "text": "First paragraph."},
            {"type": "paragraph", "text": "Second paragraph."},
        ]
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path)
        # Assert
        assert "First paragraph." in output_path.read_text()

    def test_export_tex_with_paragraphs_writes_second_paragraph_text(
        self, tmp_path
    ):
        # Arrange
        doc = _minimal_doc()
        doc["blocks"] = [
            {"type": "paragraph", "text": "First paragraph."},
            {"type": "paragraph", "text": "Second paragraph."},
        ]
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path)
        # Assert
        assert "Second paragraph." in output_path.read_text()

    def test_export_tex_unordered_list_opens_itemize_environment(
        self, tmp_path
    ):
        # Arrange
        doc = _minimal_doc()
        doc["blocks"] = [
            {
                "type": "list-item",
                "text": "First item",
                "list_type": "unordered",
            },
            {
                "type": "list-item",
                "text": "Second item",
                "list_type": "unordered",
            },
            {"type": "paragraph", "text": "After list."},
        ]
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path)
        # Assert
        assert r"\begin{itemize}" in output_path.read_text()

    def test_export_tex_unordered_list_emits_first_item_command(self, tmp_path):
        # Arrange
        doc = _minimal_doc()
        doc["blocks"] = [
            {
                "type": "list-item",
                "text": "First item",
                "list_type": "unordered",
            },
            {
                "type": "list-item",
                "text": "Second item",
                "list_type": "unordered",
            },
        ]
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path)
        # Assert
        assert r"\item First item" in output_path.read_text()

    def test_export_tex_unordered_list_emits_second_item_command(
        self, tmp_path
    ):
        # Arrange
        doc = _minimal_doc()
        doc["blocks"] = [
            {
                "type": "list-item",
                "text": "First item",
                "list_type": "unordered",
            },
            {
                "type": "list-item",
                "text": "Second item",
                "list_type": "unordered",
            },
        ]
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path)
        # Assert
        assert r"\item Second item" in output_path.read_text()

    def test_export_tex_unordered_list_closes_itemize_environment(
        self, tmp_path
    ):
        # Arrange
        doc = _minimal_doc()
        doc["blocks"] = [
            {
                "type": "list-item",
                "text": "First item",
                "list_type": "unordered",
            },
            {
                "type": "list-item",
                "text": "Second item",
                "list_type": "unordered",
            },
        ]
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path)
        # Assert
        assert r"\end{itemize}" in output_path.read_text()

    def test_export_tex_ordered_list_opens_enumerate_environment(
        self, tmp_path
    ):
        # Arrange
        doc = _minimal_doc()
        doc["blocks"] = [
            {"type": "list-item", "text": "First", "list_type": "ordered"},
            {"type": "list-item", "text": "Second", "list_type": "ordered"},
        ]
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path)
        # Assert
        assert r"\begin{enumerate}" in output_path.read_text()

    def test_export_tex_ordered_list_closes_enumerate_environment(
        self, tmp_path
    ):
        # Arrange
        doc = _minimal_doc()
        doc["blocks"] = [
            {"type": "list-item", "text": "First", "list_type": "ordered"},
            {"type": "list-item", "text": "Second", "list_type": "ordered"},
        ]
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path)
        # Assert
        assert r"\end{enumerate}" in output_path.read_text()


class TestExportTexReferences:
    """Tests for export_tex with references."""

    def test_export_tex_with_references_opens_thebibliography_environment(
        self, tmp_path
    ):
        # Arrange
        doc = _minimal_doc()
        doc["references"] = [{"number": 1, "text": "Smith, 2020"}]
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path)
        # Assert
        assert r"\begin{thebibliography}" in output_path.read_text()

    def test_export_tex_with_references_emits_bibitem_for_ref_one(
        self, tmp_path
    ):
        # Arrange
        doc = _minimal_doc()
        doc["references"] = [{"number": 1, "text": "Smith, 2020"}]
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path)
        # Assert
        assert r"\bibitem{ref1}" in output_path.read_text()

    def test_export_tex_with_references_closes_thebibliography_environment(
        self, tmp_path
    ):
        # Arrange
        doc = _minimal_doc()
        doc["references"] = [{"number": 1, "text": "Smith, 2020"}]
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path)
        # Assert
        assert r"\end{thebibliography}" in output_path.read_text()


class TestExportTexBibtex:
    """Tests for export_tex with use_bibtex=True."""

    def test_export_tex_use_bibtex_emits_bibliography_command(self, tmp_path):
        # Arrange
        doc = _minimal_doc()
        doc["references"] = [{"number": 1, "text": "Reference text"}]
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path, use_bibtex=True)
        # Assert
        assert r"\bibliography{test}" in output_path.read_text()

    def test_export_tex_use_bibtex_creates_companion_bib_file(self, tmp_path):
        # Arrange
        doc = _minimal_doc()
        doc["references"] = [{"number": 1, "text": "Reference text"}]
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path, use_bibtex=True)
        # Assert
        assert output_path.with_suffix(".bib").exists()

    def test_export_tex_use_bibtex_writes_misc_entry_into_bib_file(
        self, tmp_path
    ):
        # Arrange
        doc = _minimal_doc()
        doc["references"] = [{"number": 1, "text": "Reference text"}]
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path, use_bibtex=True)
        # Assert
        assert "@misc" in output_path.with_suffix(".bib").read_text()


class TestExportTexOptions:
    """Tests for export_tex with class options, presets, packages."""

    def test_export_tex_with_ieee_preset_emits_ieeetran_documentclass(
        self, tmp_path
    ):
        # Arrange
        doc = _minimal_doc()
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path, journal_preset="ieee")
        # Assert
        assert (
            r"\documentclass[conference]{IEEEtran}" in output_path.read_text()
        )

    def test_export_tex_with_class_options_includes_12pt_option(
        self, tmp_path
    ):
        # Arrange
        doc = _minimal_doc()
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path, class_options=["12pt", "twocolumn"])
        # Assert
        assert "12pt" in output_path.read_text()

    def test_export_tex_with_class_options_includes_twocolumn_option(
        self, tmp_path
    ):
        # Arrange
        doc = _minimal_doc()
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path, class_options=["12pt", "twocolumn"])
        # Assert
        assert "twocolumn" in output_path.read_text()

    def test_export_tex_with_packages_includes_usepackage_booktabs(
        self, tmp_path
    ):
        # Arrange
        doc = _minimal_doc()
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path, packages=["booktabs", "siunitx"])
        # Assert
        assert r"\usepackage{booktabs}" in output_path.read_text()

    def test_export_tex_with_packages_includes_usepackage_siunitx(
        self, tmp_path
    ):
        # Arrange
        doc = _minimal_doc()
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path, packages=["booktabs", "siunitx"])
        # Assert
        assert r"\usepackage{siunitx}" in output_path.read_text()

    def test_export_tex_with_preamble_string_includes_preamble_body(
        self, tmp_path
    ):
        # Arrange
        doc = _minimal_doc()
        preamble = r"\newcommand{\mycommand}{test}"
        output_path = tmp_path / "test.tex"
        # Act
        export_tex(doc, output_path, preamble=preamble)
        # Assert
        assert preamble in output_path.read_text()


# =============================================================================
# compile_tex
# =============================================================================


class TestCompileTexErrors:
    """Tests for compile_tex error and edge cases."""

    def test_compile_tex_nonexistent_file_returns_failure_result(self):
        # Arrange
        bad_path = "/nonexistent/path/file.tex"
        # Act
        result = compile_tex(bad_path)
        # Assert
        assert result.success is False

    def test_compile_tex_nonexistent_file_reports_not_found_in_output(self):
        # Arrange
        bad_path = "/nonexistent/path/file.tex"
        # Act
        result = compile_tex(bad_path)
        # Assert
        assert (
            "not found" in result.stderr.lower()
            or "not found" in str(result.errors).lower()
        )

    def test_compile_tex_missing_compiler_returns_failure_result(
        self, tmp_path
    ):
        # Arrange
        tex_path = tmp_path / "test.tex"
        tex_path.write_text(
            r"\documentclass{article}\begin{document}Test\end{document}"
        )
        # Act
        result = compile_tex(tex_path, compiler="nonexistent_compiler")
        # Assert
        assert result.success is False

    def test_compile_tex_missing_compiler_reports_exit_code_127(self, tmp_path):
        # Arrange
        tex_path = tmp_path / "test.tex"
        tex_path.write_text(
            r"\documentclass{article}\begin{document}Test\end{document}"
        )
        # Act
        result = compile_tex(tex_path, compiler="nonexistent_compiler")
        # Assert
        assert result.exit_code == 127


def _install_sleep_shim(bin_dir: Path, *, shim_name: str, sleep_seconds: int = 30) -> Path:
    """Write a real shell shim that just sleeps, exercising the real
    subprocess + timeout codepath in `compile_tex` instead of mocking
    `subprocess.run`. Returns the shim binary path.
    """
    bin_dir.mkdir(parents=True, exist_ok=True)
    shim = bin_dir / shim_name
    shim.write_text(
        "#!/usr/bin/env bash\n"
        f"sleep {sleep_seconds}\n"
        "exit 0\n"
    )
    mode = shim.stat().st_mode
    shim.chmod(mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    return shim


class TestCompileTexTimeout:
    """Tests for compile_tex subprocess timeout handling — no mocks; the
    test prepends a real sleep-only shell shim onto $PATH and asks
    compile_tex for a 1-second timeout, exercising the real
    `subprocess.TimeoutExpired` codepath.
    """

    def test_compile_tex_subprocess_timeout_returns_failure_result(
        self, tmp_path
    ):
        # Arrange
        bin_dir = tmp_path / "bin"
        _install_sleep_shim(bin_dir, shim_name="slow_pdflatex", sleep_seconds=30)
        tex_path = tmp_path / "test.tex"
        tex_path.write_text(
            r"\documentclass{article}\begin{document}Test\end{document}"
        )
        original_path = os.environ.get("PATH", "")
        os.environ["PATH"] = f"{bin_dir}{os.pathsep}{original_path}"
        try:
            # Act
            result = compile_tex(
                tex_path, compiler="slow_pdflatex", timeout=1, clean=False
            )
        finally:
            os.environ["PATH"] = original_path
        # Assert
        assert result.success is False

    def test_compile_tex_subprocess_timeout_records_exit_code_124(
        self, tmp_path
    ):
        # Arrange
        bin_dir = tmp_path / "bin"
        _install_sleep_shim(bin_dir, shim_name="slow_pdflatex", sleep_seconds=30)
        tex_path = tmp_path / "test.tex"
        tex_path.write_text(
            r"\documentclass{article}\begin{document}Test\end{document}"
        )
        original_path = os.environ.get("PATH", "")
        os.environ["PATH"] = f"{bin_dir}{os.pathsep}{original_path}"
        try:
            # Act
            result = compile_tex(
                tex_path, compiler="slow_pdflatex", timeout=1, clean=False
            )
        finally:
            os.environ["PATH"] = original_path
        # Assert
        assert result.exit_code == 124

    def test_compile_tex_subprocess_timeout_reports_timed_out_in_stderr(
        self, tmp_path
    ):
        # Arrange
        bin_dir = tmp_path / "bin"
        _install_sleep_shim(bin_dir, shim_name="slow_pdflatex", sleep_seconds=30)
        tex_path = tmp_path / "test.tex"
        tex_path.write_text(
            r"\documentclass{article}\begin{document}Test\end{document}"
        )
        original_path = os.environ.get("PATH", "")
        os.environ["PATH"] = f"{bin_dir}{os.pathsep}{original_path}"
        try:
            # Act
            result = compile_tex(
                tex_path, compiler="slow_pdflatex", timeout=1, clean=False
            )
        finally:
            os.environ["PATH"] = original_path
        # Assert
        assert "timed out" in result.stderr.lower()


@pytest.mark.skipif(
    shutil.which("pdflatex") is None,
    reason="pdflatex not installed",
)
class TestCompileTexRealLatex:
    """Tests for compile_tex against a real pdflatex install."""

    def test_compile_tex_simple_document_succeeds_when_pdflatex_available(
        self, tmp_path
    ):
        # Arrange
        tex_path = tmp_path / "test.tex"
        tex_path.write_text(
            r"""
\documentclass{article}
\begin{document}
Hello, World!
\end{document}
"""
        )
        # Act
        result = compile_tex(tex_path, clean=True)
        # Assert
        assert result.success is True

    def test_compile_tex_simple_document_produces_pdf_file_on_disk(
        self, tmp_path
    ):
        # Arrange
        tex_path = tmp_path / "test.tex"
        tex_path.write_text(
            r"""
\documentclass{article}
\begin{document}
Hello, World!
\end{document}
"""
        )
        # Act
        result = compile_tex(tex_path, clean=True)
        # Assert
        assert result.pdf_path is not None and result.pdf_path.exists()

    def test_compile_tex_bad_latex_reports_failure_result(self, tmp_path):
        # Arrange
        tex_path = tmp_path / "test.tex"
        tex_path.write_text(
            r"""
\documentclass{article}
\begin{document}
\badcommand
\end{document}
"""
        )
        # Act
        result = compile_tex(tex_path, clean=False)
        # Assert
        assert result.success is False

    def test_compile_tex_bad_latex_collects_at_least_one_parsed_error(
        self, tmp_path
    ):
        # Arrange
        tex_path = tmp_path / "test.tex"
        tex_path.write_text(
            r"""
\documentclass{article}
\begin{document}
\badcommand
\end{document}
"""
        )
        # Act
        result = compile_tex(tex_path, clean=False)
        # Assert
        assert len(result.errors) > 0


# =============================================================================
# _write_images_to_dir
# =============================================================================


class TestWriteImagesToDir:
    """Tests for _write_images_to_dir helper function."""

    def test_write_images_to_dir_returns_mapping_keyed_by_image_hash(
        self, tmp_path
    ):
        # Arrange
        image_dir = tmp_path / "figures"
        image_dir.mkdir()
        images = [
            {
                "hash": "abc123",
                "extension": ".png",
                "data": b"\x89PNG\r\n\x1a\n",
            },
        ]
        # Act
        result = _write_images_to_dir(images, image_dir, tmp_path)
        # Assert
        assert "abc123" in result

    def test_write_images_to_dir_value_contains_image_subdirectory_name(
        self, tmp_path
    ):
        # Arrange
        image_dir = tmp_path / "figures"
        image_dir.mkdir()
        images = [
            {
                "hash": "abc123",
                "extension": ".png",
                "data": b"\x89PNG\r\n\x1a\n",
            },
        ]
        # Act
        result = _write_images_to_dir(images, image_dir, tmp_path)
        # Assert
        assert "figures" in result["abc123"]

    def test_write_images_to_dir_deduplicates_entries_with_same_hash(
        self, tmp_path
    ):
        # Arrange
        image_dir = tmp_path / "figures"
        image_dir.mkdir()
        images = [
            {"hash": "abc123", "extension": ".png", "data": b"data1"},
            {"hash": "abc123", "extension": ".png", "data": b"data2"},
        ]
        # Act
        result = _write_images_to_dir(images, image_dir, tmp_path)
        # Assert
        assert len(result) == 1

    def test_write_images_to_dir_skips_entries_missing_hash_or_data(
        self, tmp_path
    ):
        # Arrange
        image_dir = tmp_path / "figures"
        image_dir.mkdir()
        images = [
            {"hash": None, "extension": ".png", "data": b"data"},
            {"hash": "abc", "extension": ".png", "data": None},
        ]
        # Act
        result = _write_images_to_dir(images, image_dir, tmp_path)
        # Assert
        assert len(result) == 0


# =============================================================================
# _build_latex_document
# =============================================================================


class TestBuildLatexDocument:
    """Tests for _build_latex_document helper function."""

    def test_build_latex_document_minimal_emits_documentclass_article(self):
        # Arrange
        kwargs = dict(
            blocks=[],
            metadata={},
            references=[],
            document_class="article",
        )
        # Act
        result = _build_latex_document(**kwargs)
        # Assert
        assert r"\documentclass{article}" in result

    def test_build_latex_document_minimal_emits_begin_document_marker(self):
        # Arrange
        kwargs = dict(
            blocks=[],
            metadata={},
            references=[],
            document_class="article",
        )
        # Act
        result = _build_latex_document(**kwargs)
        # Assert
        assert r"\begin{document}" in result

    def test_build_latex_document_minimal_emits_end_document_marker(self):
        # Arrange
        kwargs = dict(
            blocks=[],
            metadata={},
            references=[],
            document_class="article",
        )
        # Act
        result = _build_latex_document(**kwargs)
        # Assert
        assert r"\end{document}" in result

    def test_build_latex_document_with_class_options_emits_bracketed_options(
        self,
    ):
        # Arrange
        kwargs = dict(
            blocks=[],
            metadata={},
            references=[],
            document_class="article",
            class_options=["12pt", "a4paper"],
        )
        # Act
        result = _build_latex_document(**kwargs)
        # Assert
        assert r"\documentclass[12pt,a4paper]{article}" in result

    @pytest.mark.parametrize(
        "expected",
        [
            r"\usepackage[utf8]{inputenc}",
            r"\usepackage[T1]{fontenc}",
            r"\usepackage{amsmath}",
            r"\usepackage{graphicx}",
            r"\usepackage{hyperref}",
        ],
    )
    def test_build_latex_document_includes_default_package_directive(
        self, expected
    ):
        # Arrange
        kwargs = dict(
            blocks=[],
            metadata={},
            references=[],
            document_class="article",
        )
        # Act
        result = _build_latex_document(**kwargs)
        # Assert
        assert expected in result


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])

# EOF
