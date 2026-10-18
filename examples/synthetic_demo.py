"""Self-contained demo on SYNTHETIC data (no real DSE prices are shipped).

Simulates a stock whose price falls into a regulatory floor during the
2022-23 BSEC window, sticks there, then trades freely after the floor lifts.

    python examples/synthetic_demo.py            # prints a summary
    python examples/synthetic_demo.py --plot     # also saves docs/example_floor_windows.png
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dse_floor import run_pipeline, sensitivity_grid  # noqa: E402


def make_demo(seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    days = pd.bdate_range("2021-09-01", "2024-06-30", freq="C", weekmask="Sun Mon Tue Wed Thu")
    ret = rng.normal(0, 0.012, len(days))
    # Free trading before the floor; once the floor bites (31 Jul 2022 -
    # 18 Jan 2024, the ALL-securities window) the price cannot close below
    # Tk 80.0, so a downward drift pins it at the floor.
    floor = 80.0
    in_floor = (days >= "2022-07-31") & (days <= "2024-01-18")
    drift = np.where(in_floor, -0.004, 0.0)
    price = np.empty(len(days))
    price[0] = 130.0
    for t in range(1, len(days)):
        price[t] = price[t - 1] * np.exp(ret[t] + drift[t])
        if in_floor[t]:
            price[t] = max(price[t], floor)   # the regulator will not let it close lower
    close = np.round(price / 0.1) * 0.1
    return pd.DataFrame({
        "Trading_Code": "DEMO", "Date": days, "Open": close, "High": close * 1.01,
        "Low": close * 0.99, "Close": close, "Volume": rng.integers(50_000, 400_000, len(days)),
    })


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plot", action="store_true")
    args = ap.parse_args()

    out, diag = run_pipeline(make_demo(), return_diagnostics=True)
    print(f"Rows               : {len(out)}")
    print(f"Floor-period days  : {int(out['Floor_Period_Flag'].sum())}")
    print(f"Floor-locked days  : {int(out['Floor_Locked_Flag'].sum())}")
    print("\nPer-block diagnostics:")
    print(diag.to_string(index=False))
    print("\nSensitivity grid:")
    print(sensitivity_grid(out.drop(columns=["Floor_Locked_Flag", "Floor_Price"])).to_string(index=False))

    if args.plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from dse_floor.plotting import plot_floor_windows

        ax = plot_floor_windows(out, "DEMO", title="Synthetic stock: closing price, floor windows, locked days")
        target = Path(__file__).resolve().parents[1] / "docs" / "example_floor_windows.png"
        ax.figure.tight_layout()
        ax.figure.savefig(target, dpi=150)
        print(f"\nSaved {target}")


if __name__ == "__main__":
    main()
