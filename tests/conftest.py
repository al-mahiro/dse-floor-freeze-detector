import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pandas as pd


def dse_days(start, periods):
    """Sunday-Thursday trading calendar."""
    return pd.bdate_range(start, periods=periods, freq="C", weekmask="Sun Mon Tue Wed Thu")
