import joblib
import pandas as pd
import config
import os

class HeartDiseasePredictor:
    def __init__(self):
        self.model = self._load_artifact(config.MODEL_SAVE_PATH)
        self.scaler = self._load_artifact(config.SCALER_SAVE_PATH)

    def _load_artifact(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"❌ Model dosyası bulunamadı: {path}. Önce eğitimi çalıştırın.")
        return joblib.load(path)

    def predict(self, patient_data: dict) -> dict:
        df = pd.DataFrame([patient_data])
         
        X_scaled = self.scaler.transform(df)
        
        prediction = self.model.predict(X_scaled)[0]
        probability = self.model.predict_proba(X_scaled)[0][1]
        
        return {
            "prediction": int(prediction),
            "risk_score": round(probability * 100, 2),
            "status": "RİSKLİ" if prediction == 1 else "SAĞLIKLI"
        }