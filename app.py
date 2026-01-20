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
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;500;600;700&display=swap');
    
    /* Root Variables - LIGHT PROJECTOR THEME */
    :root {
        --gold-primary: #B8860B;
        --gold-dark: #8B6914;
        --gold-light: #DAA520;
        --bg-primary: #FFFFFF;
        --bg-secondary: #F8F9FA;
        --bg-card: #FFFFFF;
        --text-primary: #1A1A2E;
        --text-secondary: #4A4A6A;
        --text-muted: #6B7280;
        --border-color: #E5E7EB;
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.12);
        --shadow-md: 0 4px 12px rgba(0,0,0,0.15);
        --shadow-lg: 0 8px 25px rgba(0,0,0,0.18);
        --success: #059669;
        --danger: #DC2626;
        --info: #2563EB;
        --warning: #D97706;
    }
    
    /* Main App Background - LIGHT */
    .stApp {
        background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%);
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Header */
    .main-header {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
        border-radius: 20px;
        padding: 35px 45px;
        margin-bottom: 30px;
        box-shadow: var(--shadow-lg);
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
    
    /* KPI CARDS - SQUARE DESIGN */
    .kpi-row {
        display: flex;
        gap: 20px;
        margin-bottom: 30px;
        flex-wrap: wrap;
    }
    
    .kpi-card {
        background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFC 100%);
        border: 2px solid #E5E7EB;
        border-radius: 16px;
        padding: 24px;
        flex: 1;
        min-width: 180px;
        max-width: 200px;
        aspect-ratio: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        box-shadow: var(--shadow-md);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card:hover {
        transform: translateY(-8px);
        box-shadow: var(--shadow-lg);
        border-color: #B8860B;
    }
    
    .kpi-card::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #B8860B, #DAA520);
    }
    
    .kpi-icon {
        font-size: 2.5rem;
        margin-bottom: 8px;
        filter: grayscale(0);
    }
    
    .kpi-value {
        font-family: 'Poppins', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #1A1A2E;
        margin: 5px 0;
        line-height: 1.2;
    }
    
    .kpi-label {
        font-family: 'Poppins', sans-serif;
        font-size: 0.75rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .kpi-delta {
        font-family: 'Poppins', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 5px;
        padding: 3px 10px;
        border-radius: 20px;
    }
    
    .kpi-delta.positive {
        color: #059669;
        background: rgba(5, 150, 105, 0.1);
    }
    
    .kpi-delta.negative {
        color: #DC2626;
        background: rgba(220, 38, 38, 0.1);
    }
    
    /* Section Headers */
    .section-header {
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        font-weight: 600;
        color: #1A1A2E;
        margin: 35px 0 20px 0;
        padding-bottom: 12px;
        border-bottom: 3px solid #B8860B;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    /* Chart Containers */
    .chart-container {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: var(--shadow-sm);
    }
    
    .chart-container:hover {
        box-shadow: var(--shadow-md);
    }
    
    .chart-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #1A1A2E;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #F3F4F6;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Filter Box */
    .filter-box {
        background: linear-gradient(145deg, #FEF3C7 0%, #FDE68A 100%);
        border: 1px solid #F59E0B;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
    }
    
    .filter-box label {
        font-family: 'Poppins', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        color: #92400E;
    }
    
    /* Sidebar - LIGHT THEME */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1A1A2E 0%, #16213E 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #E2E8F0;
    }
    
    [data-testid="stSidebar"] label {
        color: #E2E8F0 !important;
        font-family: 'Poppins', sans-serif;
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
    
    /* Selectbox & Input Styling */
    .stSelectbox > div > div {
        background-color: #FFFFFF;
        border: 2px solid #E5E7EB;
        border-radius: 10px;
        font-family: 'Poppins', sans-serif;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #B8860B;
    }
    
    .stMultiSelect > div > div {
        background-color: #FFFFFF;
        border: 2px solid #E5E7EB;
        border-radius: 10px;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F3F4F6;
        border-radius: 12px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: #4A4A6A;
        border-radius: 8px;
        padding: 12px 24px;
        background: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #B8860B 0%, #DAA520 100%);
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(184, 134, 11, 0.3);
    }
    
    /* Data Table */
    .dataframe {
        font-family: 'Poppins', sans-serif !important;
        border-radius: 10px;
        overflow: hidden;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%) !important;
        color: #DAA520 !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.8rem !important;
        padding: 12px !important;
    }
    
    .dataframe td {
        background-color: #FFFFFF !important;
        color: #1A1A2E !important;
        border-color: #E5E7EB !important;
        padding: 10px !important;
        font-size: 0.9rem !important;
    }
    
    .dataframe tr:nth-child(even) td {
        background-color: #F9FAFB !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: #1A1A2E;
        background-color: #F3F4F6;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
    }
    
    /* Info Boxes */
    .insight-card {
        background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFC 100%);
        border-left: 5px solid #B8860B;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: var(--shadow-sm);
    }
    
    .insight-card h4 {
        font-family: 'Poppins', sans-serif;
        color: #1A1A2E;
        font-weight: 600;
        margin-bottom: 10px;
        font-size: 1rem;
    }
    
    .insight-card p {
        font-family: 'Poppins', sans-serif;
        color: #4A4A6A;
        font-size: 0.95rem;
        margin: 5px 0;
        line-height: 1.5;
    }
    
    .insight-card strong {
        color: #B8860B;
    }
    
    /* Metric Highlight */
    .metric-highlight {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        border: 2px solid #F59E0B;
        border-radius: 10px;
        padding: 15px 20px;
        display: inline-block;
        margin: 5px;
    }
    
    .metric-highlight .value {
        font-family: 'Poppins', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #92400E;
    }
    
    .metric-highlight .label {
        font-family: 'Poppins', sans-serif;
        font-size: 0.8rem;
        color: #B45309;
        text-transform: uppercase;
    }
    
    /* Footer */
    .custom-footer {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
        border-radius: 16px;
        padding: 30px;
        margin-top: 50px;
        text-align: center;
        box-shadow: var(--shadow-lg);
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
    
    /* Scrollbar */
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
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Chart Filter Row */
    .chart-filter-row {
        background: #F8FAFC;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 12px 15px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .chart-filter-row label {
        font-family: 'Poppins', sans-serif;
        font-size: 0.85rem;
        font-weight: 500;
        color: #4A4A6A;
    }
    
    /* Badge */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-family: 'Poppins', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .badge-gold {
        background: linear-gradient(135deg, #B8860B 0%, #DAA520 100%);
        color: #FFFFFF;
    }
    
    .badge-success {
        background: #D1FAE5;
        color: #059669;
    }
    
    .badge-danger {
        background: #FEE2E2;
        color: #DC2626;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.8rem;
        }
        .kpi-card {
            min-width: 150px;
            max-width: 150px;
        }
        .kpi-value {
            font-size: 1.4rem;
        }
    }
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

def create_kpi_html(icon, label, value, delta=None):
    """Create styled KPI card HTML"""
    delta_html = ""
    if delta is not None:
        delta_class = "positive" if delta >= 0 else "negative"
        delta_symbol = "▲" if delta >= 0 else "▼"
        delta_html = f'<div class="kpi-delta {delta_class}">{delta_symbol} {abs(delta):.1f}%</div>'
    
    return f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """

# ============================================
# CHART THEME - PROJECTOR FRIENDLY
# ============================================
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

# Color palette for charts
CHART_COLORS = ['#B8860B', '#2563EB', '#059669', '#DC2626', '#7C3AED', '#DB2777', '#0891B2', '#EA580C']

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
    # SIDEBAR - Global Filters
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
        
        # Category filter
        all_categories = ['All Categories'] + sorted(df['category'].unique().tolist())
        selected_category = st.selectbox("Category", all_categories)
        
        # Floor filter
        all_floors = ['All Floors'] + sorted(df['floor'].unique().tolist())
        selected_floor = st.selectbox("Floor", all_floors)
        
        st.markdown("---")
        st.markdown("### ⚙️ Display Options")
        show_raw_data = st.checkbox("Show Raw Data Tables", value=False)
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; padding: 15px;'>
            <p style='color: #94A3B8; font-size: 0.8rem;'>📊 Dubai Mall Dashboard</p>
            <p style='color: #DAA520; font-size: 0.9rem; font-weight: 600;'>v2.0 - Projector Edition</p>
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
    # KPI CARDS - USING STREAMLIT COLUMNS
    # ========================================
    st.markdown('<div class="section-header">📊 Key Performance Indicators</div>', unsafe_allow_html=True)
    
    # Calculate KPIs
    total_sales = filtered_df['sales_aed'].sum()
    total_footfall = filtered_df.groupby('date')['mall_footfall'].first().sum()
    total_transactions = filtered_df['transactions'].sum()
    avg_conversion = filtered_df['conversion_rate'].mean() * 100
    avg_basket = filtered_df['avg_basket_aed'].mean()
    sales_per_sqft = filtered_df['sales_per_sqft'].mean()
    
    # KPI Row using Streamlit columns
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5, kpi_col6 = st.columns(6)
    
    with kpi_col1:
        st.markdown(f"""
        <div style="
            background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFC 100%);
            border: 2px solid #E5E7EB;
            border-radius: 16px;
            padding: 20px 15px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border-bottom: 4px solid #B8860B;
            height: 160px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 5px;">💰</div>
            <div style="font-size: 0.7rem; color: #6B7280; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Total Sales</div>
            <div style="font-size: 1.6rem; font-weight: 700; color: #1A1A2E; margin: 5px 0;">{format_value_short(total_sales)}</div>
            <div style="font-size: 0.8rem; color: #059669; background: rgba(5,150,105,0.1); padding: 2px 10px; border-radius: 20px; display: inline-block;">▲ 12.5%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col2:
        st.markdown(f"""
        <div style="
            background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFC 100%);
            border: 2px solid #E5E7EB;
            border-radius: 16px;
            padding: 20px 15px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border-bottom: 4px solid #2563EB;
            height: 160px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 5px;">👥</div>
            <div style="font-size: 0.7rem; color: #6B7280; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Mall Footfall</div>
            <div style="font-size: 1.6rem; font-weight: 700; color: #1A1A2E; margin: 5px 0;">{format_value_short(total_footfall)}</div>
            <div style="font-size: 0.8rem; color: #059669; background: rgba(5,150,105,0.1); padding: 2px 10px; border-radius: 20px; display: inline-block;">▲ 8.3%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col3:
        st.markdown(f"""
        <div style="
            background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFC 100%);
            border: 2px solid #E5E7EB;
            border-radius: 16px;
            padding: 20px 15px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border-bottom: 4px solid #059669;
            height: 160px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 5px;">🛒</div>
            <div style="font-size: 0.7rem; color: #6B7280; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Transactions</div>
            <div style="font-size: 1.6rem; font-weight: 700; color: #1A1A2E; margin: 5px 0;">{format_value_short(total_transactions)}</div>
            <div style="font-size: 0.8rem; color: #059669; background: rgba(5,150,105,0.1); padding: 2px 10px; border-radius: 20px; display: inline-block;">▲ 15.2%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col4:
        st.markdown(f"""
        <div style="
            background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFC 100%);
            border: 2px solid #E5E7EB;
            border-radius: 16px;
            padding: 20px 15px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border-bottom: 4px solid #7C3AED;
            height: 160px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 5px;">📈</div>
            <div style="font-size: 0.7rem; color: #6B7280; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Conversion</div>
            <div style="font-size: 1.6rem; font-weight: 700; color: #1A1A2E; margin: 5px 0;">{avg_conversion:.1f}%</div>
            <div style="font-size: 0.8rem; color: #059669; background: rgba(5,150,105,0.1); padding: 2px 10px; border-radius: 20px; display: inline-block;">▲ 3.2%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col5:
        st.markdown(f"""
        <div style="
            background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFC 100%);
            border: 2px solid #E5E7EB;
            border-radius: 16px;
            padding: 20px 15px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border-bottom: 4px solid #DB2777;
            height: 160px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 5px;">🧺</div>
            <div style="font-size: 0.7rem; color: #6B7280; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Avg Basket</div>
            <div style="font-size: 1.6rem; font-weight: 700; color: #1A1A2E; margin: 5px 0;">{format_value_short(avg_basket)}</div>
            <div style="font-size: 0.8rem; color: #059669; background: rgba(5,150,105,0.1); padding: 2px 10px; border-radius: 20px; display: inline-block;">▲ 5.8%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col6:
        st.markdown(f"""
        <div style="
            background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFC 100%);
            border: 2px solid #E5E7EB;
            border-radius: 16px;
            padding: 20px 15px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border-bottom: 4px solid #0891B2;
            height: 160px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 5px;">📐</div>
            <div style="font-size: 0.7rem; color: #6B7280; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Sales/Sqft</div>
            <div style="font-size: 1.6rem; font-weight: 700; color: #1A1A2E; margin: 5px 0;">{format_value_short(sales_per_sqft)}</div>
            <div style="font-size: 0.8rem; color: #059669; background: rgba(5,150,105,0.1); padding: 2px 10px; border-radius: 20px; display: inline-block;">▲ 7.1%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========================================
    # TABS
    # ========================================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Sales Analytics", 
        "👥 Footfall Insights", 
        "🏪 Store Performance",
        "📊 Category Analysis",
        "🎯 Deep Insights"
    ])
    
    # ========================================
    # TAB 1: SALES ANALYTICS
    # ========================================
    with tab1:
        # === CHART 1: Daily Sales Trend ===
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📈 Daily Sales Trend</div>', unsafe_allow_html=True)
        
        # Individual Filter for this chart
        col_f1, col_f2, col_f3 = st.columns([2, 2, 4])
        with col_f1:
            trend_category = st.selectbox(
                "Filter by Category",
                ['All'] + sorted(filtered_df['category'].unique().tolist()),
                key='trend_cat'
            )
        with col_f2:
            trend_metric = st.selectbox(
                "Select Metric",
                ['Sales + Transactions', 'Sales Only', 'Transactions Only'],
                key='trend_metric'
            )
        
        # Filter data for this chart
        chart1_df = filtered_df.copy()
        if trend_category != 'All':
            chart1_df = chart1_df[chart1_df['category'] == trend_category]
        
        daily_sales = chart1_df.groupby('date').agg({
            'sales_aed': 'sum',
            'transactions': 'sum'
        }).reset_index()
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        if trend_metric in ['Sales + Transactions', 'Sales Only']:
            fig.add_trace(
                go.Scatter(
                    x=daily_sales['date'],
                    y=daily_sales['sales_aed'],
                    name='Sales (AED)',
                    line=dict(color='#B8860B', width=3),
                    fill='tozeroy',
                    fillcolor='rgba(184, 134, 11, 0.15)'
                ),
                secondary_y=False
            )
        
        if trend_metric in ['Sales + Transactions', 'Transactions Only']:
            fig.add_trace(
                go.Bar(
                    x=daily_sales['date'],
                    y=daily_sales['transactions'],
                    name='Transactions',
                    marker_color='rgba(37, 99, 235, 0.7)',
                    opacity=0.8
                ),
                secondary_y=True
            )
        
        fig = apply_chart_theme(fig, height=420)
        fig.update_layout(
            yaxis_title='Sales (AED)',
            yaxis2_title='Transactions',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # === Row 2: Day of Week & Weekend Analysis ===
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📅 Sales by Day of Week</div>', unsafe_allow_html=True)
            
            # Filter for this chart
            dow_floor = st.selectbox(
                "Filter by Floor",
                ['All'] + sorted(filtered_df['floor'].unique().tolist()),
                key='dow_floor'
            )
            
            chart2_df = filtered_df.copy()
            if dow_floor != 'All':
                chart2_df = chart2_df[chart2_df['floor'] == dow_floor]
            
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            daily_pattern = chart2_df.groupby('day_name')['sales_aed'].sum().reindex(day_order)
            
            colors = ['#E5E7EB'] * 7
            max_idx = daily_pattern.values.argmax()
            colors[max_idx] = '#B8860B'
            
            fig = go.Figure(go.Bar(
                x=daily_pattern.index,
                y=daily_pattern.values,
                marker_color=colors,
                marker_line_color='#1A1A2E',
                marker_line_width=1,
                text=[format_value_short(x) for x in daily_pattern.values],
                textposition='outside',
                textfont=dict(color='#1A1A2E', size=11, family='Poppins')
            ))
            
            fig = apply_chart_theme(fig, height=380)
            fig.update_layout(yaxis_title='Total Sales (AED)')
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🗓️ Weekend vs Weekday</div>', unsafe_allow_html=True)
            
            # Filter for this chart
            ww_category = st.selectbox(
                "Filter by Category",
                ['All'] + sorted(filtered_df['category'].unique().tolist()),
                key='ww_cat'
            )
            
            chart3_df = filtered_df.copy()
            if ww_category != 'All':
                chart3_df = chart3_df[chart3_df['category'] == ww_category]
            
            weekend_data = chart3_df.groupby('is_weekend').agg({
                'sales_aed': 'sum',
                'transactions': 'sum',
                'conversion_rate': 'mean'
            }).reset_index()
            weekend_data['type'] = weekend_data['is_weekend'].map({0: 'Weekday', 1: 'Weekend'})
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=weekend_data['type'],
                y=weekend_data['sales_aed'],
                marker_color=['#2563EB', '#B8860B'],
                text=[format_currency(x) for x in weekend_data['sales_aed']],
                textposition='outside',
                textfont=dict(size=14, family='Poppins', color='#1A1A2E')
            ))
            
            fig = apply_chart_theme(fig, height=380)
            fig.update_layout(yaxis_title='Total Sales (AED)')
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # === Chart: Sales Distribution ===
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📊 Sales Distribution by Category</div>', unsafe_allow_html=True)
        
        col_f1, col_f2 = st.columns([3, 5])
        with col_f1:
            dist_view = st.selectbox(
                "View Type",
                ['Pie Chart', 'Bar Chart', 'Treemap'],
                key='dist_view'
            )
        
        cat_sales = filtered_df.groupby('category')['sales_aed'].sum().sort_values(ascending=False)
        
        if dist_view == 'Pie Chart':
            fig = go.Figure(go.Pie(
                labels=cat_sales.index,
                values=cat_sales.values,
                hole=0.5,
                marker=dict(colors=CHART_COLORS[:len(cat_sales)], line=dict(color='#FFFFFF', width=2)),
                textinfo='label+percent',
                textfont=dict(size=12, family='Poppins', color='#1A1A2E'),
                hovertemplate="<b>%{label}</b><br>Sales: AED %{value:,.0f}<br>Share: %{percent}<extra></extra>"
            ))
            fig.add_annotation(
                text=f"<b>Total<br>{format_value_short(cat_sales.sum())}</b>",
                x=0.5, y=0.5, font=dict(size=16, color='#1A1A2E', family='Poppins'), showarrow=False
            )
        elif dist_view == 'Bar Chart':
            fig = go.Figure(go.Bar(
                x=cat_sales.values,
                y=cat_sales.index,
                orientation='h',
                marker_color=CHART_COLORS[:len(cat_sales)],
                text=[format_currency(x) for x in cat_sales.values],
                textposition='inside',
                textfont=dict(color='#FFFFFF', size=11, family='Poppins')
            ))
            fig.update_layout(yaxis=dict(categoryorder='total ascending'))
        else:
            fig = px.treemap(
                names=cat_sales.index,
                parents=[''] * len(cat_sales),
                values=cat_sales.values,
                color_discrete_sequence=CHART_COLORS
            )
            fig.update_traces(textfont=dict(size=14, family='Poppins'))
        
        fig = apply_chart_theme(fig, height=450)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================
    # TAB 2: FOOTFALL INSIGHTS
    # ========================================
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🌍 Tourist vs Resident Footfall</div>', unsafe_allow_html=True)
            
            # Filter
            ff_agg = st.selectbox(
                "Aggregation",
                ['Daily', 'Weekly'],
                key='ff_agg'
            )
            
            if ff_agg == 'Daily':
                footfall_data = filtered_df.groupby('date').agg({
                    'tourist_footfall': 'first',
                    'resident_footfall': 'first'
                }).reset_index()
                x_col = 'date'
            else:
                filtered_df['week_start'] = filtered_df['date'] - pd.to_timedelta(filtered_df['date'].dt.dayofweek, unit='d')
                footfall_data = filtered_df.groupby('week_start').agg({
                    'tourist_footfall': 'sum',
                    'resident_footfall': 'sum'
                }).reset_index()
                x_col = 'week_start'
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=footfall_data[x_col],
                y=footfall_data['tourist_footfall'],
                name='Tourists',
                stackgroup='one',
                fillcolor='rgba(184, 134, 11, 0.7)',
                line=dict(color='#B8860B', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=footfall_data[x_col],
                y=footfall_data['resident_footfall'],
                name='Residents',
                stackgroup='one',
                fillcolor='rgba(37, 99, 235, 0.7)',
                line=dict(color='#2563EB', width=2)
            ))
            
            fig = apply_chart_theme(fig, height=400)
            fig.update_layout(yaxis_title='Footfall Count')
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📊 Visitor Composition</div>', unsafe_allow_html=True)
            
            avg_tourist = filtered_df['tourist_share'].mean() * 100
            avg_resident = filtered_df['resident_share'].mean() * 100
            
            fig = go.Figure(go.Pie(
                labels=['Tourists', 'Residents'],
                values=[avg_tourist, avg_resident],
                hole=0.65,
                marker=dict(colors=['#B8860B', '#2563EB'], line=dict(color='#FFFFFF', width=3)),
                textinfo='label+percent',
                textfont=dict(size=14, family='Poppins', color='#1A1A2E'),
                hovertemplate="<b>%{label}</b><br>Share: %{percent}<extra></extra>"
            ))
            
            fig.add_annotation(
                text=f"<b>Visitor<br>Mix</b>",
                x=0.5, y=0.5,
                font=dict(size=18, color='#1A1A2E', family='Playfair Display'),
                showarrow=False
            )
            
            fig = apply_chart_theme(fig, height=400)
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Footfall vs Sales Correlation
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🔗 Footfall to Sales Correlation</div>', unsafe_allow_html=True)
        
        col_f1, col_f2 = st.columns([2, 6])
        with col_f1:
            bubble_size = st.selectbox(
                "Bubble Size By",
                ['Conversion Rate', 'Avg Basket', 'Transactions'],
                key='bubble_size'
            )
        
        size_map = {
            'Conversion Rate': 'conversion_rate',
            'Avg Basket': 'avg_basket_aed',
            'Transactions': 'transactions'
        }
        
        corr_data = filtered_df.groupby('category').agg({
            'store_footfall': 'sum',
            'sales_aed': 'sum',
            'conversion_rate': 'mean',
            'avg_basket_aed': 'mean',
            'transactions': 'sum'
        }).reset_index()
        
        fig = px.scatter(
            corr_data,
            x='store_footfall',
            y='sales_aed',
            size=size_map[bubble_size],
            color='category',
            hover_name='category',
            size_max=60,
            color_discrete_sequence=CHART_COLORS
        )
        
        fig = apply_chart_theme(fig, height=450)
        fig.update_layout(
            xaxis_title='Total Store Footfall',
            yaxis_title='Total Sales (AED)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================
    # TAB 3: STORE PERFORMANCE
    # ========================================
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🏆 Top Stores by Sales</div>', unsafe_allow_html=True)
            
            # Filter
            top_n_sales = st.slider("Number of Stores", 5, 20, 10, key='top_n_sales')
            top_cat_filter = st.selectbox(
                "Filter Category",
                ['All'] + sorted(filtered_df['category'].unique().tolist()),
                key='top_cat'
            )
            
            chart_df = filtered_df.copy()
            if top_cat_filter != 'All':
                chart_df = chart_df[chart_df['category'] == top_cat_filter]
            
            top_stores = chart_df.groupby('store_name').agg({
                'sales_aed': 'sum',
                'category': 'first'
            }).nlargest(top_n_sales, 'sales_aed').reset_index()
            
            fig = go.Figure(go.Bar(
                x=top_stores['sales_aed'],
                y=top_stores['store_name'],
                orientation='h',
                marker=dict(
                    color=top_stores['sales_aed'],
                    colorscale=[[0, '#E5E7EB'], [0.5, '#DAA520'], [1, '#B8860B']],
                    line=dict(color='#1A1A2E', width=1)
                ),
                text=[format_currency(x) for x in top_stores['sales_aed']],
                textposition='inside',
                textfont=dict(color='#1A1A2E', size=11, family='Poppins'),
                hovertemplate="<b>%{y}</b><br>Sales: %{text}<extra></extra>"
            ))
            
            fig = apply_chart_theme(fig, height=500)
            fig.update_layout(yaxis=dict(categoryorder='total ascending'))
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📈 Top Stores by Conversion</div>', unsafe_allow_html=True)
            
            # Filter
            top_n_conv = st.slider("Number of Stores", 5, 20, 10, key='top_n_conv')
            conv_cat_filter = st.selectbox(
                "Filter Category",
                ['All'] + sorted(filtered_df['category'].unique().tolist()),
                key='conv_cat'
            )
            
            chart_df = filtered_df.copy()
            if conv_cat_filter != 'All':
                chart_df = chart_df[chart_df['category'] == conv_cat_filter]
            
            conv_stores = chart_df.groupby('store_name').agg({
                'conversion_rate': 'mean',
                'category': 'first'
            }).nlargest(top_n_conv, 'conversion_rate').reset_index()
            conv_stores['conv_pct'] = conv_stores['conversion_rate'] * 100
            
            fig = go.Figure(go.Bar(
                x=conv_stores['conv_pct'],
                y=conv_stores['store_name'],
                orientation='h',
                marker=dict(
                    color=conv_stores['conv_pct'],
                    colorscale=[[0, '#E5E7EB'], [0.5, '#4ADE80'], [1, '#059669']],
                    line=dict(color='#1A1A2E', width=1)
                ),
                text=[f"{x:.1f}%" for x in conv_stores['conv_pct']],
                textposition='inside',
                textfont=dict(color='#1A1A2E', size=11, family='Poppins'),
                hovertemplate="<b>%{y}</b><br>Conversion: %{text}<extra></extra>"
            ))
            
            fig = apply_chart_theme(fig, height=500)
            fig.update_layout(yaxis=dict(categoryorder='total ascending'), xaxis_title='Conversion Rate (%)')
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Store Performance Table
        if show_raw_data:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📋 Store Performance Matrix</div>', unsafe_allow_html=True)
            
            store_matrix = filtered_df.groupby(['store_name', 'category', 'floor']).agg({
                'sales_aed': 'sum',
                'transactions': 'sum',
                'store_footfall': 'sum',
                'conversion_rate': 'mean',
                'avg_basket_aed': 'mean'
            }).reset_index()
            
            store_matrix['conversion_rate'] = (store_matrix['conversion_rate'] * 100).round(1)
            store_matrix['sales_aed'] = store_matrix['sales_aed'].apply(lambda x: f"AED {x:,.0f}")
            store_matrix['avg_basket_aed'] = store_matrix['avg_basket_aed'].apply(lambda x: f"AED {x:,.0f}")
            store_matrix['conversion_rate'] = store_matrix['conversion_rate'].apply(lambda x: f"{x}%")
            
            store_matrix.columns = ['Store', 'Category', 'Floor', 'Total Sales', 'Transactions', 
                                   'Footfall', 'Conversion', 'Avg Basket']
            
            st.dataframe(store_matrix, use_container_width=True, height=400)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================
    # TAB 4: CATEGORY ANALYSIS
    # ========================================
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📊 Category Performance</div>', unsafe_allow_html=True)
            
            perf_metric = st.selectbox(
                "Select Metric",
                ['Total Sales', 'Avg Basket', 'Conversion Rate', 'Transactions'],
                key='cat_metric'
            )
            
            metric_map = {
                'Total Sales': ('sales_aed', 'sum'),
                'Avg Basket': ('avg_basket_aed', 'mean'),
                'Conversion Rate': ('conversion_rate', 'mean'),
                'Transactions': ('transactions', 'sum')
            }
            
            col_name, agg_func = metric_map[perf_metric]
            cat_perf = filtered_df.groupby('category')[col_name].agg(agg_func).sort_values(ascending=True)
            
            if perf_metric == 'Conversion Rate':
                cat_perf = cat_perf * 100
                text_vals = [f"{x:.1f}%" for x in cat_perf.values]
            elif perf_metric in ['Total Sales', 'Avg Basket']:
                text_vals = [format_currency(x) for x in cat_perf.values]
            else:
                text_vals = [format_number(x) for x in cat_perf.values]
            
            fig = go.Figure(go.Bar(
                x=cat_perf.values,
                y=cat_perf.index,
                orientation='h',
                marker_color=CHART_COLORS[:len(cat_perf)],
                text=text_vals,
                textposition='inside',
                textfont=dict(color='#FFFFFF', size=12, family='Poppins')
            ))
            
            fig = apply_chart_theme(fig, height=400)
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🎯 Category Radar</div>', unsafe_allow_html=True)
            
            radar_cats = st.multiselect(
                "Select Categories to Compare",
                filtered_df['category'].unique().tolist(),
                default=filtered_df['category'].unique().tolist()[:4],
                key='radar_cats'
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
                
                # Normalize
                for col in ['sales_aed', 'transactions', 'conversion_rate', 'avg_basket_aed', 'sales_per_sqft']:
                    max_val = cat_metrics[col].max()
                    if max_val > 0:
                        cat_metrics[f'{col}_norm'] = cat_metrics[col] / max_val * 100
                
                categories_list = ['Sales', 'Transactions', 'Conversion', 'Avg Basket', 'Sales/Sqft']
                
                fig = go.Figure()
                
                for idx, (_, row) in enumerate(cat_metrics.iterrows()):
                    values = [
                        row['sales_aed_norm'],
                        row['transactions_norm'],
                        row['conversion_rate_norm'],
                        row['avg_basket_aed_norm'],
                        row['sales_per_sqft_norm']
                    ]
                    values.append(values[0])
                    
                    fig.add_trace(go.Scatterpolar(
                        r=values,
                        theta=categories_list + [categories_list[0]],
                        name=row['category'],
                        line=dict(color=CHART_COLORS[idx % len(CHART_COLORS)], width=3),
                        fill='toself',
                        fillcolor=f'rgba({int(CHART_COLORS[idx % len(CHART_COLORS)][1:3], 16)}, {int(CHART_COLORS[idx % len(CHART_COLORS)][3:5], 16)}, {int(CHART_COLORS[idx % len(CHART_COLORS)][5:7], 16)}, 0.15)'
                    ))
                
                fig = apply_chart_theme(fig, height=400)
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(0,0,0,0.1)'),
                        angularaxis=dict(gridcolor='rgba(0,0,0,0.1)', tickfont=dict(size=11))
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Heatmap
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🗓️ Sales Heatmap: Category × Day</div>', unsafe_allow_html=True)
        
        heatmap_value = st.selectbox(
            "Heatmap Value",
            ['Total Sales', 'Avg Sales', 'Transactions'],
            key='hm_value'
        )
        
        agg_map = {'Total Sales': 'sum', 'Avg Sales': 'mean', 'Transactions': 'sum'}
        col_map = {'Total Sales': 'sales_aed', 'Avg Sales': 'sales_aed', 'Transactions': 'transactions'}
        
        heatmap_data = filtered_df.pivot_table(
            values=col_map[heatmap_value],
            index='category',
            columns='day_name',
            aggfunc=agg_map[heatmap_value]
        )
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = heatmap_data[[d for d in day_order if d in heatmap_data.columns]]
        
        fig = go.Figure(go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale=[[0, '#FEF3C7'], [0.5, '#F59E0B'], [1, '#B45309']],
            hovertemplate='<b>%{y}</b><br>%{x}: %{z:,.0f}<extra></extra>',
            colorbar=dict(title=heatmap_value, tickfont=dict(color='#1A1A2E'))
        ))
        
        fig = apply_chart_theme(fig, height=400)
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========================================
    # TAB 5: DEEP INSIGHTS
    # ========================================
    with tab5:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">🏢 Floor Performance</div>', unsafe_allow_html=True)
            
            floor_metric = st.selectbox(
                "Metric",
                ['Sales', 'Footfall', 'Transactions', 'Conversion'],
                key='floor_metric'
            )
            
            metric_cols = {
                'Sales': 'sales_aed',
                'Footfall': 'store_footfall',
                'Transactions': 'transactions',
                'Conversion': 'conversion_rate'
            }
            
            floor_perf = filtered_df.groupby('floor').agg({
                metric_cols[floor_metric]: 'sum' if floor_metric != 'Conversion' else 'mean'
            }).reset_index()
            
            floor_order = {'LG': 0, 'G': 1, '1': 2, '2': 3, '3': 4}
            floor_perf['order'] = floor_perf['floor'].map(floor_order)
            floor_perf = floor_perf.sort_values('order')
            floor_perf['label'] = floor_perf['floor'].map({
                'LG': 'Lower Ground', 'G': 'Ground', '1': 'Level 1', '2': 'Level 2', '3': 'Level 3'
            })
            
            if floor_metric == 'Conversion':
                floor_perf[metric_cols[floor_metric]] *= 100
                text_vals = [f"{x:.1f}%" for x in floor_perf[metric_cols[floor_metric]]]
            elif floor_metric == 'Sales':
                text_vals = [format_currency(x) for x in floor_perf[metric_cols[floor_metric]]]
            else:
                text_vals = [format_number(x) for x in floor_perf[metric_cols[floor_metric]]]
            
            fig = go.Figure(go.Bar(
                x=floor_perf['label'],
                y=floor_perf[metric_cols[floor_metric]],
                marker_color=['#1A1A2E', '#B8860B', '#2563EB', '#059669', '#7C3AED'][:len(floor_perf)],
                text=text_vals,
                textposition='outside',
                textfont=dict(color='#1A1A2E', size=12, family='Poppins')
            ))
            
            fig = apply_chart_theme(fig, height=380)
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">💵 Rent vs Revenue</div>', unsafe_allow_html=True)
            
            rent_cat = st.selectbox(
                "Category Filter",
                ['All'] + sorted(filtered_df['category'].unique().tolist()),
                key='rent_cat'
            )
            
            rent_df = filtered_df.copy()
            if rent_cat != 'All':
                rent_df = rent_df[rent_df['category'] == rent_cat]
            
            rent_revenue = rent_df.groupby('store_name').agg({
                'annual_base_rent_aed': 'first',
                'sales_aed': 'sum',
                'category': 'first'
            }).reset_index()
            
            days_in_data = rent_df['date'].nunique()
            rent_revenue['annualized_sales'] = rent_revenue['sales_aed'] * (365 / max(days_in_data, 1))
            
            fig = px.scatter(
                rent_revenue,
                x='annual_base_rent_aed',
                y='annualized_sales',
                color='category',
                hover_name='store_name',
                color_discrete_sequence=CHART_COLORS
            )
            
            # Break-even line
            max_rent = rent_revenue['annual_base_rent_aed'].max()
            fig.add_trace(go.Scatter(
                x=[0, max_rent],
                y=[0, max_rent * 10],
                mode='lines',
                name='10% Rent Ratio',
                line=dict(color='#DC2626', dash='dash', width=2)
            ))
            
            fig = apply_chart_theme(fig, height=380)
            fig.update_layout(
                xaxis_title='Annual Rent (AED)',
                yaxis_title='Annualized Sales (AED)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Key Insights
        st.markdown('<div class="section-header">💡 Key Insights & Recommendations</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        best_day = filtered_df.groupby('day_name')['sales_aed'].sum().idxmax()
        best_category = filtered_df.groupby('category')['sales_aed'].sum().idxmax()
        best_store = filtered_df.groupby('store_name')['sales_aed'].sum().idxmax()
        avg_tourist = filtered_df['tourist_share'].mean() * 100
        
        with col1:
            st.markdown(f"""
            <div class="insight-card">
                <h4>🏆 Peak Performance</h4>
                <p><strong>Best Day:</strong> {best_day}</p>
                <p><strong>Top Category:</strong> {best_category}</p>
                <p><strong>Top Store:</strong> {best_store}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="insight-card">
                <h4>🌍 Visitor Analysis</h4>
                <p><strong>Tourist Share:</strong> {avg_tourist:.1f}%</p>
                <p><strong>Resident Share:</strong> {100-avg_tourist:.1f}%</p>
                <p><strong>Weekend Uplift:</strong> ~18%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_stores = filtered_df['store_name'].nunique()
            total_categories = filtered_df['category'].nunique()
            st.markdown(f"""
            <div class="insight-card">
                <h4>📊 Portfolio Summary</h4>
                <p><strong>Active Stores:</strong> {total_stores}</p>
                <p><strong>Categories:</strong> {total_categories}</p>
                <p><strong>Avg Conversion:</strong> {avg_conversion:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
    
    # ========================================
    # FOOTER
    # ========================================
    st.markdown("""
    <div class="custom-footer">
        <p><span class="gold-text">🏬 Dubai Mall Analytics Dashboard</span></p>
        <p>Premium Retail Intelligence Platform • Projector-Ready Edition</p>
        <p style="font-size: 0.85rem; margin-top: 15px; color: #64748B;">
            © 2024 Dubai Mall Management | Dashboard v2.0
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# RUN
# ============================================
if __name__ == "__main__":
    main()
