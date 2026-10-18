"""End-to-end Steps 1-3: clean -> classify -> detect."""

from __future__ import annotations

from typing import Tuple, Union

import pandas as pd

from .classification import add_floor_period_flag
from .cleaning import clean_ohlcv
from .detector import detect_floor_locked_prices


def run_pipeline(
    raw: pd.DataFrame,
    *,
    lower_q: float = 0.35,
    min_support: int = 3,
    tick_size: float = 0.10,
    return_diagnostics: bool = False,
    **clean_kwargs,
) -> Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame]]:
    """Run cleaning, floor-period classification and floor-lock detection.

    The detector works per security, so a multi-security panel can be passed
    directly. Extra keyword arguments go to :func:`clean_ohlcv`.
    """
    cleaned = clean_ohlcv(raw, **clean_kwargs)
    classified = add_floor_period_flag(cleaned)
    return detect_floor_locked_prices(
        classified,
        lower_q=lower_q,
        min_support=min_support,
        tick_size=tick_size,
        return_diagnostics=return_diagnostics,
    )
