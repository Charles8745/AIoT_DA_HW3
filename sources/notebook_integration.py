"""
Notebook Integration Utilities

This module provides utilities to facilitate integration of the new
evaluation and standardization tools into existing Jupyter notebooks.

Functions:
- get_integration_code(): Returns code snippets for notebook integration
- create_integration_section(): Returns formatted markdown section
"""

from typing import Dict, Tuple


def get_standard_imports() -> str:
    """
    Get standard import statements for notebooks.
    
    Returns:
        Multi-line string with all necessary imports
    """
    return '''# Standard imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# AIoT_DA_HW3 modules
from sys import path
path.insert(0, '.')

from sources.data_standardization import load_dataset, standardize_all_datasets
from sources.model_evaluation import ModelEvaluator, plot_model_comparison
from sources.model_evaluation import plot_confusion_matrix, plot_roc_curve, generate_report

# Visualization settings
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
%matplotlib inline
'''


def get_data_loading_code(dataset_name: str = 'sms_spam_main') -> str:
    """
    Get code snippet for loading standardized data.
    
    Args:
        dataset_name: Name of dataset to load
        
    Returns:
        Python code for data loading
    """
    return f'''# Load standardized data
df = load_dataset('{dataset_name}')

# Separate features and labels
X = df['text'].values
y = df['label'].values

print(f"Dataset: {dataset_name}")
print(f"Total samples: {{len(df)}}")
print(f"Label distribution:")
print(df['label'].value_counts())

# Train-test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)
'''


def get_model_training_code(model_name: str = 'LogisticRegression') -> str:
    """
    Get code snippet for model training.
    
    Args:
        model_name: Type of model to train
        
    Returns:
        Python code for model training
    """
    models_code = {
        'LogisticRegression': '''from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

# Vectorize text data
vectorizer = TfidfVectorizer(max_features=5000, lowercase=True, 
                             stop_words='english')
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train model
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_vec, y_train)

print(f"Model trained. Accuracy: {model.score(X_test_vec, y_test):.4f}")
''',
        'SVM': '''from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer

# Vectorize text data
vectorizer = TfidfVectorizer(max_features=5000, lowercase=True, 
                             stop_words='english')
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train model
model = SVC(kernel='rbf', probability=True, random_state=42)
model.fit(X_train_vec, y_train)

print(f"Model trained. Accuracy: {model.score(X_test_vec, y_test):.4f}")
''',
        'Perceptron': '''from sklearn.linear_model import Perceptron
from sklearn.feature_extraction.text import TfidfVectorizer

# Vectorize text data
vectorizer = TfidfVectorizer(max_features=5000, lowercase=True, 
                             stop_words='english')
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train model
model = Perceptron(max_iter=100, random_state=42)
model.fit(X_train_vec, y_train)

print(f"Model trained. Accuracy: {model.score(X_test_vec, y_test):.4f}")
''',
    }
    
    return models_code.get(model_name, models_code['LogisticRegression'])


def get_evaluation_code() -> str:
    """
    Get code snippet for model evaluation using ModelEvaluator.
    
    Returns:
        Python code for evaluation
    """
    return '''# Model Evaluation using AIoT_DA_HW3 tools
# Note: Requires vectorized features (X_train_vec, X_test_vec) and trained model

# Create evaluator wrapper for vectorized model
class VectorizedModelEvaluator:
    """Wrapper to adapt vectorized model to ModelEvaluator interface"""
    def __init__(self, vectorizer, model, X_train, y_train, X_test, y_test, task_name=None):
        self.vectorizer = vectorizer
        self.model = model
        self.X_train_vec = vectorizer.transform(X_train)
        self.X_test_vec = vectorizer.transform(X_test)
        self.y_train = y_train
        self.y_test = y_test
        self.task_name = task_name
    
    def predict(self, X):
        X_vec = self.vectorizer.transform(X) if isinstance(X, list) else self.vectorizer.transform(X)
        return self.model.predict(X_vec)
    
    def predict_proba(self, X):
        X_vec = self.vectorizer.transform(X) if isinstance(X, list) else self.vectorizer.transform(X)
        return self.model.predict_proba(X_vec)

# Create evaluator
wrapped_model = VectorizedModelEvaluator(vectorizer, model, X_train, y_train, X_test, y_test,
                                         task_name='Spam Detector')

evaluator = ModelEvaluator(wrapped_model, X_train, y_train, X_test, y_test,
                           task_name='Spam Detector')

# Calculate metrics
metrics = evaluator.calculate_metrics()
print("\\n=== Model Metrics ===")
for metric, value in metrics.items():
    print(f"{metric}: {value:.4f}")

# Generate visualizations
fig1, ax1 = evaluator.plot_confusion_matrix(use_test=True)
plt.show()

fig2, ax2 = evaluator.plot_roc_curve(use_test=True)
plt.show()

# Generate text report
report = evaluator.generate_report(use_test=True)
print("\\n" + report)
'''


def get_comparison_code() -> str:
    """
    Get code snippet for comparing multiple models.
    
    Returns:
        Python code for model comparison
    """
    return '''# Comparing Multiple Models
# Assumes you have trained multiple models and created evaluators

# Example: Train multiple models
models_to_compare = []

# Model 1: Logistic Regression
from sklearn.linear_model import LogisticRegression
model1 = LogisticRegression(max_iter=1000, random_state=42)
model1.fit(X_train_vec, y_train)
ev1 = ModelEvaluator(model1, X_train_vec.toarray(), y_train, X_test_vec.toarray(), y_test,
                     task_name='Logistic Regression')
models_to_compare.append(ev1)

# Model 2: SVM
from sklearn.svm import SVC
model2 = SVC(kernel='rbf', probability=True, random_state=42)
model2.fit(X_train_vec, y_train)
ev2 = ModelEvaluator(model2, X_train_vec.toarray(), y_train, X_test_vec.toarray(), y_test,
                     task_name='SVM')
models_to_compare.append(ev2)

# Compare on different metrics
metrics_to_compare = ['accuracy_test', 'precision_test', 'recall_test', 'f1_test', 'auc_roc_test']

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for idx, metric in enumerate(metrics_to_compare):
    plot_model_comparison(models_to_compare, metric=metric, ax=axes[idx])

plt.tight_layout()
plt.show()
'''


def get_integration_guide() -> str:
    """
    Get complete integration guide for notebooks.
    
    Returns:
        Markdown formatted integration guide
    """
    return '''# Notebook Integration Guide

## Overview
This guide shows how to integrate the new AIoT_DA_HW3 evaluation tools into your Jupyter notebooks.

## New Features Available

### 1. Data Standardization
All datasets now available in unified format (label, text).

```python
from sources.data_standardization import load_dataset

df = load_dataset('sms_spam_main')  # or 'phishing', etc.
X = df['text'].values
y = df['label'].values
```

### 2. Model Evaluation
Comprehensive evaluation metrics with visualization.

```python
from sources.model_evaluation import ModelEvaluator

evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)
metrics = evaluator.calculate_metrics()

# Visualizations
evaluator.plot_confusion_matrix(use_test=True)
evaluator.plot_roc_curve(use_test=True)
report = evaluator.generate_report(use_test=True)
```

### 3. Model Comparison
Compare multiple models on same metrics.

```python
from sources.model_evaluation import plot_model_comparison

evaluators = [ev1, ev2, ev3]  # List of ModelEvaluator instances
fig, ax = plot_model_comparison(evaluators, metric='f1_test')
```

## Integration Steps

### Step 1: Add Imports
Copy the standard imports from get_standard_imports()

### Step 2: Load Data
Use the standardized data loading code

### Step 3: Train Models
Use existing model training code or update as needed

### Step 4: Evaluate Models
Add evaluation code using ModelEvaluator

### Step 5: Compare Results
Use plot_model_comparison() to compare multiple models

## Code Examples

See get_data_loading_code(), get_model_training_code(), 
get_evaluation_code(), get_comparison_code() for specific examples.

## Benefits
- Standardized data across all notebooks
- Consistent evaluation metrics
- Professional visualizations
- Easy model comparison
- Better reproducibility
'''


def create_integration_summary() -> Dict[str, str]:
    """
    Create summary of all integration code snippets.
    
    Returns:
        Dictionary with code snippets by category
    """
    return {
        'imports': get_standard_imports(),
        'data_loading': get_data_loading_code(),
        'model_training_lr': get_model_training_code('LogisticRegression'),
        'model_training_svm': get_model_training_code('SVM'),
        'model_training_perceptron': get_model_training_code('Perceptron'),
        'evaluation': get_evaluation_code(),
        'comparison': get_comparison_code(),
        'guide': get_integration_guide(),
    }


if __name__ == "__main__":
    # Print integration guide
    guide = get_integration_guide()
    print(guide)
    
    # Save code snippets
    summary = create_integration_summary()
    
    print("\n" + "="*80)
    print("AVAILABLE CODE SNIPPETS:")
    print("="*80)
    for name in summary.keys():
        print(f"  - {name}")
