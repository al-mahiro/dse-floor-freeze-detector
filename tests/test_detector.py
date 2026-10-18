import numpy as np
import pandas as pd
import pytest

from conftest import dse_days
from dse_floor import detect_floor_locked_prices, estimate_block_floor, run_pipeline, sensitivity_grid


def test_estimate_block_floor_modal_tail_and_tie_rule():
    ticks = [286, 286, 286, 286, 290, 300, 310, 320, 330, 340]
    floor, support, bmin = estimate_block_floor(ticks, 0.35, 3)
    assert (floor, support, bmin) == (286.0, 4, 286.0)
    # tie between 100 and 101 -> lowest price wins
    f, s, _ = estimate_block_floor([100, 100, 101, 101, 150, 160, 170, 180], 0.5, 2)
    assert f == 100.0 and s == 2


def test_support_rule_and_single_day_block():
    f, s, bmin = estimate_block_floor([100, 101, 102, 103, 104, 105], 0.5, 3)
    assert np.isnan(f) and s == 1 and bmin == 100.0  # rejected, no fallback
    assert estimate_block_floor([555], 0.35, 5) == (555.0, 1, 555.0)
    assert np.isnan(estimate_block_floor([np.nan], 0.35, 3)[0])


def _series(prices, flag, code="X", start="2022-08-07"):
    d = dse_days(start, len(prices))
    return pd.DataFrame({"Trading_Code": code, "Date": d, "Close": prices,
                         "Floor_Period_Flag": flag})


def test_flags_frozen_days_only_inside_floor_blocks():
    frozen = [28.5] * 20
    free = list(28.5 + np.arange(1, 11) * 0.5)
    df = _series([40.0, 41.0] + frozen + free + [28.5, 28.5, 28.5],
                 [0, 0] + [1] * 30 + [0, 0, 0])
    out = detect_floor_locked_prices(df)
    assert out["Floor_Locked_Flag"].sum() == 20
    assert set(out.loc[out["Floor_Locked_Flag"] == 1, "Floor_Price"]) == {28.5}
    # outside the floor block, even a price equal to the floor is not flagged
    assert out["Floor_Locked_Flag"].iloc[-3:].sum() == 0
    assert out["Floor_Price"].iloc[:2].isna().all()


def test_diagnostics_and_input_untouched_and_order_restored():
    df = _series([28.5] * 6 + [30.0, 31.0, 32.0], [1] * 9)
    shuffled = df.sample(frac=1, random_state=0)
    before = shuffled.copy()
    out, diag = detect_floor_locked_prices(shuffled, return_diagnostics=True)
    pd.testing.assert_frame_equal(shuffled, before)          # input not modified
    assert out.index.tolist() == shuffled.index.tolist()      # original order
    assert len(diag) == 1
    row = diag.iloc[0]
    assert row["Estimated_Floor_Price"] == 28.5 and row["Floor_Associated_Days"] == 6
    assert row["Block_Days"] == 9


def test_two_blocks_and_two_tickers_are_independent():
    a = _series([10.0] * 8 + [12, 13, 14], [1] * 11, code="A")
    b = _series([50.0] * 8 + [52, 53, 54], [1] * 11, code="B")
    out, diag = detect_floor_locked_prices(pd.concat([a, b], ignore_index=True), return_diagnostics=True)
    assert out.groupby("Trading_Code")["Floor_Locked_Flag"].sum().to_dict() == {"A": 8, "B": 8}
    assert sorted(diag["Estimated_Floor_Price"]) == [10.0, 50.0]


def test_validation_errors():
    df = _series([1.0] * 5, [1] * 5)
    with pytest.raises(KeyError):
        detect_floor_locked_prices(df.drop(columns="Close"))
    with pytest.raises(ValueError):
        detect_floor_locked_prices(df, lower_q=1.5)
    with pytest.raises(ValueError):
        detect_floor_locked_prices(df, min_support=0)
    with pytest.raises(ValueError):
        detect_floor_locked_prices(pd.concat([df, df]))  # duplicate index


def test_sensitivity_grid_shape():
    df = _series([28.5] * 12 + [30.0, 31.0, 32.0], [1] * 15)
    g = sensitivity_grid(df)
    assert len(g) == 12 and (g["locked_days"] >= 0).all()


def test_pipeline_end_to_end():
    d = dse_days("2022-08-07", 60)
    close = np.r_[np.linspace(60, 40, 10), np.full(30, 38.5), np.linspace(39, 50, 20)]
    raw = pd.DataFrame({"Trading_Code": "GP", "Date": d, "Open": close, "High": close,
                        "Low": close, "Close": close, "Volume": 1000.0})
    out = run_pipeline(raw)
    assert out["Floor_Period_Flag"].eq(1).all()  # all inside Jul-Dec 2022 ALL period (sample dates)
    assert out["Floor_Locked_Flag"].sum() >= 30
