"""Blue Mart Retail | Interactive public portfolio.

Data sources: user-provided bm_sales_cleaned, bm_skus_cleaned, bm_stores_cleaned.
KPI definitions are based on the user's Power BI model.
"""
from pathlib import Path
import calendar

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from core import load_and_prepare, filter_data, kpis, fmt_compact, fmt_pct, summarize

st.set_page_config(
    page_title="Blue Mart | Retail Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY = "#18263F"
TEAL = "#0A7980"
ORANGE = "#F4A952"
PURPLE = "#8172C9"
RED = "#D85E68"
COLORS = [TEAL, NAVY, ORANGE, PURPLE, "#49A69E", "#6492C5", RED]
PLOT_FONT = dict(family="Arial, sans-serif", color="#2B3850")

st.markdown("""
<style>
.stApp {background-color:#F6F8FB; color:#25354B;}
.block-container {padding-top:1.4rem; padding-bottom:3rem; max-width:1500px;}
h1,h2,h3 {color:#18263F; letter-spacing:-0.015em;}
h1 {font-size:2.2rem !important; margin-bottom:0.25rem !important;}
h3 {font-size:1.13rem !important;}
[data-testid="stSidebar"] {background-color:#FFFFFF; border-right:1px solid #E7EAF0;}
[data-testid="stMetric"] {background:#FFFFFF; padding:18px 18px 16px; border:1px solid #E9EEF5; border-radius:14px; box-shadow:0 5px 20px rgba(30,54,87,.025);}
[data-testid="stMetricLabel"] {font-weight:600;}
[data-testid="stMetricValue"] {font-weight:730; color:#18263F;}
[data-testid="stPlotlyChart"] {background:#FFFFFF; border:1px solid #E9EEF5; border-radius:14px; padding:10px 10px 4px;}
section[data-testid="stSidebar"] h2 {color:#18263F;}
.small-note {font-size:.88rem;color:#637287;margin:0 0 12px 0;}
.info-banner {background:#E8F4F3;border:1px solid #CBE6E3;color:#276A6C;border-radius:12px;padding:11px 14px;margin:8px 0 16px 0;font-size:.92rem;}
[data-testid="stDataFrame"] {border:1px solid #E9EEF5;border-radius:12px;}
</style>
""", unsafe_allow_html=True)


def style_chart(fig, percent_y=False, height=370, legend=True):
    fig.update_layout(
        font=PLOT_FONT, height=height, paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF", margin=dict(l=18, r=20, t=42, b=35),
        colorway=COLORS, hovermode="closest",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        showlegend=legend,
    )
    fig.update_xaxes(showgrid=False, linecolor="#DCE4ED", tickfont=dict(color="#64748B"))
    fig.update_yaxes(gridcolor="#EFF3F7", zeroline=False, tickfont=dict(color="#64748B"))
    if percent_y: fig.update_yaxes(tickformat=".0%")
    return fig


def chart(fig, key=None):
    st.plotly_chart(fig, use_container_width=True, key=key)


def title(name, desc):
    st.title(name)
    st.markdown(f'<p class="small-note">{desc}</p>', unsafe_allow_html=True)


def metric_strip(stats):
    cols = st.columns(5)
    specs = [
        ("Doanh thu", fmt_compact(stats["revenue"])),
        ("Lợi nhuận gộp", fmt_compact(stats["gross_profit"])),
        ("Biên LN gộp", fmt_pct(stats["gross_margin"])),
        ("Sản phẩm bán ra", fmt_compact(stats["units"], digits=2)),
        ("Dòng bán", f'{stats["sales_rows"]:,}'),
    ]
    for c,(label,value) in zip(cols,specs):
        c.metric(label, value)


@st.cache_data(show_spinner="Đang nạp dữ liệu Blue Mart…")
def get_data():
    root=Path(__file__).parent / "data"
    return load_and_prepare(root)

try:
    df=get_data()
except (FileNotFoundError, ValueError) as exc:
    st.error(f"Không tải được dữ liệu: {exc}")
    st.info("Hãy giữ nguyên thư mục data/ khi đưa project lên GitHub.")
    st.stop()

st.sidebar.markdown("## 🛍️ Blue Mart")
st.sidebar.caption("Retail Intelligence • Portfolio")
page=st.sidebar.radio(
    "Trang phân tích",
    ["01 · Tổng quan & mùa vụ", "02 · Kênh & điểm bán", "03 · Chiến dịch & chiết khấu", "04 · Danh mục sản phẩm"],
)
st.sidebar.divider()
st.sidebar.markdown("#### Bộ lọc chung")
min_date=df["date"].min().date(); max_date=df["date"].max().date()
dates=st.sidebar.date_input("Khoảng thời gian",value=(min_date,max_date),min_value=min_date,max_value=max_date,format="DD/MM/YYYY")
if not isinstance(dates,(list,tuple)) or len(dates)!=2:
    st.warning("Hãy chọn cả ngày bắt đầu và ngày kết thúc.")
    st.stop()
start,end=dates
cities=st.sidebar.multiselect("Thành phố", sorted(df["city"].dropna().unique()))
store_types=st.sidebar.multiselect("Loại cửa hàng", sorted(df["store_type"].dropna().unique()))
channels=st.sidebar.multiselect("Kênh bán", sorted(df["channel"].dropna().unique()))
categories=st.sidebar.multiselect("Ngành hàng", sorted(df["category"].dropna().unique()))
brands=st.sidebar.multiselect("Thương hiệu", sorted(df["brand"].dropna().unique()))
st.sidebar.caption("Để trống một bộ lọc = chọn tất cả.")
st.sidebar.divider()
st.sidebar.caption("Nguồn: Blue Mart cleaned data | 01/2021–10/2025")
st.sidebar.caption("Web độc lập, không sử dụng Power BI Service.")

f=filter_data(df,start,end,cities,store_types,channels,categories,brands)
if f.empty:
    st.warning("Không có giao dịch nào thỏa mãn các bộ lọc đang chọn.")
    st.stop()

stats=kpis(f)

if page.startswith("01"):
    title("Tổng quan kinh doanh & mùa vụ", "Theo dõi doanh thu, lợi nhuận và biến động bán hàng trên toàn bộ hệ thống.")
    metric_strip(stats)
    st.write("")
    monthly=(f.groupby("month",observed=True,as_index=False)
             .agg(revenue=("total_value","sum"), gross_profit=("gross_profit","sum"), units=("quantity","sum")))
    monthly["gross_margin"]=monthly["gross_profit"]/monthly["revenue"].where(monthly["revenue"]!=0)
    c1,c2=st.columns([1.55,1.0])
    with c1:
        st.subheader("Doanh thu theo tháng")
        fig=px.area(monthly,x="month",y="revenue",labels={"month":"Tháng","revenue":"Doanh thu"})
        fig.update_traces(line_color=TEAL,fillcolor="rgba(10,121,128,0.12)",hovertemplate="%{x|%m/%Y}<br>Doanh thu: %{y:,.0f}<extra></extra>")
        chart(style_chart(fig,legend=False))
    with c2:
        st.subheader("Biên lợi nhuận gộp theo tháng")
        fig=px.line(monthly,x="month",y="gross_margin",markers=True,labels={"month":"Tháng","gross_margin":"GM%"})
        fig.update_traces(line_color=PURPLE,marker_size=5,hovertemplate="%{x|%m/%Y}<br>GM: %{y:.2%}<extra></extra>")
        chart(style_chart(fig,percent_y=True,legend=False))
    c3,c4=st.columns(2)
    with c3:
        st.subheader("Mùa vụ: Doanh thu TB theo tháng trong năm")
        by_month=monthly.assign(month_num=monthly.month.dt.month).groupby("month_num",as_index=False)["revenue"].mean()
        by_month["thang"]=[f"T{m:02d}" for m in by_month.month_num]
        fig=px.bar(by_month,x="thang",y="revenue",text_auto=".2s",color_discrete_sequence=[TEAL])
        fig.update_layout(xaxis_title="Tháng",yaxis_title="Doanh thu trung bình")
        chart(style_chart(fig,legend=False))
    with c4:
        st.subheader("Doanh thu theo năm")
        annual=f.groupby("year",as_index=False).agg(revenue=("total_value","sum"),gp=("gross_profit","sum"))
        annual["year"]=annual["year"].astype(str)
        fig=go.Figure()
        fig.add_bar(x=annual.year,y=annual.revenue,name="Doanh thu",marker_color=TEAL)
        fig.add_bar(x=annual.year,y=annual.gp,name="Lợi nhuận gộp",marker_color=ORANGE)
        fig.update_layout(barmode="group",xaxis_title="Năm",yaxis_title="Giá trị")
        chart(style_chart(fig))
        st.caption("Lưu ý: năm 2025 chỉ có dữ liệu đến 31/10, không phải cả năm.")

elif page.startswith("02"):
    title("Kênh bán & điểm bán", "So sánh các kênh bán và hiệu quả hoạt động của hệ thống cửa hàng vật lý.")
    metric_strip(stats)
    sales_channel=f.groupby("channel",observed=True,as_index=False).agg(revenue=("total_value","sum"),gp=("gross_profit","sum"),units=("quantity","sum"))
    sales_channel["margin"]=sales_channel.gp/sales_channel.revenue
    sales_channel=sales_channel.sort_values("revenue",ascending=False)
    online_share=f.loc[f.channel.ne("Store"),"total_value"].sum()/stats["revenue"] if stats["revenue"] else 0
    st.markdown(f'<div class="info-banner"><b>Tỷ trọng doanh thu Online:</b> {fmt_pct(online_share)} &nbsp; • &nbsp; Online = Website + MobileApp + Amazon.ae + Noon</div>',unsafe_allow_html=True)
    c1,c2=st.columns([1.4,1])
    with c1:
        st.subheader("Doanh thu theo kênh")
        fig=px.bar(sales_channel,x="revenue",y="channel",orientation="h",text_auto=".3s",color="channel",color_discrete_sequence=COLORS)
        fig.update_layout(yaxis=dict(categoryorder="total ascending"),xaxis_title="Doanh thu",yaxis_title="")
        chart(style_chart(fig,legend=False))
    with c2:
        st.subheader("Cơ cấu kênh")
        fig=px.pie(sales_channel,values="revenue",names="channel",hole=.63,color_discrete_sequence=COLORS)
        fig.update_traces(textposition="outside",textinfo="percent+label")
        chart(style_chart(fig,legend=False))
    st.subheader("Hiệu quả cửa hàng vật lý")
    phys=f.loc[f.channel.eq("Store")]
    if phys.empty:
        st.info("Dữ liệu hiện lọc không chứa kênh Store. Hãy bỏ lọc kênh bán để xem điểm bán vật lý.")
    else:
        stores=phys.groupby(["store_id","store_name","city"],observed=True,as_index=False).agg(revenue=("total_value","sum"),gp=("gross_profit","sum"))
        stores["margin"]=stores.gp/stores.revenue
        avg_st=stores.revenue.mean()
        under=(stores.revenue < avg_st).sum()
        c3,c4,c5=st.columns(3)
        c3.metric("Cửa hàng có phát sinh bán",len(stores))
        c4.metric("Doanh thu TB / cửa hàng",fmt_compact(avg_st))
        c5.metric("Cửa hàng dưới mức TB",f"{under}/{len(stores)}")
        c6,c7=st.columns([1.4,1])
        with c6:
            st.subheader("Top 12 cửa hàng theo doanh thu")
            top=stores.nlargest(12,"revenue").sort_values("revenue")
            fig=px.bar(top,x="revenue",y="store_name",orientation="h",color_discrete_sequence=[TEAL])
            fig.add_vline(x=avg_st,line_dash="dash",line_color=ORANGE,annotation_text="TB cửa hàng")
            fig.update_layout(yaxis_title="",xaxis_title="Doanh thu")
            chart(style_chart(fig,legend=False,height=440))
        with c7:
            st.subheader("Doanh thu theo thành phố")
            city=phys.groupby("city",observed=True,as_index=False).total_value.sum().sort_values("total_value",ascending=False)
            fig=px.bar(city,x="city",y="total_value",color_discrete_sequence=[PURPLE])
            fig.update_layout(xaxis_title="Thành phố",yaxis_title="Doanh thu")
            chart(style_chart(fig,legend=False,height=440))

elif page.startswith("03"):
    title("Chiến dịch & chiết khấu", "Đánh giá tác động của những ngày tỷ lệ giao dịch giảm giá cao lên doanh thu và biên lợi nhuận.")
    metric_strip(stats)
    st.markdown('<div class="info-banner"><b>Định nghĩa:</b> Ngày chiến dịch = ngày có ít nhất 50% dòng bán được giảm giá (discount_pct &gt; 0), tính trên toàn bộ dữ liệu gốc. Nhãn ngày được giữ ổn định khi lọc.</div>',unsafe_allow_html=True)
    days=f.groupby(["date","is_campaign_day"],observed=True,as_index=False).agg(revenue=("total_value","sum"),gp=("gross_profit","sum"),rows=("sale_id","size"),avg_discount=("discount_pct","mean"))
    campaign_summary=days.groupby("is_campaign_day",observed=True).agg(days=("date","nunique"),revenue=("revenue","sum"),gp=("gp","sum"),rows=("rows","sum")).reset_index()
    campaign_summary["revenue_per_day"]=campaign_summary.revenue/campaign_summary.days
    campaign_summary["margin"]=campaign_summary.gp/campaign_summary.revenue
    campaign_summary["group"]=campaign_summary.is_campaign_day.map({True:"Ngày chiến dịch",False:"Ngày thường"})
    comp=campaign_summary.set_index("is_campaign_day")
    if True in comp.index and False in comp.index:
        uplift=comp.loc[True,"revenue_per_day"]/comp.loc[False,"revenue_per_day"]-1
        delta_margin=(comp.loc[True,"margin"]-comp.loc[False,"margin"])*100
        ca,cb,cc=st.columns(3)
        ca.metric("Số ngày chiến dịch",int(comp.loc[True,"days"]))
        cb.metric("Chênh doanh thu/ngày",f"{uplift:+.1%}")
        cc.metric("Chênh biên LN gộp",f"{delta_margin:+.2f} điểm %")
    c1,c2=st.columns(2)
    with c1:
        st.subheader("Doanh thu/ngày: chiến dịch so với ngày thường")
        fig=px.bar(campaign_summary,x="group",y="revenue_per_day",color="group",text_auto=".3s",color_discrete_sequence=[TEAL,ORANGE])
        fig.update_layout(xaxis_title="",yaxis_title="Doanh thu/ngày")
        chart(style_chart(fig,legend=False))
    with c2:
        st.subheader("Biên lợi nhuận gộp theo nhóm ngày")
        fig=px.bar(campaign_summary,x="group",y="margin",color="group",text_auto=".1%",color_discrete_sequence=[TEAL,ORANGE])
        fig.update_layout(xaxis_title="",yaxis_title="GM%")
        chart(style_chart(fig,percent_y=True,legend=False))
    c3,c4=st.columns([1.1,1])
    with c3:
        st.subheader("Quan hệ chiết khấu và biên lợi nhuận theo ngày")
        days["gm"]=days.gp/days.revenue.where(days.revenue!=0)
        days["group"]=days.is_campaign_day.map({True:"Chiến dịch",False:"Ngày thường"})
        fig=px.scatter(days,x="avg_discount",y="gm",color="group",opacity=.6,
                       color_discrete_map={"Chiến dịch":ORANGE,"Ngày thường":TEAL},
                       hover_data={"date":True,"revenue":":,.0f","rows":True},
                       labels={"avg_discount":"Giảm giá TB (%)","gm":"GM%","group":"Nhóm ngày"})
        chart(style_chart(fig,percent_y=True))
    with c4:
        st.subheader("Tỷ trọng doanh thu theo mức giảm giá")
        bin_labels=["0%",">0–10%",">10–20%",">20–35%"]
        bands=pd.cut(f.discount_pct,bins=[-0.1,0,10,20,100],labels=bin_labels,include_lowest=True)
        tbl=f.groupby(bands,observed=True).total_value.sum().reindex(bin_labels,fill_value=0).reset_index()
        tbl.columns=["band","revenue"]
        fig=px.bar(tbl,x="band",y="revenue",color_discrete_sequence=[PURPLE])
        fig.update_layout(xaxis_title="Mức chiết khấu",yaxis_title="Doanh thu")
        chart(style_chart(fig,legend=False))

elif page.startswith("04"):
    title("Danh mục sản phẩm", "Phân tích ngành hàng, SKU, hiệu quả lợi nhuận và mức độ tập trung doanh thu (ABC).")
    metric_strip(stats)
    categories=f.groupby("category",observed=True,as_index=False).agg(revenue=("total_value","sum"),gp=("gross_profit","sum"),units=("quantity","sum"))
    categories["margin"]=categories.gp/categories.revenue
    categories=categories.sort_values("revenue",ascending=False)
    c1,c2=st.columns([1.15,1])
    with c1:
        st.subheader("Doanh thu theo ngành hàng")
        fig=px.bar(categories,x="revenue",y="category",orientation="h",color="margin",color_continuous_scale="Teal",text_auto=".3s")
        fig.update_layout(yaxis=dict(categoryorder="total ascending"),yaxis_title="",xaxis_title="Doanh thu",coloraxis_colorbar=dict(title="GM%",tickformat=".0%"))
        chart(style_chart(fig,legend=False,height=425))
    with c2:
        st.subheader("Cơ cấu doanh thu")
        fig=px.treemap(categories,path=["category"],values="revenue",color="margin",color_continuous_scale="Teal")
        fig.update_traces(textinfo="label+percent root")
        chart(style_chart(fig,legend=False,height=425))
    products=f.groupby(["sku_id","sku_name","category"],observed=True,as_index=False).agg(revenue=("total_value","sum"),gp=("gross_profit","sum"),units=("quantity","sum"))
    products["margin"]=products.gp/products.revenue
    products=products.sort_values("revenue",ascending=False).reset_index(drop=True)
    products["cumulative_share"]=products.revenue.cumsum()/products.revenue.sum()
    products["ABC"]=pd.cut(products.cumulative_share,bins=[-0.0001,.8,.95,1.0000001],labels=["A","B","C"])
    st.subheader("Top 12 SKU theo doanh thu")
    top=products.head(12).iloc[::-1]
    fig=px.bar(top,x="revenue",y="sku_name",orientation="h",color_discrete_sequence=[TEAL],
               hover_data={"margin":":.1%","units":True})
    fig.update_layout(yaxis_title="",xaxis_title="Doanh thu",height=490)
    chart(style_chart(fig,legend=False,height=490))
    c3,c4=st.columns([1.15,1])
    with c3:
        st.subheader("Phân tích ABC: Tập trung doanh thu")
        products["rank"]=range(1,len(products)+1)
        fig=px.line(products,x="rank",y="cumulative_share",markers=False,color_discrete_sequence=[PURPLE])
        fig.add_hline(y=.8,line_dash="dash",line_color=ORANGE,annotation_text="80%")
        fig.add_hline(y=.95,line_dash="dash",line_color=TEAL,annotation_text="95%")
        fig.update_layout(xaxis_title="Thứ hạng SKU theo doanh thu",yaxis_title="Tỷ trọng cộng dồn")
        chart(style_chart(fig,percent_y=True,legend=False))
    with c4:
        st.subheader("Tỷ trọng SKU theo nhóm ABC")
        abc=products.groupby("ABC",observed=True).agg(sku_count=("sku_id","size"),revenue=("revenue","sum")).reset_index()
        fig=px.bar(abc,x="ABC",y="sku_count",color="ABC",text_auto=True,color_discrete_sequence=[TEAL,ORANGE,PURPLE])
        fig.update_layout(xaxis_title="Nhóm",yaxis_title="Số SKU")
        chart(style_chart(fig,legend=False))
    st.subheader("Chi tiết SKU")
    shown=products[["sku_id","sku_name","category","revenue","gp","margin","units","cumulative_share","ABC"]].head(100).copy()
    shown.columns=["SKU ID","Tên SKU","Ngành hàng","Doanh thu","Lợi nhuận gộp","GM%","Đơn vị","Tỷ trọng lũy kế","Nhóm ABC"]
    st.dataframe(shown,hide_index=True,use_container_width=True,column_config={
        "Doanh thu":st.column_config.NumberColumn(format="%.2f"),
        "Lợi nhuận gộp":st.column_config.NumberColumn(format="%.2f"),
        "GM%":st.column_config.NumberColumn(format="%.2f"),
        "Tỷ trọng lũy kế":st.column_config.NumberColumn(format="%.3f"),
    })

st.divider()
with st.expander("📐 Định nghĩa KPI & phương pháp tính"):
    st.markdown("""
    - **Doanh thu** = `SUM(sales.total_value)`.
    - **Lợi nhuận gộp** = `SUM(sales.total_value - sales.quantity × skus.cost_price)`.
    - **Biên lợi nhuận gộp** = Lợi nhuận gộp / Doanh thu.
    - **Sản phẩm bán ra** = `SUM(sales.quantity)`.
    - **Dòng bán** = số dòng trong bảng `sales`; **Giao dịch** = `nunique(sale_id)`.
    - **Campaign day**: ít nhất 50% dòng bán toàn chuỗi trong ngày có `discount_pct > 0`.
    - Dữ liệu lấy từ ba bảng `sales`, `skus`, `stores` với các quan hệ `sku_id`, `store_id` tương ứng.
    - **Đơn vị tiền tệ:** giữ nguyên đơn vị của nguồn Blue Mart; không tự quy đổi.
    """)
with st.expander("📥 Tải dữ liệu tổng hợp sau lọc"):
    export=(f.groupby(["month","channel","category"],observed=True,as_index=False)
            .agg(revenue=("total_value","sum"),gross_profit=("gross_profit","sum"),units=("quantity","sum")))
    export["gross_margin"]=export.gross_profit/export.revenue.where(export.revenue!=0)
    st.download_button("Tải bảng tổng hợp (.csv)",data=export.to_csv(index=False).encode("utf-8-sig"),
                       file_name="blue_mart_filtered_summary.csv",mime="text/csv")
st.caption("Portfolio demo • Xây dựng lại trên Streamlit và Plotly, độc lập với Power BI • Không đồng bộ tự động với báo cáo Power BI.")
