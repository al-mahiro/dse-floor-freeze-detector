# Data

No market data is distributed with this repository.

## Expected input

One row per security per trading day, with these columns:

| Column | Notes |
|---|---|
| `Trading_Code` | DSE ticker, for example `GP`. Whitespace and case are normalised. |
| `Date` | Trading date. DSE trades Sunday to Thursday. |
| `Open`, `High`, `Low`, `Close` | Prices in Taka. Zeros are treated as missing. |
| `Volume` | Shares traded. Zero is treated as missing. |

CSV and Excel files are supported through `dse_floor.load_ohlcv`.

## Source used in the thesis

The thesis uses a public Dhaka Stock Exchange historical dataset (1999 to 2025) hosted on Harvard Dataverse. The version the authors used ends on **8 April 2025**, so it does not cover the June 2026 floor withdrawal. Check the dataset page for its current license and terms before redistributing any derived files.

## Running on one security from a large panel

```bash
python -m dse_floor DSE_Data.csv -o GP_labelled.csv --tickers GP --diagnostics GP_blocks.csv
```

## Checks before trusting a series

- Run `dse_floor.calendar_anomalies(raw)`. Friday/Saturday rows or rows inside the 26 Mar - 30 May 2020 market closure usually mean dates were misaligned in the export. The authors found such rows in one pilot file, which is why the check exists; repair dates before computing floor-day counts.
- Compare the detector's per-block output with the raw price chart for any block longer than a few months.
