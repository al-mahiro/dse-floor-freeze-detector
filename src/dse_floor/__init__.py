"""dse_floor: data cleaning and freeze (floor-lock) detection for DSE prices."""

from .classification import add_floor_period_flag, classify_floor_period
from .cleaning import calendar_anomalies, clean_ohlcv, load_ohlcv
from .detector import detect_floor_locked_prices, estimate_block_floor, sensitivity_grid
from .pipeline import run_pipeline
from .timeline import FLOOR_PERIODS

__version__ = "0.1.0"

__all__ = [
    "FLOOR_PERIODS", "add_floor_period_flag", "calendar_anomalies",
    "classify_floor_period", "clean_ohlcv", "detect_floor_locked_prices",
    "estimate_block_floor", "load_ohlcv", "run_pipeline", "sensitivity_grid",
]
