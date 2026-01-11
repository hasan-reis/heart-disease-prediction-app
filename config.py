import os

# Projenin Ana Dizini (Root)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Klasör Yolları
DATA_RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
ARTIFACTS_DIR = os.path.join(BASE_DIR, 'artifacts')
SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts') # src yerine scripts

# İşlenmiş verinin duracağı yer
DATA_PATH = os.path.join(DATA_PROCESSED_DIR, 'imputed_dataset_.csv')

# Modellerin kaydedileceği yer
MODEL_SAVE_PATH = os.path.join(MODELS_DIR, 'best_heart_model_clean.pkl')
SCALER_SAVE_PATH = os.path.join(MODELS_DIR, 'scaler_clean.pkl')

# Ham Veri Dosyalarının Listesi (prepare_dataset.py için)
RAW_DATA_FILES = [
    os.path.join(DATA_RAW_DIR, 'processed.cleveland.data'),
    os.path.join(DATA_RAW_DIR, 'processed.hungarian.data'),
    os.path.join(DATA_RAW_DIR, 'processed.switzerland.data'),
    os.path.join(DATA_RAW_DIR, 'processed.va.data')
]

# Eğer klasörler yoksa otomatik oluştur
for directory in [DATA_RAW_DIR, DATA_PROCESSED_DIR, MODELS_DIR, ARTIFACTS_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Model Parametreleri
TEST_SIZE = 0.2
RANDOM_STATE = 42