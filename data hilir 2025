import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Hilirisasi Dashboard", layout="wide")

@st.cache_data
def load_data():
    # Nama file harus sama dengan yang diupload ke GitHub
    file_name = 'KBK_Hilirisasi 2025 Full Year (Sent).xlsx'
    df = pd.read_excel(file_name, sheet_name='Realisasi Hilirisasi', skiprows=6)
    df = df[['Periode', 'Entitas', 'Jenis Produk', 'Qty', 'Revenue', 'Gross Profit']].dropna(subset=['Periode'])
    return df

try:
    df = load_data()
    st.title("📊 Monitoring Hilirisasi 2025")
    
    list_bulan = sorted(df['Periode'].unique().astype(int))
    nama_bulan = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"Mei", 6:"Jun", 7:"Jul", 8:"Agt", 9:"Sep", 10:"Okt", 11:"Nov", 12:"Des"}
    sel_bulan = st.sidebar.selectbox("Pilih Bulan", list_bulan, format_func=lambda x: nama_bulan[x])

    df_f = df[df['Periode'] == sel_bulan]

    # Metrics Row
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Tonase", f"{df_f['Qty'].sum():,.2f} Ton")
    c2.metric("Total Revenue", f"Rp {df_f['Revenue'].sum():,.0f}")
    c3.metric("Total Gross Profit", f"Rp {df_f['Gross Profit'].sum():,.0f}")

    st.write("---")
    
    # Chart Row
    fig = px.bar(df_f, x='Revenue', y='Jenis Produk', color='Entitas', orientation='h', title=f"Revenue Produk - {nama_bulan[sel_bulan]}")
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Gagal memuat data. Pastikan file Excel sudah ada di GitHub. Error: {e}")
