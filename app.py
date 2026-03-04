# CSS Final: Hapus Logo GitHub tapi Tombol Sidebar Tetap Ada
st.markdown("""
    <style>
    /* 1. Menghilangkan elemen spesifik di dalam header (Logo GitHub & Menu) */
    /* Namun membiarkan header tetap ada agar tombol sidebar tidak hilang */
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0) !important;
    }
    
    /* Target spesifik untuk tombol GitHub dan Menu kanan agar hancur/hilang */
    [data-testid="stHeader"] > div:first-child {
        visibility: hidden !important;
    }

    /* 2. Memastikan tombol kontrol Sidebar (panah) tetap terlihat */
    /* Kita paksa tombol ini untuk tetap 'visible' meskipun induknya hidden */
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        background-color: #f0f2f6 !important; /* Memberi warna background agar tombol terlihat jelas */
        border-radius: 50% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }

    /* 3. Menghilangkan Footer 'Made with Streamlit' */
    footer {visibility: hidden !important;}

    /* 4. Menyesuaikan padding agar tampilan tidak terpotong */
    .block-container {
        padding-top: 2rem !important;
    }

    /* --- Style Kartu Metrik & Tab --- */
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
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E3A8A !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
