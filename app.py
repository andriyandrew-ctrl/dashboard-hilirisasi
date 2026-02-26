import streamlit as st
import pandas as pd
import plotly.express as px

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Dashboard Monitoring Hilirisasi",
    page_icon="📊",
    layout="wide"
)

# Custom CSS untuk mempercantik tampilan
st.markdown("""
    <style>
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    h1 {
        color: #1E3A8A;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNGSI LOAD DATA
@st.cache_data
def load_data():
    file_name = 'KBK_Hilirisasi 2025 Full Year (Sent).xlsx'
    try:
        # Load data, lewati header atas (skiprows=6)
        df = pd.read_excel(file_name, sheet_name='Realisasi Hilirisasi', skiprows=6)
        
        # Bersihkan data
        df = df.dropna(subset=['Periode', 'Jenis Produk'])
        
        # Pastikan kolom numerik benar
        cols_to_fix = ['Qty', 'Revenue', 'Gross Profit']
        for col in cols_to_fix:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
        return df
    except Exception as e:
        st.error(f"Gagal membaca file: {e}")
        return pd.DataFrame()

# 3. LOGIKA UTAMA
df = load_data()

if not df.empty:
    st.title("📊 Monitoring Realisasi Hilirisasi")
    
    # --- SIDEBAR FILTER ---
    st.sidebar.header("📁 Filter Laporan")
    
    # Cek kolom Tahun
    if 'Tahun' in df.columns:
        list_tahun = sorted(df['Tahun'].unique().astype(int), reverse=True)
    else:
        df['Tahun'] = 2025
        list_tahun = [2025]
        
    sel_tahun = st.sidebar.selectbox("📅 Pilih Tahun", list_tahun)
    
    nama_bulan = {
        1:"Januari", 2:"Februari", 3:"Maret", 4:"April", 5:"Mei", 6:"Juni",
        7:"Juli", 8:"Agustus", 9:"September", 10:"Oktober", 11:"November", 12:"Desember"
    }
    
    df_tahun = df[df['Tahun'] == sel_tahun]
    list_bulan = sorted(df_tahun['Periode'].unique().astype(int))
    sel_bulan = st.sidebar.selectbox("📆 Pilih Bulan", list_bulan, format_func=lambda x: nama_bulan[x])

    # Data Filtered
    df_f = df_tahun[df_tahun['Periode'] == sel_bulan].copy()

    if not df_f.empty:
        # --- METRIK TOTAL ---
        st.subheader(f"📍 Ringkasan: {nama_bulan[sel_bulan]} {sel_tahun}")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Tonase", f"{df_f['Qty'].sum():,.2f} Ton")
        m2.metric("Total Revenue", f"Rp {df_f['Revenue'].sum():,.0f}")
        m3.metric("Total Gross Profit", f"Rp {df_f['Gross Profit'].sum():,.0f}")

        st.divider()

        # --- HIGHLIGHT TERTINGGI ---
        st.subheader("🏆 Pencapaian Tertinggi")
        c1, c2, c3 = st.columns(3)
        
        idx_rev = df_f['Revenue'].idxmax()
        idx_qty = df_f['Qty'].idxmax()
        
        with c1:
            st.info(f"**Revenue Terbesar:**\n\n{df_f.loc[idx_rev, 'Jenis Produk']} (Rp {df_f.loc[idx_rev, 'Revenue']:,.0f})")
        with c2:
            st.success(f"**Tonase Terbesar:**\n\n{df_f.loc[idx_qty, 'Jenis Produk']} ({df_f.loc[idx_qty, 'Qty']:,.2f} Ton)")
        with c3:
            st.warning(f"**Top Entitas:**\n\n{df_f.loc[idx_rev, 'Entitas']}")

        # --- GRAFIK ---
        st.subheader("📈 Analisis Visual")
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            fig_rev = px.bar(df_f.sort_values('Revenue'), x='Revenue', y='Jenis Produk', 
                             color='Entitas', orientation='h', title="Revenue per Produk",
                             text_auto='.2s')
            st.plotly_chart(fig_rev, use_container_width=True)

        with col_chart2:
            fig_qty = px.bar(df_f.sort_values('Qty'), x='Qty', y='Jenis Produk', 
                             color='Entitas', orientation='h', title="Tonase per Produk",
                             text_auto='.2f')
            st.plotly_chart(fig_qty, use_container_width=True)

        # --- TABEL DETAIL (BAGIAN YANG DIPERBAIKI) ---
        with st.expander("🔍 Klik untuk lihat detail data mentah"):
            st.dataframe(df_f, use_container_width=True)
            
    else:
        st.warning(f"Data tidak ditemukan.")
else:
    st.error("File Excel belum terbaca dengan benar.")
