"""scitex-tex quickstart: build LaTeX vector strings + LaTeX preview helpers."""

import scitex_tex


def main():
    # 1. to_vec: convert a label into LaTeX vector notation,
    # falling back to plain/unicode if a real LaTeX engine isn't usable.
    ab = scitex_tex.to_vec("AB")
    print("vec(AB) ->", ab)
    assert "AB" in ab

    bc = scitex_tex.to_vec("BC", fallback_strategy="plain")
    print("vec(BC) plain ->", bc)
    assert "BC" in bc

    # 2. to_vec on an empty input is well-defined (returns empty string).
    assert scitex_tex.to_vec("") == ""

    # 3. preview: build a small LaTeX-formatted string list, used for axis
    # labels / titles in matplotlib. We exercise the formatting helper only —
    # no actual TeX compilation is required for this smoke check.
    labels = ["x_1", "x_2", "y"]
    rendered = [scitex_tex.to_vec(lbl) for lbl in labels]
    for orig, latex in zip(labels, rendered):
        print(f"  {orig!r:8s} -> {latex}")
        assert latex  # non-empty


if __name__ == "__main__":
    main()
