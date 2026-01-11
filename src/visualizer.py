import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc
import config
import os

def save_correlation_matrix(df):
    plt.figure(figsize=(12, 10))
    sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap='coolwarm')
    plt.title("Özellikler Arası Korelasyon")
    
    save_path = os.path.join(config.ARTIFACTS_DIR, 'correlation_matrix.png')
    plt.savefig(save_path)
    plt.close()
    print(f"📊 Korelasyon grafiği kaydedildi: {save_path}")

def save_feature_importance(model, feature_names, model_name="Model"):
    """Özellik önem düzeylerini çizer."""
    if hasattr(model, 'coef_'): # Lojistik Regresyon
        importances = np.abs(model.coef_[0])
    elif hasattr(model, 'feature_importances_'): # Ağaç tabanlılar
        importances = model.feature_importances_
    else:
        return # Özellik önemi olmayan modeller için pas geç

    indices = np.argsort(importances)[::-1]
     
    plt.figure(figsize=(10, 6))
    plt.title(f"{model_name} - Özellik Önem Düzeyleri")
    plt.bar(range(len(importances)), importances[indices], align="center")
    plt.xticks(range(len(importances)), feature_names[indices], rotation=90)
    plt.tight_layout()
    
    save_path = os.path.join(config.ARTIFACTS_DIR, 'feature_importance.png')
    plt.savefig(save_path)
    plt.close()
    print(f"📊 Özellik önem grafiği kaydedildi: {save_path}")