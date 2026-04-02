from __future__ import annotations

from typing import Iterable

import pandas as pd


def build_column_metadata(values: Iterable[str]) -> pd.DataFrame:
    """Build a metadata dataframe from a list of strings.

    Output columns:
    - col_name
    - genealogy_level
    - flag_proc_param
    - flag_rm
    - elem_name
    """
    rows = []

    for value in values:
        first_underscore = value.find("_")
        char_before_first_underscore = (
            value[first_underscore - 1] if first_underscore > 0 else ""
        )

        if value.startswith("L") and len(value) > 1 and value[1].isdigit():
            genealogy_level = int(value[1])
        else:
            genealogy_level = 99

        flag_proc_param = char_before_first_underscore == "M"
        flag_rm = char_before_first_underscore == "L"

        elem_name = None
        if flag_rm:
            last_segment = value.rsplit("_", 1)[-1]
            if 1 <= len(last_segment) <= 2:
                elem_name = last_segment

        rows.append(
            {
                "col_name": value,
                "genealogy_level": genealogy_level,
                "flag_proc_param": flag_proc_param,
                "flag_rm": flag_rm,
                "elem_name": elem_name,
            }
        )

    return pd.DataFrame(
        rows,
        columns=[
            "col_name",
            "genealogy_level",
            "flag_proc_param",
            "flag_rm",
            "elem_name",
        ],
    )
