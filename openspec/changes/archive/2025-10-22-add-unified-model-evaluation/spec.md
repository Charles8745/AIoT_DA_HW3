# Specification: Model Evaluation Framework for Binary Classification

## Scope
This specification defines the `ModelEvaluator` class and related utilities for evaluating binary classification models. The framework supports task-scoped comparisons (same dataset, different algorithms) but explicitly excludes cross-task comparisons (different datasets).

## Requirements

### R1: Unified Binary Classification Metrics
Provide consistent calculation of classification metrics for binary classification models.

#### R1.1: Calculate Standard Metrics
```python
from sources.model_evaluation import ModelEvaluator

# Any sklearn-compatible binary classifier
evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)
metrics = evaluator.calculate_metrics()

# Returns dict with:
# - accuracy_train, accuracy_test
# - precision_train, precision_test
# - recall_train, recall_test
# - f1_train, f1_test
# - auc_roc_train, auc_roc_test
# - task_name (if provided)
```

**Acceptance Criteria**:
- ✅ All metrics match scikit-learn's implementation
- ✅ Handles edge cases (e.g., no positive samples in fold)
- ✅ Works with any sklearn binary classifier

#### R1.2: Input Validation
```python
# Error case: Multi-class classification (>2 classes)
try:
    evaluator = ModelEvaluator(model, X_train, y_train_multiclass, X_test, y_test_multiclass)
except ValueError as e:
    print(e)  # "Only binary classification supported. Found 4 classes"

# Error case: Model lacks predict_proba
try:
    evaluator = ModelEvaluator(linear_regression_model, X_train, y_train, X_test, y_test)
except AttributeError as e:
    print(e)  # "Model must have predict_proba() method. Linear Regression is not supported."
```

**Acceptance Criteria**:
- ✅ Raises ValueError for non-binary classification
- ✅ Raises AttributeError for incompatible models
- ✅ Clear error messages guide user

### R2: Model Visualizations
Provide standardized plots for analyzing binary classification models.

#### R2.1: Confusion Matrix Plot
```python
evaluator.plot_confusion_matrix()
# Displays:
# - 2x2 heatmap with TP, TN, FP, FN counts
# - Class labels (if available)
# - Color gradient (low=white, high=blue)
# - Title: "Confusion Matrix - [Task Name]"
```

**Acceptance Criteria**:
- ✅ Works for all binary classifiers
- ✅ Correctly counts TP, TN, FP, FN
- ✅ Handles imbalanced classes

#### R2.2: ROC Curve Plot
```python
evaluator.plot_roc_curve()
# Displays:
# - FPR vs TPR curve
# - AUC score in legend
# - Diagonal reference line (random classifier)
# - Title: "ROC Curve - [Task Name]"
```

**Acceptance Criteria**:
- ✅ ROC curve shape correct (curves from (0,0) to (1,1))
- ✅ AUC score matches sklearn.metrics.auc()
- ✅ Handles different probability thresholds

### R3: Task-Scoped Model Comparison
Enable fair comparison of different algorithms on the SAME dataset.

#### R3.1: Pairwise Comparison
```python
# Both evaluators trained on phishing_dataset.csv with same train/test split
evaluator_dt = ModelEvaluator(dt_model, X_train_phish, y_train_phish, 
                               X_test_phish, y_test_phish, task_name='phishing')
evaluator_lr = ModelEvaluator(lr_model, X_train_phish, y_train_phish, 
                               X_test_phish, y_test_phish, task_name='phishing')

# Comparison requires same dataset
comparison = evaluator_dt.compare_with(evaluator_lr)
# Returns DataFrame with metrics side-by-side

# Example output:
#              Decision_Tree  Logistic_Regression
# accuracy_train      0.96              0.94
# accuracy_test       0.94              0.93
# precision_test      0.91              0.89
# recall_test         0.92              0.91
# f1_test             0.915             0.900
# auc_roc_test        0.97              0.95
```

**Acceptance Criteria**:
- ✅ Returns pandas DataFrame with models as columns
- ✅ Raises ValueError if datasets have different shapes
- ✅ Works with 2+ models

#### R3.2: Cross-Dataset Comparison (Rejected)
```python
# NOT SUPPORTED: Cross-task comparison
evaluator_bayes = ModelEvaluator(bayes, X_train_spam, y_train_spam, 
                                  X_test_spam, y_test_spam, task_name='spam')
evaluator_dt = ModelEvaluator(dt, X_train_phish, y_train_phish, 
                               X_test_phish, y_test_phish, task_name='phishing')

try:
    comparison = evaluator_bayes.compare_with(evaluator_dt)
except ValueError as e:
    print(e)  # "Cannot compare: different dataset sizes (5574 vs 11054 samples)"
```

**Acceptance Criteria**:
- ✅ Raises ValueError for different dataset shapes
- ✅ Prevents misleading cross-task comparisons

#### R3.3: Multi-Model Visualization
```python
from sources.model_evaluation import plot_model_comparison

evaluators = {
    'Bayesian': eval_bayes,
    'SVM': eval_svm,
    'Perceptron': eval_perceptron
}

plot_model_comparison(evaluators)
# Displays bar chart with grouped metrics:
# - X-axis: Metric (accuracy, precision, recall, F1, AUC)
# - Y-axis: Score
# - Grouped by model (different colors)
# - Title: "Model Comparison - [Task Name]"
```

**Acceptance Criteria**:
- ✅ Works with 2+ evaluators from same task
- ✅ Clear visual distinction between models
- ✅ Readable legend with model names

### R4: Integration with Supported Models
Framework must work with all supported binary classifiers and reject unsupported models.

#### R4.1: Supported Models ✅
```python
# All these should work:
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import Perceptron, LogisticRegression
from sklearn.svm import SVC

evaluator = ModelEvaluator(GaussianNB(), X_train, y_train, X_test, y_test)
evaluator = ModelEvaluator(DecisionTreeClassifier(), X_train, y_train, X_test, y_test)
evaluator = ModelEvaluator(Perceptron(), X_train, y_train, X_test, y_test)
evaluator = ModelEvaluator(LogisticRegression(), X_train, y_train, X_test, y_test)
evaluator = ModelEvaluator(SVC(probability=True), X_train, y_train, X_test, y_test)
```

**Acceptance Criteria**:
- ✅ All models initialize successfully
- ✅ All generate metrics without error
- ✅ All generate visualizations

#### R4.2: Explicitly Unsupported Models ❌
```python
# Linear Regression - not classification
from sklearn.linear_model import LinearRegression
try:
    evaluator = ModelEvaluator(LinearRegression(), X_train, y_train, X_test, y_test)
except AttributeError as e:
    print(e)  # "Model must have predict_proba() method. Linear Regression is not supported."

# Multi-class classifier
from sklearn.ensemble import RandomForestClassifier
y_multiclass = [0, 1, 2, 0, 1, 2, ...]  # 3 classes
try:
    evaluator = ModelEvaluator(RandomForestClassifier(), X_train, y_multiclass, X_test, y_test_multiclass)
except ValueError as e:
    print(e)  # "Only binary classification supported. Found 3 classes: [0 1 2]"
```

**Acceptance Criteria**:
- ✅ Linear Regression raises clear error
- ✅ Multi-class raises clear error
- ✅ Error messages explain why

### R5: Data Standardization Requirements
All models for a given task must use the same train/test split for meaningful comparison.

#### R5.1: Phishing Detection Task
- **Dataset**: `datasets/phishing_dataset.csv`
- **Samples**: 11,054
- **Train/Test Split**: 70/30 (random_state=42)
- **Models**: Decision Tree, Logistic Regression

#### R5.2: Spam Detection Task (Standardized)
- **Dataset**: `datasets/sms_spam_no_header.csv` (standardized)
- **Samples**: 5,574
- **Train/Test Split**: 70/30 (random_state=42)
- **Models**: Bayesian, Perceptron, SVM
- **Note**: Perceptron and SVM will migrate from their smaller datasets (sms_spam_perceptron.csv, sms_spam_svm.csv)

**Acceptance Criteria**:
- ✅ All models for phishing task use phishing_dataset.csv
- ✅ All models for spam task use sms_spam_no_header.csv
- ✅ All use identical train/test splits
- ✅ Results are comparable across models

## Code Examples

### Example 1: Evaluate Single Model
```python
from sources.model_evaluation import ModelEvaluator
from sklearn.tree import DecisionTreeClassifier

# Train model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Evaluate
evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test, task_name='phishing')
metrics = evaluator.calculate_metrics()
print(f"Test Accuracy: {metrics['accuracy_test']:.3f}")

# Visualize
evaluator.plot_confusion_matrix()
evaluator.plot_roc_curve()
```

### Example 2: Compare Two Algorithms
```python
from sources.model_evaluation import ModelEvaluator
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression

# Train both models on same data
dt_model = DecisionTreeClassifier().fit(X_train, y_train)
lr_model = LogisticRegression().fit(X_train, y_train)

# Create evaluators
eval_dt = ModelEvaluator(dt_model, X_train, y_train, X_test, y_test, task_name='phishing')
eval_lr = ModelEvaluator(lr_model, X_train, y_train, X_test, y_test, task_name='phishing')

# Compare
comparison = eval_dt.compare_with(eval_lr)
print(comparison)
```

### Example 3: Compare Multiple Spam Algorithms
```python
from sources.model_evaluation import ModelEvaluator, plot_model_comparison
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.svm import SVC

# All trained on same spam dataset
eval_bayes = ModelEvaluator(GaussianNB().fit(X_train, y_train), 
                             X_train, y_train, X_test, y_test, task_name='spam')
eval_perceptron = ModelEvaluator(Perceptron().fit(X_train, y_train), 
                                  X_train, y_train, X_test, y_test, task_name='spam')
eval_svm = ModelEvaluator(SVC(probability=True).fit(X_train, y_train), 
                           X_train, y_train, X_test, y_test, task_name='spam')

# Multi-model comparison
plot_model_comparison({
    'Bayesian': eval_bayes,
    'Perceptron': eval_perceptron,
    'SVM': eval_svm
})
```

## Constraints
- ✅ Binary classification only (2 classes)
- ✅ Task-scoped comparison only (same dataset required)
- ✅ sklearn-compatible models only
- ✅ Models must have predict() and predict_proba() methods
- ✅ No multi-class support in this version

