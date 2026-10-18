"""Command line: ``python -m dse_floor input.csv -o out.csv --diagnostics diag.csv``"""

from __future__ import annotations

import argparse

from .cleaning import load_ohlcv
from .detector import sensitivity_grid
from .pipeline import run_pipeline


def main(argv=None) -> None:
    p = argparse.ArgumentParser(prog="dse_floor", description=__doc__)
    p.add_argument("input", help="CSV/XLSX with Trading_Code, Date, Open, High, Low, Close, Volume")
    p.add_argument("-o", "--output", required=True, help="labelled output (.csv or .xlsx)")
    p.add_argument("--diagnostics", help="write per-block diagnostics to this CSV")
    p.add_argument("--lower-q", type=float, default=0.35)
    p.add_argument("--min-support", type=int, default=3)
    p.add_argument("--tick-size", type=float, default=0.10)
    p.add_argument("--drop-weekend-rows", action="store_true")
    p.add_argument("--drop-closure-rows", action="store_true")
    p.add_argument("--sensitivity", action="store_true", help="print the (lower_q, min_support) grid")
    a = p.parse_args(argv)

    raw = load_ohlcv(a.input)
    out, diag = run_pipeline(
        raw, lower_q=a.lower_q, min_support=a.min_support, tick_size=a.tick_size,
        return_diagnostics=True, drop_weekend_rows=a.drop_weekend_rows,
        drop_closure_rows=a.drop_closure_rows,
    )
    if a.output.lower().endswith(".xlsx"):
        out.to_excel(a.output, index=False)
    else:
        out.to_csv(a.output, index=False)
    if a.diagnostics:
        diag.to_csv(a.diagnostics, index=False)

    print(f"Rows: {len(out)}")
    print(f"Floor-period days: {int(out['Floor_Period_Flag'].sum())}")
    print(f"Floor-locked days: {int(out['Floor_Locked_Flag'].sum())}")
    if a.sensitivity:
        print(sensitivity_grid(out.drop(columns=["Floor_Locked_Flag", "Floor_Price"]),
                               tick_size=a.tick_size).to_string(index=False))


if __name__ == "__main__":
    main()
