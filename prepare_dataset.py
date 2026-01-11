import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
import config

columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
           'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'num']

def read_heart_data(filename):
    print(f"Okunuyor: {filename}")
    return pd.read_csv(filename, names=columns, na_values=['?', '-9.0', '-9', ''])

df_list = [read_heart_data(path) for path in config.RAW_DATA_FILES]
df = pd.concat(df_list, ignore_index=True)

# Mantıksız '0' Değerlerini NaN Yapma
for col in ['trestbps', 'chol', 'thalach']:
    df[col] = df[col].replace(0, np.nan)

# IMPUTATION (Doldurma)
numeric_features = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
categorical_features = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']

imputer_num = SimpleImputer(strategy='median')
df[numeric_features] = imputer_num.fit_transform(df[numeric_features])

imputer_cat = SimpleImputer(strategy='most_frequent')
df[categorical_features] = imputer_cat.fit_transform(df[categorical_features])

df['target'] = df['num'].apply(lambda x: 1 if x > 0 else 0)
df.drop(columns=['num'], inplace=True)

print("-" * 30)
print(f"✅ İşlem Tamam! Yeni Boyut: {df.shape}")
print(df.head())

df.to_csv(config.DATA_PATH, index=False)
print(f"💾 Dosya kaydedildi: {config.DATA_PATH}")