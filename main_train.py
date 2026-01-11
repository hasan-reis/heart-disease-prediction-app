from src import dataset_preparation
from src import visualizer
from src import model_trainer 
import config

def run_training_pipeline():
    # 1. Veriyi Yükle
    df = dataset_preparation.load_data(config.DATA_PATH)

    # 2. Korelasyon Matrisi Çiz ve Kaydet
    visualizer.save_correlation_matrix(df)

    # 3. Veriyi Hazırla (X, y ayrımı ve Scale)
    X, y = dataset_preparation.prepare_features_target(df)
    X_train, X_test, y_train, y_test, scaler = dataset_preparation.split_and_scale_data(X, y)

    # 4. Modelleri Karşıılaştır
    models = model_trainer.get_models() 
    best_model, best_name = model_trainer.train_and_evaluate(
        models, X_train, y_train, X_test, y_test
    )

    # 5. Sonuç Grafiğini Çiz
    visualizer.save_feature_importance(best_model, X.columns, model_name=best_name)

    # 6. Modeli Kaydet
    model_trainer.save_artifacts(best_model, scaler)

if __name__ == "__main__":
    run_training_pipeline()