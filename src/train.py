import pandas as pd
import mlflow
import mlflow.sklearn
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# --- LOGIKA PATH (ANTI-NYASAR) ---
# Kita tentukan folder mlruns harus ada di sebelah file train.py ini (naik satu level)
BASE_DIR = Path(__file__).resolve().parent.parent
MLRUNS_DIR = BASE_DIR / "mlruns"
DATA_PATH = BASE_DIR / "data" / "data.csv"

# Paksa MLflow pakai folder ini
mlflow.set_tracking_uri(MLRUNS_DIR.as_uri())
mlflow.set_experiment("House_Price_Prediction")

print(f"📂 Tracking URI: {mlflow.get_tracking_uri()}")
print(f"📂 Data Path   : {DATA_PATH}")

def train():
    # Load Data
    if not DATA_PATH.exists():
        print(f"❌ Error: File data tidak ditemukan di {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)
    
    # Preprocessing Simple
    X = df.drop(['price', 'date', 'street', 'city', 'statezip', 'country'], axis=1)
    y = df['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    with mlflow.start_run():
        print("🚀 Mulai Training...")
        model = RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42)
        model.fit(X_train, y_train)
        
        # Metrik
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        
        # Logging
        mlflow.log_param("n_estimators", 50)
        mlflow.log_metric("mae", mae)
        
        # Simpan Model
        mlflow.sklearn.log_model(model, "model")
        print(f"✅ Training Selesai! MAE: {mae}")
        print(f"✅ Model tersimpan di: {MLRUNS_DIR}")

if __name__ == "__main__":
    train()