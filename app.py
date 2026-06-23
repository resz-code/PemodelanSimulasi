import streamlit as st
import numpy as np
import pandas as pd
import pickle
import plotly.express as px  # Library grafik interaktif profesional

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Pro-Sim: Profit Simulator", page_icon="📈", layout="wide")

# --- KUSTOMISASI CSS (Ciri Khas UI Elegan) ---
st.markdown("""
    <style>
    .main-title {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #616161;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    .ai-box {
        background-color: #E3F2FD;
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #1E88E5;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. LOAD MODEL ---
@st.cache_resource
def load_model():
    with open('model.pkl', 'rb') as file:
        return pickle.load(file)

model = load_model()

# --- 2. SETUP BASELINE ---
baseline_input = np.array([[10, 10]])
baseline_pred = model.predict(baseline_input)[0]

# --- 3. LOGIKA SIMULATOR ---
def run_simulation(new_iklan, new_diskon):
    intervention_input = np.array([[new_iklan, new_diskon]])
    prediction = model.predict(intervention_input)[0]
    delta_y = prediction - baseline_pred
    return prediction, delta_y

# --- 4. IMPLEMENTASI UI STREAMLIT ---
# Header Kustom
st.markdown('<p class="main-title">🚀 Pro-Sim: Retail Analytics</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Digital Twin & What-If Analysis Dashboard</p>', unsafe_allow_html=True)
st.write("---")

# Sidebar Interaktif
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3233/3233483.png", width=120)
st.sidebar.markdown("## 🎛️ Control Panel")
st.sidebar.info("Geser tuas di bawah ini untuk mensimulasikan strategi masa depan.")

iklan_slider = st.sidebar.slider("📢 Anggaran Iklan (Juta)", 0, 50, 10)
diskon_slider = st.sidebar.slider("🏷️ Besaran Diskon (%)", 0, 50, 10)

st.sidebar.markdown("---")
st.sidebar.caption("👨‍💻 Dibuat untuk Tugas Praktikum Pemodelan M14")

# Engine Simulasi
hasil_pred, delta = run_simulation(iklan_slider, diskon_slider)

# --- CIRI KHAS 1: METRIK DENGAN PROGRESS TARGET ---
st.markdown("### 📊 Executive Summary")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Kondisi Baseline (Saat Ini)", value=f"Rp {baseline_pred:.2f} Jt")
with col2:
    st.metric(label="Proyeksi Intervensi Baru", value=f"Rp {hasil_pred:.2f} Jt", delta=f"{delta:.2f} Jt")
with col3:
    # Gamifikasi pencapaian target profit (Misal target = 150 Juta)
    target_profit = 150.0
    persentase = min((hasil_pred / target_profit) * 100, 100)
    st.metric(label="Pencapaian Target (150 Jt)", value=f"{persentase:.1f}%")

# Bar progres berwarna otomatis
st.progress(int(persentase))
st.write("---")

# --- CIRI KHAS 2: AI CONSULTANT BOX ---
st.markdown("### 🤖 Rekomendasi AI Consultant")

if delta > 20:
    badge = "🌟 STRATEGI HYPER-GROWTH"
    msg = "Tindakan yang sangat agresif! Kombinasi iklan dan diskon ini memberikan lonjakan profit luar biasa. Pastikan kapasitas stok gudang Anda siap menghadapi ledakan permintaan pasar."
    st.balloons() # Munculkan animasi balon
elif delta > 0:
    badge = "📈 PERTUMBUHAN STABIL"
    msg = "Strategi yang aman dan sangat direkomendasikan. Anda mencetak pertumbuhan positif tanpa membebani biaya operasional terlalu ekstrem."
elif delta == 0:
    badge = "⚖️ STATUS QUO"
    msg = "Angka ini sama persis dengan kondisi saat ini. Kebijakan ini tidak memberikan perubahan signifikan pada profit bersih perusahaan."
else:
    badge = "⚠️ RISIKO KERUGIAN"
    msg = "Peringatan! Kombinasi iklan dan diskon ini diprediksi akan MENGGERUS margin keuntungan. Pertimbangkan untuk mengurangi besaran diskon agar margin tetap aman."
    st.snow() # Munculkan animasi salju

# Menampilkan UI Box menggunakan HTML
st.markdown(f"""
    <div class="ai-box">
        <h4 style="margin-top:0px; color:#1565C0;">{badge}</h4>
        <p style="margin-bottom:0px; font-size: 16px;">{msg}</p>
    </div>
""", unsafe_allow_html=True)

st.write("---")

# --- CIRI KHAS 3: GRAFIK INTERAKTIF PLOTLY ---
st.markdown("### 📉 Visualisasi Komparatif")

df_plot = pd.DataFrame({
    'Skenario': ['Baseline (Strategi Lama)', 'Intervensi (Strategi Baru)'],
    'Keuntungan (Juta)': [baseline_pred, hasil_pred]
})

# Membuat grafik batang interaktif
fig = px.bar(df_plot, x='Skenario', y='Keuntungan (Juta)', 
             color='Skenario', 
             color_discrete_sequence=['#9E9E9E', '#1E88E5'], # Abu-abu vs Biru Elegan
             text_auto='.2f')

# Merapikan tampilan grafik
fig.update_traces(textfont_size=16, textangle=0, textposition="outside", cliponaxis=False)
fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Profit (Juta Rupiah)", 
                  margin=dict(t=30, b=0, l=0, r=0))

st.plotly_chart(fig, use_container_width=True)