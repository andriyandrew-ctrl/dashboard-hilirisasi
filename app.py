import streamlit as st
import pandas as pd
import plotly.express as px

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Hilirisasi Digital Dashboard V3",
    page_icon="📈",
    layout="wide"
)

# Custom CSS untuk tampilan lebih elegan
st.markdown("""
    <style>
    .metric-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e6e9ef;
        text-align: center;
    }
    .percentage-text {
        font-size: 24px;
        font-weight: bold;
        color: #1E3A8A;
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
        df = pd.read_excel(file_name, sheet_name='Input Data')
        # Pastikan kolom numerik benar
        cols = ['TONASE', 'REVENUE', 'GROSS PROFIT']
        for col in cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        # Pastikan kolom waktu terbaca
        df['MONTH'] = pd.to_datetime(df['MONTH'])
        return df
    except Exception as e:
        st.error(f"Gagal memuat file Excel: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    st.title("📊 Hilirisasi Strategic Dashboard - V3")
    
    # --- SIDEBAR FILTER ---
    st.sidebar.header("⚙️ Filter Data")
    list_tahun = sorted(df['YEARLY'].unique(), reverse=True)
    sel_tahun = st.sidebar.selectbox("Pilih Tahun", list_tahun)
    df_year = df[df['YEARLY'] == sel_tahun].copy()

    # --- MEMBUAT TAB ---
    tab1, tab2 = st.tabs(["📅 Monthly Report", "🌓 Semester Comparison"])

    # --- TAB 1: MONTHLY REPORT ---
    with tab1:
        list_bulan = ["January", "February", "March", "April", "May", "June", 
                      "July", "August", "September", "October", "November", "December"]
        available_months = df_year['MONTHLY'].unique()
        sel_bulan = st.selectbox("Pilih Bulan", [m for m in list_bulan if m in available_months])
        df_month = df_year[df_year['MONTHLY'] == sel_bulan]

        # Metrics & Charts (Sama seperti sebelumnya)
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Tonase", f"{df_month['TONASE'].sum():,.2f} Ton")
        m2.metric("Total Revenue", f"Rp {df_month['REVENUE'].sum():,.0f}")
        m3.metric("Total Gross Profit", f"Rp {df_month['GROSS PROFIT'].sum():,.0f}")
        
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            fig_rev = px.bar(df_month.sort_values('REVENUE'), x='REVENUE', y='PRODUCT', color='SUBSIDIARY', orientation='h', title="Revenue per Produk")
            st.plotly_chart(fig_rev, use_container_width=True)
        with c2:
            fig_qty = px.bar(df_month.sort_values('TONASE'), x='TONASE', y='PRODUCT', color='SUBSIDIARY', orientation='h', title="Tonase per Produk")
            st.plotly_chart(fig_qty, use_container_width=True)

    # --- TAB 2: SEMESTER COMPARISON ---
    with tab2:
        st.subheader(f"Analisis Performa Semester - {sel_tahun}")
        
        # 1. PERHITUNGAN PERSENTASE
        df_sem = df_year.groupby('SEMESTER')[['TONASE', 'REVENUE', 'GROSS PROFIT']].sum().reset_index()
        total_rev = df_sem['REVENUE'].sum()
        
        # Hitung % kontribusi masing-masing semester
        p1, p2 = st.columns(2)
        for i, row in df_sem.iterrows():
            pct = (row['REVENUE'] / total_rev * 100) if total_rev > 0 else 0
            with (p1 if row['SEMESTER'] == 'SMT-1' else p2):
                st.markdown(f"""
                <div class="metric-container">
                    <p style="margin:0; color:gray;">Kontribusi Revenue {row['SEMESTER']}</p>
                    <p class="percentage-text">{pct:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)

        st.write("") # Spasi
        
        # 2. BAR CHART (Perbandingan)
        s1, s2, s3 = st.columns(3)
        with s1:
            st.plotly_chart(px.bar(df_sem, x='SEMESTER', y='TONASE', color='SEMESTER', title="Tonase (Ton)", text_auto='.2f'), use_container_width=True)
        with s2:
            st.plotly_chart(px.bar(df_sem, x='SEMESTER', y='REVENUE', color='SEMESTER', title="Revenue (Rp)", text_auto='.2s'), use_container_width=True)
        with s3:
            st.plotly_chart(px.bar(df_sem, x='SEMESTER', y='GROSS PROFIT', color='SEMESTER', title="Gross Profit (Rp)", text_auto='.2s'), use_container_width=True)

        st.markdown("---")

        # 3. LINE CHART (Tren Bulanan)
        st.subheader("📈 Tren Bulanan (Timeline)")
        # Mengurutkan data berdasarkan bulan agar line chart tidak acak
        df_trend = df_year.groupby(['MONTH', 'MONTHLY'])[['TONASE', 'REVENUE', 'GROSS PROFIT']].sum().reset_index()
        df_trend = df_trend.sort_values('MONTH')

        # Pilihan metrik untuk Line Chart
        metrik_pilihan = st.radio("Pilih Data Tren:", ["REVENUE", "TONASE", "GROSS PROFIT"], horizontal=True)
        
        fig_line = px.line(df_trend, x='MONTHLY', y=metrik_pilihan, 
                           title=f"Tren {metrik_pilihan} dari Bulan ke Bulan",
                           markers=True, line_shape='linear',
                           labels={'MONTHLY': 'Bulan', metrik_pilihan: 'Nilai'})
        
        # Menambahkan area di bawah garis agar lebih cantik
        fig_line.update_traces(fill='tozeroy')
        st.plotly_chart(fig_line, use_container_width=True)

else:
    st.error("Data tidak ditemukan. Pastikan file 'Dashboard Hilirisasi V2.xlsx' sudah di-upload ke GitHub.")
