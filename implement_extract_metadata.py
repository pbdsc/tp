from __future__ import annotations

from typing import Iterable, Optional

import pandas as pd


# Standard chemical element symbols (1-2 letters) in canonical case.
_ELEMENT_SYMBOLS = {
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
    "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y",
    "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce",
    "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir",
    "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm",
    "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc",
    "Lv", "Ts", "Og",
}
_ELEMENT_LOOKUP = {symbol.lower(): symbol for symbol in _ELEMENT_SYMBOLS}


def extract_metadata(
    column_names: Iterable[str],
    analyses: Iterable[str],
    rms: Iterable[str],
) -> pd.DataFrame:
    """Extract metadata from column names.

    Output columns:
    - column_name
    - level
    - rm
    - source
    - flag_qty
    - element
    - analysis
    """
    analysis_list = [a for a in analyses]
    rm_list = [r for r in rms]

    analysis_pairs = [(a, a.lower()) for a in analysis_list if a]
    rm_pairs = [(r, r.lower()) for r in rm_list if r]

    rows = []

    for column_name in column_names:
        name = column_name
        lower_name = name.lower()

        level: Optional[int] = None
        if name.startswith("L") and len(name) > 1 and name[1].isdigit():
            parsed_level = int(name[1])
            level = 99 if parsed_level == 0 else parsed_level

        matched_rm = next((orig for orig, low in rm_pairs if low in lower_name), None)
        matched_analysis = next((orig for orig, low in analysis_pairs if low in lower_name), None)

        first_underscore = name.find("_")
        char_before_first_underscore = name[first_underscore - 1] if first_underscore > 0 else ""
        source: Optional[str] = None
        if char_before_first_underscore == "M":
            source = "M"
        elif char_before_first_underscore == "L":
            source = "L"

        flag_qty: Optional[bool] = True if ("qty" in lower_name or "quantity" in lower_name) else None

        last_part = name.rsplit("_", 1)[-1]
        element: Optional[str] = None
        if 1 <= len(last_part) <= 2:
            element = _ELEMENT_LOOKUP.get(last_part.lower())

        rows.append(
            {
                "column_name": name,
                "level": level,
                "rm": matched_rm,
                "source": source,
                "flag_qty": flag_qty,
                "element": element,
                "analysis": matched_analysis,
            }
        )

    return pd.DataFrame(
        rows,
        columns=["column_name", "level", "rm", "source", "flag_qty", "element", "analysis"],
    )
