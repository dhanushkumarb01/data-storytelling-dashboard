"""
data_utils.py
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
Utility functions for the BizLens Data Storytelling Dashboard.
Covers data loading, filtering, KPI computation, cohort analysis,
and RFM segmentation.
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple, List


def load_orders(csv_path: str) -> pd.DataFrame:
    """
    Load the orders CSV, parse dates, and derive helper columns.

    Parameters
    ----------
    csv_path : str
        Path to the orders CSV file.

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame with `order_month` and `profit` columns added.
    """
    df = pd.read_csv(csv_path, parse_dates=["order_date"])
    df["order_month"] = df["order_date"].values.astype("datetime64[M]")
    df["profit"]      = df["revenue"] - df["cost"]
    return df


def filter_df(
    df: pd.DataFrame,
    date_range: Tuple,
    countries:  Optional[List[str]] = None,
    channels:   Optional[List[str]] = None,
    categories: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Apply date + dimension filters and return a filtered copy.

    Parameters
    ----------
    df         : Source DataFrame.
    date_range : Tuple of (start_date, end_date).
    countries  : List of country names to include (None = all).
    channels   : List of channel names to include (None = all).
    categories : List of category names to include (None = all).

    Returns
    -------
    pd.DataFrame
        Filtered DataFrame (copy).
    """
    mask = (
        (df["order_date"].dt.date >= date_range[0]) &
        (df["order_date"].dt.date <= date_range[1])
    )
    if countries:  mask &= df["country"].isin(countries)
    if channels:   mask &= df["channel"].isin(channels)
    if categories: mask &= df["category"].isin(categories)
    return df.loc[mask].copy()


def compute_kpis(df: pd.DataFrame) -> dict:
    """
    Compute high-level business KPIs from a (filtered) orders DataFrame.

    Returns
    -------
    dict with keys: Revenue, Profit, Orders, Customers, AOV, Margin%
    """
    revenue = df["revenue"].sum()
    profit  = df["profit"].sum()
    return {
        "Revenue":   revenue,
        "Profit":    profit,
        "Orders":    df["order_id"].nunique(),
        "Customers": df["customer_id"].nunique(),
        "AOV":       df.groupby("order_id")["revenue"].sum().mean() if not df.empty else 0,
        "Margin%":   (profit / revenue) if revenue > 0 else 0,
    }


def cohort_analysis(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Build monthly cohort tables (absolute counts + retention rates).

    Cohort month = month of a customer's first order.
    Cohort index = months since that first order (1-based).

    Returns
    -------
    cohort_pivot : pd.DataFrame  â€” absolute active-customer counts
    cohort_ret   : pd.DataFrame  â€” retention rates (cohort_pivot Ã· cohort size)
    """
    first = (
        df.groupby("customer_id")["order_month"]
          .min()
          .rename("cohort_month")
    )
    tmp = df.merge(first, on="customer_id", how="left")
    tmp["cohort_index"] = (
        (tmp["order_month"].dt.year  - tmp["cohort_month"].dt.year)  * 12 +
        (tmp["order_month"].dt.month - tmp["cohort_month"].dt.month) + 1
    )
    cohort = (
        tmp.groupby(["cohort_month", "cohort_index"])["customer_id"]
           .nunique()
           .reset_index()
    )
    cohort_pivot = (
        cohort.pivot(index="cohort_month", columns="cohort_index", values="customer_id")
              .fillna(0)
              .astype(int)
    )
    cohort_ret = cohort_pivot.divide(cohort_pivot[1], axis=0).round(3)
    return cohort_pivot, cohort_ret


def rfm_segmentation(
    df: pd.DataFrame,
    as_of: Optional[pd.Timestamp] = None,
) -> pd.DataFrame:
    """
    Compute RFM scores and assign a business segment to each customer.

    Segments:
      Champions  â€” RFM score 8â€“9
      Active     â€” RFM score 6â€“7
      New/Cold   â€” RFM score 3â€“5

    Parameters
    ----------
    df    : Orders DataFrame (filtered or full).
    as_of : Reference date for recency calculation (default = max order date + 1 day).

    Returns
    -------
    pd.DataFrame with columns: customer_id, R, F, M, RFM_Score, Segment
    """
    if as_of is None:
        as_of = df["order_date"].max().normalize() + pd.Timedelta(days=1)

    recency   = df.groupby("customer_id")["order_date"].max().apply(lambda d: (as_of - d).days)
    frequency = df.groupby("customer_id")["order_id"].nunique()
    monetary  = df.groupby("customer_id")["revenue"].sum()

    r = pd.qcut(recency,                       3, labels=[3, 2, 1])
    f = pd.qcut(frequency.rank(method="first"), 3, labels=[1, 2, 3])
    m = pd.qcut(monetary.rank(method="first"),  3, labels=[1, 2, 3])

    rfm = pd.DataFrame({"R": r.astype(int), "F": f.astype(int), "M": m.astype(int)})
    rfm["RFM_Score"] = rfm.sum(axis=1)
    rfm["Segment"]   = pd.cut(
        rfm["RFM_Score"],
        bins=[2, 5, 7, 9],
        labels=["New/Cold", "Active", "Champions"],
        include_lowest=True,
    )
    rfm.index.name = "customer_id"
    return rfm.reset_index()