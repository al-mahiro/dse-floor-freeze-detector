import pandas as pd
import pytest

from conftest import dse_days
from dse_floor.__main__ import main


def _panel(path):
    d = dse_days("2022-08-07", 40)
    frames = []
    for code, floor in (("AAA", 28.5), ("BBB", 51.0)):
        close = [floor] * 25 + [floor + i for i in range(1, 16)]
        frames.append(pd.DataFrame({"Trading_Code": code, "Date": d, "Open": close, "High": close,
                                    "Low": close, "Close": close, "Volume": 1000}))
    pd.concat(frames).to_csv(path, index=False)


def test_cli_filters_tickers_and_writes_outputs(tmp_path, capsys):
    src, out, diag = tmp_path / "in.csv", tmp_path / "out.csv", tmp_path / "diag.csv"
    _panel(src)
    main([str(src), "-o", str(out), "--diagnostics", str(diag), "--tickers", "aaa"])
    res = pd.read_csv(out)
    assert set(res["Trading_Code"]) == {"AAA"}
    assert res["Floor_Locked_Flag"].sum() == 25
    assert len(pd.read_csv(diag)) == 1
    assert "Floor-locked days: 25" in capsys.readouterr().out


def test_cli_unknown_ticker_exits(tmp_path):
    src = tmp_path / "in.csv"
    _panel(src)
    with pytest.raises(SystemExit):
        main([str(src), "-o", str(tmp_path / "o.csv"), "--tickers", "ZZZ"])
