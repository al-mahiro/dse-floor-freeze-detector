import numpy as np
import pandas as pd
import pytest

from conftest import dse_days
from dse_floor import calendar_anomalies, clean_ohlcv


def _raw(n=30, code=" gp "):
    d = dse_days("2022-01-02", n)
    return pd.DataFrame({
        "Trading_Code": code, "Date": d, "Open": 100.0, "High": 101.0, "Low": 99.0,
        "Close": np.linspace(100, 110, n), "Volume": np.arange(1, n + 1) * 1000.0,
    })


def test_basic_cleaning_and_derived_columns():
    out = clean_ohlcv(_raw())
    assert (out["Trading_Code"] == "GP").all()
    assert out["Trading_Day_Index"].tolist() == list(range(1, 31))
    assert np.isnan(out["Observed_Log_Return"].iloc[0])
    assert out["Observed_Log_Return"].iloc[1] == pytest.approx(np.log(out["Close"].iloc[1] / out["Close"].iloc[0]))
    assert np.isnan(out["Volume_Z"].iloc[0])


def test_zero_prices_become_missing_and_dupes_keep_last():
    raw = _raw(5)
    raw.loc[2, "Close"] = 0
    dup = raw.iloc[[4]].copy()
    dup["Close"] = 999.0
    out = clean_ohlcv(pd.concat([raw, dup], ignore_index=True))
    assert len(out) == 5
    assert np.isnan(out.loc[2, "Close"])
    assert out["Close"].iloc[-1] == 999.0


def test_bad_rows_dropped_and_missing_column_error():
    raw = _raw(5)
    raw["Date"] = raw["Date"].astype(object)
    raw.loc[1, "Date"] = "not a date"
    raw.loc[3, "Trading_Code"] = "  "
    assert len(clean_ohlcv(raw)) == 3
    with pytest.raises(ValueError):
        clean_ohlcv(raw.drop(columns="Volume"))


def test_calendar_anomalies_warn_and_optional_drop():
    raw = _raw(5)
    raw.loc[0, "Date"] = pd.Timestamp("2022-01-07")  # Friday
    raw.loc[1, "Date"] = pd.Timestamp("2020-04-12")  # inside closure (a Sunday)
    assert calendar_anomalies(raw) == {"friday_saturday_rows": 1, "closure_rows": 1}
    with pytest.warns(UserWarning):
        kept = clean_ohlcv(raw)
    assert len(kept) == 5
    with pytest.warns(UserWarning):
        dropped = clean_ohlcv(raw, drop_weekend_rows=True, drop_closure_rows=True)
    assert len(dropped) == 3
