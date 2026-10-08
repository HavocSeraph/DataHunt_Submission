import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Executive Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Premium Custom CSS Styling (Minimalist Financial Report Aesthetics)
st.markdown("""
<style>
    /* Hide Streamlit default interface elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Root container adjustments */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1400px;
    }

    /* Minimalist Dark Background */
    .stApp {
        background-color: #0B0F17;
        color: #E2E8F0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Metric Cards Custom Styling */
    div[data-testid="stMetric"], div[data-testid="metric-container"] {
        background: transparent !important;
        border: 1px solid #333333 !important;
        padding: 15px !important;
        border-radius: 4px !important;
    }

    div[data-testid="stMetricLabel"] label, div[data-testid="stMetricLabel"] p {
        color: #888888 !important;
        font-weight: 400 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-size: 0.75rem !important;
    }

    div[data-testid="stMetricValue"] div {
        color: #F8FAFC !important;
        font-weight: 500 !important;
        font-size: 1.6rem !important;
    }

    /* Minimal Expander Header Styling */
    div[data-testid="stExpander"] {
        background: transparent !important;
        border: 1px solid #222222 !important;
        border-radius: 4px !important;
    }

    /* Clean Divider */
    hr {
        border-color: #222222 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Immutable Backend & Data Pipeline
@st.cache_data
def load_data():
    df = pd.read_csv('THE_DATA_HUNT_dataset.csv')
    df = df.drop_duplicates()
    df['shipping_days'] = df['shipping_days'].apply(lambda x: x if pd.notnull(x) and x >= 0 else None)
    df['discount_pct'] = df['discount_pct'].apply(lambda x: x if pd.notnull(x) and 0 <= x <= 1 else None)
    df = df.dropna()
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

# 4. Main Title & Closed Pipeline Expander
st.markdown("<h1 style='font-weight: 300; letter-spacing: -0.5px; margin-bottom: 0.2rem;'>Executive Financial Performance</h1>", unsafe_allow_html=True)

with st.expander("Data Cleaning Pipeline", expanded=False):
    st.markdown("""
    - Removed exact duplicate records.
    - Nullified negative shipping days via conditional lambda evaluation.
    - Clamped discount percentage strictly between 0.0 and 1.0.
    - Removed missing values to ensure strict numerical precision.
    """)

st.divider()

# 5. Sidebar Filters
st.sidebar.markdown("<h3 style='font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; color: #888888; font-weight: 500;'>Filters</h3>", unsafe_allow_html=True)
cat_filter = st.sidebar.multiselect("Category", df['category'].unique(), default=df['category'].unique())
reg_filter = st.sidebar.multiselect("Region", df['region'].unique(), default=df['region'].unique())
seg_filter = st.sidebar.multiselect("Segment", df['segment'].unique(), default=df['segment'].unique())

filtered_df = df[
    (df['category'].isin(cat_filter)) & 
    (df['region'].isin(reg_filter)) & 
    (df['segment'].isin(seg_filter))
]

# 6. Advanced Metrics Layout
col1, col2, col3, col4 = st.columns(4)

total_revenue = filtered_df['revenue'].sum() if len(filtered_df) > 0 else 0
total_profit = filtered_df['profit'].sum() if len(filtered_df) > 0 else 0
profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
total_orders = len(filtered_df)
returns_count = len(filtered_df[filtered_df['order_status'].isin(['Returned', 'Cancelled'])])
return_rate = (returns_count / total_orders * 100) if total_orders > 0 else 0

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}", delta=f"{profit_margin:.1f}% Margin", delta_color="normal" if profit_margin >= 0 else "inverse")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Return Rate", f"{return_rate:.2f}%", delta=f"{returns_count:,} Cancelled/Returned", delta_color="inverse")

st.divider()

# 7. High Data-Ink Ratio Plotly Visualizations with Dynamic Insights
ACCENT_COLOR = "#60A5FA"
MUTED_COLOR = "#334155"

row1_col1, row1_col2 = st.columns(2)

# Chart 1: Grouped Bar Chart (Revenue vs Profit by Category)
with row1_col1:
    if len(filtered_df) > 0:
        agg_cat = filtered_df.groupby('category')[['revenue', 'profit']].sum().reset_index()
        top_cat_row = agg_cat.sort_values('revenue', ascending=False).iloc[0]
        header_text = f"{top_cat_row['category']} leads performance with ${top_cat_row['revenue']:,.0f} in revenue"
    else:
        header_text = "Revenue vs Profit by Category"
        agg_cat = pd.DataFrame(columns=['category', 'revenue', 'profit'])

    st.markdown(f"<h3 style='font-weight: 300; color: #CBD5E1; font-size: 0.95rem; margin-bottom: 0.8rem;'>{header_text}</h3>", unsafe_allow_html=True)
    
    fig1 = px.bar(
        agg_cat, 
        x='category', 
        y=['revenue', 'profit'], 
        barmode='group', 
        template="plotly_dark",
        color_discrete_sequence=[ACCENT_COLOR, MUTED_COLOR]
    )
    fig1.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    fig1.update_xaxes(showgrid=False, zeroline=False, title=None)
    fig1.update_yaxes(showgrid=False, zeroline=False, title=None)
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Line Chart (Monthly Revenue and Profit Trend for 2025)
with row1_col2:
    if len(filtered_df) > 0:
        df_trend = filtered_df.copy()
        df_trend['month'] = df_trend['order_date'].dt.strftime('%Y-%m')
        agg_month = df_trend.groupby('month')[['revenue', 'profit']].sum().reset_index()
        peak_month_row = agg_month.sort_values('revenue', ascending=False).iloc[0]
        header_text = f"Peak monthly revenue of ${peak_month_row['revenue']:,.0f} registered in {peak_month_row['month']}"
    else:
        header_text = "Monthly Revenue and Profit Trend"
        agg_month = pd.DataFrame(columns=['month', 'revenue', 'profit'])

    st.markdown(f"<h3 style='font-weight: 300; color: #CBD5E1; font-size: 0.95rem; margin-bottom: 0.8rem;'>{header_text}</h3>", unsafe_allow_html=True)

    fig2 = px.line(
        agg_month, 
        x='month', 
        y=['revenue', 'profit'], 
        template="plotly_dark",
        color_discrete_sequence=[ACCENT_COLOR, MUTED_COLOR]
    )
    fig2.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    fig2.update_xaxes(showgrid=False, zeroline=False, title=None)
    fig2.update_yaxes(showgrid=False, zeroline=False, title=None)
    st.plotly_chart(fig2, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

# Chart 3: Histogram (Count of Returns/Cancellations by Category)
with row2_col1:
    bad_orders = filtered_df[filtered_df['order_status'].isin(['Returned', 'Cancelled'])]
    if len(bad_orders) > 0:
        bad_cat_counts = bad_orders.groupby('category').size().reset_index(name='count').sort_values('count', ascending=False)
        top_bad_cat = bad_cat_counts.iloc[0]
        header_text = f"{top_bad_cat['category']} experienced highest returns and cancellations ({top_bad_cat['count']:,} orders)"
    else:
        header_text = "Count of Returns and Cancellations by Category"

    st.markdown(f"<h3 style='font-weight: 300; color: #CBD5E1; font-size: 0.95rem; margin-bottom: 0.8rem;'>{header_text}</h3>", unsafe_allow_html=True)

    fig3 = px.histogram(
        bad_orders, 
        x='category', 
        template="plotly_dark",
        color_discrete_sequence=[ACCENT_COLOR]
    )
    fig3.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    fig3.update_xaxes(showgrid=False, zeroline=False, title=None)
    fig3.update_yaxes(showgrid=False, zeroline=False, title=None)
    st.plotly_chart(fig3, use_container_width=True)

# Chart 4: Horizontal Bar Chart (Top 10 Cities by Revenue)
with row2_col2:
    if len(filtered_df) > 0:
        top_cities = filtered_df.groupby('city')['revenue'].sum().reset_index().sort_values('revenue', ascending=False).head(10)
        top_city_row = top_cities.iloc[0]
        header_text = f"{top_city_row['city']} dominates urban revenue generation at ${top_city_row['revenue']:,.0f}"
    else:
        header_text = "Top 10 Cities by Revenue"
        top_cities = pd.DataFrame(columns=['city', 'revenue'])

    st.markdown(f"<h3 style='font-weight: 300; color: #CBD5E1; font-size: 0.95rem; margin-bottom: 0.8rem;'>{header_text}</h3>", unsafe_allow_html=True)

    # Highlight top city with accent color, others with muted color
    if len(top_cities) > 0:
        top_cities['color'] = [ACCENT_COLOR if i == 0 else MUTED_COLOR for i in range(len(top_cities))]
    else:
        top_cities['color'] = []

    fig4 = px.bar(
        top_cities, 
        x='revenue', 
        y='city', 
        orientation='h', 
        template="plotly_dark",
        color='color',
        color_discrete_map="identity"
    )
    fig4.update_layout(
        yaxis={'categoryorder':'total ascending'}, 
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    fig4.update_xaxes(showgrid=False, zeroline=False, title=None)
    fig4.update_yaxes(showgrid=False, zeroline=False, title=None)
    st.plotly_chart(fig4, use_container_width=True)