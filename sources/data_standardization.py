"""
Data Standardization Module for AIoT_DA_HW3

This module provides standardization pipelines to convert all datasets
to a consistent format (sms_spam_no_header.csv structure with 'label' and 'text' columns).

Datasets standardized:
- phishing_dataset.csv: Binary classification features (no text, numerical)
- sms_spam_perceptron.csv: Subset with 3 columns (type, sex, buy)
- sms_spam_svm.csv: Subset with 3 columns (type, suspect, neutral)
- sms_spam_no_header.csv: Target format (label, text)

Author: AIoT_DA_HW3
Date: 2024-12-19
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional, Dict, Any
import logging
from sklearn.preprocessing import LabelEncoder

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataStandardizer:
    """
    Standardize different datasets to a common format.
    
    Target format:
    - Columns: 'label', 'text'
    - Label: binary (0, 1 or 'ham', 'spam')
    - Text: string representation of data
    """

    # Standard dataset paths
    PHISHING_PATH = Path('datasets/phishing_dataset.csv')
    SMS_SPAM_MAIN_PATH = Path('datasets/sms_spam_no_header.csv')
    SMS_SPAM_PERCEPTRON_PATH = Path('datasets/sms_spam_perceptron.csv')
    SMS_SPAM_SVM_PATH = Path('datasets/sms_spam_svm.csv')

    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialize DataStandardizer.
        
        Args:
            base_path: Base path for datasets (default: current working directory)
        """
        self.base_path = base_path or Path('.')
        self.standardized_data = {}

    def load_sms_spam_main(self) -> pd.DataFrame:
        """
        Load sms_spam_no_header.csv (already in target format).
        
        Returns:
            DataFrame with columns: label, text
        """
        path = self.base_path / self.SMS_SPAM_MAIN_PATH
        logger.info(f"Loading SMS Spam main dataset from {path}")
        
        df = pd.read_csv(path, quotechar='"', skipinitialspace=True)
        df.columns = ['label', 'text']
        
        # Normalize labels
        df['label'] = df['label'].str.lower().str.strip()
        df['label'] = df['label'].map({'ham': 0, 'spam': 1})
        
        logger.info(f"Loaded {len(df)} records from SMS Spam main dataset")
        return df

    def load_phishing_dataset(self) -> pd.DataFrame:
        """
        Load phishing_dataset.csv and convert to standard format.
        
        Phishing dataset has 31 numerical features and 1 label column.
        No text data, so we'll create text representation of features.
        
        Returns:
            DataFrame with columns: label, text
        """
        path = self.base_path / self.PHISHING_PATH
        logger.info(f"Loading Phishing dataset from {path}")
        
        df = pd.read_csv(path, header=None)
        
        # Last column is label (-1, 1), first 31 are features
        label_col = df.iloc[:, -1]
        feature_cols = df.iloc[:, :-1]
        
        # Convert label: -1 (legitimate) -> 0, 1 (phishing) -> 1
        df_std = pd.DataFrame({
            'label': label_col.map({-1: 0, 1: 1}),
            'text': feature_cols.apply(
                lambda row: ','.join(map(str, row.values)),
                axis=1
            )
        })
        
        logger.info(f"Loaded {len(df_std)} records from Phishing dataset")
        return df_std

    def load_sms_spam_perceptron(self) -> pd.DataFrame:
        """
        Load sms_spam_perceptron.csv and convert to standard format.
        
        Has columns: type (label), sex, buy
        
        Returns:
            DataFrame with columns: label, text
        """
        path = self.base_path / self.SMS_SPAM_PERCEPTRON_PATH
        logger.info(f"Loading SMS Spam Perceptron dataset from {path}")
        
        df = pd.read_csv(path, quotechar='"')
        
        # 'type' is the label, combine sex and buy as text
        df_std = pd.DataFrame({
            'label': df['type'].str.lower().str.strip().map({'ham': 0, 'spam': 1}),
            'text': df.apply(
                lambda row: f"sex:{row['sex']},buy:{row['buy']}",
                axis=1
            )
        })
        
        logger.info(f"Loaded {len(df_std)} records from SMS Spam Perceptron dataset")
        return df_std

    def load_sms_spam_svm(self) -> pd.DataFrame:
        """
        Load sms_spam_svm.csv and convert to standard format.
        
        Has columns: type (label), suspect, neutral
        
        Returns:
            DataFrame with columns: label, text
        """
        path = self.base_path / self.SMS_SPAM_SVM_PATH
        logger.info(f"Loading SMS Spam SVM dataset from {path}")
        
        df = pd.read_csv(path)
        
        # 'type' is the label, combine suspect and neutral as text
        df_std = pd.DataFrame({
            'label': df['type'].str.lower().str.strip().map({'ham': 0, 'spam': 1}),
            'text': df.apply(
                lambda row: f"suspect:{row['suspect']},neutral:{row['neutral']}",
                axis=1
            )
        })
        
        logger.info(f"Loaded {len(df_std)} records from SMS Spam SVM dataset")
        return df_std

    def standardize_all(self) -> Dict[str, pd.DataFrame]:
        """
        Load and standardize all datasets.
        
        Returns:
            Dictionary with standardized dataframes
        """
        self.standardized_data = {
            'sms_spam_main': self.load_sms_spam_main(),
            'phishing': self.load_phishing_dataset(),
            'sms_spam_perceptron': self.load_sms_spam_perceptron(),
            'sms_spam_svm': self.load_sms_spam_svm(),
        }
        
        total_records = sum(len(df) for df in self.standardized_data.values())
        logger.info(f"Total standardized records: {total_records}")
        
        return self.standardized_data

    def get_standardized_data(self, dataset_name: str) -> pd.DataFrame:
        """
        Get standardized data for a specific dataset.
        
        Args:
            dataset_name: Name of dataset ('sms_spam_main', 'phishing', etc.)
            
        Returns:
            Standardized DataFrame
            
        Raises:
            ValueError: If dataset not found
        """
        if not self.standardized_data:
            self.standardize_all()
        
        if dataset_name not in self.standardized_data:
            raise ValueError(f"Dataset '{dataset_name}' not found")
        
        return self.standardized_data[dataset_name]

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics for all standardized datasets.
        
        Returns:
            Dictionary with statistics
        """
        if not self.standardized_data:
            self.standardize_all()
        
        stats = {}
        for name, df in self.standardized_data.items():
            labels = df['label'].value_counts()
            stats[name] = {
                'total_records': len(df),
                'label_0_count': labels.get(0, 0),
                'label_1_count': labels.get(1, 0),
                'label_0_pct': f"{labels.get(0, 0) / len(df) * 100:.2f}%",
                'label_1_pct': f"{labels.get(1, 0) / len(df) * 100:.2f}%",
                'avg_text_length': df['text'].str.len().mean(),
            }
        
        return stats

    def print_statistics(self):
        """Print statistics for all standardized datasets."""
        stats = self.get_statistics()
        
        print("\n" + "=" * 80)
        print("DATA STANDARDIZATION STATISTICS")
        print("=" * 80)
        
        for dataset_name, dataset_stats in stats.items():
            print(f"\n{dataset_name.upper()}")
            print("-" * 80)
            for key, value in dataset_stats.items():
                print(f"  {key}: {value}")
        
        print("\n" + "=" * 80)


def load_dataset(
    dataset_name: str = 'sms_spam_main',
    base_path: Optional[Path] = None
) -> pd.DataFrame:
    """
    Convenience function to load and standardize a dataset.
    
    Args:
        dataset_name: Name of dataset to load
        base_path: Base path for datasets
        
    Returns:
        Standardized DataFrame with columns: label, text
        
    Example:
        >>> df = load_dataset('sms_spam_main')
        >>> print(df.head())
    """
    standardizer = DataStandardizer(base_path)
    return standardizer.get_standardized_data(dataset_name)


def standardize_all_datasets(
    base_path: Optional[Path] = None
) -> Dict[str, pd.DataFrame]:
    """
    Convenience function to load and standardize all datasets.
    
    Args:
        base_path: Base path for datasets
        
    Returns:
        Dictionary of standardized dataframes
        
    Example:
        >>> datasets = standardize_all_datasets()
        >>> for name, df in datasets.items():
        ...     print(f"{name}: {len(df)} records")
    """
    standardizer = DataStandardizer(base_path)
    return standardizer.standardize_all()


if __name__ == "__main__":
    # Example usage
    standardizer = DataStandardizer()
    standardizer.standardize_all()
    standardizer.print_statistics()
