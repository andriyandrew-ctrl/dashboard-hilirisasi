import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. KONFIGURASI HALAMAN ---
# Harus dipanggil pertama kali sebelum elemen UI lainnya
st.set_page_config(
    page_title="Hilirisasi Strategic Dashboard",
    page_icon="📈",
    layout="wide"
)

# --- 2. CSS CUSTOM (Hapus Logo GitHub & Rapikan UI) ---
st.markdown("""
    <style>
    /* Menghilangkan elemen spesifik di dalam header (Logo GitHub & Menu) */
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0) !important;
    }
    
    /* Target agar logo GitHub & menu kanan hilang */
    [data-testid="stHeader"] > div:first-child {
        visibility: hidden !important;
    }

    /* Memastikan tombol kontrol Sidebar (panah) tetap terlihat saat sidebar tertutup */
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        background-color: #f0f2f6 !important;
        border-radius: 50% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }

    /* Menghilangkan Footer 'Made with Streamlit' */
    footer {visibility: hidden !important;}

    /* Menyesuaikan jarak konten agar tidak terpotong header transparan */
    .block-container {
        padding-top: 2rem !important;
    }

    /* Style Kartu Metrik Tahunan */
    .year-metric {
        background-color: #1E3A8A;
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Style Kartu Highlight Product/Profit */
    .highlight-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-left: 5px solid #1E3A8A;
        border-radius: 5px;
        margin-bottom: 10px;
    }

    /* Warna Tab yang aktif */
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
        # Load data dari sheet 'Input Data'
        df = pd.read_excel(file_name, sheet_name='Input Data')
        # Konversi kolom angka
        for col in ['TONASE', 'REVENUE', 'GROSS PROFIT']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        # Pastikan kolom waktu terformat benar
        df['MONTH'] = pd.to_datetime(df['MONTH'])
        return df
    except Exception as e:
        st.error(f"Gagal memuat file Excel: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    st.title("🚀 Hilirisasi Strategic Dashboard")
    
    # --- SIDEBAR FILTER ---
    st.sidebar.header("⚙️ Global Filter")
    list_tahun = sorted(df['YEARLY'].unique(), reverse=True)
    sel_tahun = st.sidebar.selectbox("Pilih Tahun Analisis", list_tahun)
    df_year = df[df['YEARLY'] == sel_tahun].copy()

    # --- SECTION: TOTAL TAHUNAN ---
    st.subheader(f"📊 Ringkasan Performa Seluruh Tahun {sel_tahun}")
    yt1, yt2, yt3 = st.columns(3)
    
    yt1.markdown(f'<div class="year-metric"><b>TOTAL TONASE TAHUNAN</b><br><span style="font-size:24px;">{df_year["TONASE"].sum():,.2f} Ton</span></div>', unsafe_allow_html=True)
    yt2.markdown(f'<div class="year-metric"><b>TOTAL REVENUE TAHUNAN</b><br><span style="font-size:24px;">Rp {df_year["REVENUE"].sum():,.0f}</span></div>', unsafe_allow_html=True)
    yt3.markdown(f'<div class="year-metric"><b>TOTAL PROFIT TAHUNAN</b><br><span style="font-size:24px;">Rp {df_year["GROSS PROFIT"].sum():,.0f}</span></div>', unsafe_allow_html=True)

    # --- TABS ---
    tab1, tab2 = st.tabs(["📅 Monthly Report", "🌓 Semester Comparison"])

    # TAB 1: MONTHLY REPORT
    with tab1:
        st.subheader("Laporan Detail Bulanan")
        list_bulan = ["January", "February", "March", "April", "May", "June", 
                      "July", "August", "September", "October", "November", "December"]
        available_months = df_year['MONTHLY'].unique()
        sel_bulan = st.selectbox("Pilih Bulan", [m for m in list_bulan if m in available_months])
        
        df_month = df_year[df_year['MONTHLY'] == sel_bulan]

        m1, m2, m3 = st.columns(3)
        m1.metric("Tonase", f"{df_month['TONASE'].sum():,.2f} Ton")
        m2.metric("Revenue", f"Rp {df_month['REVENUE'].sum():,.0f}")
        m3.metric("Profit", f"Rp {df_month['GROSS PROFIT'].sum():,.0f}")

        st.markdown("---")
        
        if not df_month.empty:
            h1, h2 = st.columns(2)
            top_qty_row = df_month.loc[df_month['TONASE'].idxmax()]
            top_profit_row = df_month.loc[df_month['GROSS PROFIT'].idxmax()]
            
            with h1:
                st.markdown(f"""
                <div class="highlight-card">
                    <p style="margin:0; font-size:14px; color:gray;">📦 <b>Top Product (By Tonase)</b></p>
                    <p style="margin:0; font-size:20px; color:#1E3A8A;"><b>{top_qty_row['PRODUCT']}</b></p>
                    <p style="margin:0; font-size:16px;">Volume: {top_qty_row['TONASE']:,.2f} Ton</p>
                </div>
                """, unsafe_allow_html=True)
            
            with h2:
                st.markdown(f"""
                <div class="highlight-card">
                    <p style="margin:0; font-size:14px; color:gray;">💰 <b>Top Profit (By Product)</b></p>
                    <p style="margin:0; font-size:20px; color:#10B981;"><b>{top_profit_row['PRODUCT']}</b></p>
                    <p style="margin:0; font-size:16px;">Profit: Rp {top_profit_row['GROSS PROFIT']:,.0f}</p>
                </div>
                """, unsafe_allow_html=True)

            chart_col1, chart_col2 = st.columns(2)
            with chart_col1:
                fig_rev = px.bar(df_month.sort_values('REVENUE'), x='REVENUE', y='PRODUCT', color='SUBSIDIARY', orientation='h', title="Revenue per Produk", text_auto='.2s')
                st.plotly_chart(fig_rev, use_container_width=True)
            with chart_col2:
                fig_qty = px.bar(df_month.sort_values('TONASE'), x='TONASE', y='PRODUCT', color='SUBSIDIARY', orientation='h', title="Tonase per Produk", text_auto='.2f')
                st.plotly_chart(fig_qty, use_container_width=True)

    # TAB 2: SEMESTER COMPARISON
    with tab2:
        st.subheader(f"Analisis Performa Semester - {sel_tahun}")
        df_sem = df_year.groupby('SEMESTER')[['TONASE', 'REVENUE', 'GROSS PROFIT']].sum().reset_index()
        total_rev_year = df_sem['REVENUE'].sum()
        
        p1, p2 = st.columns(2)
        for i, row in df_sem.iterrows():
            pct = (row['REVENUE'] / total_rev_year * 100) if total_rev_year > 0 else 0
            with (p1 if row['SEMESTER'] == 'SMT-1' else p2):
                st.markdown(f'<div style="text-align:center; padding:10px; border:1px solid #ddd; border-radius:10px;"><b>Kontribusi Revenue {row["SEMESTER"]}</b><br><span style="font-size:30px; color:#1E3A8A;">{pct:.1f}%</span></div>', unsafe_allow_html=True)

        st.write("") 
        s1, s2, s3 = st.columns(3)
        with s1: st.plotly_chart(px.bar(df_sem, x='SEMESTER', y='TONASE', color='SEMESTER', title="Tonase (Ton)", text_auto='.2f'), use_container_width=True)
        with s2: st.plotly_chart(px.bar(df_sem, x='SEMESTER', y='REVENUE', color='SEMESTER', title="Revenue (Rp)", text_auto='.2s'), use_container_width=True)
        with s3: st.plotly_chart(px.bar(df_sem, x='SEMESTER', y='GROSS PROFIT', color='SEMESTER', title="Profit (Rp)", text_auto='.2s'), use_container_width=True)

        st.markdown("---")
        st.subheader("📈 Tren Bulanan (Timeline)")
        df_trend = df_year.groupby(['MONTH', 'MONTHLY'])[['TONASE', 'REVENUE', 'GROSS PROFIT']].sum().reset_index().sort_values('MONTH')
        metrik_pilihan = st.radio("Pilih Data Tren:", ["REVENUE", "TONASE", "GROSS PROFIT"], horizontal=True)
        fig_line = px.line(df_trend, x='MONTHLY', y=metrik_pilihan, markers=True, title=f"Tren {metrik_pilihan}")
        fig_line.update_traces(fill='tozeroy')
        st.plotly_chart(fig_line, use_container_width=True)
else:
    st.error("Data tidak ditemukan atau struktur file salah.")
