"""
=============================================================
ANTARMUKA STREAMLIT — RAG UTS Data Engineering
=============================================================

Jalankan dengan: streamlit run ui/app.py
=============================================================
"""

import sys
import os
from pathlib import Path

# Agar bisa import dari folder src/ sebagai module
sys.path.append(str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()

# ─── Konfigurasi Halaman ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Fiqih Assistant",
    page_icon="📖",
    layout="wide"
)

# ─── MASSIVE CSS INJECTION ────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,400&family=Amiri:ital,wght@0,400;0,700;1,400&display=swap');

/* ══════════════════════════════════════════════════
   GLOBAL — Parchment Background
══════════════════════════════════════════════════ */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #1a0f07 !important;
}

[data-testid="stAppViewContainer"] {
    background-image:
        radial-gradient(ellipse at 20% 10%, rgba(180,120,40,0.12) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 90%, rgba(120,60,20,0.15) 0%, transparent 50%),
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='400' height='400' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
    background-size: cover, cover, 400px 400px;
}

/* ── Floating Stars Decoration ── */
[data-testid="stAppViewContainer"]::before {
    content: '✦  ✧  ✦  ✧  ✦  ✧  ✦  ✧  ✦  ✧  ✦  ✧';
    position: fixed;
    top: 12px;
    left: 0; right: 0;
    text-align: center;
    font-size: 10px;
    letter-spacing: 18px;
    color: rgba(212,175,55,0.35);
    pointer-events: none;
    z-index: 9999;
    animation: starFloat 8s ease-in-out infinite alternate;
}
[data-testid="stAppViewContainer"]::after {
    content: '✦  ✧  ✦  ✧  ✦  ✧  ✦  ✧  ✦  ✧  ✦  ✧';
    position: fixed;
    bottom: 70px;
    left: 0; right: 0;
    text-align: center;
    font-size: 10px;
    letter-spacing: 18px;
    color: rgba(212,175,55,0.2);
    pointer-events: none;
    z-index: 9999;
    animation: starFloat 10s ease-in-out infinite alternate-reverse;
}
@keyframes starFloat {
    from { opacity: 0.3; letter-spacing: 18px; }
    to   { opacity: 0.7; letter-spacing: 22px; }
}

/* ══════════════════════════════════════════════════
   MAIN CONTENT AREA
══════════════════════════════════════════════════ */
[data-testid="stMain"] > div {
    background: rgba(26,15,7,0.0) !important;
}
.main .block-container {
    padding-top: 2rem !important;
    max-width: 900px !important;
}

/* ══════════════════════════════════════════════════
   HEADER — Ornamental Title
══════════════════════════════════════════════════ */
h1 {
    font-family: 'Cinzel Decorative', serif !important;
    color: #D4AF37 !important;
    font-size: 2.1rem !important;
    font-weight: 700 !important;
    text-align: center !important;
    text-shadow:
        0 0 30px rgba(212,175,55,0.5),
        0 0 60px rgba(212,175,55,0.2),
        2px 2px 4px rgba(0,0,0,0.8) !important;
    letter-spacing: 2px !important;
    padding-bottom: 0.3rem !important;
    border-bottom: none !important;
}

/* Ornament line above title */
h1::before {
    content: '── ✦ ──';
    display: block;
    font-family: 'Crimson Pro', serif;
    font-size: 0.9rem;
    color: rgba(212,175,55,0.6);
    letter-spacing: 12px;
    margin-bottom: 0.5rem;
}

.stCaption, [data-testid="stCaptionContainer"] p {
    font-family: 'Amiri', serif !important;
    color: rgba(212,175,55,0.65) !important;
    text-align: center !important;
    font-size: 1rem !important;
    font-style: italic !important;
    letter-spacing: 1px !important;
}

/* Divider glow */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(
        to right,
        transparent,
        rgba(212,175,55,0.2) 20%,
        rgba(212,175,55,0.7) 50%,
        rgba(212,175,55,0.2) 80%,
        transparent
    ) !important;
    margin: 1.2rem 0 !important;
}

/* ══════════════════════════════════════════════════
   SIDEBAR — Dark Walnut Panel
══════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #120a04 0%, #1e1006 40%, #150c05 100%) !important;
    border-right: 1px solid rgba(212,175,55,0.25) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.6) !important;
}
[data-testid="stSidebar"]::before {
    content: '';
    display: block;
    height: 4px;
    background: linear-gradient(to right, transparent, #D4AF37, transparent);
    margin-bottom: 1rem;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: 'Cinzel Decorative', serif !important;
    color: #D4AF37 !important;
    font-size: 0.85rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown {
    font-family: 'Crimson Pro', serif !important;
    color: rgba(245,230,200,0.85) !important;
    font-size: 0.95rem !important;
}

/* Sidebar metric cards */
[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: rgba(212,175,55,0.08) !important;
    border: 1px solid rgba(212,175,55,0.2) !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
}
[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
    color: rgba(212,175,55,0.7) !important;
    font-family: 'Amiri', serif !important;
    font-size: 0.8rem !important;
}
[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    color: #D4AF37 !important;
    font-family: 'Cinzel Decorative', serif !important;
    font-size: 1.3rem !important;
}

/* Sidebar slider */
[data-testid="stSidebar"] [data-testid="stSlider"] > div > div > div > div {
    background: linear-gradient(to right, #8B6914, #D4AF37) !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] [aria-valuenow] {
    background: #D4AF37 !important;
    border: 2px solid #8B6914 !important;
    box-shadow: 0 0 8px rgba(212,175,55,0.6) !important;
}

/* Sidebar checkbox */
[data-testid="stSidebar"] [data-testid="stCheckbox"] label span {
    color: rgba(245,230,200,0.85) !important;
    font-family: 'Crimson Pro', serif !important;
}

/* Sidebar info box */
[data-testid="stSidebar"] [data-testid="stAlert"] {
    background: rgba(212,175,55,0.08) !important;
    border: 1px solid rgba(212,175,55,0.3) !important;
    border-left: 3px solid #D4AF37 !important;
    border-radius: 4px !important;
    color: rgba(245,230,200,0.8) !important;
    font-family: 'Amiri', serif !important;
    font-size: 0.9rem !important;
}

/* Sidebar table (anggota) */
[data-testid="stSidebar"] table {
    width: 100% !important;
    border-collapse: collapse !important;
    font-family: 'Crimson Pro', serif !important;
    font-size: 0.85rem !important;
}
[data-testid="stSidebar"] th {
    color: #D4AF37 !important;
    border-bottom: 1px solid rgba(212,175,55,0.3) !important;
    padding: 4px 6px !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] td {
    color: rgba(245,230,200,0.8) !important;
    padding: 3px 6px !important;
    border-bottom: 1px solid rgba(212,175,55,0.1) !important;
}

/* ══════════════════════════════════════════════════
   TABS — Ornamental Nav
══════════════════════════════════════════════════ */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: rgba(212,175,55,0.05) !important;
    border-bottom: 1px solid rgba(212,175,55,0.3) !important;
    border-radius: 8px 8px 0 0 !important;
    gap: 0 !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: 'Cinzel Decorative', serif !important;
    font-size: 0.75rem !important;
    color: rgba(212,175,55,0.55) !important;
    letter-spacing: 1.5px !important;
    padding: 10px 28px !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.3s ease !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: #D4AF37 !important;
    border-bottom: 2px solid #D4AF37 !important;
    background: rgba(212,175,55,0.08) !important;
    text-shadow: 0 0 12px rgba(212,175,55,0.5) !important;
}

/* ══════════════════════════════════════════════════
   CHAT MESSAGES — Scroll Paper Style
══════════════════════════════════════════════════ */
[data-testid="stChatMessage"] {
    background: rgba(212,175,55,0.04) !important;
    border: 1px solid rgba(212,175,55,0.12) !important;
    border-radius: 12px !important;
    margin-bottom: 0.8rem !important;
    padding: 1rem 1.2rem !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3) !important;
    backdrop-filter: blur(4px) !important;
    transition: border-color 0.3s ease !important;
}
[data-testid="stChatMessage"]:hover {
    border-color: rgba(212,175,55,0.28) !important;
}

/* User message accent */
[data-testid="stChatMessage"][data-testid*="user"],
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    border-left: 3px solid #D4AF37 !important;
    background: rgba(212,175,55,0.07) !important;
}

/* Message text */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] .stMarkdown p {
    font-family: 'Crimson Pro', serif !important;
    font-size: 1.05rem !important;
    color: rgba(245,235,210,0.92) !important;
    line-height: 1.7 !important;
}

/* ── Chat Input ── */
[data-testid="stChatInput"] {
    background: rgba(26,15,7,0.9) !important;
    border-top: 1px solid rgba(212,175,55,0.2) !important;
    padding: 10px 0 !important;
}
[data-testid="stChatInput"] textarea {
    background: rgba(212,175,55,0.06) !important;
    border: 1px solid rgba(212,175,55,0.3) !important;
    border-radius: 24px !important;
    color: rgba(245,235,210,0.92) !important;
    font-family: 'Crimson Pro', serif !important;
    font-size: 1rem !important;
    padding: 12px 20px !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: rgba(212,175,55,0.7) !important;
    box-shadow: 0 0 16px rgba(212,175,55,0.2) !important;
    outline: none !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(212,175,55,0.35) !important;
    font-style: italic !important;
}

/* ── Send Button ── */
[data-testid="stChatInput"] button {
    background: rgba(212,175,55,0.15) !important;
    border: 1px solid rgba(212,175,55,0.4) !important;
    border-radius: 50% !important;
    color: #D4AF37 !important;
    transition: all 0.2s ease !important;
}
[data-testid="stChatInput"] button:hover {
    background: rgba(212,175,55,0.3) !important;
    box-shadow: 0 0 12px rgba(212,175,55,0.4) !important;
}

/* ══════════════════════════════════════════════════
   EXPANDER — Scroll Case Style
══════════════════════════════════════════════════ */
[data-testid="stExpander"] {
    background: rgba(212,175,55,0.04) !important;
    border: 1px solid rgba(212,175,55,0.18) !important;
    border-radius: 8px !important;
    margin-top: 0.5rem !important;
}
[data-testid="stExpander"] summary {
    font-family: 'Amiri', serif !important;
    font-size: 0.95rem !important;
    color: rgba(212,175,55,0.8) !important;
    padding: 8px 14px !important;
}
[data-testid="stExpander"] summary:hover {
    color: #D4AF37 !important;
    background: rgba(212,175,55,0.06) !important;
    border-radius: 8px 8px 0 0 !important;
}
[data-testid="stExpander"] summary svg {
    fill: rgba(212,175,55,0.6) !important;
}
[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    border-top: 1px solid rgba(212,175,55,0.15) !important;
    padding: 12px 16px !important;
}
[data-testid="stExpander"] p,
[data-testid="stExpander"] .stMarkdown p {
    font-family: 'Crimson Pro', serif !important;
    color: rgba(235,220,195,0.85) !important;
    font-size: 0.95rem !important;
    line-height: 1.65 !important;
}

/* ══════════════════════════════════════════════════
   SUCCESS / ERROR / INFO ALERTS
══════════════════════════════════════════════════ */
[data-testid="stAlert"][data-baseweb="notification"] {
    font-family: 'Amiri', serif !important;
    font-size: 1rem !important;
    border-radius: 8px !important;
}
/* Success */
[data-testid="stAlert"].st-success,
div[data-testid="stAlert"][class*="success"] {
    background: rgba(34,80,30,0.3) !important;
    border: 1px solid rgba(100,180,80,0.4) !important;
    border-left: 3px solid #6db55b !important;
    color: rgba(180,230,170,0.9) !important;
}
/* Error */
div[data-testid="stAlert"][class*="error"] {
    background: rgba(80,20,10,0.4) !important;
    border: 1px solid rgba(180,60,40,0.4) !important;
    border-left: 3px solid #c0523a !important;
    color: rgba(245,180,165,0.9) !important;
}
/* Info */
div[data-testid="stAlert"][class*="info"] {
    background: rgba(30,50,80,0.35) !important;
    border: 1px solid rgba(80,130,200,0.35) !important;
    border-left: 3px solid #5a8fd0 !important;
    color: rgba(180,210,245,0.9) !important;
}

/* ══════════════════════════════════════════════════
   BUTTONS
══════════════════════════════════════════════════ */
[data-testid="stButton"] > button {
    font-family: 'Cinzel Decorative', serif !important;
    font-size: 0.7rem !important;
    letter-spacing: 2px !important;
    color: rgba(212,175,55,0.8) !important;
    background: rgba(212,175,55,0.08) !important;
    border: 1px solid rgba(212,175,55,0.35) !important;
    border-radius: 4px !important;
    padding: 8px 20px !important;
    transition: all 0.25s ease !important;
}
[data-testid="stButton"] > button:hover {
    background: rgba(212,175,55,0.18) !important;
    border-color: rgba(212,175,55,0.7) !important;
    color: #D4AF37 !important;
    box-shadow: 0 0 14px rgba(212,175,55,0.25) !important;
}

/* ══════════════════════════════════════════════════
   METRICS (Analitik tab)
══════════════════════════════════════════════════ */
[data-testid="stMetric"] {
    background: rgba(212,175,55,0.06) !important;
    border: 1px solid rgba(212,175,55,0.18) !important;
    border-radius: 10px !important;
    padding: 14px 18px !important;
    text-align: center !important;
    transition: border-color 0.3s !important;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(212,175,55,0.4) !important;
}
[data-testid="stMetricLabel"] p {
    font-family: 'Amiri', serif !important;
    font-size: 0.85rem !important;
    color: rgba(212,175,55,0.65) !important;
    letter-spacing: 0.5px !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Cinzel Decorative', serif !important;
    color: #D4AF37 !important;
    font-size: 1.8rem !important;
    text-shadow: 0 0 10px rgba(212,175,55,0.35) !important;
}

/* ══════════════════════════════════════════════════
   DATAFRAME
══════════════════════════════════════════════════ */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(212,175,55,0.2) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] th {
    background: rgba(212,175,55,0.12) !important;
    color: #D4AF37 !important;
    font-family: 'Cinzel Decorative', serif !important;
    font-size: 0.7rem !important;
    letter-spacing: 1px !important;
    border-bottom: 1px solid rgba(212,175,55,0.25) !important;
}
[data-testid="stDataFrame"] td {
    color: rgba(235,220,195,0.85) !important;
    font-family: 'Crimson Pro', serif !important;
    border-bottom: 1px solid rgba(212,175,55,0.08) !important;
}
[data-testid="stDataFrame"] tr:hover td {
    background: rgba(212,175,55,0.05) !important;
}

/* ══════════════════════════════════════════════════
   SUBHEADERS & GENERAL TEXT
══════════════════════════════════════════════════ */
h2, h3 {
    font-family: 'Cinzel Decorative', serif !important;
    color: #D4AF37 !important;
    font-size: 1.1rem !important;
    letter-spacing: 1.5px !important;
    text-shadow: 0 0 15px rgba(212,175,55,0.3) !important;
}
p, li, .stMarkdown p {
    font-family: 'Crimson Pro', serif !important;
    color: rgba(235,220,195,0.88) !important;
    font-size: 1rem !important;
    line-height: 1.7 !important;
}
code, .stCode {
    background: rgba(212,175,55,0.08) !important;
    border: 1px solid rgba(212,175,55,0.2) !important;
    color: rgba(212,175,55,0.9) !important;
    border-radius: 4px !important;
    font-size: 0.85rem !important;
    padding: 2px 6px !important;
}
pre code {
    display: block !important;
    padding: 12px 16px !important;
    line-height: 1.6 !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] p {
    color: rgba(212,175,55,0.7) !important;
    font-family: 'Amiri', serif !important;
    font-style: italic !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(26,15,7,0.5); }
::-webkit-scrollbar-thumb {
    background: rgba(212,175,55,0.3);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(212,175,55,0.55); }

/* ── Hide default Streamlit branding ── */
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden !important; }
header[data-testid="stHeader"] {
    background: rgba(26,15,7,0.95) !important;
    border-bottom: 1px solid rgba(212,175,55,0.15) !important;
}
</style>

<!-- Bismillah ornament above title -->
<div style="
    text-align:center;
    font-family: 'Amiri', serif;
    font-size: 1.5rem;
    color: rgba(212,175,55,0.55);
    letter-spacing: 4px;
    margin-bottom: -10px;
    margin-top: -10px;
    animation: fadeIn 2s ease;
">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيم</div>

<style>
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-6px); }
    to   { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
st.title("📖 Smart Fiqih Assistant")
st.caption("Asisten Pintar Berbasis RAG untuk Memahami Kitab Fiqih Ibtida")
st.divider()

# ─── Sidebar: Info & Konfigurasi ─────────────────────────────────────────────
with st.sidebar:
    top_k = st.slider(
        "Jumlah dokumen relevan (top-k)",
        min_value=1, max_value=5, value=3,
        help="Berapa banyak chunk yang diambil dari vector database"
    )

    show_context = st.checkbox("Tampilkan konteks yang digunakan", value=True)
    show_prompt  = st.checkbox("Tampilkan prompt ke LLM", value=False)
    show_chart   = st.checkbox("Tampilkan grafik skor relevansi", value=True)

    st.divider()
    st.header("Info Sistem")
    st.markdown("""
    **Kelompok:** Fiqih-Ibtida Squad  
    **Anggota:** 
    - Dani (Data Engineer)  
    - Habib (Project Manager)  
    - Novandy (UI & Data Analyst)  
    **Domain:** Kitab Fiqih Ibtida  
    **LLM:** Gemini 2.5 Flash  
    **Vector DB:** ChromaDB  
    """)

    st.divider()
    st.info("💡 Tip: Mulai dengan pertanyaan spesifik yang jawabannya ada di dalam dokumen Anda.")


# ─── Load Vector Store (cached) ──────────────────────────────────────────────
@st.cache_resource
def load_vs():
    """Load vector store sekali saja, di-cache untuk performa."""
    try:
        from src.query import load_vectorstore
        return load_vectorstore(), None
    except FileNotFoundError as e:
        return None, str(e)
    except Exception as e:
        return None, f"Error: {e}"


# ─── Fungsi Visualisasi ───────────────────────────────────────────────────────
def render_relevance_chart(contexts: list, question: str):
    """Bar chart horizontal skor relevansi setiap chunk."""
    labels = [
        f"Chunk {i+1} ({ctx['source'].split('/')[-1][:20]})"
        for i, ctx in enumerate(contexts)
    ]
    scores = [ctx["score"] for ctx in contexts]
    max_s  = max(scores) if scores else 1

    colors = px.colors.sample_colorscale(
        "RdYlGn", [s / max_s for s in scores]
    )

    fig = go.Figure(go.Bar(
        x=scores,
        y=labels,
        orientation="h",
        marker_color=colors,
        text=[f"{s:.4f}" for s in scores],
        textposition="outside",
    ))
    fig.update_layout(
        title="📊 Skor Relevansi Chunk (lebih kecil = lebih relevan di ChromaDB)",
        xaxis_title="Distance Score",
        yaxis_title="",
        height=200 + len(contexts) * 45,
        margin=dict(l=10, r=70, t=50, b=40),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(18,10,4,0.0)",
        font=dict(size=12, color="#c9a84c", family="Crimson Pro, serif"),
        xaxis=dict(gridcolor="rgba(212,175,55,0.15)", color="#c9a84c"),
        yaxis=dict(color="#c9a84c"),
        title_font=dict(color="#D4AF37", family="Amiri, serif"),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_session_stats():
    """Statistik ringkasan sesi percakapan."""
    msgs      = st.session_state.messages
    user_msgs = [m for m in msgs if m["role"] == "user"]
    asst_msgs = [m for m in msgs if m["role"] == "assistant"]
    all_scores = [
        ctx["score"]
        for m in asst_msgs if "contexts" in m
        for ctx in m["contexts"]
    ]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💬 Total Pertanyaan",    len(user_msgs))
    col2.metric("✅ Jawaban Dihasilkan",   len(asst_msgs))
    col3.metric("📚 Total Chunk Diambil", len(all_scores))
    col4.metric(
        "📈 Avg Skor Relevansi",
        f"{sum(all_scores)/len(all_scores):.4f}" if all_scores else "—"
    )

    if len(asst_msgs) >= 2:
        tren_data = []
        for i, m in enumerate(asst_msgs):
            if "contexts" in m and m["contexts"]:
                avg = sum(c["score"] for c in m["contexts"]) / len(m["contexts"])
                tren_data.append({"Pertanyaan": f"Q{i+1}", "Avg Score": avg})

        if tren_data:
            df_tren = pd.DataFrame(tren_data)
            fig = px.line(
                df_tren, x="Pertanyaan", y="Avg Score",
                markers=True,
                title="📉 Tren Rata-rata Skor Relevansi per Pertanyaan",
                labels={"Avg Score": "Avg Score", "Pertanyaan": ""},
            )
            fig.update_layout(
                height=280,
                margin=dict(l=10, r=10, t=50, b=40),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#c9a84c", family="Crimson Pro, serif"),
                xaxis=dict(gridcolor="rgba(212,175,55,0.15)", color="#c9a84c"),
                yaxis=dict(gridcolor="rgba(212,175,55,0.15)", color="#c9a84c"),
                title_font=dict(color="#D4AF37"),
            )
            fig.update_traces(line_color="#D4AF37", marker_color="#8B6914",
                              marker_size=8)
            st.plotly_chart(fig, use_container_width=True)


# ─── Main Content ─────────────────────────────────────────────────────────────
vectorstore, error = load_vs()

if error:
    st.error(f"❌ {error}")
    st.info("Jalankan terlebih dahulu: `python src/indexing.py`")
    st.stop()

if not error:
    st.success("✅ Pengetahuan Kitab Fiqih telah dimuat. Silakan ajukan pertanyaan!")

# ─── Tab Layout ───────────────────────────────────────────────────────────────
tab_chat, tab_analitik = st.tabs(["💬 Chat", "📊 Analitik Sesi"])

# ══════════════════════════════════════════════════════════════
# TAB 1: CHAT
# ══════════════════════════════════════════════════════════════
with tab_chat:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Tampilkan riwayat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg["role"] == "assistant":
                if show_context and "contexts" in msg:
                    with st.expander("🔍 Referensi Sumber Terkait"):
                        for i, ctx in enumerate(msg["contexts"], 1):
                            st.markdown(
                                f"**[{i}] Skor: `{ctx['score']:.4f}`** · `{ctx['source']}`"
                            )
                            st.text(ctx["content"][:300] + "...")
                            if i < len(msg["contexts"]):
                                st.divider()
                if show_chart and "contexts" in msg and msg["contexts"]:
                    render_relevance_chart(msg["contexts"], msg.get("question", ""))

    # Input pertanyaan baru
    if question := st.chat_input("Ketik pertanyaan seputar fiqih ibtida di sini..."):

        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("⏳ Sedang membedah kitab dan merangkum jawaban untukmu..."):
                try:
                    from src.query import answer_question
                    result = answer_question(question, vectorstore, top_k=top_k)

                    st.write(result["answer"])

                    if show_context:
                        with st.expander("📚 Konteks yang digunakan"):
                            for i, ctx in enumerate(result["contexts"], 1):
                                st.markdown(
                                    f"**[{i}] Skor relevansi: `{ctx['score']:.4f}`** · `{ctx['source']}`"
                                )
                                st.text(ctx["content"][:300] + "...")
                                if i < len(result["contexts"]):
                                    st.divider()

                    if show_chart and result["contexts"]:
                        render_relevance_chart(result["contexts"], question)

                    if show_prompt:
                        with st.expander("🔧 Prompt yang dikirim ke LLM"):
                            st.code(result["prompt"], language="text")

                    st.session_state.messages.append({
                        "role":     "assistant",
                        "content":  result["answer"],
                        "contexts": result["contexts"],
                        "question": question,
                    })

                except Exception as e:
                    error_msg = (
                        f"❌ Error: {e}\n\n"
                        "Pastikan `GOOGLE_API_KEY` sudah diatur di file `.env`"
                    )
                    st.error(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg}
                    )

    if st.session_state.get("messages"):
        if st.button("🗑️ Hapus Riwayat Chat"):
            st.session_state.messages = []
            st.rerun()


# ══════════════════════════════════════════════════════════════
# TAB 2: ANALITIK SESI
# ══════════════════════════════════════════════════════════════
with tab_analitik:
    st.subheader("📊 Statistik Sesi Percakapan")

    if not st.session_state.get("messages"):
        st.info("📭 Belum ada percakapan. Mulai bertanya di tab Chat terlebih dahulu.")
    else:
        render_session_stats()

        st.divider()
        st.subheader("📋 Riwayat Pertanyaan")

        user_msgs = [m for m in st.session_state.messages if m["role"] == "user"]
        asst_msgs = [m for m in st.session_state.messages if m["role"] == "assistant"]

        rows = []
        for i, (u, a) in enumerate(zip(user_msgs, asst_msgs), 1):
            scores = [c["score"] for c in a.get("contexts", [])]
            rows.append({
                "No":                 i,
                "Pertanyaan":         u["content"],
                "Chunks Diambil":     len(scores),
                "Avg Skor Relevansi": f"{sum(scores)/len(scores):.4f}" if scores else "—",
                "Best Score":         f"{min(scores):.4f}" if scores else "—",
            })

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
