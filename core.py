"""Reusable, independently testable Blue Mart data and business metrics."""
from pathlib import Path
import pandas as pd


def load_and_prepare(folder: Path) -> pd.DataFrame:
    folder=Path(folder)
    sales=pd.read_csv(folder/"sales.csv.gz",parse_dates=["date"],dtype={
        "sale_id":"int32", "store_id":"int16", "sku_id":"int16", "quantity":"int16",
        "unit_price":"float64", "total_value":"float64", "channel":"category", "discount_pct":"float32"
    })
    skus=pd.read_csv(folder/"skus.csv")
    stores=pd.read_csv(folder/"stores.csv")
    required_sales={"sale_id","date","store_id","sku_id","quantity","total_value","channel","discount_pct"}
    if not required_sales.issubset(sales.columns): raise ValueError("Bảng sales thiếu cột bắt buộc.")
    if skus.sku_id.duplicated().any() or stores.store_id.duplicated().any():
        raise ValueError("Khóa sku_id/store_id trong bảng dimension bị trùng.")
    df=sales.merge(skus[["sku_id","sku_name","category","subcategory","brand","cost_price"]],on="sku_id",how="left",validate="many_to_one")
    df=df.merge(stores[["store_id","store_name","city","store_type"]],on="store_id",how="left",validate="many_to_one")
    if df["cost_price"].isna().any() or df["store_name"].isna().any():
        raise ValueError("Có giao dịch không khớp mã SKU/cửa hàng.")
    df["gross_profit"]=df["total_value"]-df["quantity"]*df["cost_price"]
    df["month"]=df["date"].dt.to_period("M").dt.to_timestamp()
    df["year"]=df["date"].dt.year.astype("int16")
    df["month_no"]=df["date"].dt.month.astype("int8")
    # Stable campaign classification, calculated on the whole source dataset.
    day_discount=(df["discount_pct"].gt(0).groupby(df["date"]).mean())
    df["is_campaign_day"]=df["date"].map(day_discount.ge(.5)).astype(bool)
    for name in ("sku_name","category","subcategory","brand","store_name","city","store_type"):
        df[name]=df[name].astype("category")
    return df


def filter_data(df,start,end,cities,store_types,channels,categories,brands):
    mask=df["date"].between(pd.Timestamp(start),pd.Timestamp(end))
    for name,selected in (("city",cities),("store_type",store_types),("channel",channels),
                          ("category",categories),("brand",brands)):
        if selected: mask &= df[name].isin(selected)
    return df.loc[mask]


def kpis(f):
    revenue=float(f.total_value.sum())
    profit=float(f.gross_profit.sum())
    return dict(revenue=revenue,gross_profit=profit,gross_margin=profit/revenue if revenue else 0,
                units=int(f.quantity.sum()),sales_rows=len(f),transactions=int(f.sale_id.nunique()))


def fmt_compact(value,digits=2):
    a=abs(float(value))
    if a>=1e9:return f"{value/1e9:,.{digits}f}B"
    if a>=1e6:return f"{value/1e6:,.{digits}f}M"
    if a>=1e3:return f"{value/1e3:,.{digits}f}K"
    return f"{value:,.0f}"


def fmt_pct(value): return f"{value:.2%}"


def summarize(df):
    stats=kpis(df)
    stats["date_min"]=str(df.date.min().date())
    stats["date_max"]=str(df.date.max().date())
    stats["campaign_days"]=int(df.loc[df.is_campaign_day,"date"].nunique())
    stats["regular_days"]=int(df.loc[~df.is_campaign_day,"date"].nunique())
    stats["skus"]=int(df.sku_id.nunique())
    stats["stores"]=int(df.store_id.nunique())
    return stats
