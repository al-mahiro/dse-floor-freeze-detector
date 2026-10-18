"""Step 3 - rule-based floor-lock ("freeze") detector.

Inside each contiguous block of floor-period days the detector estimates the
binding floor from the *lower tail* of observed closes and flags every close
that sits in the floor-associated region ``[block_min, floor]``.

Algorithm (per security, per contiguous block ``b`` with ``Floor_Period_Flag == 1``)
-----------------------------------------------------------------------------------
1. **Ticks.** Prices are converted to integer ticks (``round(close / tick_size)``)
   so equality tests are exact; 31.40 can never differ from 31.40 through
   floating-point noise. The DSE tick size is Tk 0.10.
2. **Lower tail.** Keep ticks ``<= Q_{lower_q}`` of the block's closes. Free
   trading in the upper part of the block would otherwise dominate the mode.
3. **Modal floor.** ``floor_b`` is the most frequent tick in that tail; ties
   resolve to the *lowest* price. Its count is the *modal support*.
4. **Support rule.** If ``support < min_support`` the block gets no estimate and
   none of its days is flagged (there is no fallback to the block minimum).
   A single-day block is the exception: its one close *is* the floor.
5. **Locked region.** A close is floor-locked iff
   ``block_min <= tick <= floor_b``; both ends inclusive, compared as integers.

``Floor_Locked_Flag`` therefore marks the empirical region around the binding
floor, and ``Floor_Price`` is a *data-driven proxy* for the regulatory price
level, not a direct observation of the legal floor.

Known limitation: one floor is estimated per block. If the legal floor was
re-set inside a block (e.g. an average-price reset), the second level can fall
below ``block_min``'s band and be mis-handled. Use ``return_diagnostics=True``
and inspect blocks that are long or show several flat levels.
"""

from __future__ import annotations

from typing import Tuple, Union

import numpy as np
import pandas as pd

DIAGNOSTIC_COLUMNS = [
    "Trading_Code", "Floor_Block_ID", "Block_Start", "Block_End", "Block_Days",
    "Block_Min_Price", "Estimated_Floor_Price", "Modal_Support",
    "Floor_Associated_Days", "Floor_Associated_Percentage",
]


def estimate_block_floor(
    block_ticks, lower_q: float, min_support: int
) -> Tuple[float, int, float]:
    """Estimate the floor of ONE block, working in whole ticks.

    Returns ``(floor, support, block_min)`` as tick numbers; ``floor`` is NaN
    when the block yields no usable estimate.
    """
    ticks = pd.Series(block_ticks).dropna().to_numpy(dtype=np.int64)
    if ticks.size == 0:
        return np.nan, 0, np.nan

    block_min = int(ticks.min())
    if ticks.size == 1:  # single-day rule: the one close is the floor
        return float(ticks[0]), 1, float(block_min)

    cutoff = np.quantile(ticks, lower_q)
    lower_tail = ticks[ticks <= cutoff]
    if lower_tail.size == 0:
        return np.nan, 0, float(block_min)

    # np.unique sorts ascending and argmax takes the first maximum, so ties
    # resolve to the lowest price.
    levels, counts = np.unique(lower_tail, return_counts=True)
    winner = int(np.argmax(counts))
    floor, support = float(levels[winner]), int(counts[winner])

    if support < min_support:
        return np.nan, support, float(block_min)
    return floor, support, float(block_min)


def detect_floor_locked_prices(
    df: pd.DataFrame,
    price_col: str = "Close",
    floor_flag_col: str = "Floor_Period_Flag",
    group_col: str = "Trading_Code",
    date_col: str = "Date",
    tick_size: float = 0.10,
    lower_q: float = 0.35,
    min_support: int = 3,
    return_diagnostics: bool = False,
) -> Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame]]:
    """Flag closes sitting inside the floor-associated region.

    Adds exactly two columns, ``Floor_Locked_Flag`` (int8) and ``Floor_Price``
    (the estimated floor on locked days, NaN elsewhere). The input is not
    modified and rows are returned in their original order. The input index
    must be unique.

    With ``return_diagnostics=True`` also returns one row per floor block
    (columns in :data:`DIAGNOSTIC_COLUMNS`).
    """
    needed = (price_col, floor_flag_col, group_col, date_col)
    missing = [c for c in needed if c not in df.columns]
    if missing:
        raise KeyError(f"Missing required columns: {missing}")
    if not 0 < lower_q < 1:
        raise ValueError("lower_q must be between 0 and 1")
    if min_support < 1:
        raise ValueError("min_support must be at least 1")

    result = df.copy()
    if not result.index.is_unique:
        raise ValueError("Input index must be unique. Call .reset_index(drop=True) first.")

    result["__row_order"] = np.arange(len(result))
    # mergesort is stable, so rows sharing (ticker, date) keep their order.
    ordered = result.sort_values([group_col, date_col], kind="mergesort")

    ticks = (ordered[price_col] / tick_size).round()

    # Number the contiguous floor blocks within each ticker.
    on_floor = ordered[floor_flag_col].eq(1)
    was_on_floor = (
        on_floor.groupby(ordered[group_col], sort=False).shift(1).fillna(False).astype(bool)
    )
    block_starts = on_floor & ~was_on_floor
    block_id = block_starts.groupby(ordered[group_col], sort=False).cumsum().where(on_floor)

    floor_of_row = pd.Series(np.nan, index=ordered.index)
    min_of_row = pd.Series(np.nan, index=ordered.index)
    summary = []

    if on_floor.any():
        keys = pd.DataFrame({"ticker": ordered[group_col], "block": block_id})[on_floor]
        for (ticker, block), rows in keys.groupby(["ticker", "block"], sort=False).groups.items():
            floor, support, block_min = estimate_block_floor(ticks.loc[rows], lower_q, min_support)

            if not np.isnan(floor):
                floor_of_row.loc[rows] = floor
                min_of_row.loc[rows] = block_min

            if return_diagnostics:
                block_rows = ordered.loc[rows]
                in_band = 0
                if not np.isnan(floor):
                    bt = ticks.loc[rows]
                    in_band = int(((bt >= block_min) & (bt <= floor)).sum())
                n_days = len(block_rows)
                summary.append({
                    group_col: ticker,
                    "Floor_Block_ID": int(block),
                    "Block_Start": block_rows[date_col].min(),
                    "Block_End": block_rows[date_col].max(),
                    "Block_Days": n_days,
                    "Block_Min_Price": round(block_min * tick_size, 2) if not np.isnan(block_min) else np.nan,
                    "Estimated_Floor_Price": round(floor * tick_size, 2) if not np.isnan(floor) else np.nan,
                    "Modal_Support": support,
                    "Floor_Associated_Days": in_band,
                    "Floor_Associated_Percentage": round(in_band / n_days * 100, 1) if n_days else np.nan,
                })

    # block_min <= price <= estimated floor, both ends inclusive, in integer
    # ticks. Rows outside a floor period, in a rejected block, or with a
    # missing close have NaN on one side and evaluate to False.
    is_locked = (
        ticks.notna() & floor_of_row.notna() & ticks.ge(min_of_row) & ticks.le(floor_of_row)
    )
    floor_price = pd.Series(
        np.where(is_locked, floor_of_row * tick_size, np.nan), index=ordered.index
    ).round(2)

    result["Floor_Locked_Flag"] = is_locked.astype("int8").reindex(result.index)
    result["Floor_Price"] = floor_price.reindex(result.index)
    result = result.sort_values("__row_order").drop(columns="__row_order")

    if return_diagnostics:
        cols = [group_col] + DIAGNOSTIC_COLUMNS[1:]
        diag = pd.DataFrame(summary, columns=cols) if summary else pd.DataFrame(columns=cols)
        return result, diag
    return result


def sensitivity_grid(
    df: pd.DataFrame,
    lower_qs=(0.20, 0.25, 0.35, 0.40),
    min_supports=(2, 3, 5),
    **kwargs,
) -> pd.DataFrame:
    """Locked-day counts over a grid of ``(lower_q, min_support)`` settings.

    A grid whose counts never change is not evidence of robustness by itself:
    it can also mean the grid never alters the modal estimate. Inspect
    per-block diagnostics alongside it.
    """
    rows = []
    for q in lower_qs:
        for ms in min_supports:
            t = detect_floor_locked_prices(df, lower_q=q, min_support=ms, **kwargs)
            rows.append({"lower_q": q, "min_support": ms, "locked_days": int(t["Floor_Locked_Flag"].sum())})
    return pd.DataFrame(rows)
