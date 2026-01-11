import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import config  

def load_data(path):
    try:
        df = pd.read_csv(path)
        print(f"✅ Veri yüklendi: {df.shape}")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"❌ Dosya bulunamadı: {path}")

def prepare_features_target(df, target_col='target'):
    X = df.drop(columns=[target_col])
    y = df[target_col]
    return X, y

def split_and_scale_data(X, y):
    # 1. Ölçeklendirme
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 2. Bölme
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, 
        y, 
        test_size=config.TEST_SIZE, 
        random_state=config.RANDOM_STATE, 
        stratify=y
    )
    
    return X_train, X_test, y_train, y_test, scaler