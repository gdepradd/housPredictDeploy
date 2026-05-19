import mlflow.pyfunc
from mlflow.tracking import MlflowClient
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os

app = FastAPI(title="House Price Prediction")

# --- LOGIKA PATH ---
BASE_DIR = Path(__file__).resolve().parent.parent
MLRUNS_DIR = BASE_DIR / "mlruns"

print(f"📂 Menghubungkan ke MLflow di: {MLRUNS_DIR}")
mlflow.set_tracking_uri(MLRUNS_DIR.as_uri())

model = None

# --- LOAD MODEL (SMART SEARCH) ---
try:
    client = MlflowClient()
    exp = client.get_experiment_by_name("House_Price_Prediction")
    
    if exp:
        # Ambil experiment ID
        experiment_id = exp.experiment_id
        
        # ### SMART SEARCH: Cari file model.pkl dimanapun dia berada ###
        print(f"🕵️‍♂️ Sedang mencari 'model.pkl' di dalam folder eksperimen {experiment_id}...")
        
        found_model_path = None
        target_dir = MLRUNS_DIR / experiment_id
        
        # Loop nelesup ke semua sub-folder
        for root, dirs, files in os.walk(target_dir):
            if "model.pkl" in files:
                found_model_path = root
                print(f"🎉 KETEMU! Model ngumpet di: {found_model_path}")
                break
        
        if found_model_path:
            # Load dari path yang ditemukan
            model_uri = Path(found_model_path).as_uri()
            model = mlflow.pyfunc.load_model(model_uri)
            print("✅ Model BERHASIL di-load!")
        else:
            print("❌ Gawat. File 'model.pkl' benar-benar tidak ada di dalam folder mlruns.")
            print("   Cek apakah permission folder sudah 777?")
            # Intip isi folder buat debugging
            print(f"   Isi {target_dir}: {os.listdir(target_dir)}")

    else:
        print("❌ Eksperimen tidak ditemukan.")

except Exception as e:
    print(f"❌ Error Fatal saat start-up: {e}")

# --- API ENDPOINTS (Tetap Sama) ---
class HouseData(BaseModel):
    bedrooms: float = 3.0
    bathrooms: float = 2.0
    sqft_living: int = 1500
    sqft_lot: int = 4000
    floors: float = 1.0
    waterfront: int = 0
    view: int = 0
    condition: int = 3
    sqft_above: int = 1500
    sqft_basement: int = 0
    yr_built: int = 1990
    yr_renovated: int = 0

@app.post("/predict")
def predict(data: HouseData):
    if not model:
        return {"error": "Model belum siap."}
    
    df = pd.DataFrame([data.dict()])
    pred = model.predict(df)
    return {"predicted_price": float(pred[0])}