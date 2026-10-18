"""Step 1 - data cleaning and trading-day returns for DSE OHLCV data.

Input: a table with columns ``Trading_Code, Date, Open, High, Low, Close,
Volume`` (one row per security per trading day).

Output adds three derived columns:

``Observed_Log_Return``
    ``ln(P_t) - ln(P_{t-1})`` per security, in trading-day order. The first
    observation of each security is NaN.
``Volume_Z``
    z-score of volume against its trailing 21-day window (per security).
``Trading_Day_Index``
    1-based trading-day counter per security.

Returns are measured between consecutive *trading* days, so weekends and
market holidays do not create artificial observations.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Union
import warnings

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = ["Trading_Code", "Date", "Open", "High", "Low", "Close", "Volume"]
PRICE_COLUMNS = ["Open", "High", "Low", "Close"]

# DSE trades Sunday-Thursday; the market was closed 26 Mar - 30 May 2020.
NON_TRADING_WEEKDAYS = (4, 5)  # Friday=4, Saturday=5 (pandas dayofweek)
COVID_CLOSURE = ("2020-03-26", "2020-05-30")


def calendar_anomalies(df: pd.DataFrame, date_col: str = "Date") -> dict:
    """Count rows dated on a Friday/Saturday or inside the 2020 market closure.

    Such rows indicate a date-alignment problem in the raw export. They are
    reported, never silently removed (see ``drop_weekend_rows`` and
    ``drop_closure_rows`` in :func:`clean_ohlcv`).
    """
    d = pd.to_datetime(df[date_col], errors="coerce")
    start, end = (pd.Timestamp(x) for x in COVID_CLOSURE)
    return {
        "friday_saturday_rows": int(d.dt.dayofweek.isin(NON_TRADING_WEEKDAYS).sum()),
        "closure_rows": int(((d >= start) & (d <= end)).sum()),
    }


def clean_ohlcv(
    df: pd.DataFrame,
    *,
    drop_weekend_rows: bool = False,
    drop_closure_rows: bool = False,
    verbose: bool = False,
) -> pd.DataFrame:
    """Clean raw OHLCV data and add returns, volume z-score and day index.

    Steps (in order): keep the seven required columns; strip/upper-case
    ``Trading_Code``; parse ``Date`` (bad values become NaT); coerce prices and
    volume to numeric; treat zeros as missing; drop rows lacking a code or a
    date; sort by (code, date); drop duplicate (code, date) rows keeping the
    last; derive the three columns described in the module docstring.

    Parameters
    ----------
    drop_weekend_rows, drop_closure_rows:
        Optional removal of Friday/Saturday rows and rows inside the
        26 Mar - 30 May 2020 closure. Off by default so behaviour matches the
        original notebook; a warning is emitted when such rows are present.
    """
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    out = df[REQUIRED_COLUMNS].copy()

    code = out["Trading_Code"].astype("string").str.strip().str.upper()
    out["Trading_Code"] = code.mask(code == "", pd.NA)
    out["Date"] = pd.to_datetime(out["Date"], errors="coerce")

    numeric = PRICE_COLUMNS + ["Volume"]
    for col in numeric:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    # A price or volume of exactly 0 is not a valid observation.
    out[numeric] = out[numeric].replace(0, np.nan)

    out = out.dropna(subset=["Trading_Code", "Date"])

    anomalies = calendar_anomalies(out)
    if any(anomalies.values()):
        warnings.warn(
            "Calendar anomalies found "
            f"({anomalies['friday_saturday_rows']} Friday/Saturday rows, "
            f"{anomalies['closure_rows']} rows inside the 2020 closure). "
            "Check that dates are aligned to DSE trading days.",
            stacklevel=2,
        )
    if drop_weekend_rows:
        out = out[~out["Date"].dt.dayofweek.isin(NON_TRADING_WEEKDAYS)]
    if drop_closure_rows:
        start, end = (pd.Timestamp(x) for x in COVID_CLOSURE)
        out = out[~out["Date"].between(start, end)]

    out = out.sort_values(["Trading_Code", "Date"]).reset_index(drop=True)

    n_dupes = int(out.duplicated(subset=["Trading_Code", "Date"]).sum())
    out = out.drop_duplicates(subset=["Trading_Code", "Date"], keep="last")
    out = out.reset_index(drop=True)
    if verbose:
        print(f"Duplicate rows removed: {n_dupes}")

    by_code = out.groupby("Trading_Code", sort=False)
    out["Observed_Log_Return"] = by_code["Close"].transform(
        lambda x: np.log(x / x.shift(1))
    )

    # 21-day rolling volume z-score. std() needs >= 2 points, so the first
    # observation of each security is always NaN.
    roll_mean = by_code["Volume"].transform(lambda x: x.rolling(21, min_periods=1).mean())
    roll_std = by_code["Volume"].transform(lambda x: x.rolling(21, min_periods=2).std())
    out["Volume_Z"] = (out["Volume"] - roll_mean) / roll_std

    out["Observed_Log_Return"] = out["Observed_Log_Return"].replace([np.inf, -np.inf], np.nan)
    out["Volume_Z"] = out["Volume_Z"].replace([np.inf, -np.inf], np.nan)

    out["Trading_Day_Index"] = by_code.cumcount() + 1
    return out


def load_ohlcv(path: Union[str, Path], sheet_name: Optional[str] = None) -> pd.DataFrame:
    """Read a CSV or Excel file of raw OHLCV data."""
    p = str(path)
    if p.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(p, sheet_name=sheet_name or 0)
    return pd.read_csv(p)
