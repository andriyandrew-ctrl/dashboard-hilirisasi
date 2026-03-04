import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Hilirisasi Strategic Dashboard",
    page_icon="📈",
    layout="wide"
)

# --- 2. CSS CUSTOM (SOLUSI SIDEBAR & HAPUS GITHUB) ---
st.markdown("""
    <style>
    /* Menghilangkan dekorasi warna di bagian paling atas */
    header {
        background-color: rgba(0,0,0,0) !important;
    }

    /* Menghilangkan Logo GitHub dan Menu (Tiga Titik) secara spesifik */
    /* Namun tetap membiarkan area tombol Sidebar bisa diklik */
    [data-testid="stHeader"] > div:first-child {
        visibility: hidden !important;
    }

    /* Memastikan tombol Sidebar (panah >) tetap terlihat dan berwarna agar mudah ditemukan */
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        background-color: #f0f2f6 !important;
        border-radius: 0 10px 10px 0 !important;
        width: 40px !important;
        height: 40px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        left: 0 !important;
        top: 0 !important;
    }

    /* Menghilangkan Footer 'Made with Streamlit' */
    footer {visibility: hidden !important;}

    /* Style Kartu Metrik & Highlight */
    .year-metric {
        background-color: #1E3A8A;
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
    }
    .highlight-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-left: 5px solid #1E3A8A;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E3A8A !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNGSI LOAD DATA ---
@st.cache_data
def load_data():
    file_name = 'Dashboard Hilirisasi V2.xlsx'
    try:
        df = pd.read_excel(file_name, sheet_name='Input Data')
        for col in ['TONASE', 'REVENUE', 'GROSS PROFIT']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        df['MONTH'] = pd.to_datetime(df['MONTH'])
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    st.title("🚀 Hilirisasi Strategic Dashboard")
    
    # --- SIDEBAR ---
    st.sidebar.header("⚙️ Global Filter")
    list_tahun = sorted(df['YEARLY'].unique(), reverse=True)
    sel_tahun = st.sidebar.selectbox("Pilih Tahun", list_tahun)
    df_year = df[df['YEARLY'] == sel_tahun].copy()

    # --- RINGKASAN TAHUNAN ---
    st.subheader(f"📊 Ringkasan Performa Tahun {sel_tahun}")
    yt1, yt2, yt3 = st.columns(3)
    yt1.markdown(f'<div class="year-metric"><b>TOTAL TONASE</b><br><span style="font-size:24px;">{df_year["TONASE"].sum():,.2f} Ton</span></div>', unsafe_allow_html=True)
    yt2.markdown(f'<div class="year-metric"><b>TOTAL REVENUE</b><br><span style="font-size:24px;">Rp {df_year["REVENUE"].sum():,.0f}</span></div>', unsafe_allow_html=True)
    yt3.markdown(f'<div class="year-metric"><b>TOTAL PROFIT</b><br><span style="font-size:24px;">Rp {df_year["GROSS PROFIT"].sum():,.0f}</span></div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📅 Monthly Report", "🌓 Semester Comparison"])

    with tab1:
        st.subheader("Laporan Bulanan")
        list_bulan = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        available_months = df_year['MONTHLY'].unique()
        sel_bulan = st.selectbox("Pilih Bulan", [m for m in list_bulan if m in available_months])
        df_month = df_year[df_year['MONTHLY'] == sel_bulan]

        if not df_month.empty:
            m1, m2, m3 = st.columns(3)
            m1.metric("Tonase", f"{df_month['TONASE'].sum():,.2f} Ton")
            m2.metric("Revenue", f"Rp {df_month['REVENUE'].sum():,.0f}")
            m3.metric("Profit", f"Rp {df_month['GROSS PROFIT'].sum():,.0f}")

            st.markdown("---")
            h1, h2 = st.columns(2)
            top_qty = df_month.loc[df_month['TONASE'].idxmax()]
            top_profit = df_month.loc[df_month['GROSS PROFIT'].idxmax()]
            
            h1.markdown(f'<div class="highlight-card"><b>📦 Top Product (Tonase)</b><br>{top_qty["PRODUCT"]}<br>{top_qty["TONASE"]:,.2f} Ton</div>', unsafe_allow_html=True)
            h2.markdown(f'<div class="highlight-card"><b>💰 Top Profit (Product)</b><br>{top_profit["PRODUCT"]}<br>Rp {top_profit["GROSS PROFIT"]:,.0f}</div>', unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1: st.plotly_chart(px.bar(df_month.sort_values('REVENUE'), x='REVENUE', y='PRODUCT', color='SUBSIDIARY', orientation='h', title="Revenue per Produk"), use_container_width=True)
            with c2: st.plotly_chart(px.bar(df_month.sort_values('TONASE'), x='TONASE', y='PRODUCT', color='SUBSIDIARY', orientation='h', title="Tonase per Produk"), use_container_width=True)

    with tab2:
        st.subheader(f"Analisis Semester {sel_tahun}")
        df_sem = df_year.groupby('SEMESTER')[['TONASE', 'REVENUE', 'GROSS PROFIT']].sum().reset_index()
        s1, s2, s3 = st.columns(3)
        with s1: st.plotly_chart(px.bar(df_sem, x='SEMESTER', y='TONASE', color='SEMESTER', title="Tonase"), use_container_width=True)
        with s2: st.plotly_chart(px.bar(df_sem, x='SEMESTER', y='REVENUE', color='SEMESTER', title="Revenue"), use_container_width=True)
        with s3: st.plotly_chart(px.bar(df_sem, x='SEMESTER', y='GROSS PROFIT', color='SEMESTER', title="Profit"), use_container_width=True)
else:
    st.error("Data tidak ditemukan.")
