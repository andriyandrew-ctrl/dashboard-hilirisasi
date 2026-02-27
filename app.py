import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Hilirisasi Digital Dashboard",
    page_icon="📈",
    layout="wide"
)

# Custom CSS untuk tampilan profesional
st.markdown("""
    <style>
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #f0f2f6;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f8f9fa;
        border-radius: 5px 5px 0px 0px;
        gap: 1px;
        padding-top: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E3A8A !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNGSI LOAD DATA
@st.cache_data
def load_data():
    file_name = 'Dashboard Hilirisasi V2.xlsx'
    try:
        # Membaca sheet 'Input Data' yang sudah bersih
        df = pd.read_excel(file_name, sheet_name='Input Data')
        
        # Pastikan kolom numerik tidak error
        cols = ['TONASE', 'REVENUE', 'GROSS PROFIT']
        for col in cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
        # Pastikan kolom waktu terbaca
        df['MONTH'] = pd.to_datetime(df['MONTH'])
        return df
    except Exception as e:
        st.error(f"Gagal memuat file Excel: {e}")
        return pd.DataFrame()

# 3. LOGIKA APLIKASI
df = load_data()

if not df.empty:
    st.title("📊 Hilirisasi Strategic Dashboard")
    
    # --- SIDEBAR FILTER ---
    st.sidebar.header("⚙️ Filter Data")
    list_tahun = sorted(df['YEARLY'].unique(), reverse=True)
    sel_tahun = st.sidebar.selectbox("Pilih Tahun", list_tahun)
    
    # Filter Data berdasarkan Tahun
    df_year = df[df['YEARLY'] == sel_tahun]

    # --- MEMBUAT TAB ---
    tab1, tab2 = st.tabs(["📅 Monthly Report", "🌓 Semester Comparison"])

    # --- TAB 1: MONTHLY REPORT ---
    with tab1:
        list_bulan = ["January", "February", "March", "April", "May", "June", 
                      "July", "August", "September", "October", "November", "December"]
        # Hanya ambil bulan yang ada datanya di tahun tersebut
        available_months = df_year['MONTHLY'].unique()
        sel_bulan = st.selectbox("Pilih Bulan Berjalan", [m for m in list_bulan if m in available_months])
        
        df_month = df_year[df_year['MONTHLY'] == sel_bulan]

        # Row 1: Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Tonase", f"{df_month['TONASE'].sum():,.2f} Ton")
        m2.metric("Total Revenue", f"Rp {df_month['REVENUE'].sum():,.0f}")
        m3.metric("Total Gross Profit", f"Rp {df_month['GROSS PROFIT'].sum():,.0f}")

        st.markdown("---")
        
        # Row 2: Highlights
        if not df_month.empty:
            c1, c2 = st.columns(2)
            top_rev = df_month.loc[df_month['REVENUE'].idxmax()]
            top_qty = df_month.loc[df_month['TONASE'].idxmax()]
            
            with c1:
                st.info(f"🏆 **Revenue Tertinggi:** {top_rev['PRODUCT']} \n\n (Sellers: {top_rev['SUBSIDIARY']})")
            with c2:
                st.success(f"📦 **Tonase Tertinggi:** {top_qty['PRODUCT']} \n\n ({top_qty['TONASE']:,.2f} Ton)")

            # Row 3: Charts
            chart_col1, chart_col2 = st.columns(2)
            with chart_col1:
                fig_rev = px.bar(df_month.sort_values('REVENUE'), x='REVENUE', y='PRODUCT', 
                                 color='SUBSIDIARY', orientation='h', title="Revenue per Produk",
                                 text_auto='.2s', template="plotly_white")
                st.plotly_chart(fig_rev, use_container_width=True)
            with chart_col2:
                fig_qty = px.bar(df_month.sort_values('TONASE'), x='TONASE', y='PRODUCT', 
                                 color='SUBSIDIARY', orientation='h', title="Tonase per Produk",
                                 text_auto='.2f', template="plotly_white")
                st.plotly_chart(fig_qty, use_container_width=True)
        else:
            st.warning("Data tidak tersedia untuk bulan ini.")

    # --- TAB 2: SEMESTER COMPARISON ---
    with tab2:
        st.subheader(f"Perbandingan Performa Semester - Tahun {sel_tahun}")
        
        # Agregasi data per Semester
        df_sem = df_year.groupby('SEMESTER')[['TONASE', 'REVENUE', 'GROSS PROFIT']].sum().reset_index()
        
        # Perbaikan urutan semester agar SMT-1 muncul duluan
        df_sem = df_sem.sort_values('SEMESTER')

        # Visualisasi Semester (3 Grafik Berdampingan)
        s1, s2, s3 = st.columns(3)
        
        with s1:
            fig_s1 = px.bar(df_sem, x='SEMESTER', y='TONASE', color='SEMESTER',
                            title="Perbandingan Tonase (Ton)", text_auto='.2f',
                            color_discrete_map={"SMT-1": "#3498db", "SMT-2": "#2ecc71"})
            st.plotly_chart(fig_s1, use_container_width=True)
            
        with s2:
            fig_s2 = px.bar(df_sem, x='SEMESTER', y='REVENUE', color='SEMESTER',
                            title="Perbandingan Revenue (Rp)", text_auto='.2s',
                            color_discrete_map={"SMT-1": "#3498db", "SMT-2": "#2ecc71"})
            st.plotly_chart(fig_s2, use_container_width=True)
            
        with s3:
            fig_s3 = px.bar(df_sem, x='SEMESTER', y='GROSS PROFIT', color='SEMESTER',
                            title="Perbandingan Profit (Rp)", text_auto='.2s',
                            color_discrete_map={"SMT-1": "#3498db", "SMT-2": "#2ecc71"})
            st.plotly_chart(fig_s3, use_container_width=True)

        # Tabel Perbandingan Angka
        st.write("### Detail Angka Per Semester")
        st.table(df_sem.style.format({
            'TONASE': '{:,.2f}',
            'REVENUE': 'Rp {:,.0f}',
            'GROSS PROFIT': 'Rp {:,.0f}'
        }))

else:
    st.error("Data tidak ditemukan. Pastikan file 'Dashboard Hilirisasi V2.xlsx' sudah di-upload ke GitHub.")
