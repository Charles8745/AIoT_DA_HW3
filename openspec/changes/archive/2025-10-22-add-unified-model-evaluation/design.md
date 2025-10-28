# Design: Unified Model Evaluation Framework

## Overview
This module provides a standardized evaluation framework for **binary classification models**. It encapsulates common evaluation patterns found across existing ML notebooks, enabling consistent metrics calculation and task-scoped model comparison.

## Architecture

### Module Structure
```
sources/model_evaluation.py
├── ModelEvaluator (class)
│   ├── __init__(model, X_train, y_train, X_test, y_test, task_name=None)
│   ├── calculate_metrics() → dict
│   ├── plot_confusion_matrix() → matplotlib.figure
│   ├── plot_roc_curve() → matplotlib.figure
│   ├── generate_report() → str
│   └── compare_with(other_evaluator) → DataFrame
└── Utility Functions
    ├── _validate_binary_classification(y)
    ├── _validate_model_compatibility(model)
    └── plot_model_comparison(evaluators_dict) → matplotlib.figure
```

## Key Components

### 1. ModelEvaluator Class

```python
class ModelEvaluator:
    def __init__(self, model, X_train, y_train, X_test, y_test, task_name=None):
        """
        Initialize evaluator for binary classification model.
        
        Raises:
            ValueError: If y is not binary classification
            AttributeError: If model lacks required methods
        """
```

**Initialization Validation**:
1. **Model Compatibility Check**
   - Verify model has `predict()` method
   - Verify model has `predict_proba()` method (for ROC curve)
   - Raise error if not sklearn-compatible

2. **Binary Classification Check**
   - Verify `y_train` has exactly 2 unique classes
   - Verify `y_test` has exactly 2 unique classes
   - Raise ValueError if not binary

3. **Data Shape Validation**
   - Verify X_train.shape[0] == len(y_train)
   - Verify X_test.shape[0] == len(y_test)
   - Verify X_train.shape[1] == X_test.shape[1]

### 2. Metrics Calculation

**Supported Metrics** (binary classification only):
- **Accuracy**: (TP + TN) / (TP + TN + FP + FN)
- **Precision**: TP / (TP + FP)
- **Recall**: TP / (TP + FN)
- **F1-Score**: 2 * (Precision * Recall) / (Precision + Recall)
- **AUC-ROC**: Area under ROC curve

### 3. Visualizations

**Confusion Matrix**:
- 2x2 heatmap showing TP, TN, FP, FN
- Automatically labeled with class names if available

**ROC Curve**:
- Plot FPR vs TPR with AUC score

### 4. Task-Scoped Comparison

```python
def compare_with(self, other_evaluator) -> pd.DataFrame:
    """
    Compare metrics with another evaluator.
    Requirements: Same dataset, both binary classification
    """
```

**Comparison Validation**:
- Check that both evaluators use same test set size
- Check that both evaluators use same feature count
- Allow comparison only if checks pass

## Design Decisions

### Decision 1: Binary Classification Only ✅
**Rationale**: All current datasets are binary

### Decision 2: Task-Scoped Comparison ✅
**Rationale**: Phishing and spam use different datasets - cross-task comparison would be misleading

### Decision 3: Linear Regression Exclusion ✅
**Rationale**: Regression algorithm, not classification

## Supported Models

### ✅ Supported
- Bayesian Classifier
- Decision Tree Classifier
- Perceptron
- Support Vector Machine (SVM)
- Logistic Regression

### ❌ Explicitly Not Supported
- Linear Regression (regression algorithm)
- Multi-class classifiers

## Integration Strategy

### Phishing Detection Task
```python
from sources.model_evaluation import ModelEvaluator

evaluator_dt = ModelEvaluator(dt_model, X_train, y_train, X_test, y_test, 
                               task_name='phishing')
evaluator_dt.plot_confusion_matrix()
evaluator_dt.plot_roc_curve()
metrics_dt = evaluator_dt.calculate_metrics()

# Compare models within same task
evaluator_lr = ModelEvaluator(lr_model, X_train, y_train, X_test, y_test,
                               task_name='phishing')
comparison = evaluator_dt.compare_with(evaluator_lr)
```

### Spam Detection Task (Standardized Dataset)
```python
# All models use same dataset: sms_spam_no_header.csv

evaluator_bayes = ModelEvaluator(bayes_model, X_train, y_train, X_test, y_test,
                                  task_name='spam')
evaluator_svm = ModelEvaluator(svm_model, X_train, y_train, X_test, y_test,
                                task_name='spam')

# Compare on same dataset
comparison = evaluator_bayes.compare_with(evaluator_svm)
```

## Future Extensions
- Cross-validation metrics
- Feature importance visualization
- Threshold optimization curve

