import streamlit as st
import requests
import os

st.set_page_config(page_title="Prediksi Harga Rumah", layout="centered")

st.title("🏠 AI Penaksir Harga Rumah")
st.markdown("---")

# Bagi kolom biar rapi
col1, col2 = st.columns(2)

with col1:
    bedrooms = st.number_input("Kamar Tidur", min_value=1, value=2)
    bathrooms = st.number_input("Kamar Mandi", min_value=1, value=2)
    sqft_living = st.number_input("Luas Bangunan (sqft)", min_value=100, value=1500)
    sqft_lot = st.number_input("Luas Tanah (sqft)", min_value=100, value=4000)
    floors = st.number_input("Lantai", min_value=1, value=1)
    waterfront = st.selectbox("Pemandangan Laut?", [0, 1], format_func=lambda x: "Ya" if x==1 else "Tidak")

with col2:
    view = st.slider("Rating Pemandangan (0-4)", 0, 4, 0)
    condition = st.slider("Kondisi Rumah (1-5)", 1, 5, 3)
    sqft_above = st.number_input("Luas Atas (sqft)", min_value=100, value=1500)
    sqft_basement = st.number_input("Luas Bawah Tanah (sqft)", min_value=0, value=0)
    yr_built = st.number_input("Tahun Dibangun", min_value=1800, max_value=2025, value=1990)
    yr_renovated = st.number_input("Tahun Renovasi (0 jika belum)", min_value=0, value=0)

st.markdown("---")

if st.button("💰 PREDIKSI HARGA SEKARANG", use_container_width=True):
    # Siapkan data payload sesuai format FastAPI
    payload = {
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "sqft_living": sqft_living,
        "sqft_lot": sqft_lot,
        "floors": floors,
        "waterfront": waterfront,
        "view": view,
        "condition": condition,
        "sqft_above": sqft_above,
        "sqft_basement": sqft_basement,
        "yr_built": yr_built,
        "yr_renovated": yr_renovated
    }

    try:
        api_url = os.getenv("API_URL", "http://127.0.0.1:8000/predict")
        with st.spinner("Sedang menghitung..."):
            response = requests.post(api_url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if "predicted_price" in result:
                harga = result["predicted_price"]
                st.success(f"### Estimasi Harga: ${harga:,.2f}")
            else:
                st.error(f"Gagal parsing hasil: {result}")
        else:
            st.error(f"Error dari Server: {response.text}")
            
    except Exception as e:
        st.error(f"Koneksi Gagal! Pastikan FastAPI jalan. Error: {e}")