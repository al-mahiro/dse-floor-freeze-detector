"""Step 2 - BSEC floor-period classification.

Tags every (security, date) with whether a regulatory floor was in force:

====================  ===============================================
``Floor_Period_Flag``  ``Floor_Period_Regime``
====================  ===============================================
1                      ``ALL_SECURITIES``: floor applied to everyone
1                      ``SECURITY_SPECIFIC``: this security was floored
0                      ``EXEMPTED``: exempted during an EXEMPTED period
0                      ``NO_FLOOR``: no floor regime in effect
0                      ``INVALID_DATE``: date missing or unparseable
====================  ===============================================

A flag of 1 means a floor *could* bind; it does not mean the price was
frozen. Frozen days are identified in Step 3 (:mod:`dse_floor.detector`).
"""

from __future__ import annotations

from typing import Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from .timeline import FLOOR_PERIODS, FloorPeriod


def classify_floor_period(
    date, trading_code: str, periods: Sequence[FloorPeriod] = FLOOR_PERIODS
) -> Tuple[int, str]:
    """Classify one trading day for one security."""
    if pd.isna(date):
        return 0, "INVALID_DATE"
    date = pd.Timestamp(date)
    code = str(trading_code).strip().upper()

    for start, end, regime, companies in periods:
        if date < pd.Timestamp(start) or date > pd.Timestamp(end):
            continue
        if regime == "ALL":
            return 1, "ALL_SECURITIES"
        if regime == "WITH_FLOOR":
            return (1, "SECURITY_SPECIFIC") if code in companies else (0, "NO_FLOOR")
        if regime == "EXEMPTED":
            return (0, "EXEMPTED") if code in companies else (1, "SECURITY_SPECIFIC")
        raise ValueError(f"Unknown regime {regime!r}")
    return 0, "NO_FLOOR"


def add_floor_period_flag(
    df: pd.DataFrame,
    *,
    code_col: str = "Trading_Code",
    date_col: str = "Date",
    periods: Sequence[FloorPeriod] = FLOOR_PERIODS,
) -> pd.DataFrame:
    """Add ``Floor_Period_Flag`` and ``Floor_Period_Regime`` (vectorised).

    Equivalent to applying :func:`classify_floor_period` row by row, but loops
    over the (few) regulatory periods rather than over rows.
    """
    out = df.copy()
    dates = pd.to_datetime(out[date_col], errors="coerce")
    codes = out[code_col].astype("string").str.strip().str.upper()

    flag = np.zeros(len(out), dtype="int8")
    regime = np.full(len(out), "NO_FLOOR", dtype=object)
    regime[dates.isna().to_numpy()] = "INVALID_DATE"
    unresolved = ~dates.isna().to_numpy()  # first matching period wins

    for start, end, kind, companies in periods:
        in_window = unresolved & ((dates >= pd.Timestamp(start)) & (dates <= pd.Timestamp(end))).to_numpy()
        if not in_window.any():
            continue
        if kind == "ALL":
            flag[in_window] = 1
            regime[in_window] = "ALL_SECURITIES"
        else:
            listed = codes.isin(list(companies)).to_numpy()
            if kind == "WITH_FLOOR":
                hit = in_window & listed
                flag[hit] = 1
                regime[hit] = "SECURITY_SPECIFIC"
                # not listed -> stays NO_FLOOR
            elif kind == "EXEMPTED":
                hit = in_window & ~listed
                flag[hit] = 1
                regime[hit] = "SECURITY_SPECIFIC"
                regime[in_window & listed] = "EXEMPTED"
            else:
                raise ValueError(f"Unknown regime {kind!r}")
        unresolved &= ~in_window

    out["Floor_Period_Flag"] = flag
    out["Floor_Period_Regime"] = regime
    return out
