"""
Unit tests for data loader module.
Week 12 Capstone Enhancement
"""

import pytest
import pandas as pd
import numpy as np
from src.data_loader import (
    DataConfig,
    DataSplit,
    load_data,
    load_forecast_data,
    split_data,
    get_feature_names
)


def test_data_config_defaults() -> None:
    """Test that DataConfig has correct defaults."""
    config = DataConfig()
    assert config.random_state == 42
    assert config.test_size == 0.2
    assert config.raw_path == 'data/raw/'
    assert config.processed_path == 'data/processed/'


def test_data_config_custom_values() -> None:
    """Test that DataConfig accepts custom values."""
    config = DataConfig(
        raw_path='custom_raw/',
        processed_path='custom_processed/',
        random_state=123,
        test_size=0.3
    )
    assert config.random_state == 123
    assert config.test_size == 0.3
    assert config.raw_path == 'custom_raw/'
    assert config.processed_path == 'custom_processed/'


def test_data_split_container() -> None:
    """Test DataSplit container holds arrays correctly."""
    X_train = np.array([[1, 2], [3, 4]])
    X_test = np.array([[5, 6]])
    y_train = np.array([0, 1])
    y_test = np.array([0])
    
    split = DataSplit(
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test
    )
    
    assert split.X_train.shape == (2, 2)
    assert split.X_test.shape == (1, 2)
    assert split.y_train.shape == (2,)
    assert split.y_test.shape == (1,)


def test_load_data_file_not_found() -> None:
    """Test that load_data raises FileNotFoundError for missing file."""
    with pytest.raises(FileNotFoundError):
        load_data('non_existent_file.csv')


def test_load_forecast_data_returns_dataframe() -> None:
    """Test forecast data loading returns DataFrame or empty DataFrame."""
    df = load_forecast_data()
    assert isinstance(df, pd.DataFrame)


def test_split_data_returns_correct_shapes() -> None:
    """Test that split_data returns expected shapes with stratified split."""
    df = pd.DataFrame({
        'feature1': range(100),
        'feature2': range(100, 200),
        'target': [0] * 80 + [1] * 20
    })
    
    config = DataConfig(test_size=0.2, random_state=42)
    result = split_data(df, 'target', config)
    
    assert result.X_train.shape[0] == 80
    assert result.X_test.shape[0] == 20
    assert result.y_train.shape[0] == 80
    assert result.y_test.shape[0] == 20


def test_split_data_preserves_class_distribution() -> None:
    """Test that split_data preserves class distribution."""
    df = pd.DataFrame({
        'feature1': range(100),
        'feature2': range(100, 200),
        'target': [0] * 80 + [1] * 20
    })
    
    config = DataConfig(test_size=0.2, random_state=42)
    result = split_data(df, 'target', config)
    
    train_ratio = result.y_train.sum() / len(result.y_train)
    test_ratio = result.y_test.sum() / len(result.y_test)
    
    assert abs(train_ratio - 0.2) < 0.05
    assert abs(test_ratio - 0.2) < 0.05


def test_get_feature_names() -> None:
    """Test that get_feature_names returns correct feature list."""
    df = pd.DataFrame({
        'feature1': range(10),
        'feature2': range(10, 20),
        'target': [0] * 8 + [1] * 2
    })
    
    features = get_feature_names(df, 'target')
    assert features == ['feature1', 'feature2']
    assert 'target' not in features 