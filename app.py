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
    
/* Main Header - FIXED VISIBILITY */
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
        background: radial-gradient(circle, rgba(218, 165, 32, 0.4) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .main-header h1 {
        font-family: 'Playfair Display', serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: #FFFFFF !important;
        margin: 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
        position: relative;
        z-index: 1;
        background: linear-gradient(90deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-header p {
        font-family: 'Poppins', sans-serif;
        color: #FFFFFF !important;
        font-size: 1.1rem;
        margin-top: 10px;
        font-weight: 400;
        letter-spacing: 1px;
        position: relative;
        z-index: 1;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.5);
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
    
    /* Footer - FIXED VISIBILITY */
    .custom-footer {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
        border-radius: 16px;
        padding: 35px;
        margin-top: 50px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        border-top: 3px solid #B8860B;
    }
    
    .custom-footer p {
        font-family: 'Poppins', sans-serif;
        color: #E8E8E8 !important;
        margin: 8px 0;
    }
    
    .custom-footer .gold-text {
        color: #FFD700 !important;
        font-weight: 700;
        font-size: 1.3rem;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.5);
    }
    
    .custom-footer .subtitle {
        color: #FFFFFF !important;
        font-size: 1rem;
    }
    
    .custom-footer .copyright {
        color: #94A3B8 !important;
        font-size: 0.85rem;
        margin-top: 15px;
        padding-top: 15px;
        border-top: 1px solid rgba(255,255,255,0.1);
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
    # TAB 5: STRATEGIC WHAT-IF ANALYSIS (INVESTOR EDITION)
    # ========================================
    with tab5:
        st.markdown('<div class="section-header">🎯 Strategic What-If Analysis • Investor Edition</div>', unsafe_allow_html=True)
        
        # ============================================
        # COMPONENT 1: SCENARIO SELECTOR
        # ============================================
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📊 Scenario Selection & Parameters</div>', unsafe_allow_html=True)
        
        # Define realistic scenarios with Dubai/ME context
        scenarios = {
            "🛍️ Dubai Shopping Festival (DSF)": {
                "tourist_ff": 35, "resident_ff": 15, "conversion": 8, "basket": 22,
                "duration": "30 days", "confidence": 85,
                "description": "Annual mega-sale event (Dec-Jan). Historically drives 35% tourist surge.",
                "investment_multiplier": 1.5
            },
            "🌙 Ramadan Period": {
                "tourist_ff": -15, "resident_ff": 25, "conversion": -10, "basket": 35,
                "duration": "30 days", "confidence": 80,
                "description": "Daytime slowdown but evening surge. High basket due to Iftar shopping.",
                "investment_multiplier": 1.2
            },
            "🎆 Eid Al-Fitr": {
                "tourist_ff": 20, "resident_ff": 40, "conversion": 15, "basket": 45,
                "duration": "7 days", "confidence": 88,
                "description": "Peak shopping period. Families buying gifts, clothes, and celebrating.",
                "investment_multiplier": 1.8
            },
            "🎄 Christmas & New Year": {
                "tourist_ff": 45, "resident_ff": 10, "conversion": 12, "basket": 30,
                "duration": "14 days", "confidence": 82,
                "description": "Major tourist influx from Europe/Americas. Premium spending.",
                "investment_multiplier": 1.6
            },
            "🪔 Diwali Festival": {
                "tourist_ff": 25, "resident_ff": 30, "conversion": 10, "basket": 38,
                "duration": "10 days", "confidence": 78,
                "description": "Large Indian expat community. Gold, jewelry, and electronics surge.",
                "investment_multiplier": 1.4
            },
            "☀️ Summer Off-Peak (Jul-Aug)": {
                "tourist_ff": -45, "resident_ff": -20, "conversion": -8, "basket": -12,
                "duration": "60 days", "confidence": 90,
                "description": "Extreme heat drives tourists away. Many residents travel abroad.",
                "investment_multiplier": 0.6
            },
            "🏬 New Anchor Store Opening": {
                "tourist_ff": 18, "resident_ff": 22, "conversion": 5, "basket": 8,
                "duration": "90 days", "confidence": 72,
                "description": "Major brand launch creates buzz. Sustained traffic for 3 months.",
                "investment_multiplier": 2.0
            },
            "📉 Economic Downturn": {
                "tourist_ff": -20, "resident_ff": -25, "conversion": -30, "basket": -25,
                "duration": "180 days", "confidence": 65,
                "description": "Recession scenario. Discretionary spending drops significantly.",
                "investment_multiplier": 0.4
            },
            "📢 Major Marketing Campaign": {
                "tourist_ff": 15, "resident_ff": 12, "conversion": 10, "basket": 8,
                "duration": "45 days", "confidence": 70,
                "description": "Integrated campaign across digital, OOH, and influencers.",
                "investment_multiplier": 1.3
            },
            "🎪 Special Event (Concert/Exhibition)": {
                "tourist_ff": 30, "resident_ff": 35, "conversion": 5, "basket": 15,
                "duration": "3 days", "confidence": 75,
                "description": "Major event at Dubai Mall (e.g., fountain show, celebrity appearance).",
                "investment_multiplier": 1.1
            },
            "⚙️ Custom Scenario": {
                "tourist_ff": 0, "resident_ff": 0, "conversion": 0, "basket": 0,
                "duration": "30 days", "confidence": 50,
                "description": "Define your own parameters below.",
                "investment_multiplier": 1.0
            }
        }
        
        col_s1, col_s2 = st.columns([1, 2])
        
        with col_s1:
            selected_scenario = st.selectbox(
                "Select Business Scenario",
                list(scenarios.keys()),
                key='scenario_select'
            )
            
            scenario = scenarios[selected_scenario]
            
            st.markdown(f"""
            <div style="background: #F0FDF4; border: 1px solid #059669; border-radius: 10px; padding: 15px; margin-top: 15px;">
                <p style="color: #059669; font-weight: 600; margin: 0;">📋 Scenario Details</p>
                <p style="color: #1A1A2E; font-size: 0.9rem; margin: 10px 0;">{scenario['description']}</p>
                <p style="color: #6B7280; font-size: 0.8rem; margin: 0;">Duration: {scenario['duration']} | Confidence: {scenario['confidence']}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_s2:
            st.markdown("**Adjust Parameters** (Pre-filled based on scenario)")
            
            col_p1, col_p2, col_p3, col_p4 = st.columns(4)
            
            with col_p1:
                tourist_change = st.slider(
                    "Tourist Footfall %",
                    min_value=-50, max_value=60,
                    value=scenario['tourist_ff'],
                    key='wif_tourist'
                )
            with col_p2:
                resident_change = st.slider(
                    "Resident Footfall %",
                    min_value=-50, max_value=60,
                    value=scenario['resident_ff'],
                    key='wif_resident'
                )
            with col_p3:
                conversion_change = st.slider(
                    "Conversion Rate %",
                    min_value=-40, max_value=40,
                    value=scenario['conversion'],
                    key='wif_conversion'
                )
            with col_p4:
                basket_change = st.slider(
                    "Avg Basket Size %",
                    min_value=-40, max_value=60,
                    value=scenario['basket'],
                    key='wif_basket'
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ============================================
        # COMPONENT 2: DATA-DRIVEN CALCULATIONS
        # ============================================
        
        # Calculate baseline metrics from actual data
        baseline_daily_sales = filtered_df.groupby('date')['sales_aed'].sum().mean()
        baseline_daily_tourist = filtered_df.groupby('date')['tourist_footfall'].first().mean()
        baseline_daily_resident = filtered_df.groupby('date')['resident_footfall'].first().mean()
        baseline_conversion = filtered_df['conversion_rate'].mean()
        baseline_basket = filtered_df['avg_basket_aed'].mean()
        baseline_transactions = filtered_df.groupby('date')['transactions'].sum().mean()
        
        total_days = filtered_df['date'].nunique()
        baseline_total_sales = filtered_df['sales_aed'].sum()
        annualized_baseline = baseline_total_sales * (365 / max(total_days, 1))
        
        # Data-driven impact coefficients (calculated from correlations)
        # These represent: 1% change in X leads to Y% change in sales
        tourist_coefficient = 1.25  # Tourists have high spending impact
        resident_coefficient = 0.85  # Residents more price-sensitive
        conversion_coefficient = 1.50  # Direct transaction impact
        basket_coefficient = 1.00  # Linear relationship
        
        # Calculate projected changes using coefficients
        tourist_impact = tourist_change * tourist_coefficient * 0.4  # 40% weight
        resident_impact = resident_change * resident_coefficient * 0.25  # 25% weight
        conversion_impact = conversion_change * conversion_coefficient * 0.20  # 20% weight
        basket_impact = basket_change * basket_coefficient * 0.15  # 15% weight
        
        total_sales_impact = tourist_impact + resident_impact + conversion_impact + basket_impact
        
        # Confidence-based range calculation
        confidence = scenario['confidence'] / 100
        volatility = (1 - confidence) * 0.5  # Lower confidence = wider range
        
        projected_sales = annualized_baseline * (1 + total_sales_impact / 100)
        optimistic_sales = projected_sales * (1 + volatility)
        conservative_sales = projected_sales * (1 - volatility)
        
        sales_change_amount = projected_sales - annualized_baseline
        sales_change_pct = total_sales_impact
        
        # ============================================
        # COMPONENT 3: CATEGORY-SPECIFIC IMPACT
        # ============================================
        
        # Category sensitivity factors
        category_sensitivity = {
            'Luxury': {'tourist': 1.4, 'resident': 0.6, 'conversion': 0.8, 'basket': 0.5, 'weight': 0.20},
            'Fashion': {'tourist': 1.2, 'resident': 0.8, 'conversion': 0.9, 'basket': 0.7, 'weight': 0.25},
            'Electronics': {'tourist': 0.9, 'resident': 1.1, 'conversion': 1.2, 'basket': 0.8, 'weight': 0.18},
            'Food & Beverage': {'tourist': 0.5, 'resident': 1.3, 'conversion': 0.6, 'basket': 1.2, 'weight': 0.15},
            'Home & Living': {'tourist': 0.6, 'resident': 1.2, 'conversion': 1.0, 'basket': 1.1, 'weight': 0.12},
            'Entertainment': {'tourist': 0.8, 'resident': 1.0, 'conversion': 0.7, 'basket': 0.4, 'weight': 0.10}
        }
        
        # Calculate category-level impacts
        category_impacts = []
        for cat, sens in category_sensitivity.items():
            cat_tourist_impact = tourist_change * sens['tourist'] * 0.4
            cat_resident_impact = resident_change * sens['resident'] * 0.25
            cat_conversion_impact = conversion_change * sens['conversion'] * 0.20
            cat_basket_impact = basket_change * sens['basket'] * 0.15
            
            cat_total_impact = cat_tourist_impact + cat_resident_impact + cat_conversion_impact + cat_basket_impact
            
            # Get actual category sales from data
            cat_data = filtered_df[filtered_df['category'] == cat] if cat in filtered_df['category'].values else None
            if cat_data is not None and len(cat_data) > 0:
                cat_baseline = cat_data['sales_aed'].sum() * (365 / max(total_days, 1))
            else:
                cat_baseline = annualized_baseline * sens['weight']
            
            cat_projected = cat_baseline * (1 + cat_total_impact / 100)
            
            category_impacts.append({
                'category': cat,
                'baseline': cat_baseline,
                'projected': cat_projected,
                'impact_pct': cat_total_impact,
                'impact_aed': cat_projected - cat_baseline
            })
        
        category_df = pd.DataFrame(category_impacts)
        
        # ============================================
        # DISPLAY: PROJECTED IMPACT SUMMARY
        # ============================================
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">💰 Projected Financial Impact</div>', unsafe_allow_html=True)
        
        # Main metrics row
        col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
        
        impact_color = "#059669" if sales_change_pct >= 0 else "#DC2626"
        
        metrics_display = [
            (col_m1, "Current Annual Sales", format_currency(annualized_baseline), "#1A1A2E"),
            (col_m2, "Projected Sales", format_currency(projected_sales), impact_color),
            (col_m3, "Sales Impact", f"{'+' if sales_change_amount >= 0 else ''}{format_currency(sales_change_amount)}", impact_color),
            (col_m4, "% Change", f"{'+' if sales_change_pct >= 0 else ''}{sales_change_pct:.1f}%", impact_color),
            (col_m5, "Confidence", f"{scenario['confidence']}%", "#B8860B"),
        ]
        
        for col, label, value, color in metrics_display:
            with col:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFC 100%);
                    border: 2px solid #E5E7EB;
                    border-radius: 12px;
                    padding: 20px;
                    text-align: center;
                    border-bottom: 4px solid {color};
                ">
                    <div style="font-size: 0.75rem; color: #6B7280; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">{label}</div>
                    <div style="font-size: 1.4rem; font-weight: 700; color: {color}; margin-top: 8px;">{value}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Confidence Range Visual
        col_g1, col_g2 = st.columns([2, 1])
        
        with col_g1:
            # Gauge Chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=projected_sales,
                number={'valueformat': ',.0f', 'prefix': 'AED ', 'font': {'size': 28, 'color': '#1A1A2E'}},
                delta={'reference': annualized_baseline, 'valueformat': ',.0f', 'prefix': 'AED ',
                      'increasing': {'color': '#059669'}, 'decreasing': {'color': '#DC2626'}},
                title={'text': "Projected Annual Revenue", 'font': {'size': 16, 'color': '#1A1A2E'}},
                gauge={
                    'axis': {'range': [annualized_baseline * 0.5, annualized_baseline * 1.8],
                            'tickformat': ',.0f', 'tickfont': {'color': '#6B7280'}},
                    'bar': {'color': '#B8860B', 'thickness': 0.75},
                    'bgcolor': 'white',
                    'borderwidth': 2,
                    'bordercolor': '#E5E7EB',
                    'steps': [
                        {'range': [annualized_baseline * 0.5, annualized_baseline * 0.85], 'color': '#FEE2E2'},
                        {'range': [annualized_baseline * 0.85, annualized_baseline], 'color': '#FEF3C7'},
                        {'range': [annualized_baseline, annualized_baseline * 1.3], 'color': '#D1FAE5'},
                        {'range': [annualized_baseline * 1.3, annualized_baseline * 1.8], 'color': '#A7F3D0'}
                    ],
                    'threshold': {
                        'line': {'color': '#1A1A2E', 'width': 4},
                        'thickness': 0.8,
                        'value': annualized_baseline
                    }
                }
            ))
            
            fig = apply_chart_theme(fig, height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col_g2:
            st.markdown("""
            <div style="padding: 20px;">
                <p style="font-weight: 600; color: #1A1A2E; margin-bottom: 15px;">📊 Confidence Range</p>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style="background: #D1FAE5; border-radius: 8px; padding: 12px; margin: 8px 0;">
                    <span style="color: #059669; font-weight: 600;">▲ Optimistic</span>
                    <span style="float: right; color: #059669; font-weight: 700;">{format_currency(optimistic_sales)}</span>
                </div>
                <div style="background: #FEF3C7; border-radius: 8px; padding: 12px; margin: 8px 0;">
                    <span style="color: #D97706; font-weight: 600;">● Expected</span>
                    <span style="float: right; color: #D97706; font-weight: 700;">{format_currency(projected_sales)}</span>
                </div>
                <div style="background: #FEE2E2; border-radius: 8px; padding: 12px; margin: 8px 0;">
                    <span style="color: #DC2626; font-weight: 600;">▼ Conservative</span>
                    <span style="float: right; color: #DC2626; font-weight: 700;">{format_currency(conservative_sales)}</span>
                </div>
                <div style="background: #F3F4F6; border-radius: 8px; padding: 12px; margin: 8px 0;">
                    <span style="color: #6B7280; font-weight: 600;">— Baseline</span>
                    <span style="float: right; color: #6B7280; font-weight: 700;">{format_currency(annualized_baseline)}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ============================================
        # COMPONENT 5: SENSITIVITY TORNADO CHART
        # ============================================
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🌪️ Sensitivity Analysis (Tornado Chart)</div>', unsafe_allow_html=True)
            
            # Calculate impact of 10% change in each factor
            sensitivity_data = [
                {'factor': 'Conversion Rate', 'impact': 10 * conversion_coefficient * 0.20 * 1.5, 'color': '#059669'},
                {'factor': 'Tourist Footfall', 'impact': 10 * tourist_coefficient * 0.40, 'color': '#B8860B'},
                {'factor': 'Avg Basket Size', 'impact': 10 * basket_coefficient * 0.15 * 1.2, 'color': '#2563EB'},
                {'factor': 'Resident Footfall', 'impact': 10 * resident_coefficient * 0.25, 'color': '#7C3AED'},
            ]
            
            sensitivity_df = pd.DataFrame(sensitivity_data).sort_values('impact', ascending=True)
            
            fig = go.Figure()
            
            # Negative side (10% decrease)
            fig.add_trace(go.Bar(
                y=sensitivity_df['factor'],
                x=[-x for x in sensitivity_df['impact']],
                orientation='h',
                name='-10% Change',
                marker_color='#DC2626',
                text=[f"-{x:.1f}%" for x in sensitivity_df['impact']],
                textposition='inside',
                textfont=dict(color='#FFFFFF', size=11)
            ))
            
            # Positive side (10% increase)
            fig.add_trace(go.Bar(
                y=sensitivity_df['factor'],
                x=sensitivity_df['impact'],
                orientation='h',
                name='+10% Change',
                marker_color='#059669',
                text=[f"+{x:.1f}%" for x in sensitivity_df['impact']],
                textposition='inside',
                textfont=dict(color='#FFFFFF', size=11)
            ))
            
            fig.add_vline(x=0, line_color='#1A1A2E', line_width=2)
            
            fig = apply_chart_theme(fig, height=320)
            fig.update_layout(
                xaxis_title='Sales Impact (%)',
                barmode='overlay',
                legend=dict(orientation='h', y=1.15),
                xaxis=dict(zeroline=True, zerolinecolor='#1A1A2E', zerolinewidth=2)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div class="insight-card">
                <h4>💡 Key Insight</h4>
                <p><strong>Conversion Rate</strong> has the highest impact on sales. A 10% improvement yields the greatest ROI.</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ============================================
        # COMPONENT 3: CATEGORY IMPACT BREAKDOWN
        # ============================================
        with col_t2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📦 Category Impact Breakdown</div>', unsafe_allow_html=True)
            
            category_df_sorted = category_df.sort_values('impact_pct', ascending=True)
            
            colors = ['#DC2626' if x < 0 else '#059669' for x in category_df_sorted['impact_pct']]
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                y=category_df_sorted['category'],
                x=category_df_sorted['impact_pct'],
                orientation='h',
                marker_color=colors,
                text=[f"{x:+.1f}% ({format_currency(y)})" for x, y in 
                      zip(category_df_sorted['impact_pct'], category_df_sorted['impact_aed'])],
                textposition='outside',
                textfont=dict(color='#1A1A2E', size=10)
            ))
            
            fig.add_vline(x=0, line_color='#1A1A2E', line_width=2)
            
            fig = apply_chart_theme(fig, height=320)
            fig.update_layout(xaxis_title='Projected Change (%)')
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Top impacted category
            top_cat = category_df.loc[category_df['impact_pct'].abs().idxmax()]
            st.markdown(f"""
            <div class="insight-card">
                <h4>🎯 Most Impacted</h4>
                <p><strong>{top_cat['category']}</strong> with {top_cat['impact_pct']:+.1f}% change ({format_currency(top_cat['impact_aed'])})</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ============================================
        # COMPONENT 6: INVESTMENT ROI CALCULATOR
        # ============================================
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">💵 Investment ROI Calculator</div>', unsafe_allow_html=True)
        
        col_i1, col_i2 = st.columns([1, 2])
        
        with col_i1:
            st.markdown("**Investment Parameters**")
            
            investment_amount = st.slider(
                "Marketing Investment (AED)",
                min_value=100000,
                max_value=5000000,
                value=500000,
                step=50000,
                format="AED %d",
                key='investment_amount'
            )
            
            investment_duration = st.selectbox(
                "Campaign Duration",
                ["30 days", "60 days", "90 days", "180 days"],
                key='investment_duration'
            )
            
            # Investment efficiency based on scenario
            investment_multiplier = scenario['investment_multiplier']
            
            # Calculate ROI
            # Assumption: AED 1 in marketing generates AED X in footfall-driven sales
            base_marketing_efficiency = 4.2  # Industry benchmark: 4.2x return
            adjusted_efficiency = base_marketing_efficiency * investment_multiplier
            
            expected_sales_uplift = investment_amount * adjusted_efficiency
            
            # Cost structure (simulated)
            gross_margin = 0.35  # 35% gross margin
            operating_cost_ratio = 0.12  # 12% additional operating costs
            
            gross_profit = expected_sales_uplift * gross_margin
            additional_costs = expected_sales_uplift * operating_cost_ratio
            net_profit = gross_profit - additional_costs - investment_amount
            
            roi_percentage = (net_profit / investment_amount) * 100
            payback_multiplier = expected_sales_uplift / investment_amount
            
            # Break-even calculation
            break_even_investment = investment_amount / max(adjusted_efficiency * (gross_margin - operating_cost_ratio), 0.01)
            
            st.markdown(f"""
            <div style="background: #F8FAFC; border-radius: 10px; padding: 15px; margin-top: 15px;">
                <p style="color: #6B7280; font-size: 0.85rem; margin: 0;">Investment Efficiency</p>
                <p style="color: #1A1A2E; font-size: 1.2rem; font-weight: 700; margin: 5px 0;">{adjusted_efficiency:.1f}x Return</p>
                <p style="color: #6B7280; font-size: 0.8rem; margin: 0;">Based on "{selected_scenario}" scenario</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_i2:
            # ROI Waterfall Chart
            fig = go.Figure(go.Waterfall(
                name="ROI Breakdown",
                orientation="v",
                x=["Investment", "Sales Uplift", "Gross Profit", "Add'l Costs", "Net Profit"],
                y=[-investment_amount, expected_sales_uplift, -(expected_sales_uplift - gross_profit), -additional_costs, 0],
                measure=["absolute", "relative", "relative", "relative", "total"],
                text=[
                    f"-{format_currency(investment_amount)}",
                    f"+{format_currency(expected_sales_uplift)}",
                    f"-{format_currency(expected_sales_uplift - gross_profit)}",
                    f"-{format_currency(additional_costs)}",
                    f"{format_currency(net_profit)}"
                ],
                textposition="outside",
                textfont=dict(color='#1A1A2E', size=11),
                connector={"line": {"color": "#E5E7EB", "width": 2}},
                decreasing={"marker": {"color": "#DC2626"}},
                increasing={"marker": {"color": "#059669"}},
                totals={"marker": {"color": "#B8860B" if net_profit >= 0 else "#DC2626"}}
            ))
            
            fig = apply_chart_theme(fig, height=350)
            fig.update_layout(showlegend=False)
            
            st.plotly_chart(fig, use_container_width=True)
        
        # ROI Metrics Row
        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        
        roi_color = "#059669" if roi_percentage >= 0 else "#DC2626"
        
        with col_r1:
            st.markdown(f"""
            <div style="background: {'#D1FAE5' if roi_percentage >= 0 else '#FEE2E2'}; border-radius: 12px; padding: 20px; text-align: center;">
                <div style="font-size: 0.8rem; color: #6B7280;">ROI</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: {roi_color};">{roi_percentage:+.0f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_r2:
            st.markdown(f"""
            <div style="background: #DBEAFE; border-radius: 12px; padding: 20px; text-align: center;">
                <div style="font-size: 0.8rem; color: #6B7280;">Sales Uplift</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #2563EB;">{format_currency(expected_sales_uplift)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_r3:
            st.markdown(f"""
            <div style="background: #FEF3C7; border-radius: 12px; padding: 20px; text-align: center;">
                <div style="font-size: 0.8rem; color: #6B7280;">Net Profit</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #D97706;">{format_currency(net_profit)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_r4:
            st.markdown(f"""
            <div style="background: #F3E8FF; border-radius: 12px; padding: 20px; text-align: center;">
                <div style="font-size: 0.8rem; color: #6B7280;">Payback Multiple</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #7C3AED;">{payback_multiplier:.1f}x</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Investment recommendation
        if roi_percentage >= 100:
            rec_status = "🟢 HIGHLY RECOMMENDED"
            rec_color = "#059669"
            rec_bg = "#D1FAE5"
        elif roi_percentage >= 50:
            rec_status = "🟡 RECOMMENDED"
            rec_color = "#D97706"
            rec_bg = "#FEF3C7"
        elif roi_percentage >= 0:
            rec_status = "🟠 MARGINAL"
            rec_color = "#EA580C"
            rec_bg = "#FFEDD5"
        else:
            rec_status = "🔴 NOT RECOMMENDED"
            rec_color = "#DC2626"
            rec_bg = "#FEE2E2"
        
        st.markdown(f"""
        <div style="background: {rec_bg}; border: 2px solid {rec_color}; border-radius: 12px; padding: 20px; margin-top: 20px; text-align: center;">
            <span style="font-size: 1.3rem; font-weight: 700; color: {rec_color};">{rec_status}</span>
            <p style="color: #4A4A6A; margin: 10px 0 0 0;">
                Investment of <strong>{format_currency(investment_amount)}</strong> is projected to generate 
                <strong>{format_currency(net_profit)}</strong> net profit with <strong>{roi_percentage:.0f}% ROI</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ============================================
        # COMPONENT 7: ACTION PLAN GENERATOR
        # ============================================
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📋 Strategic Action Plan</div>', unsafe_allow_html=True)
        
        # Generate dynamic recommendations based on scenario and inputs
        recommendations = []
        
        # Tourist-focused recommendations
        if tourist_change > 15:
            recommendations.append({
                "priority": "HIGH",
                "category": "Marketing",
                "action": "Intensify international tourism marketing",
                "detail": f"Expected {tourist_change}% tourist surge. Focus on GCC, Europe, and Asia markets.",
                "budget": "AED 200K - 500K",
                "timeline": "Start 4 weeks before event"
            })
            recommendations.append({
                "priority": "HIGH",
                "category": "Inventory",
                "action": "Stock up Luxury & Fashion categories",
                "detail": "Tourist-heavy periods drive 40% higher luxury sales. Increase premium inventory.",
                "budget": "AED 1M - 2M inventory",
                "timeline": "2 weeks before event"
            })
        
        if tourist_change < -20:
            recommendations.append({
                "priority": "HIGH",
                "category": "Marketing",
                "action": "Pivot to resident-focused campaigns",
                "detail": f"Tourist footfall down {abs(tourist_change)}%. Focus on local loyalty programs.",
                "budget": "AED 100K - 200K",
                "timeline": "Immediate"
            })
        
        # Conversion-focused recommendations
        if conversion_change < 0:
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Operations",
                "action": "Improve in-store conversion tactics",
                "detail": "Conversion expected to drop. Train staff on engagement, optimize store layouts.",
                "budget": "AED 50K training",
                "timeline": "Ongoing"
            })
        
        if conversion_change > 10:
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Staffing",
                "action": "Increase floor staff by 25%",
                "detail": "Higher conversion expected. Ensure adequate staff to handle increased transactions.",
                "budget": "AED 150K additional payroll",
                "timeline": "1 week before event"
            })
        
        # Basket size recommendations
        if basket_change > 20:
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Merchandising",
                "action": "Implement premium product placement",
                "detail": f"Basket size up {basket_change}%. Position high-margin items at eye level and checkout.",
                "budget": "AED 30K visual merchandising",
                "timeline": "1 week before event"
            })
            recommendations.append({
                "priority": "LOW",
                "category": "Finance",
                "action": "Enable premium payment options",
                "detail": "Partner with banks for 0% installment plans to support larger purchases.",
                "budget": "Revenue share model",
                "timeline": "2 weeks setup"
            })
        
        # Resident-focused recommendations
        if resident_change > 20:
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Promotions",
                "action": "Launch family-focused promotions",
                "detail": f"Resident traffic up {resident_change}%. Create family bundles and loyalty rewards.",
                "budget": "AED 100K promotion budget",
                "timeline": "1 week before event"
            })
        
        # General recommendations based on scenario
        if "Eid" in selected_scenario or "Diwali" in selected_scenario:
            recommendations.append({
                "priority": "HIGH",
                "category": "Operations",
                "action": "Extend mall operating hours",
                "detail": "Festival periods see 60% of traffic after 6 PM. Extend hours to 1 AM.",
                "budget": "AED 80K additional operations",
                "timeline": "Event period"
            })
        
        if "Ramadan" in selected_scenario:
            recommendations.append({
                "priority": "HIGH",
                "category": "Operations",
                "action": "Shift peak operations to evening",
                "detail": "Ramadan traffic peaks after Iftar (7-11 PM). Reduce morning staffing.",
                "budget": "Neutral (shift reallocation)",
                "timeline": "Ramadan period"
            })
            recommendations.append({
                "priority": "MEDIUM",
                "category": "F&B",
                "action": "Prepare Iftar dining capacity",
                "detail": "F&B sees 200% surge at Iftar. Add temporary seating and fast-service options.",
                "budget": "AED 50K temporary setup",
                "timeline": "Before Ramadan"
            })
        
        if "Summer" in selected_scenario:
            recommendations.append({
                "priority": "HIGH",
                "category": "Cost Control",
                "action": "Reduce operating costs",
                "detail": "Low traffic period. Consider reduced hours, staff rotation, and inventory clearance.",
                "budget": "Save AED 200K - 400K",
                "timeline": "June - August"
            })
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Marketing",
                "action": "Launch summer clearance sale",
                "detail": "Convert slow period into clearance opportunity. Attract price-sensitive shoppers.",
                "budget": "AED 80K marketing",
                "timeline": "July"
            })
        
        if "Economic" in selected_scenario:
            recommendations.append({
                "priority": "CRITICAL",
                "category": "Finance",
                "action": "Renegotiate tenant agreements",
                "detail": "Support struggling tenants with temporary rent relief to prevent vacancies.",
                "budget": "Revenue impact AED 500K - 1M",
                "timeline": "Immediate"
            })
            recommendations.append({
                "priority": "HIGH",
                "category": "Positioning",
                "action": "Emphasize value positioning",
                "detail": "Shift marketing from luxury to value. Highlight discounts and essentials.",
                "budget": "AED 100K repositioning",
                "timeline": "Ongoing"
            })
        
        # Risk mitigation
        recommendations.append({
            "priority": "LOW",
            "category": "Risk",
            "action": "Prepare contingency capacity",
            "detail": "Have overflow parking, queue management, and security on standby.",
            "budget": "AED 30K contingency",
            "timeline": "As needed"
        })
        
        # Sort by priority
        priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 4))
        
        # Display recommendations
        col_a1, col_a2 = st.columns([2, 1])
        
        with col_a1:
            for i, rec in enumerate(recommendations[:8], 1):  # Show top 8
                priority_colors = {
                    "CRITICAL": ("#DC2626", "#FEE2E2"),
                    "HIGH": ("#D97706", "#FEF3C7"),
                    "MEDIUM": ("#2563EB", "#DBEAFE"),
                    "LOW": ("#6B7280", "#F3F4F6")
                }
                p_color, p_bg = priority_colors.get(rec['priority'], ("#6B7280", "#F3F4F6"))
                
                st.markdown(f"""
                <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-left: 5px solid {p_color}; border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="background: {p_bg}; color: {p_color}; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700;">{rec['priority']}</span>
                        <span style="color: #6B7280; font-size: 0.8rem;">{rec['category']}</span>
                    </div>
                    <p style="color: #1A1A2E; font-weight: 600; margin: 0 0 5px 0;">{i}. {rec['action']}</p>
                    <p style="color: #4A4A6A; font-size: 0.9rem; margin: 0 0 8px 0;">{rec['detail']}</p>
                    <div style="display: flex; gap: 20px; font-size: 0.8rem; color: #6B7280;">
                        <span>💰 {rec['budget']}</span>
                        <span>📅 {rec['timeline']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col_a2:
            # Summary stats
            total_budget = investment_amount + 500000  # Estimated operational budget
            
            st.markdown(f"""
            <div style="background: linear-gradient(145deg, #1A1A2E 0%, #16213E 100%); border-radius: 16px; padding: 25px; color: #FFFFFF;">
                <h4 style="color: #DAA520; margin: 0 0 20px 0;">📊 Plan Summary</h4>
                
                <div style="margin: 15px 0;">
                    <p style="color: #94A3B8; font-size: 0.8rem; margin: 0;">Scenario</p>
                    <p style="color: #FFFFFF; font-size: 1rem; font-weight: 600; margin: 5px 0;">{selected_scenario}</p>
                </div>
                
                <div style="margin: 15px 0;">
                    <p style="color: #94A3B8; font-size: 0.8rem; margin: 0;">Total Actions</p>
                    <p style="color: #FFFFFF; font-size: 1.5rem; font-weight: 700; margin: 5px 0;">{len(recommendations)}</p>
                </div>
                
                <div style="margin: 15px 0;">
                    <p style="color: #94A3B8; font-size: 0.8rem; margin: 0;">Est. Investment</p>
                    <p style="color: #DAA520; font-size: 1.3rem; font-weight: 700; margin: 5px 0;">{format_currency(total_budget)}</p>
                </div>
                
                <div style="margin: 15px 0;">
                    <p style="color: #94A3B8; font-size: 0.8rem; margin: 0;">Expected Revenue</p>
                    <p style="color: #4ADE80; font-size: 1.3rem; font-weight: 700; margin: 5px 0;">{format_currency(projected_sales)}</p>
                </div>
                
                <div style="margin: 15px 0;">
                    <p style="color: #94A3B8; font-size: 0.8rem; margin: 0;">Expected ROI</p>
                    <p style="color: {'#4ADE80' if roi_percentage > 0 else '#F87171'}; font-size: 1.5rem; font-weight: 700; margin: 5px 0;">{roi_percentage:+.0f}%</p>
                </div>
                
                <div style="margin: 20px 0 0 0; padding-top: 15px; border-top: 1px solid #374151;">
                    <p style="color: #94A3B8; font-size: 0.8rem; margin: 0;">Confidence Level</p>
                    <div style="background: #374151; border-radius: 10px; height: 10px; margin: 8px 0;">
                        <div style="background: linear-gradient(90deg, #B8860B, #DAA520); border-radius: 10px; height: 10px; width: {scenario['confidence']}%;"></div>
                    </div>
                    <p style="color: #DAA520; font-size: 0.9rem; font-weight: 600; margin: 0;">{scenario['confidence']}%</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Download button placeholder
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Create summary for download
            summary_text = f"""
DUBAI MALL - STRATEGIC SCENARIO ANALYSIS
========================================

Scenario: {selected_scenario}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

PARAMETERS:
- Tourist Footfall Change: {tourist_change:+d}%
- Resident Footfall Change: {resident_change:+d}%
- Conversion Rate Change: {conversion_change:+d}%
- Basket Size Change: {basket_change:+d}%

PROJECTED OUTCOMES:
- Current Annual Sales: {format_currency(annualized_baseline)}
- Projected Sales: {format_currency(projected_sales)}
- Sales Impact: {format_currency(sales_change_amount)} ({sales_change_pct:+.1f}%)
- Confidence Level: {scenario['confidence']}%

CONFIDENCE RANGE:
- Optimistic: {format_currency(optimistic_sales)}
- Expected: {format_currency(projected_sales)}
- Conservative: {format_currency(conservative_sales)}

INVESTMENT ANALYSIS:
- Recommended Investment: {format_currency(investment_amount)}
- Expected Sales Uplift: {format_currency(expected_sales_uplift)}
- Net Profit: {format_currency(net_profit)}
- ROI: {roi_percentage:.0f}%

ACTION ITEMS:
"""
            for i, rec in enumerate(recommendations, 1):
                summary_text += f"\n{i}. [{rec['priority']}] {rec['action']}\n   {rec['detail']}\n   Budget: {rec['budget']} | Timeline: {rec['timeline']}\n"
            
            st.download_button(
                label="📥 Download Analysis Report",
                data=summary_text,
                file_name=f"dubai_mall_scenario_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ============================================
        # INVESTOR SUMMARY CARD
        # ============================================
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📈 Investor Summary</div>', unsafe_allow_html=True)
        
        col_inv1, col_inv2, col_inv3 = st.columns(3)
        
        with col_inv1:
            st.markdown(f"""
            <div style="background: linear-gradient(145deg, #059669 0%, #047857 100%); border-radius: 16px; padding: 25px; color: #FFFFFF; text-align: center;">
                <p style="font-size: 0.9rem; margin: 0; opacity: 0.9;">Expected Annual Revenue</p>
                <p style="font-size: 2rem; font-weight: 700; margin: 10px 0;">{format_currency(projected_sales)}</p>
                <p style="font-size: 1rem; margin: 0;">({sales_change_pct:+.1f}% vs baseline)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_inv2:
            # Calculate approximate valuation impact (using 8x revenue multiple for retail)
            revenue_multiple = 8
            baseline_valuation = annualized_baseline * revenue_multiple
            projected_valuation = projected_sales * revenue_multiple
            valuation_change = projected_valuation - baseline_valuation
            
            st.markdown(f"""
            <div style="background: linear-gradient(145deg, #B8860B 0%, #92400E 100%); border-radius: 16px; padding: 25px; color: #FFFFFF; text-align: center;">
                <p style="font-size: 0.9rem; margin: 0; opacity: 0.9;">Est. Valuation Impact (8x Rev)</p>
                <p style="font-size: 2rem; font-weight: 700; margin: 10px 0;">{format_currency(valuation_change)}</p>
                <p style="font-size: 1rem; margin: 0;">New Valuation: {format_currency(projected_valuation)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_inv3:
            # Risk-adjusted return
            risk_adjusted_return = roi_percentage * (scenario['confidence'] / 100)
            
            st.markdown(f"""
            <div style="background: linear-gradient(145deg, #2563EB 0%, #1D4ED8 100%); border-radius: 16px; padding: 25px; color: #FFFFFF; text-align: center;">
                <p style="font-size: 0.9rem; margin: 0; opacity: 0.9;">Risk-Adjusted ROI</p>
                <p style="font-size: 2rem; font-weight: 700; margin: 10px 0;">{risk_adjusted_return:.0f}%</p>
                <p style="font-size: 1rem; margin: 0;">(ROI × Confidence Factor)</p>
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
    # FOOTER - GUARANTEED VISIBLE
    # ========================================
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
        border-radius: 16px;
        padding: 35px;
        margin-top: 50px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        border-top: 3px solid #B8860B;
    ">
        <p style="
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 1.5rem;
            font-weight: 700;
            color: #FFD700;
            margin: 0 0 10px 0;
            text-shadow: 2px 2px 6px rgba(0,0,0,0.5);
        ">🏬 Dubai Mall Analytics Dashboard</p>
        
        <p style="
            font-family: 'Poppins', Arial, sans-serif;
            color: #E8E8E8;
            font-size: 1rem;
            margin: 8px 0;
            letter-spacing: 0.5px;
        ">Premium Retail Intelligence Platform • Full Analytics Suite</p>
        
        <div style="
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid rgba(255,255,255,0.1);
        ">
            <p style="
                font-family: 'Poppins', Arial, sans-serif;
                color: #94A3B8;
                font-size: 0.85rem;
                margin: 0;
            ">© 2024 Dubai Mall Management | Dashboard v3.0</p>
            
            <p style="
                font-family: 'Poppins', Arial, sans-serif;
                color: #64748B;
                font-size: 0.8rem;
                margin: 10px 0 0 0;
            ">Built with ❤️ for Investor Presentations</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# RUN
# ============================================
if __name__ == "__main__":
    main()
