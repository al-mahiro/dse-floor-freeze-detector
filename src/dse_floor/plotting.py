"""Plot a security's closing price with floor windows and locked days marked."""

from __future__ import annotations

import pandas as pd


def plot_floor_windows(df: pd.DataFrame, ticker: str, ax=None, title: str = None):
    """Closing price with floor-period blocks shaded and locked days marked.

    ``df`` must come from :func:`dse_floor.pipeline.run_pipeline` (or carry
    ``Floor_Period_Flag`` and ``Floor_Locked_Flag``). Requires matplotlib.
    """
    import matplotlib.pyplot as plt

    d = df[df["Trading_Code"] == ticker].sort_values("Date")
    if d.empty:
        raise ValueError(f"No rows for {ticker!r}")
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 4))

    ax.plot(d["Date"], d["Close"], lw=1.1, color="#1f3b5c", label="Close")

    # Shade each contiguous floor-period run.
    on = d["Floor_Period_Flag"].eq(1).to_numpy()
    dates = d["Date"].to_numpy()
    i, n = 0, len(d)
    first = True
    while i < n:
        if on[i]:
            j = i
            while j + 1 < n and on[j + 1]:
                j += 1
            ax.axvspan(dates[i], dates[j], color="#d9822b", alpha=0.15,
                       label="Floor period" if first else None)
            first = False
            i = j + 1
        else:
            i += 1

    locked = d[d["Floor_Locked_Flag"].eq(1)]
    if not locked.empty:
        ax.scatter(locked["Date"], locked["Close"], s=6, color="#b3261e", zorder=3,
                   label="Floor-locked close")

    ax.set_title(title or f"{ticker}: closing price and BSEC floor windows")
    ax.set_ylabel("Close (Tk)")
    ax.legend(loc="best", frameon=False)
    return ax
