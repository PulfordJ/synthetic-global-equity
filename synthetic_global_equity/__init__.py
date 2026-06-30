"""
synthetic_global_equity
=======================
Helper utilities for loading and splicing equity index data.
"""

from __future__ import annotations

import pandas as pd
from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data"


def load_index(filename: str, col_name: str | None = None) -> pd.Series:
    """
    Load a monthly equity index CSV from the data directory.

    Parameters
    ----------
    filename : str
        CSV filename inside ``data/``.  Must have columns ``Date`` (MM/YYYY)
        and a single value column.
    col_name : str, optional
        Override the value-column name in the returned Series.  Defaults to
        the column name found in the file.

    Returns
    -------
    pd.Series
        Monthly index levels indexed by month-end ``pd.Timestamp``, sorted
        ascending.
    """
    path = DATA_DIR / filename
    df = pd.read_csv(path)
    date_col, val_col = df.columns[0], df.columns[1]

    # Parse MM/YYYY → last day of that month
    dates = pd.to_datetime(df[date_col], format="%m/%Y") + pd.offsets.MonthEnd(0)
    series = pd.Series(df[val_col].values, index=dates, name=col_name or val_col)
    return series.sort_index()


def chain_splice(
    primary: pd.Series,
    proxy: pd.Series,
    splice_date: str,
) -> pd.Series:
    """
    Back-extend *primary* with *proxy* by scaling the proxy so that both series
    share the same value at *splice_date*.

    The splice date must be the **first date of the primary series** (i.e. the
    earliest date where the primary is available).  The returned series covers
    the entire date range of the proxy (which must start earlier) plus the
    primary from *splice_date* onwards.

    Parameters
    ----------
    primary : pd.Series
        The higher-quality / newer series (e.g. FTSE All-World).
    proxy : pd.Series
        The lower-quality / older series used to extend back in time
        (e.g. MSCI ACWI).
    splice_date : str
        ISO date string for the month that both series share (e.g.
        ``"2003-09-30"``).  Must be present in both series.

    Returns
    -------
    pd.Series
        Stitched series: proxy (scaled) before *splice_date*, primary from
        *splice_date* onwards.  Index is month-end timestamps sorted ascending.
    """
    splice_ts = pd.Timestamp(splice_date) + pd.offsets.MonthEnd(0)

    primary_val_at_splice = primary[splice_ts]
    proxy_val_at_splice = proxy[splice_ts]
    scale = primary_val_at_splice / proxy_val_at_splice

    proxy_scaled = proxy[proxy.index < splice_ts] * scale
    stitched = pd.concat([proxy_scaled, primary]).sort_index()
    stitched.name = primary.name
    return stitched
