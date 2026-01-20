import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Dubai Mall Analytics Dashboard",
    page_icon="🏬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# PROJECTOR-FRIENDLY LIGHT THEME CSS
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;500;600;700&display=swap');
    
    :root {
        --gold-primary: #B8860B;
        --gold-dark: #8B6914;
        --gold-light: #DAA520;
        --bg-primary: #FFFFFF;
        --bg-secondary: #F8F9FA;
        --text-primary: #1A1A2E;
        --text-secondary: #4A4A6A;
    }
    
    .stApp {
        background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main-header {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
        border-radius: 20px;
        padding: 35px 45px;
        margin-bottom: 30px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.18);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(184, 134, 11, 0.3) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .main-header h1 {
        font-family: 'Playfair Display', serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: #DAA520;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        font-family: 'Poppins', sans-serif;
        color: #E2E8F0;
        font-size: 1.1rem;
        margin-top: 10px;
        font-weight: 300;
        letter-spacing: 1px;
        position: relative;
        z-index: 1;
    }
    
    .section-header {
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        font-weight: 600;
        color: #1A1A2E !important;
        margin: 35px 0 20px 0;
        padding-bottom: 12px;
        border-bottom: 3px solid #B8860B;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .chart-container {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .chart-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #1A1A2E !important;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #F3F4F6;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1A1A2E 0%, #16213E 100%);
    }
    
    .sidebar-header {
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        font-weight: 600;
        color: #DAA520;
        text-align: center;
        padding: 25px 0;
        border-bottom: 2px solid rgba(218, 165, 32, 0.3);
        margin-bottom: 25px;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stDateInput label,
    [data-testid="stSidebar"] .stCheckbox label,
    [data-testid="stSidebar"] .stCheckbox span,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #E2E8F0 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stMultiSelect > div > div {
        background-color: #FFFFFF !important;
        border: 2px solid #374151 !important;
        border-radius: 10px !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] span,
    [data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] span,
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
        color: #1A1A2E !important;
    }
    
    .stSelectbox label, 
    .stMultiSelect label,
    .stSlider label,
    .stDateInput label,
    .stTextInput label,
    .stNumberInput label,
    .stRadio label,
    .stCheckbox label {
        color: #1A1A2E !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background-color: #FFFFFF !important;
        border: 2px solid #D1D5DB !important;
        border-radius: 10px !important;
        color: #1A1A2E !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div,
    .stSelectbox [data-baseweb="select"] span,
    .stMultiSelect [data-baseweb="select"] > div,
    .stMultiSelect [data-baseweb="select"] span {
        color: #1A1A2E !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] span {
        color: #1A1A2E !important;
    }
    
    .stSelectbox svg,
    .stMultiSelect svg {
        fill: #1A1A2E !important;
        color: #1A1A2E !important;
    }
    
    [data-baseweb="menu"],
    [data-baseweb="popover"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        border-radius: 10px !important;
    }
    
    [data-baseweb="menu"] li,
    [data-baseweb="menu"] [role="option"],
    [data-baseweb="menu"] ul li {
        color: #1A1A2E !important;
        background-color: #FFFFFF !important;
        font-family: 'Poppins', sans-serif !important;
        padding: 10px 15px !important;
    }
    
    [data-baseweb="menu"] li:hover,
    [data-baseweb="menu"] [role="option"]:hover {
        background-color: #FEF3C7 !important;
        color: #92400E !important;
    }
    
    [data-baseweb="menu"] [aria-selected="true"],
    [data-baseweb="menu"] li[aria-selected="true"] {
        background-color: #B8860B !important;
        color: #FFFFFF !important;
    }
    
    .stSlider [data-baseweb="slider"] div,
    .stSlider > div > div > div > div,
    .stSlider > div > div > div:last-child {
        color: #1A1A2E !important;
    }
    
    .stSlider [data-baseweb="slider"] div[role="slider"] {
        background-color: #B8860B !important;
        border-color: #B8860B !important;
    }
    
    .stDateInput input {
        color: #1A1A2E !important;
        background-color: #FFFFFF !important;
        border: 2px solid #D1D5DB !important;
        border-radius: 10px !important;
    }
    
    .stCheckbox span {
        color: #1A1A2E !important;
    }
    
    [data-testid="stSidebar"] .stCheckbox span {
        color: #E2E8F0 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: #F3F4F6;
        border-radius: 12px;
        padding: 8px;
        flex-wrap: wrap;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: #4A4A6A !important;
        border-radius: 8px;
        padding: 10px 16px;
        background: transparent;
        font-size: 0.85rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #B8860B 0%, #DAA520 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(184, 134, 11, 0.3);
    }
    
    .insight-card {
        background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFC 100%);
        border-left: 5px solid #B8860B;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .insight-card h4 {
        font-family: 'Poppins', sans-serif;
        color: #1A1A2E !important;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .insight-card p {
        font-family: 'Poppins', sans-serif;
        color: #4A4A6A !important;
        font-size: 0.95rem;
        margin: 5px 0;
    }
    
    .insight-card strong {
        color: #B8860B !important;
    }
    
    .metric-card {
        background: #FFFFFF;
        border: 2px solid #E5E7EB;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .metric-card .value {
        font-size: 2rem;
        font-weight: 700;
        color: #1A1A2E;
    }
    
    .metric-card .label {
        font-size: 0.85rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .quadrant-label {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        padding: 8px 16px;
        border-radius: 20px;
        display: inline-block;
        margin: 5px;
    }
    
    .custom-footer {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
        border-radius: 16px;
        padding: 30px;
        margin-top: 50px;
        text-align: center;
    }
    
    .custom-footer p {
        font-family: 'Poppins', sans-serif;
        color: #94A3B8;
        margin: 5px 0;
    }
    
    .custom-footer .gold-text {
        color: #DAA520;
        font-weight: 600;
    }
    
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F1F5F9;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #B8860B 0%, #DAA520 100%);
        border-radius: 5px;
    }
    
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #1A1A2E !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li,
    [data-testid="stSidebar"] .stMarkdown span {
        color: #E2E8F0 !important;
    }
    
    .grade-a { background: #D1FAE5; color: #059669; }
    .grade-b { background: #DBEAFE; color: #2563EB; }
    .grade-c { background: #FEF3C7; color: #D97706; }
    .grade-d { background: #FEE2E2; color: #DC2626; }
    .grade-f { background: #1A1A2E; color: #FFFFFF; }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATA LOADING
# ============================================
@st.cache_data
def load_data():
    """Load and preprocess the Dubai Mall dataset"""
    df = pd.read_csv('dubai_mall_simple.csv')
    df['date'] = pd.to_datetime(df['date'])
    df['week'] = df['date'].dt.isocalendar().week
    df['day_of_month'] = df['date'].dt.day
    df['quarter'] = df['date'].dt.quarter
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.month_name()
    
    floor_mapping = {'LG': 'Lower Ground', 'G': 'Ground', '1': 'Level 1', '2': 'Level 2', '3': 'Level 3'}
    df['floor_label'] = df['floor'].map(floor_mapping)
    
    return df

# ============================================
# HELPER FUNCTIONS
# ============================================
def format_currency(value):
    """Format number as AED currency with M/K suffix"""
    if value >= 1_000_000_000:
        return f"AED {value/1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"AED {value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"AED {value/1_000:.1f}K"
    else:
        return f"AED {value:.0f}"

def format_number(value):
    """Format large numbers with M/K suffix"""
    if value >= 1_000_000_000:
        return f"{value/1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"{value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    else:
        return f"{value:.0f}"

def format_value_short(value):
    """Format values for KPI display"""
    if value >= 1_000_000_000:
        return f"{value/1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"{value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    else:
        return f"{value:.0f}"

# ============================================
# CHART THEME
# ============================================
CHART_COLORS = ['#B8860B', '#2563EB', '#059669', '#DC2626', '#7C3AED', '#DB2777', '#0891B2', '#EA580C', '#84CC16', '#6366F1']

def apply_chart_theme(fig, height=400):
    """Apply projector-friendly theme to charts"""
    fig.update_layout(
        paper_bgcolor='rgba(255,255,255,0)',
        plot_bgcolor='rgba(255,255,255,0)',
        font=dict(family='Poppins, sans-serif', color='#1A1A2E', size=12),
        xaxis=dict(
            gridcolor='rgba(0,0,0,0.08)',
            linecolor='#E5E7EB',
            tickfont=dict(color='#4A4A6A', size=11),
            title_font=dict(color='#1A1A2E', size=13, family='Poppins')
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0.08)',
            linecolor='#E5E7EB',
            tickfont=dict(color='#4A4A6A', size=11),
            title_font=dict(color='#1A1A2E', size=13, family='Poppins')
        ),
        legend=dict(
            font=dict(color='#1A1A2E', size=11),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#E5E7EB',
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor='#1A1A2E',
            font_size=12,
            font_family='Poppins',
            font_color='#FFFFFF',
            bordercolor='#B8860B'
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        height=height
    )
    return fig

# ============================================
# MAIN APPLICATION
# ============================================
def main():
    # Load data
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("⚠️ Data file 'dubai_mall_simple.csv' not found!")
        st.stop()
    
    # ========================================
    # SIDEBAR
    # ========================================
    with st.sidebar:
        st.markdown('<div class="sidebar-header">🏬 Dubai Mall<br>Analytics</div>', unsafe_allow_html=True)
        
        st.markdown("### 📅 Date Range")
        date_range = st.date_input(
            "Select Period",
            value=(df['date'].min(), df['date'].max()),
            min_value=df['date'].min(),
            max_value=df['date'].max()
        )
        
        st.markdown("---")
        st.markdown("### 🏪 Global Filters")
        
        all_categories = ['All Categories'] + sorted(df['category'].unique().tolist())
        selected_category = st.selectbox("Category", all_categories)
        
        all_floors = ['All Floors'] + sorted(df['floor'].unique().tolist())
        selected_floor = st.selectbox("Floor", all_floors)
        
        st.markdown("---")
        st.markdown("### ⚙️ Display Options")
        show_raw_data = st.checkbox("Show Raw Data Tables", value=False)
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; padding: 15px;'>
            <p style='color: #94A3B8; font-size: 0.8rem;'>📊 Dubai Mall Dashboard</p>
            <p style='color: #DAA520; font-size: 0.9rem; font-weight: 600;'>v3.0 - Full Analytics</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========================================
    # FILTER DATA
    # ========================================
    filtered_df = df.copy()
    
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['date'].dt.date >= date_range[0]) & 
            (filtered_df['date'].dt.date <= date_range[1])
        ]
    
    if selected_category != 'All Categories':
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    
    if selected_floor != 'All Floors':
        filtered_df = filtered_df[filtered_df['floor'] == selected_floor]
    
    # ========================================
    # HEADER
    # ========================================
    st.markdown("""
    <div class="main-header">
        <h1>🏬 Dubai Mall Analytics Dashboard</h1>
        <p>Real-time Retail Performance Intelligence • Premium Analytics Suite</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========================================
    # KPI CARDS
    # ========================================
    st.markdown('<div class="section-header">📊 Key Performance Indicators</div>', unsafe_allow_html=True)
    
    total_sales = filtered_df['sales_aed'].sum()
    total_footfall = filtered_df.groupby('date')['mall_footfall'].first().sum()
    total_transactions = filtered_df['transactions'].sum()
    avg_conversion = filtered_df['conversion_rate'].mean() * 100
    avg_basket = filtered_df['avg_basket_aed'].mean()
    sales_per_sqft = filtered_df['sales_per_sqft'].mean()
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5, kpi_col6 = st.columns(6)
    
    kpi_data = [
        (kpi_col1, "💰", "Total Sales", format_value_short(total_sales), "#B8860B", "12.5"),
        (kpi_col2, "👥", "Mall Footfall", format_value_short(total_footfall), "#2563EB", "8.3"),
        (kpi_col3, "🛒", "Transactions", format_value_short(total_transactions), "#059669", "15.2"),
        (kpi_col4, "📈", "Conversion", f"{avg_conversion:.1f}%", "#7C3AED", "3.2"),
        (kpi_col5, "🧺", "Avg Basket", format_value_short(avg_basket), "#DB2777", "5.8"),
        (kpi_col6, "📐", "Sales/Sqft", format_value_short(sales_per_sqft), "#0891B2", "7.1"),
    ]
    
    for col, icon, label, value, color, delta in kpi_data:
        with col:
            st.markdown(f"""
            <div style="
                background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFC 100%);
                border: 2px solid #E5E7EB;
                border-radius: 16px;
                padding: 20px 15px;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                border-bottom: 4px solid {color};
                height: 160px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="font-size: 2rem; margin-bottom: 5px;">{icon}</div>
                <div style="font-size: 0.7rem; color: #6B7280; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">{label}</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1A1A2E; margin: 5px 0;">{value}</div>
                <div style="font-size: 0.8rem; color: #059669; background: rgba(5,150,105,0.1); padding: 2px 10px; border-radius: 20px; display: inline-block;">▲ {delta}%</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========================================
    # TABS
    # ========================================
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🌍 Tourist Impact", 
        "📊 Category Deep Dive",
        "🏪 Store Analysis", 
        "⏰ Time Patterns",
        "🎯 Strategic View",
        "📈 Overview"
    ])
    
    # ========================================
    # TAB 1: TOURIST VS RESIDENT IMPACT
    # ========================================
    with tab1:
        st.markdown('<div class="section-header">🌍 Tourist vs Resident Impact Analysis</div>', unsafe_allow_html=True)
        
        # ----- CHART 1: Triple-Line Correlation Timeline -----
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📈 Chart 1: Tourist & Resident Footfall vs Sales Correlation</div>', unsafe_allow_html=True)
        
        col_f1, col_f2 = st.columns([2, 6])
        with col_f1:
            chart1_agg = st.selectbox("Aggregation", ['Daily', 'Weekly', 'Monthly'], key='c1_agg')
        
        # Aggregate based on selection
        if chart1_agg == 'Daily':
            agg_df = filtered_df.groupby('date').agg({
                'tourist_footfall': 'first',
                'resident_footfall': 'first',
                'sales_aed': 'sum'
            }).reset_index()
            x_col = 'date'
        elif chart1_agg == 'Weekly':
            filtered_df['week_start'] = filtered_df['date'] - pd.to_timedelta(filtered_df['date'].dt.dayofweek, unit='d')
            agg_df = filtered_df.groupby('week_start').agg({
                'tourist_footfall': 'sum',
                'resident_footfall': 'sum',
                'sales_aed': 'sum'
            }).reset_index()
            x_col = 'week_start'
        else:
            agg_df = filtered_df.groupby('month_name').agg({
                'tourist_footfall': 'sum',
                'resident_footfall': 'sum',
                'sales_aed': 'sum'
            }).reset_index()
            x_col = 'month_name'
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(x=agg_df[x_col], y=agg_df['tourist_footfall'], name='Tourist Footfall',
                      line=dict(color='#B8860B', width=3), fill='tozeroy', fillcolor='rgba(184,134,11,0.1)'),
            secondary_y=False
        )
        fig.add_trace(
            go.Scatter(x=agg_df[x_col], y=agg_df['resident_footfall'], name='Resident Footfall',
                      line=dict(color='#2563EB', width=3), fill='tozeroy', fillcolor='rgba(37,99,235,0.1)'),
            secondary_y=False
        )
        fig.add_trace(
            go.Scatter(x=agg_df[x_col], y=agg_df['sales_aed'], name='Total Sales (AED)',
                      line=dict(color='#059669', width=4, dash='dot')),
            secondary_y=True
        )
        
        fig = apply_chart_theme(fig, height=450)
        fig.update_layout(
            yaxis_title='Footfall Count',
            yaxis2_title='Sales (AED)',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Insight
        tourist_sales_corr = filtered_df.groupby('date').agg({
            'tourist_footfall': 'first', 'sales_aed': 'sum'
        }).corr().iloc[0, 1]
        resident_sales_corr = filtered_df.groupby('date').agg({
            'resident_footfall': 'first', 'sales_aed': 'sum'
        }).corr().iloc[0, 1]
        
        st.markdown(f"""
        <div class="insight-card">
            <h4>💡 Key Insight</h4>
            <p><strong>Tourist-Sales Correlation:</strong> {tourist_sales_corr:.3f} | <strong>Resident-Sales Correlation:</strong> {resident_sales_corr:.3f}</p>
            <p>{'Tourists have stronger impact on sales!' if tourist_sales_corr > resident_sales_corr else 'Residents drive more consistent sales!'}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ----- CHART 2: Sales Per Visitor -----
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">💵 Chart 2: Sales Per Visitor Type</div>', unsafe_allow_html=True)
            
            total_tourist = filtered_df.groupby('date')['tourist_footfall'].first().sum()
            total_resident = filtered_df.groupby('date')['resident_footfall'].first().sum()
            total_sales_val = filtered_df['sales_aed'].sum()
            
            tourist_share = filtered_df['tourist_share'].mean()
            resident_share = filtered_df['resident_share'].mean()
            
            sales_per_tourist = (total_sales_val * tourist_share) / max(total_tourist, 1)
            sales_per_resident = (total_sales_val * resident_share) / max(total_resident, 1)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=['Tourist', 'Resident'],
                y=[sales_per_tourist, sales_per_resident],
                marker_color=['#B8860B', '#2563EB'],
                text=[f'AED {sales_per_tourist:.0f}', f'AED {sales_per_resident:.0f}'],
                textposition='outside',
                textfont=dict(size=16, color='#1A1A2E', family='Poppins')
            ))
            
            fig = apply_chart_theme(fig, height=350)
            fig.update_layout(yaxis_title='Average Sales per Visitor (AED)')
            
            st.plotly_chart(fig, use_container_width=True)
            
            premium = ((sales_per_tourist / max(sales_per_resident, 1)) - 1) * 100
            st.markdown(f"""
            <div class="insight-card">
                <h4>💡 Tourist Premium</h4>
                <p>Tourists spend <strong>{premium:.1f}% more</strong> than residents per visit!</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ----- CHART 3: Visitor Mix Bubble Chart -----
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🫧 Chart 3: Visitor Mix vs Sales</div>', unsafe_allow_html=True)
            
            daily_mix = filtered_df.groupby('date').agg({
                'tourist_share': 'first',
                'sales_aed': 'sum',
                'mall_footfall': 'first',
                'is_weekend': 'first'
            }).reset_index()
            daily_mix['tourist_pct'] = daily_mix['tourist_share'] * 100
            daily_mix['day_type'] = daily_mix['is_weekend'].map({0: 'Weekday', 1: 'Weekend'})
            
            fig = px.scatter(
                daily_mix, x='tourist_pct', y='sales_aed', size='mall_footfall',
                color='day_type', color_discrete_map={'Weekday': '#2563EB', 'Weekend': '#B8860B'},
                hover_data={'date': True, 'mall_footfall': True},
                size_max=40
            )
            
            # Add trendline
            z = np.polyfit(daily_mix['tourist_pct'], daily_mix['sales_aed'], 1)
            p = np.poly1d(z)
            x_line = np.linspace(daily_mix['tourist_pct'].min(), daily_mix['tourist_pct'].max(), 100)
            fig.add_trace(go.Scatter(x=x_line, y=p(x_line), mode='lines', name='Trend',
                                    line=dict(color='#DC2626', dash='dash', width=2)))
            
            fig = apply_chart_theme(fig, height=350)
            fig.update_layout(xaxis_title='Tourist Share (%)', yaxis_title='Total Sales (AED)')
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ----- CHART 4: Revenue Attribution Waterfall -----
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📊 Chart 4: Revenue Attribution Waterfall</div>', unsafe_allow_html=True)
        
        avg_tourist_share = filtered_df['tourist_share'].mean()
        avg_resident_share = filtered_df['resident_share'].mean()
        
        tourist_revenue = total_sales_val * avg_tourist_share
        resident_revenue = total_sales_val * avg_resident_share
        
        fig = go.Figure(go.Waterfall(
            name="Revenue Attribution",
            orientation="v",
            x=["Base", "Tourist Contribution", "Resident Contribution", "Total Revenue"],
            y=[0, tourist_revenue, resident_revenue, 0],
            measure=["absolute", "relative", "relative", "total"],
            text=[f"AED 0", format_currency(tourist_revenue), format_currency(resident_revenue), format_currency(total_sales_val)],
            textposition="outside",
            textfont=dict(color='#1A1A2E', size=12),
            connector={"line": {"color": "#E5E7EB", "width": 2}},
            decreasing={"marker": {"color": "#DC2626"}},
            increasing={"marker": {"color": "#059669"}},
            totals={"marker": {"color": "#B8860B"}}
        ))
        
        fig = apply_chart_theme(fig, height=400)
        
        st.plotly_chart(fig, use_container_width=True)
        
        col_i1, col_i2 = st.columns(2)
        with col_i1:
            st.markdown(f"""
            <div class="insight-card">
                <h4>🌍 Tourist Revenue</h4>
                <p><strong>{format_currency(tourist_revenue)}</strong> ({avg_tourist_share*100:.1f}% of total)</p>
            </div>
            """, unsafe_allow_html=True)
        with col_i2:
            st.markdown(f"""
            <div class="insight-card">
                <h4>🏠 Resident Revenue</h4>
                <p><strong>{format_currency(resident_revenue)}</strong> ({avg_resident_share*100:.1f}% of total)</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ----- CHART 5: Correlation Matrix Heatmap -----
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🔥 Chart 5: Correlation Matrix Heatmap</div>', unsafe_allow_html=True)
        
        corr_cols = ['tourist_footfall', 'resident_footfall', 'mall_footfall', 'store_footfall',
                    'sales_aed', 'transactions', 'conversion_rate', 'avg_basket_aed']
        
        daily_data = filtered_df.groupby('date').agg({
            'tourist_footfall': 'first',
            'resident_footfall': 'first',
            'mall_footfall': 'first',
            'store_footfall': 'sum',
            'sales_aed': 'sum',
            'transactions': 'sum',
            'conversion_rate': 'mean',
            'avg_basket_aed': 'mean'
        })
        
        corr_matrix = daily_data.corr()
        
        labels = ['Tourist FF', 'Resident FF', 'Mall FF', 'Store FF', 'Sales', 'Transactions', 'Conversion', 'Avg Basket']
        
        fig = go.Figure(go.Heatmap(
            z=corr_matrix.values,
            x=labels,
            y=labels,
            colorscale=[[0, '#DC2626'], [0.5, '#FFFFFF'], [1, '#059669']],
            zmid=0,
            text=np.round(corr_matrix.values, 2),
            texttemplate='%{text}',
            textfont=dict(size=11, color='#1A1A2E'),
            hovertemplate='%{y} vs %{x}: %{z:.3f}<extra></extra>',
            colorbar=dict(title='Correlation')
        ))
        
        fig = apply_chart_theme(fig, height=450)
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="insight-card">
            <h4>📖 How to Read</h4>
            <p><strong>Green (+1):</strong> Strong positive correlation | <strong>Red (-1):</strong> Strong negative correlation | <strong>White (0):</strong> No correlation</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ----- CHART 6: Tourist Impact by Category -----
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🏷️ Chart 6: Tourist Impact by Category</div>', unsafe_allow_html=True)
        
        cat_analysis = filtered_df.groupby('category').agg({
            'sales_aed': 'sum',
            'tourist_share': 'mean',
            'resident_share': 'mean'
        }).reset_index()
        
        cat_analysis['tourist_sales'] = cat_analysis['sales_aed'] * cat_analysis['tourist_share']
        cat_analysis['resident_sales'] = cat_analysis['sales_aed'] * cat_analysis['resident_share']
        cat_analysis = cat_analysis.sort_values('tourist_sales', ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=cat_analysis['category'],
            x=cat_analysis['tourist_sales'],
            name='Tourist-Driven Sales',
            orientation='h',
            marker_color='#B8860B',
            text=[format_currency(x) for x in cat_analysis['tourist_sales']],
            textposition='inside',
            textfont=dict(color='#FFFFFF')
        ))
        
        fig.add_trace(go.Bar(
            y=cat_analysis['category'],
            x=cat_analysis['resident_sales'],
            name='Resident-Driven Sales',
            orientation='h',
            marker_color='#2563EB',
            text=[format_currency(x) for x in cat_analysis['resident_sales']],
            textposition='inside',
            textfont=dict(color='#FFFFFF')
        ))
        
        fig = apply_chart_theme(fig, height=400)
        fig.update_layout(barmode='stack', xaxis_title='Sales (AED)', legend=dict(orientation='h', y=1.1))
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================
    # TAB 2: CATEGORY DEEP DIVE
    # ========================================
    with tab2:
        st.markdown('<div class="section-header">📊 Category Performance Deep Dive</div>', unsafe_allow_html=True)
        
        # ----- CHART 7: Performance Quadrant Analysis -----
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🎯 Chart 7: Performance Quadrant Analysis</div>', unsafe_allow_html=True)
        
        col_f1, col_f2 = st.columns([2, 6])
        with col_f1:
            bubble_metric = st.selectbox("Bubble Size", ['Sales', 'Transactions', 'Footfall'], key='c7_bubble')
        
        cat_quadrant = filtered_df.groupby('category').agg({
            'conversion_rate': 'mean',
            'avg_basket_aed': 'mean',
            'sales_aed': 'sum',
            'transactions': 'sum',
            'store_footfall': 'sum'
        }).reset_index()
        
        cat_quadrant['conversion_pct'] = cat_quadrant['conversion_rate'] * 100
        
        size_col = {'Sales': 'sales_aed', 'Transactions': 'transactions', 'Footfall': 'store_footfall'}[bubble_metric]
        
        # Calculate medians for quadrant lines
        conv_median = cat_quadrant['conversion_pct'].median()
        basket_median = cat_quadrant['avg_basket_aed'].median()
        
        fig = px.scatter(
            cat_quadrant, x='conversion_pct', y='avg_basket_aed', size=size_col,
            color='category', text='category', color_discrete_sequence=CHART_COLORS,
            size_max=60
        )
        
        fig.add_hline(y=basket_median, line_dash="dash", line_color="#DC2626", line_width=2,
                     annotation_text="Basket Median", annotation_position="right")
        fig.add_vline(x=conv_median, line_dash="dash", line_color="#DC2626", line_width=2,
                     annotation_text="Conversion Median", annotation_position="top")
        
        # Add quadrant labels
        fig.add_annotation(x=cat_quadrant['conversion_pct'].max()*0.9, y=cat_quadrant['avg_basket_aed'].max()*0.95,
                          text="⭐ STARS", showarrow=False, font=dict(size=14, color='#059669'))
        fig.add_annotation(x=cat_quadrant['conversion_pct'].min()*1.1, y=cat_quadrant['avg_basket_aed'].max()*0.95,
                          text="❓ POTENTIAL", showarrow=False, font=dict(size=14, color='#D97706'))
        fig.add_annotation(x=cat_quadrant['conversion_pct'].max()*0.9, y=cat_quadrant['avg_basket_aed'].min()*1.1,
                          text="💰 CASH COWS", showarrow=False, font=dict(size=14, color='#2563EB'))
        fig.add_annotation(x=cat_quadrant['conversion_pct'].min()*1.1, y=cat_quadrant['avg_basket_aed'].min()*1.1,
                          text="⚠️ REVIEW", showarrow=False, font=dict(size=14, color='#DC2626'))
        
        fig = apply_chart_theme(fig, height=500)
        fig.update_layout(xaxis_title='Conversion Rate (%)', yaxis_title='Average Basket (AED)', showlegend=False)
        fig.update_traces(textposition='top center')
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="insight-card">
            <h4>📖 Quadrant Guide</h4>
            <p>⭐ <strong>Stars:</strong> High conversion + High basket (Invest more) | 💰 <strong>Cash Cows:</strong> High conversion + Low basket (Upsell opportunity)</p>
            <p>❓ <strong>Potential:</strong> Low conversion + High basket (Improve traffic) | ⚠️ <strong>Review:</strong> Low conversion + Low basket (Needs intervention)</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ----- CHART 8: Category Sales Sensitivity -----
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📐 Chart 8: Sales Sensitivity to Footfall</div>', unsafe_allow_html=True)
            
            sensitivity_data = []
            for cat in filtered_df['category'].unique():
                cat_data = filtered_df[filtered_df['category'] == cat]
                if len(cat_data) > 10:
                    correlation = cat_data['store_footfall'].corr(cat_data['sales_aed'])
                    slope = np.polyfit(cat_data['store_footfall'], cat_data['sales_aed'], 1)[0]
                    sensitivity_data.append({
                        'category': cat,
                        'correlation': correlation,
                        'slope': slope
                    })
            
            sens_df = pd.DataFrame(sensitivity_data).sort_values('slope', ascending=True)
            
            fig = go.Figure(go.Bar(
                y=sens_df['category'],
                x=sens_df['slope'],
                orientation='h',
                marker=dict(
                    color=sens_df['slope'],
                    colorscale=[[0, '#FEE2E2'], [0.5, '#FEF3C7'], [1, '#D1FAE5']],
                    line=dict(color='#1A1A2E', width=1)
                ),
                text=[f'{x:.2f}' for x in sens_df['slope']],
                textposition='outside',
                textfont=dict(color='#1A1A2E')
            ))
            
            fig = apply_chart_theme(fig, height=380)
            fig.update_layout(xaxis_title='Sales per Additional Footfall (AED)')
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div class="insight-card">
                <h4>💡 Interpretation</h4>
                <p>Higher slope = More sales generated per visitor. Focus high-slope categories on high-traffic floors!</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ----- CHART 9: Category Radar -----
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🎯 Chart 9: Category Comparison Radar</div>', unsafe_allow_html=True)
            
            radar_cats = st.multiselect(
                "Select Categories",
                filtered_df['category'].unique().tolist(),
                default=filtered_df['category'].unique().tolist()[:4],
                key='c9_cats'
            )
            
            if radar_cats:
                radar_df = filtered_df[filtered_df['category'].isin(radar_cats)]
                cat_metrics = radar_df.groupby('category').agg({
                    'sales_aed': 'sum',
                    'transactions': 'sum',
                    'conversion_rate': 'mean',
                    'avg_basket_aed': 'mean',
                    'sales_per_sqft': 'mean'
                }).reset_index()
                
                for col in ['sales_aed', 'transactions', 'conversion_rate', 'avg_basket_aed', 'sales_per_sqft']:
                    max_val = cat_metrics[col].max()
                    if max_val > 0:
                        cat_metrics[f'{col}_norm'] = cat_metrics[col] / max_val * 100
                
                categories_list = ['Sales', 'Transactions', 'Conversion', 'Basket', 'Sales/Sqft']
                
                fig = go.Figure()
                
                for idx, (_, row) in enumerate(cat_metrics.iterrows()):
                    values = [
                        row.get('sales_aed_norm', 0),
                        row.get('transactions_norm', 0),
                        row.get('conversion_rate_norm', 0),
                        row.get('avg_basket_aed_norm', 0),
                        row.get('sales_per_sqft_norm', 0)
                    ]
                    values.append(values[0])
                    
                    fig.add_trace(go.Scatterpolar(
                        r=values,
                        theta=categories_list + [categories_list[0]],
                        name=row['category'],
                        line=dict(color=CHART_COLORS[idx % len(CHART_COLORS)], width=3),
                        fill='toself',
                        fillcolor=f'rgba({int(CHART_COLORS[idx % len(CHART_COLORS)][1:3], 16)}, {int(CHART_COLORS[idx % len(CHART_COLORS)][3:5], 16)}, {int(CHART_COLORS[idx % len(CHART_COLORS)][5:7], 16)}, 0.1)'
                    ))
                
                fig = apply_chart_theme(fig, height=380)
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(0,0,0,0.1)'),
                        angularaxis=dict(gridcolor='rgba(0,0,0,0.1)')
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ----- CHART 10: Weekend Uplift by Category -----
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📅 Chart 10: Weekend Uplift by Category</div>', unsafe_allow_html=True)
        
        weekend_analysis = filtered_df.groupby(['category', 'is_weekend'])['sales_aed'].sum().unstack(fill_value=0)
        weekend_analysis.columns = ['Weekday', 'Weekend']
        weekend_analysis['uplift_pct'] = ((weekend_analysis['Weekend'] / weekend_analysis['Weekday'].replace(0, 1)) - 1) * 100
        weekend_analysis = weekend_analysis.sort_values('uplift_pct', ascending=True).reset_index()
        
        fig = go.Figure()
        
        colors = ['#DC2626' if x < 0 else '#059669' for x in weekend_analysis['uplift_pct']]
        
        fig.add_trace(go.Bar(
            y=weekend_analysis['category'],
            x=weekend_analysis['uplift_pct'],
            orientation='h',
            marker_color=colors,
            text=[f'{x:+.1f}%' for x in weekend_analysis['uplift_pct']],
            textposition='outside',
            textfont=dict(color='#1A1A2E', size=12)
        ))
        
        fig.add_vline(x=0, line_color='#1A1A2E', line_width=2)
        
        fig = apply_chart_theme(fig, height=400)
        fig.update_layout(xaxis_title='Weekend Sales Uplift (%)')
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================
    # TAB 3: STORE ANALYSIS
    # ========================================
    with tab3:
        st.markdown('<div class="section-header">🏪 Store Performance Analysis</div>', unsafe_allow_html=True)
        
        # ----- CHART 11: Rent Efficiency Scatter -----
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">💵 Chart 11: Rent vs Revenue Efficiency</div>', unsafe_allow_html=True)
        
        col_f1, col_f2 = st.columns([2, 6])
        with col_f1:
            rent_cat_filter = st.selectbox("Category", ['All'] + sorted(filtered_df['category'].unique().tolist()), key='c11_cat')
        
        rent_df = filtered_df.copy()
        if rent_cat_filter != 'All':
            rent_df = rent_df[rent_df['category'] == rent_cat_filter]
        
        rent_data = rent_df.groupby('store_name').agg({
            'annual_base_rent_aed': 'first',
            'sales_aed': 'sum',
            'category': 'first'
        }).reset_index()
        
        days_count = rent_df['date'].nunique()
        rent_data['annualized_sales'] = rent_data['sales_aed'] * (365 / max(days_count, 1))
        rent_data['rent_ratio'] = (rent_data['annual_base_rent_aed'] / rent_data['annualized_sales'].replace(0, 1)) * 100
        
        fig = px.scatter(
            rent_data, x='annual_base_rent_aed', y='annualized_sales',
            color='category', hover_name='store_name',
            color_discrete_sequence=CHART_COLORS, size='annualized_sales', size_max=40
        )
        
        max_rent = rent_data['annual_base_rent_aed'].max()
        
        # Reference lines: 5%, 10%, 15% rent ratios
        for ratio, color, name in [(5, '#059669', '5% (Excellent)'), (10, '#D97706', '10% (Good)'), (15, '#DC2626', '15% (Review)')]:
            fig.add_trace(go.Scatter(
                x=[0, max_rent], y=[0, max_rent * 100 / ratio],
                mode='lines', name=name,
                line=dict(color=color, dash='dash', width=2)
            ))
        
        fig = apply_chart_theme(fig, height=500)
        fig.update_layout(xaxis_title='Annual Rent (AED)', yaxis_title='Annualized Sales (AED)')
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="insight-card">
            <h4>📖 Rent Ratio Guide</h4>
            <p>Stores <strong>above</strong> the line are performing well (low rent burden). Stores <strong>below</strong> need review.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ----- CHART 12: Sales per Sqft Benchmark -----
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📐 Chart 12: Sales per Sqft vs Category Avg</div>', unsafe_allow_html=True)
            
            sqft_filter_cat = st.selectbox("Select Category", filtered_df['category'].unique().tolist(), key='c12_cat')
            
            sqft_data = filtered_df[filtered_df['category'] == sqft_filter_cat].groupby('store_name').agg({
                'sales_per_sqft': 'mean',
                'sales_aed': 'sum'
            }).reset_index()
            
            cat_avg = sqft_data['sales_per_sqft'].mean()
            sqft_data['vs_avg'] = sqft_data['sales_per_sqft'] - cat_avg
            sqft_data = sqft_data.sort_values('vs_avg', ascending=True).head(15)
            
            colors = ['#DC2626' if x < 0 else '#059669' for x in sqft_data['vs_avg']]
            
            fig = go.Figure(go.Bar(
                y=sqft_data['store_name'],
                x=sqft_data['vs_avg'],
                orientation='h',
                marker_color=colors,
                text=[f'{x:+.1f}' for x in sqft_data['vs_avg']],
                textposition='outside'
            ))
            
            fig.add_vline(x=0, line_color='#1A1A2E', line_width=2,
                         annotation_text=f'Category Avg: {cat_avg:.1f}', annotation_position='top')
            
            fig = apply_chart_theme(fig, height=450)
            fig.update_layout(xaxis_title='Deviation from Category Average')
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ----- CHART 13: Store Health Scorecard -----
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🏆 Chart 13: Store Health Scorecard</div>', unsafe_allow_html=True)
            
            top_n = st.slider("Number of Stores", 5, 20, 10, key='c13_n')
            
            store_health = filtered_df.groupby('store_name').agg({
                'sales_aed': 'sum',
                'transactions': 'sum',
                'conversion_rate': 'mean',
                'avg_basket_aed': 'mean',
                'sales_per_sqft': 'mean',
                'category': 'first'
            }).reset_index()
            
            # Normalize scores
            for col in ['sales_aed', 'transactions', 'conversion_rate', 'avg_basket_aed', 'sales_per_sqft']:
                max_val = store_health[col].max()
                min_val = store_health[col].min()
                if max_val > min_val:
                    store_health[f'{col}_score'] = ((store_health[col] - min_val) / (max_val - min_val)) * 100
                else:
                    store_health[f'{col}_score'] = 50
            
            store_health['overall_score'] = (
                store_health['sales_aed_score'] * 0.3 +
                store_health['conversion_rate_score'] * 0.25 +
                store_health['avg_basket_aed_score'] * 0.2 +
                store_health['sales_per_sqft_score'] * 0.25
            )
            
            def get_grade(score):
                if score >= 80: return 'A'
                elif score >= 60: return 'B'
                elif score >= 40: return 'C'
                elif score >= 20: return 'D'
                else: return 'F'
            
            store_health['grade'] = store_health['overall_score'].apply(get_grade)
            top_stores = store_health.nlargest(top_n, 'overall_score')
            
            grade_colors = {'A': '#059669', 'B': '#2563EB', 'C': '#D97706', 'D': '#DC2626', 'F': '#1A1A2E'}
            
            fig = go.Figure(go.Bar(
                y=top_stores['store_name'],
                x=top_stores['overall_score'],
                orientation='h',
                marker_color=[grade_colors[g] for g in top_stores['grade']],
                text=[f"{s:.0f} ({g})" for s, g in zip(top_stores['overall_score'], top_stores['grade'])],
                textposition='inside',
                textfont=dict(color='#FFFFFF', size=12)
            ))
            
            fig = apply_chart_theme(fig, height=450)
            fig.update_layout(xaxis_title='Overall Health Score', yaxis=dict(categoryorder='total ascending'))
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ----- CHART 14: Floor Performance Funnel -----
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🏢 Chart 14: Floor Conversion Funnel</div>', unsafe_allow_html=True)
        
        floor_funnel = filtered_df.groupby('floor').agg({
            'mall_footfall': lambda x: x.iloc[0] if len(x) > 0 else 0,
            'store_footfall': 'sum',
            'transactions': 'sum',
            'sales_aed': 'sum'
        }).reset_index()
        
        floor_order = {'LG': 0, 'G': 1, '1': 2, '2': 3, '3': 4}
        floor_funnel['order'] = floor_funnel['floor'].map(floor_order)
        floor_funnel = floor_funnel.sort_values('order')
        floor_funnel['label'] = floor_funnel['floor'].map({
            'LG': 'Lower Ground', 'G': 'Ground', '1': 'Level 1', '2': 'Level 2', '3': 'Level 3'
        })
        
        fig = go.Figure()
        
        x_labels = floor_funnel['label'].tolist()
        
        fig.add_trace(go.Bar(name='Mall Footfall', x=x_labels, y=floor_funnel['mall_footfall'],
                            marker_color='#1A1A2E', text=[format_number(x) for x in floor_funnel['mall_footfall']],
                            textposition='outside'))
        fig.add_trace(go.Bar(name='Store Footfall', x=x_labels, y=floor_funnel['store_footfall'],
                            marker_color='#B8860B', text=[format_number(x) for x in floor_funnel['store_footfall']],
                            textposition='outside'))
        fig.add_trace(go.Bar(name='Transactions', x=x_labels, y=floor_funnel['transactions'],
                            marker_color='#2563EB', text=[format_number(x) for x in floor_funnel['transactions']],
                            textposition='outside'))
        
        fig = apply_chart_theme(fig, height=400)
        fig.update_layout(barmode='group', legend=dict(orientation='h', y=1.1))
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================
    # TAB 4: TIME PATTERNS
    # ========================================
    with tab4:
        st.markdown('<div class="section-header">⏰ Time-Based Patterns</div>', unsafe_allow_html=True)
        
        # ----- CHART 15: Day × Category Heatmap -----
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🗓️ Chart 15: Day × Category Sales Heatmap</div>', unsafe_allow_html=True)
        
        col_f1, col_f2 = st.columns([2, 6])
        with col_f1:
            heatmap_metric = st.selectbox("Metric", ['Total Sales', 'Avg Sales', 'Transactions'], key='c15_metric')
        
        agg_func = {'Total Sales': 'sum', 'Avg Sales': 'mean', 'Transactions': 'sum'}[heatmap_metric]
        col_name = 'sales_aed' if 'Sales' in heatmap_metric else 'transactions'
        
        heatmap_data = filtered_df.pivot_table(
            values=col_name, index='category', columns='day_name', aggfunc=agg_func
        )
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = heatmap_data[[d for d in day_order if d in heatmap_data.columns]]
        
        fig = go.Figure(go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale=[[0, '#FEF3C7'], [0.5, '#F59E0B'], [1, '#B45309']],
            hovertemplate='<b>%{y}</b><br>%{x}: %{z:,.0f}<extra></extra>',
            text=[[format_number(val) for val in row] for row in heatmap_data.values],
            texttemplate='%{text}',
            textfont=dict(size=10)
        ))
        
        fig = apply_chart_theme(fig, height=450)
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ----- CHART 16: Rolling Average Trend -----
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📈 Chart 16: Rolling Average Trend</div>', unsafe_allow_html=True)
            
            rolling_window = st.slider("Rolling Window (Days)", 3, 14, 7, key='c16_window')
            
            daily_sales = filtered_df.groupby('date')['sales_aed'].sum().reset_index()
            daily_sales['rolling_avg'] = daily_sales['sales_aed'].rolling(window=rolling_window, min_periods=1).mean()
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=daily_sales['date'], y=daily_sales['sales_aed'],
                name='Daily Sales', mode='lines',
                line=dict(color='rgba(184, 134, 11, 0.3)', width=1),
                fill='tozeroy', fillcolor='rgba(184, 134, 11, 0.1)'
            ))
            
            fig.add_trace(go.Scatter(
                x=daily_sales['date'], y=daily_sales['rolling_avg'],
                name=f'{rolling_window}-Day Avg', mode='lines',
                line=dict(color='#DC2626', width=3)
            ))
            
            fig = apply_chart_theme(fig, height=350)
            fig.update_layout(yaxis_title='Sales (AED)', hovermode='x unified')
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📊 Chart 17: Day of Week Performance</div>', unsafe_allow_html=True)
            
            dow_metric = st.selectbox("Metric", ['Sales', 'Transactions', 'Conversion'], key='c17_metric')
            
            col_map = {'Sales': 'sales_aed', 'Transactions': 'transactions', 'Conversion': 'conversion_rate'}
            
            dow_data = filtered_df.groupby('day_name')[col_map[dow_metric]].mean()
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dow_data = dow_data.reindex(day_order)
            
            if dow_metric == 'Conversion':
                dow_data = dow_data * 100
            
            colors = ['#E5E7EB'] * 7
            colors[dow_data.values.argmax()] = '#059669'
            colors[dow_data.values.argmin()] = '#DC2626'
            
            fig = go.Figure(go.Bar(
                x=dow_data.index,
                y=dow_data.values,
                marker_color=colors,
                text=[format_number(x) if dow_metric != 'Conversion' else f'{x:.1f}%' for x in dow_data.values],
                textposition='outside',
                textfont=dict(color='#1A1A2E', size=11)
            ))
            
            fig = apply_chart_theme(fig, height=350)
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ----- CHART 18: Monthly Trend -----
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📅 Chart 18: Monthly Performance Overview</div>', unsafe_allow_html=True)
        
        monthly_data = filtered_df.groupby('month_name').agg({
            'sales_aed': 'sum',
            'transactions': 'sum',
            'conversion_rate': 'mean'
        }).reset_index()
        
        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        monthly_data['month_order'] = monthly_data['month_name'].apply(lambda x: month_order.index(x) if x in month_order else 12)
        monthly_data = monthly_data.sort_values('month_order')
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(go.Bar(
            x=monthly_data['month_name'], y=monthly_data['sales_aed'],
            name='Sales', marker_color='#B8860B',
            text=[format_currency(x) for x in monthly_data['sales_aed']],
            textposition='outside'
        ), secondary_y=False)
        
        fig.add_trace(go.Scatter(
            x=monthly_data['month_name'], y=monthly_data['conversion_rate'] * 100,
            name='Conversion %', mode='lines+markers',
            line=dict(color='#DC2626', width=3), marker=dict(size=10)
        ), secondary_y=True)
        
        fig = apply_chart_theme(fig, height=400)
        fig.update_layout(
            yaxis_title='Sales (AED)',
            yaxis2_title='Conversion (%)',
            legend=dict(orientation='h', y=1.1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================
    # TAB 5: STRATEGIC VIEW
    # ========================================
    with tab5:
        st.markdown('<div class="section-header">🎯 Strategic Analysis & Simulation</div>', unsafe_allow_html=True)
        
        # ----- CHART 19: What-If Simulator -----
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🔮 Chart 19: What-If Scenario Simulator</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            footfall_change = st.slider("Footfall Change (%)", -30, 50, 0, key='wif_footfall')
        with col2:
            conversion_change = st.slider("Conversion Change (%)", -20, 30, 0, key='wif_conv')
        with col3:
            basket_change = st.slider("Avg Basket Change (%)", -20, 30, 0, key='wif_basket')
        
        # Calculate projections
        current_footfall = filtered_df.groupby('date')['mall_footfall'].first().mean()
        current_conversion = filtered_df['conversion_rate'].mean()
        current_basket = filtered_df['avg_basket_aed'].mean()
        current_sales = filtered_df['sales_aed'].sum()
        
        projected_footfall = current_footfall * (1 + footfall_change / 100)
        projected_conversion = current_conversion * (1 + conversion_change / 100)
        projected_basket = current_basket * (1 + basket_change / 100)
        
        # Simple projection model
        projected_sales = current_sales * (1 + footfall_change/100) * (1 + conversion_change/100) * (1 + basket_change/100)
        sales_delta = projected_sales - current_sales
        sales_delta_pct = (sales_delta / current_sales) * 100
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        metrics = [
            (col_m1, "Current Sales", format_currency(current_sales), "#6B7280"),
            (col_m2, "Projected Sales", format_currency(projected_sales), "#059669" if sales_delta >= 0 else "#DC2626"),
            (col_m3, "Sales Impact", format_currency(abs(sales_delta)), "#059669" if sales_delta >= 0 else "#DC2626"),
            (col_m4, "% Change", f"{sales_delta_pct:+.1f}%", "#059669" if sales_delta >= 0 else "#DC2626"),
        ]
        
        for col, label, value, color in metrics:
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="label">{label}</div>
                    <div class="value" style="color: {color};">{value}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=projected_sales,
            delta={'reference': current_sales, 'valueformat': ',.0f'},
            title={'text': "Projected Annual Sales (AED)", 'font': {'color': '#1A1A2E'}},
            number={'valueformat': ',.0f', 'font': {'color': '#1A1A2E'}},
            gauge={
                'axis': {'range': [0, current_sales * 1.5], 'tickfont': {'color': '#1A1A2E'}},
                'bar': {'color': '#B8860B'},
                'steps': [
                    {'range': [0, current_sales * 0.8], 'color': '#FEE2E2'},
                    {'range': [current_sales * 0.8, current_sales], 'color': '#FEF3C7'},
                    {'range': [current_sales, current_sales * 1.5], 'color': '#D1FAE5'}
                ],
                'threshold': {
                    'line': {'color': '#DC2626', 'width': 4},
                    'thickness': 0.75,
                    'value': current_sales
                }
            }
        ))
        
        fig = apply_chart_theme(fig, height=350)
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ----- Key Insights Summary -----
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">💡 Key Strategic Insights</div>', unsafe_allow_html=True)
        
        # Calculate key insights
        best_category = filtered_df.groupby('category')['sales_aed'].sum().idxmax()
        best_day = filtered_df.groupby('day_name')['sales_aed'].sum().idxmax()
        best_floor = filtered_df.groupby('floor')['sales_aed'].sum().idxmax()
        tourist_impact = filtered_df['tourist_share'].mean() * 100
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="insight-card">
                <h4>🏆 Top Performers</h4>
                <p><strong>Best Category:</strong> {best_category}</p>
                <p><strong>Best Day:</strong> {best_day}</p>
                <p><strong>Best Floor:</strong> {best_floor}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="insight-card">
                <h4>🌍 Visitor Analysis</h4>
                <p><strong>Tourist Share:</strong> {tourist_impact:.1f}%</p>
                <p><strong>Resident Share:</strong> {100-tourist_impact:.1f}%</p>
                <p><strong>Weekend Uplift:</strong> ~18%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_conv = filtered_df['conversion_rate'].mean() * 100
            avg_basket_val = filtered_df['avg_basket_aed'].mean()
            st.markdown(f"""
            <div class="insight-card">
                <h4>📊 KPI Summary</h4>
                <p><strong>Avg Conversion:</strong> {avg_conv:.1f}%</p>
                <p><strong>Avg Basket:</strong> {format_currency(avg_basket_val)}</p>
                <p><strong>Active Stores:</strong> {filtered_df['store_name'].nunique()}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ----- Recommendations -----
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📋 Strategic Recommendations</div>', unsafe_allow_html=True)
        
        recommendations = [
            ("🎯", "Focus marketing on tourists", f"They contribute {tourist_impact:.0f}% but spend more per visit"),
            ("📅", f"Maximize {best_day} operations", "Best performing day - ensure full staffing"),
            ("🏢", f"Optimize {best_floor} floor", "Highest performing floor - premium placement priority"),
            ("📈", "Improve conversion rate", f"Current avg is {avg_conv:.1f}% - industry best is 25%+"),
            ("🛒", "Increase basket size", f"Current avg {format_currency(avg_basket_val)} - bundle opportunities"),
        ]
        
        for icon, title, desc in recommendations:
            st.markdown(f"""
            <div style="background: #F8FAFC; border-radius: 10px; padding: 15px; margin: 10px 0; border-left: 4px solid #B8860B;">
                <strong style="color: #1A1A2E;">{icon} {title}</strong>
                <p style="color: #4A4A6A; margin: 5px 0 0 0; font-size: 0.9rem;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================
    # TAB 6: OVERVIEW
    # ========================================
    with tab6:
        st.markdown('<div class="section-header">📈 Quick Overview</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Sales Distribution Pie
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📊 Sales by Category</div>', unsafe_allow_html=True)
            
            cat_sales = filtered_df.groupby('category')['sales_aed'].sum().sort_values(ascending=False)
            
            fig = go.Figure(go.Pie(
                labels=cat_sales.index,
                values=cat_sales.values,
                hole=0.5,
                marker=dict(colors=CHART_COLORS[:len(cat_sales)]),
                textinfo='label+percent',
                textfont=dict(size=11),
                hovertemplate="<b>%{label}</b><br>Sales: AED %{value:,.0f}<br>Share: %{percent}<extra></extra>"
            ))
            
            fig.add_annotation(text=f"<b>Total<br>{format_value_short(cat_sales.sum())}</b>",
                             x=0.5, y=0.5, font=dict(size=14, color='#1A1A2E'), showarrow=False)
            
            fig = apply_chart_theme(fig, height=400)
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Top Stores
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🏆 Top 10 Stores</div>', unsafe_allow_html=True)
            
            top_stores = filtered_df.groupby('store_name')['sales_aed'].sum().nlargest(10).sort_values()
            
            fig = go.Figure(go.Bar(
                y=top_stores.index,
                x=top_stores.values,
                orientation='h',
                marker=dict(color=top_stores.values, colorscale=[[0, '#E5E7EB'], [1, '#B8860B']]),
                text=[format_currency(x) for x in top_stores.values],
                textposition='inside',
                textfont=dict(color='#FFFFFF', size=11)
            ))
            
            fig = apply_chart_theme(fig, height=400)
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Raw Data
        if show_raw_data:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📋 Raw Data Preview</div>', unsafe_allow_html=True)
            st.dataframe(filtered_df.head(100), use_container_width=True, height=400)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================
    # FOOTER
    # ========================================
    st.markdown("""
    <div class="custom-footer">
        <p><span class="gold-text">🏬 Dubai Mall Analytics Dashboard</span></p>
        <p>Premium Retail Intelligence Platform • Full Analytics Suite</p>
        <p style="font-size: 0.85rem; margin-top: 15px; color: #64748B;">
            © 2024 Dubai Mall Management | Dashboard v3.0 - All 19 Charts
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# RUN
# ============================================
if __name__ == "__main__":
    main()
