"""
Model training and evaluation module with type hints.
Week 12 Capstone Enhancement
"""

from typing import Dict, Any, Tuple, Optional
import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    roc_auc_score,
    f1_score,
    average_precision_score,
    precision_score,
    recall_score,
    classification_report
)
from xgboost import XGBClassifier


def train_logistic_regression(
    X_train: np.ndarray,
    y_train: np.ndarray,
    random_state: int = 42,
    max_iter: int = 1000
) -> LogisticRegression:
    """
    Train logistic regression model.
    
    Args:
        X_train: Training features.
        y_train: Training labels.
        random_state: Random seed.
        max_iter: Maximum iterations.
    
    Returns:
        Trained logistic regression model.
    """
    model = LogisticRegression(
        random_state=random_state,
        max_iter=max_iter,
        class_weight='balanced'
    )
    model.fit(X_train, y_train)
    return model


def train_random_forest(
    X_train: np.ndarray,
    y_train: np.ndarray,
    n_estimators: int = 200,
    max_depth: Optional[int] = 20,
    random_state: int = 42
) -> RandomForestClassifier:
    """
    Train random forest model.
    
    Args:
        X_train: Training features.
        y_train: Training labels.
        n_estimators: Number of trees.
        max_depth: Maximum depth.
        random_state: Random seed.
    
    Returns:
        Trained random forest model.
    """
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state,
        class_weight='balanced',
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    return model


def train_xgboost(
    X_train: np.ndarray,
    y_train: np.ndarray,
    n_estimators: int = 200,
    max_depth: int = 6,
    learning_rate: float = 0.1,
    random_state: int = 42
) -> XGBClassifier:
    """
    Train XGBoost model with scale_pos_weight for imbalance.
    
    Args:
        X_train: Training features.
        y_train: Training labels.
        n_estimators: Number of trees.
        max_depth: Maximum depth.
        learning_rate: Learning rate.
        random_state: Random seed.
    
    Returns:
        Trained XGBoost model.
    """
    scale_pos_weight = len(y_train[y_train == 0]) / len(y_train[y_train == 1])
    
    model = XGBClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        scale_pos_weight=scale_pos_weight,
        random_state=random_state,
        eval_metric='logloss',
        use_label_encoder=False
    )
    model.fit(X_train, y_train)
    return model


def evaluate_model(
    model: Any,
    X_test: np.ndarray,
    y_test: np.ndarray,
    model_name: str = "Model"
) -> Dict[str, float]:
    """
    Evaluate model and return metrics.
    
    Args:
        model: Trained model with predict_proba.
        X_test: Test features.
        y_test: Test labels.
        model_name: Name for printing.
    
    Returns:
        Dictionary of metrics.
    """
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    metrics = {
        'model_name': model_name,
        'roc_auc': roc_auc_score(y_test, y_proba),
        'pr_auc': average_precision_score(y_test, y_proba),
        'f1': f1_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred)
    }
    
    print(f"\n{'='*60}")
    print(f"EVALUATION: {model_name}")
    print(f"{'='*60}")
    print(f"ROC-AUC: {metrics['roc_auc']:.4f}")
    print(f"PR-AUC: {metrics['pr_auc']:.4f}")
    print(f"F1-Score: {metrics['f1']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Legit', 'Fraud']))
    
    return metrics


def save_model(model: Any, filepath: str) -> None:
    """
    Save model to disk using joblib.
    
    Args:
        model: Trained model.
        filepath: Path to save model.
    """
    joblib.dump(model, filepath)
    print(f"✅ Model saved to: {filepath}")


def load_model(filepath: str) -> Any:
    """
    Load model from disk.
    
    Args:
        filepath: Path to saved model.
    
    Returns:
        Loaded model.
    """
    return joblib.load(filepath) 