# Synthetic FTSE All-World Index (Dec 1969 – present)

A monthly total-return equity index back-extended to December 1969 by chain-linking three publicly available index series.

## Background

The [FTSE All-World Index](https://curvo.eu/backtest/en/market-index/ftse-all-world?currency=gbp) — a broad global equity benchmark covering developed and emerging markets — only has data from September 2003. This project extends it back to December 1969 using two earlier proxies, producing a continuous 55+ year series useful for long-run return analysis and portfolio backtesting.

## Methodology

The synthetic index is built by chain-splicing three series in order of decreasing coverage quality:

| Era | Index | Period | Notes |
|-----|-------|--------|-------|
| Recent | FTSE All-World | Sep 2003 – present | Real data; target index |
| Middle | MSCI ACWI | Dec 1987 – Aug 2003 | All-country + EM proxy |
| Early | MSCI World | Dec 1969 – Nov 1987 | Developed-markets-only proxy |

**Chain-splicing** scales each proxy series to match the primary series' level at the splice date, preserving the proxy's internal monthly returns exactly. The Pearson correlation of monthly log-returns confirms MSCI ACWI (r = 0.9996) is a better proxy for FTSE All-World than MSCI World alone (r = 0.9942) over their overlapping period.

The final series is rebased to 10,000 at December 1969. Full-period CAGR (Dec 1969 – May 2026): **10.61%**.

See [`synthetic_ftse_all_world.ipynb`](synthetic_ftse_all_world.ipynb) for the complete analysis.

## Data Sources

Input data sourced from [Curvo](https://curvo.eu), denominated in GBP:

- **MSCI World** (from Dec 1969): https://curvo.eu/backtest/en/market-index/msci-world?currency=gbp
- **MSCI ACWI** (from Dec 1987): https://curvo.eu/backtest/en/market-index/msci-acwi?currency=gbp
- **FTSE All-World** (from Sep 2003): https://curvo.eu/backtest/en/market-index/ftse-all-world?currency=gbp

Raw CSVs are included in [`data/`](data/).

## Outputs

| File | Description |
|------|-------------|
| `data/synthetic_ftse_all_world.csv` | Monthly index levels (MM/YYYY, rebased to 10,000 at Dec 1969) |
| `data/synthetic_ftse_all_world_annual.csv` | December year-end levels |
| `data/synthetic_ftse_all_world_annual_returns.csv` | Calendar-year percentage returns (1970–2025) — compatible with Portfolio Charts asset toolkit |

## Usage

**With Nix (recommended):**

```bash
nix develop
jupyter notebook
```

**Without Nix:**

```bash
pip install -e .
jupyter notebook
```

Dependencies are declared in [`pyproject.toml`](pyproject.toml): Python ≥ 3.11, numpy, pandas, matplotlib, scipy, seaborn.

## License

MIT — see [LICENSE](LICENSE).
