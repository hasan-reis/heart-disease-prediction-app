from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report
import joblib
import config

def get_models():
    """
    Yarıştırılacak modelleri sözlük olarak döndürür.
    Bu liste, sınıflandırma problemleri için 'Yıldızlar Karması'dır.
    """
    return {
        # 1. Temel Doğrusal Model
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=config.RANDOM_STATE),
        
        # 2. Ağaç Tabanlı Modeller 
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=config.RANDOM_STATE),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=config.RANDOM_STATE),
        "Decision Tree": DecisionTreeClassifier(random_state=config.RANDOM_STATE),
        
        # 3. Mesafe ve Vektör Tabanlı Modeller
        "Support Vector Machine (SVM)": SVC(probability=True, kernel='linear', random_state=config.RANDOM_STATE), # probability=True: SVM'in % ihtimal verebilmesi için gerekli!
        "K-Nearest Neighbors (KNN)": KNeighborsClassifier(n_neighbors=5),
        
        # 4. Olasılık Tabanlı Model
        "Naive Bayes": GaussianNB()
    }

def train_and_evaluate(models, X_train, y_train, X_test, y_test):
    best_score = 0
    best_model = None
    best_name = ""

    print("\n🚀 Model Eğitimi ve Yarışı Başlıyor...")
    print("-" * 50)
    
    for name, model in models.items():
        try:
            model.fit(X_train, y_train)
            
            predictions = model.predict(X_test)
            accuracy = accuracy_score(y_test, predictions)
            
            print(f"   🔹 {name:<30}: Accuracy = %{accuracy*100:.2f}")

            if accuracy > best_score:
                best_score = accuracy
                best_model = model
                best_name = name
        except Exception as e:
            print(f"   ⚠️ {name} eğitilirken hata oluştu: {e}")
    
    print("-" * 50)
    print(f"\n🏆 KAZANAN MODEL: {best_name} (Başarı: %{best_score*100:.2f})")
    return best_model, best_name

def save_artifacts(model, scaler):
    joblib.dump(model, config.MODEL_SAVE_PATH)
    joblib.dump(scaler, config.SCALER_SAVE_PATH)
    print(f"En iyi model ({config.MODEL_SAVE_PATH}) ve Scaler kaydedildi.")