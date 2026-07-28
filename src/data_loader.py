"""
Data loading module with type hints and dataclasses.
Week 12 Capstone Enhancement
"""

from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict, Any
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


@dataclass
class DataConfig:
    """Configuration for data loading."""
    raw_path: str = 'data/raw/'
    processed_path: str = 'data/processed/'
    random_state: int = 42
    test_size: float = 0.2


@dataclass
class DataSplit:
    """Container for train-test split data."""
    X_train: np.ndarray
    X_test: np.ndarray
    y_train: np.ndarray
    y_test: np.ndarray


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load data from CSV file.
    
    Args:
        filepath: Path to CSV file.
    
    Returns:
        DataFrame with parsed dates.
    
    Raises:
        FileNotFoundError: If file does not exist.
    """
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")


def load_forecast_data(filepath: str = 'data/processed/forecasts_2025_2027.csv') -> pd.DataFrame:
    """
    Load forecast data.
    
    Args:
        filepath: Path to forecast CSV.
    
    Returns:
        Forecast DataFrame or empty DataFrame if not found.
    """
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        return pd.DataFrame()


def load_enriched_data(filepath: str = 'data/processed/ethiopia_fi_enriched.csv') -> pd.DataFrame:
    """
    Load enriched financial inclusion dataset.
    
    Args:
        filepath: Path to enriched CSV.
    
    Returns:
        Enriched DataFrame.
    """
    return load_data(filepath)


def split_data(
    df: pd.DataFrame,
    target_col: str,
    config: Optional[DataConfig] = None
) -> DataSplit:
    """
    Perform stratified train-test split.
    
    Args:
        df: Input DataFrame.
        target_col: Name of target column.
        config: DataConfig object.
    
    Returns:
        DataSplit object containing train/test data.
    """
    if config is None:
        config = DataConfig()
    
    X = df.drop(target_col, axis=1)
    y = df[target_col]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=config.test_size,
        random_state=config.random_state,
        stratify=y
    )
    
    return DataSplit(
        X_train=X_train.values,
        X_test=X_test.values,
        y_train=y_train.values,
        y_test=y_test.values
    )


def get_feature_names(df: pd.DataFrame, target_col: str) -> List[str]:
    """
    Get list of feature names.
    
    Args:
        df: Input DataFrame.
        target_col: Name of target column.
    
    Returns:
        List of feature column names.
    """
    return [col for col in df.columns if col != target_col]