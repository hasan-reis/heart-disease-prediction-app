from src.predictor import HeartDiseasePredictor

# Test Hastaları
patient_high = {'age': 65, 'sex': 1, 'cp': 4, 'trestbps': 160, 'chol': 310, 'fbs': 1, 'restecg': 2, 'thalach': 108, 'exang': 1, 'oldpeak': 2.5, 'slope': 2, 'ca': 3, 'thal': 7}
patient_medium = {'age': 52, 'sex': 0, 'cp': 3, 'trestbps': 135, 'chol': 245, 'fbs': 0, 'restecg': 0, 'thalach': 140, 'exang': 1, 'oldpeak': 0.8, 'slope': 2, 'ca': 0, 'thal': 6}
patient_low = {'age': 29, 'sex': 1, 'cp': 2, 'trestbps': 110, 'chol': 170, 'fbs': 0, 'restecg': 0, 'thalach': 185, 'exang': 0, 'oldpeak': 0.0, 'slope': 1, 'ca': 0, 'thal': 3}

def run_test_scenarios():
    print("🔍 Tahmin Motoru Başlatılıyor...")
    try:
        predictor = HeartDiseasePredictor()
    except FileNotFoundError as e:
        print(e)
        return

    scenarios = [
        ("🔴 YÜKSEK RİSK SENARYOSU", patient_high),
        ("🟠 ORTA RİSK SENARYOSU", patient_medium),
        ("🟢 DÜŞÜK RİSK SENARYOSU", patient_low)
    ]

    for title, patient_data in scenarios:
        print(f"\n{title}")
        print(f"👤 Veriler: {patient_data}")
        
        # Tahmin
        result = predictor.predict(patient_data)
        
        print("-" * 30)
        print(f"🩺 TAHMİN SONUCU: {result['status']}")
        print(f"📊 RİSK ORANI: %{result['risk_score']}")
        print("-" * 30)

if __name__ == "__main__":
    run_test_scenarios()