import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils.data_utils import load_orders, filter_df, compute_kpis, cohort_analysis, rfm_segmentation

st.set_page_config(
    page_title="Data Storytelling Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# â”€â”€ minimal CSS: works in both light and dark theme â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown("""
<style>
/* KPI card */
.kpi-card {
    background: var(--background-color, #f8f9fa);
    border: 1px solid rgba(128,128,128,0.2);
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
}
.kpi-label {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 26px;
    font-weight: 700;
}
.section-title {
    font-size: 18px;
    font-weight: 700;
    margin: 24px 0 10px 0;
    padding-bottom: 6px;
    border-bottom: 2px solid rgba(128,128,128,0.15);
}
</style>
""", unsafe_allow_html=True)

# â”€â”€ Data â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
DATA_PATH = os.environ.get(
    "ORDERS_CSV",
    os.path.join(os.path.dirname(__file__), "..", "data", "orders.csv")
)

@st.cache_data(show_spinner=False)
def load_data():
    return load_orders(DATA_PATH)

df = load_data()
min_d = df["order_date"].dt.date.min()
max_d = df["order_date"].dt.date.max()

# â”€â”€ Sidebar â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.sidebar.title("Data Storytelling Dashboard")
st.sidebar.markdown("---")
st.sidebar.header("Filters")

date_range = st.sidebar.date_input(
    "Date Range", value=(min_d, max_d), min_value=min_d, max_value=max_d
)
countries  = st.sidebar.multiselect("Countries",   sorted(df["country"].unique().tolist()))
channels   = st.sidebar.multiselect("Channels",    sorted(df["channel"].unique().tolist()))
categories = st.sidebar.multiselect("Categories",  sorted(df["category"].unique().tolist()))

fdf  = filter_df(df, date_range, countries, channels, categories)
kpis = compute_kpis(fdf)

# â”€â”€ Header â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.title("Data Storytelling Dashboard")
st.caption(
    f"Showing **{kpis['Orders']:,}** orders from "
    f"**{date_range[0]}** to **{date_range[1]}**  |  "
    f"**{kpis['Customers']:,}** unique customers"
)
st.markdown("---")

# â”€â”€ KPI Cards â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
kpi_data = [
    ("Revenue",    f"${kpis['Revenue']:,.0f}",          "#2196F3"),
    ("Profit",     f"${kpis['Profit']:,.0f}",           "#4CAF50"),
    ("Orders",     f"{kpis['Orders']:,}",               "#FF9800"),
    ("Customers",  f"{kpis['Customers']:,}",            "#9C27B0"),
    ("AOV",        f"${kpis['AOV']:,.2f}",              "#00BCD4"),
    ("Margin %",   f"{kpis['Margin%']*100:.1f}%",       "#F44336"),
]

cols = st.columns(6)
for col, (label, value, color) in zip(cols, kpi_data):
    col.markdown(f"""
    <div class="kpi-card" style="border-top: 3px solid {color};">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value" style="color:{color};">{value}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# â”€â”€ Auto Insight Bar â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
top_cat     = fdf.groupby("category")["revenue"].sum().idxmax()
top_channel = fdf.groupby("channel")["revenue"].sum().idxmax()
top_country = fdf.groupby("country")["revenue"].sum().idxmax()
margin_pct  = kpis["Margin%"] * 100

st.info(
    f"Top category: **{top_cat}** Â· "
    f"Top channel: **{top_channel}** Â· "
    f"Top market: **{top_country}** Â· "
    f"Overall margin: **{margin_pct:.1f}%**"
)

st.markdown("---")

# â”€â”€ Trend Chart â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown('<div class="section-title">Monthly Revenue & Profit</div>', unsafe_allow_html=True)

ts = (
    fdf.groupby("order_month")
       .agg(revenue=("revenue","sum"), profit=("profit","sum"), orders=("order_id","nunique"))
       .reset_index()
       .sort_values("order_month")
)

fig_ts = go.Figure()
fig_ts.add_trace(go.Scatter(
    x=ts["order_month"], y=ts["revenue"],
    mode="lines+markers", name="Revenue",
    line=dict(color="#2196F3", width=2),
    fill="tozeroy", fillcolor="rgba(33,150,243,0.08)"
))
fig_ts.add_trace(go.Scatter(
    x=ts["order_month"], y=ts["profit"],
    mode="lines+markers", name="Profit",
    line=dict(color="#4CAF50", width=2),
    yaxis="y2"
))
fig_ts.add_trace(go.Bar(
    x=ts["order_month"], y=ts["orders"],
    name="Orders", yaxis="y3",
    marker_color="rgba(255,152,0,0.25)",
    offsetgroup=1
))
fig_ts.update_layout(
    xaxis_title="Month",
    yaxis=dict(title="Revenue ($)", showgrid=True, gridcolor="rgba(128,128,128,0.1)"),
    yaxis2=dict(title="Profit ($)", overlaying="y", side="right", showgrid=False),
    yaxis3=dict(overlaying="y", side="right", showgrid=False, showticklabels=False, range=[0, ts["orders"].max()*6]),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    hovermode="x unified",
    height=420,
    margin=dict(l=40, r=60, t=30, b=40),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig_ts, use_container_width=True)

# â”€â”€ Category & Products â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown('<div class="section-title">Category & Product Performance</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

cat_rev = (
    fdf.groupby("category")["revenue"]
       .sum().reset_index()
       .sort_values("revenue")
)
fig_cat = px.bar(
    cat_rev, x="revenue", y="category", orientation="h",
    title="Revenue by Category",
    color="revenue", color_continuous_scale="Blues",
    labels={"revenue": "Revenue ($)", "category": ""}
)
fig_cat.update_layout(
    coloraxis_showscale=False,
    margin=dict(l=10, r=10, t=40, b=30),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
)
c1.plotly_chart(fig_cat, use_container_width=True)

prod = (
    fdf.groupby(["product_id","subcategory"])["revenue"]
       .sum().reset_index()
       .sort_values("revenue", ascending=False)
       .head(15)
)
fig_prod = px.bar(
    prod, x="revenue", y="product_id", color="subcategory",
    orientation="h", title="Top 15 Products",
    labels={"revenue": "Revenue ($)", "product_id": ""}
)
fig_prod.update_layout(
    margin=dict(l=10, r=10, t=40, b=30),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
)
c2.plotly_chart(fig_prod, use_container_width=True)

# â”€â”€ Geography â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown('<div class="section-title">Revenue by Geography</div>', unsafe_allow_html=True)

geo = fdf.groupby(["country","city"])["revenue"].sum().reset_index()
fig_geo = px.treemap(
    geo, path=["country","city"], values="revenue",
    title="Country â†’ City Revenue Breakdown",
    color="revenue", color_continuous_scale="Blues"
)
fig_geo.update_layout(margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig_geo, use_container_width=True)

# â”€â”€ Channel â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown('<div class="section-title">Channel Revenue Share</div>', unsafe_allow_html=True)

ch = fdf.groupby("channel")["revenue"].sum().reset_index()
fig_ch = px.pie(
    ch, values="revenue", names="channel",
    title="Sales by Channel", hole=0.42,
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig_ch.update_layout(margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig_ch, use_container_width=True)

# â”€â”€ Cohort Analysis â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown('<div class="section-title">Cohort Retention Analysis</div>', unsafe_allow_html=True)

cohort_abs, cohort_ret = cohort_analysis(fdf)

tab1, tab2 = st.tabs(["Retention Rate (%)", "Absolute Counts"])

with tab1:
    ret_pct = (cohort_ret * 100).round(1)
    fig_cohort = px.imshow(
        ret_pct,
        labels=dict(x="Months Since First Purchase", y="Cohort Month", color="Retention %"),
        color_continuous_scale="Blues",
        title="Customer Retention by Cohort (%)",
        aspect="auto"
    )
    fig_cohort.update_layout(
        margin=dict(l=10, r=10, t=50, b=30),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_cohort, use_container_width=True)

with tab2:
    st.dataframe(
        cohort_abs.style.background_gradient(cmap="Blues"),
        use_container_width=True
    )

# â”€â”€ RFM Segmentation â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown('<div class="section-title">RFM Customer Segmentation</div>', unsafe_allow_html=True)

rfm = rfm_segmentation(fdf)
seg_counts = rfm["Segment"].value_counts().reset_index()
seg_counts.columns = ["Segment", "Customers"]

r1, r2 = st.columns(2)

fig_rfm = px.bar(
    seg_counts, x="Segment", y="Customers",
    title="Customers by Segment",
    color="Segment",
    color_discrete_map={"Champions": "#4CAF50", "Active": "#2196F3", "New/Cold": "#FF9800"}
)
fig_rfm.update_layout(
    showlegend=False,
    margin=dict(l=10, r=10, t=40, b=30),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
)
r1.plotly_chart(fig_rfm, use_container_width=True)

fig_scatter = px.scatter(
    rfm, x="R", y="F", size="M", color="Segment",
    title="RFM Scatter (size = Monetary)",
    labels={"R": "Recency Score", "F": "Frequency Score"},
    color_discrete_map={"Champions": "#4CAF50", "Active": "#2196F3", "New/Cold": "#FF9800"}
)
fig_scatter.update_layout(
    margin=dict(l=10, r=10, t=40, b=30),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
)
r2.plotly_chart(fig_scatter, use_container_width=True)

# â”€â”€ Export â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown("---")
col_a, col_b, _ = st.columns([1, 1, 4])
col_a.download_button(
    "Download Filtered CSV",
    data=fdf.to_csv(index=False).encode("utf-8"),
    file_name="filtered_orders.csv",
    mime="text/csv"
)
col_b.download_button(
    "Download RFM Table",
    data=rfm.to_csv(index=False).encode("utf-8"),
    file_name="rfm_segments.csv",
    mime="text/csv"
)

st.caption("Data Storytelling Dashboard Â· Python Â· Streamlit Â· Plotly Â· Synthetic e-commerce dataset")