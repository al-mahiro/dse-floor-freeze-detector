import pandas as pd

from dse_floor import FLOOR_PERIODS, add_floor_period_flag, classify_floor_period
from dse_floor import timeline as T


def test_list_sizes_match_orders():
    assert len(T.COMPANIES_66) == 66
    assert len(T.COMPANIES_30) == 30
    assert len(T.COMPANIES_96) == 96  # 66 and 30 are disjoint
    assert len(T.COMPANIES_169) == 169
    assert len(T.COMPANIES_168_DEC2022) == 168
    assert len(T.COMPANIES_35) == 35
    assert len(T.COMPANIES_12) == 12
    assert len(T.COMPANIES_2) == 2


def test_periods_are_ordered_and_non_overlapping():
    spans = [(pd.Timestamp(s), pd.Timestamp(e)) for s, e, *_ in FLOOR_PERIODS]
    for (s, e), (s2, _) in zip(spans, spans[1:]):
        assert s <= e < s2


def test_key_dates():
    assert classify_floor_period("2020-06-01", "GP") == (1, "ALL_SECURITIES")
    assert classify_floor_period("2021-12-01", "GP") == (0, "NO_FLOOR")
    assert classify_floor_period("2023-06-01", "GP") == (1, "ALL_SECURITIES")
    assert classify_floor_period("2024-02-01", "GP") == (1, "SECURITY_SPECIFIC")
    assert classify_floor_period("2024-03-03", "GP") == (0, "NO_FLOOR")  # GP freed 3 Mar 2024
    assert classify_floor_period("2025-01-01", "BEXIMCO") == (1, "SECURITY_SPECIFIC")
    assert classify_floor_period("2025-01-01", "GP") == (0, "NO_FLOOR")
    assert classify_floor_period("2026-06-09", "BEXIMCO") == (0, "NO_FLOOR")
    assert classify_floor_period(pd.NaT, "GP") == (0, "INVALID_DATE")


def test_exempted_period():
    assert classify_floor_period("2021-05-01", "NURANI") == (0, "EXEMPTED")
    assert classify_floor_period("2021-05-01", "GP") == (1, "SECURITY_SPECIFIC")


def test_vectorised_matches_scalar():
    dates = pd.date_range("2020-01-01", "2026-12-31", freq="9D")
    codes = ["GP", "NURANI", "BEXIMCO", "RENWICKJA", "ABC"]
    df = pd.DataFrame(
        [(c, d) for c in codes for d in dates], columns=["Trading_Code", "Date"]
    )
    df.loc[3, "Date"] = pd.NaT
    out = add_floor_period_flag(df)
    for _, r in out.iterrows():
        assert (r["Floor_Period_Flag"], r["Floor_Period_Regime"]) == classify_floor_period(
            r["Date"], r["Trading_Code"]
        )
