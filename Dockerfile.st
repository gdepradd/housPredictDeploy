# 1. Base Image sama
FROM python:3.9-slim

# 2. Folder kerja
WORKDIR /app

# 3. Install library (sebenarnya streamlit doang yang butuh, tapi samain aja biar praktis)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy source code
COPY src/ src/

# (Note: Frontend TIDAK PERLU folder mlruns, karena dia cuma nembak API)

# 5. Buka port 8501 (Pintu default Streamlit)
EXPOSE 8501

# 6. Jalankan Streamlit
CMD ["streamlit", "run", "src/frontend.py", "--server.address=0.0.0.0"]