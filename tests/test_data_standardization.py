"""
Tests for Data Standardization Module

Tests cover:
- Loading and standardizing each dataset
- Data format validation
- Label distribution
- Text field generation
"""

import pytest
import pandas as pd
from pathlib import Path
from sources.data_standardization import (
    DataStandardizer,
    load_dataset,
    standardize_all_datasets,
)


class TestDataStandardizerBasic:
    """Basic tests for DataStandardizer initialization and loading."""

    def test_standardizer_initialization(self):
        """Test DataStandardizer can be initialized."""
        standardizer = DataStandardizer()
        assert standardizer is not None
        assert isinstance(standardizer.standardized_data, dict)

    def test_load_sms_spam_main(self):
        """Test loading SMS Spam main dataset."""
        standardizer = DataStandardizer()
        df = standardizer.load_sms_spam_main()
        
        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert 'label' in df.columns
        assert 'text' in df.columns
        assert len(df) > 0
        assert df['label'].isin([0, 1]).all()

    def test_load_phishing_dataset(self):
        """Test loading Phishing dataset."""
        standardizer = DataStandardizer()
        df = standardizer.load_phishing_dataset()
        
        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert 'label' in df.columns
        assert 'text' in df.columns
        assert len(df) > 0
        assert df['label'].isin([0, 1]).all()

    def test_load_sms_spam_perceptron(self):
        """Test loading SMS Spam Perceptron dataset."""
        standardizer = DataStandardizer()
        df = standardizer.load_sms_spam_perceptron()
        
        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert 'label' in df.columns
        assert 'text' in df.columns
        assert len(df) > 0
        assert df['label'].isin([0, 1]).all()

    def test_load_sms_spam_svm(self):
        """Test loading SMS Spam SVM dataset."""
        standardizer = DataStandardizer()
        df = standardizer.load_sms_spam_svm()
        
        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert 'label' in df.columns
        assert 'text' in df.columns
        assert len(df) > 0
        assert df['label'].isin([0, 1]).all()


class TestDataStandardization:
    """Tests for data format validation and standardization."""

    def test_standardize_all(self):
        """Test standardizing all datasets."""
        standardizer = DataStandardizer()
        all_data = standardizer.standardize_all()
        
        assert isinstance(all_data, dict)
        assert len(all_data) == 4
        assert 'sms_spam_main' in all_data
        assert 'phishing' in all_data
        assert 'sms_spam_perceptron' in all_data
        assert 'sms_spam_svm' in all_data

    def test_standardized_data_format(self):
        """Test that all standardized data has correct format."""
        standardizer = DataStandardizer()
        standardizer.standardize_all()
        
        for dataset_name, df in standardizer.standardized_data.items():
            assert isinstance(df, pd.DataFrame), f"{dataset_name} not a DataFrame"
            assert 'label' in df.columns, f"{dataset_name} missing 'label' column"
            assert 'text' in df.columns, f"{dataset_name} missing 'text' column"
            assert len(df) > 0, f"{dataset_name} is empty"
            assert df['label'].dtype in ['int64', 'float64', 'int32'], \
                f"{dataset_name} label not numeric"
            assert df['text'].dtype == 'object', f"{dataset_name} text not object type"

    def test_labels_are_binary(self):
        """Test that all labels are binary (0, 1)."""
        standardizer = DataStandardizer()
        standardizer.standardize_all()
        
        for dataset_name, df in standardizer.standardized_data.items():
            unique_labels = set(df['label'].unique())
            assert unique_labels.issubset({0, 1}), \
                f"{dataset_name} has non-binary labels: {unique_labels}"

    def test_text_field_not_empty(self):
        """Test that text field is never empty."""
        standardizer = DataStandardizer()
        standardizer.standardize_all()
        
        for dataset_name, df in standardizer.standardized_data.items():
            assert not df['text'].isna().any(), \
                f"{dataset_name} has NaN values in text"
            assert (df['text'].str.len() > 0).all(), \
                f"{dataset_name} has empty strings in text"


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_load_dataset_sms_spam(self):
        """Test loading SMS Spam dataset via convenience function."""
        df = load_dataset('sms_spam_main')
        
        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert 'label' in df.columns
        assert 'text' in df.columns
        assert len(df) > 0

    def test_load_dataset_phishing(self):
        """Test loading Phishing dataset via convenience function."""
        df = load_dataset('phishing')
        
        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert 'label' in df.columns
        assert len(df) > 0

    def test_load_dataset_invalid(self):
        """Test that invalid dataset name raises error."""
        with pytest.raises(ValueError):
            load_dataset('invalid_dataset_name')

    def test_standardize_all_datasets(self):
        """Test standardize_all_datasets function."""
        all_data = standardize_all_datasets()
        
        assert isinstance(all_data, dict)
        assert len(all_data) == 4
        assert all(isinstance(df, pd.DataFrame) for df in all_data.values())
        assert all(len(df) > 0 for df in all_data.values())


class TestStatistics:
    """Tests for statistics generation."""

    def test_get_statistics(self):
        """Test getting statistics for all datasets."""
        standardizer = DataStandardizer()
        stats = standardizer.get_statistics()
        
        assert isinstance(stats, dict)
        assert len(stats) == 4
        
        for dataset_name, dataset_stats in stats.items():
            assert 'total_records' in dataset_stats
            assert 'label_0_count' in dataset_stats
            assert 'label_1_count' in dataset_stats
            assert 'avg_text_length' in dataset_stats
            assert dataset_stats['label_0_count'] >= 0
            assert dataset_stats['label_1_count'] >= 0

    def test_label_distribution(self):
        """Test that label distribution makes sense."""
        standardizer = DataStandardizer()
        stats = standardizer.get_statistics()
        
        for dataset_name, dataset_stats in stats.items():
            total = dataset_stats['label_0_count'] + dataset_stats['label_1_count']
            assert total == dataset_stats['total_records']

    def test_text_length_positive(self):
        """Test that average text length is positive."""
        standardizer = DataStandardizer()
        stats = standardizer.get_statistics()
        
        for dataset_name, dataset_stats in stats.items():
            assert dataset_stats['avg_text_length'] > 0


class TestDataIntegrity:
    """Tests for data integrity and completeness."""

    def test_no_null_values(self):
        """Test that there are no null values in standardized data."""
        standardizer = DataStandardizer()
        standardizer.standardize_all()
        
        for dataset_name, df in standardizer.standardized_data.items():
            assert not df.isnull().any().any(), \
                f"{dataset_name} has null values"

    def test_correct_dtypes(self):
        """Test that data types are correct."""
        standardizer = DataStandardizer()
        standardizer.standardize_all()
        
        for dataset_name, df in standardizer.standardized_data.items():
            assert df['label'].dtype in ['int64', 'float64', 'int32'], \
                f"{dataset_name} label has wrong dtype"
            assert df['text'].dtype == 'object', \
                f"{dataset_name} text has wrong dtype"

    def test_label_value_counts(self):
        """Test that label value counts sum to total."""
        standardizer = DataStandardizer()
        standardizer.standardize_all()
        
        for dataset_name, df in standardizer.standardized_data.items():
            label_counts = df['label'].value_counts()
            assert label_counts.sum() == len(df)

    def test_consecutive_loading(self):
        """Test loading same dataset multiple times gives same result."""
        standardizer1 = DataStandardizer()
        df1 = standardizer1.load_sms_spam_main()
        
        standardizer2 = DataStandardizer()
        df2 = standardizer2.load_sms_spam_main()
        
        # Compare shape and basic stats
        assert df1.shape == df2.shape
        assert (df1['label'].value_counts() == df2['label'].value_counts()).all()


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_very_large_datasets(self):
        """Test handling of large datasets (SMS Spam main)."""
        standardizer = DataStandardizer()
        df = standardizer.load_sms_spam_main()
        
        assert len(df) > 1000  # Should have thousands of records
        assert len(df) < 100000  # But not impossibly large

    def test_small_datasets(self):
        """Test handling of small datasets (Perceptron and SVM)."""
        standardizer = DataStandardizer()
        df_perceptron = standardizer.load_sms_spam_perceptron()
        df_svm = standardizer.load_sms_spam_svm()
        
        assert 50 < len(df_perceptron) < 200
        assert 50 < len(df_svm) < 200

    def test_text_field_variation(self):
        """Test that text fields have variation."""
        standardizer = DataStandardizer()
        df = standardizer.load_sms_spam_main()
        
        # Check that there are unique text values
        unique_texts = df['text'].nunique()
        assert unique_texts > len(df) * 0.8  # At least 80% unique

    def test_label_balance_varies(self):
        """Test that different datasets have different label balances."""
        standardizer = DataStandardizer()
        standardizer.standardize_all()
        
        balances = {}
        for dataset_name, df in standardizer.standardized_data.items():
            label_0_count = (df['label'] == 0).sum()
            balance = label_0_count / len(df)
            balances[dataset_name] = balance
        
        # Different datasets should have different balances
        unique_balances = len(set(round(b, 2) for b in balances.values()))
        assert unique_balances >= 2  # At least 2 different balance ratios


class TestGetStandardizedData:
    """Tests for get_standardized_data method."""

    def test_get_standardized_data_single_dataset(self):
        """Test getting single standardized dataset."""
        standardizer = DataStandardizer()
        df = standardizer.get_standardized_data('sms_spam_main')
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert 'label' in df.columns
        assert 'text' in df.columns

    def test_get_standardized_data_caching(self):
        """Test that data is cached after first load."""
        standardizer = DataStandardizer()
        df1 = standardizer.get_standardized_data('sms_spam_main')
        df2 = standardizer.get_standardized_data('sms_spam_main')
        
        # Should be the same object (cached)
        assert df1 is df2

    def test_get_standardized_data_all_datasets(self):
        """Test getting all datasets via get_standardized_data."""
        standardizer = DataStandardizer()
        
        datasets = [
            'sms_spam_main',
            'phishing',
            'sms_spam_perceptron',
            'sms_spam_svm'
        ]
        
        for dataset_name in datasets:
            df = standardizer.get_standardized_data(dataset_name)
            assert isinstance(df, pd.DataFrame)
            assert len(df) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
