# Change Proposal: Unified ML Model Evaluation Framework

## Summary
Implement a standardized model evaluation and reporting module to provide consistent metrics, visualizations, and comparison tools across classification models (Bayesian, Decision Tree, Perceptron, SVM, Logistic Regression). Framework supports binary classification with task-scoped model comparisons.

## Motivation
Currently, each ML notebook implements its own evaluation logic, leading to:
- Inconsistent metric calculations and reporting
- Duplicated visualization code (confusion matrices, ROC curves, metrics)
- Difficulty comparing model performance within same task
- Manual metric extraction for comparison analysis
- No standardized documentation of evaluation methodology

This change provides reusable evaluation utilities that:
- Ensure consistent metrics across all models
- Simplify notebook code and improve maintainability
- Enable performance comparison between models within same task
- Generate standardized, reproducible reports
- Reduce code duplication (~30-40% reduction per notebook)

## Scope
- Create evaluation module in `sources/model_evaluation.py`
- **ModelEvaluator** class for binary classification tasks
- Metrics: accuracy, precision, recall, F1-score, AUC-ROC
- Visualizations: confusion matrices, ROC curves, performance comparison
- Support task-scoped model comparison (same dataset, different algorithms)
- Integration with existing notebooks (Bayesian, Decision Tree, Perceptron, SVM, Logistic Regression)

### Out of Scope (Explicitly Excluded)
- ❌ Linear Regression (regression algorithm, not classification)
- ❌ Multi-class classification (not applicable to current datasets)
- ❌ Cross-task model comparison (different datasets, different evaluation metrics)

## Supported Tasks

### ✅ Phishing Detection Task
- **Dataset**: `datasets/phishing_dataset.csv` (11,054 samples, 31 features)
- **Models**: Decision Tree, Logistic Regression
- **Classes**: Binary (0=legitimate, 1=phishing)

### ✅ Spam Detection Task (Standardized)
- **Dataset**: `datasets/sms_spam_no_header.csv` (5,574 samples)
  - **Note**: Perceptron and SVM will use this standard dataset instead of their current smaller variants
  - **Previous datasets deprecated**: sms_spam_perceptron.csv, sms_spam_svm.csv
- **Models**: Bayesian, Perceptron, SVM
- **Classes**: Binary (ham=0, spam=1)

## Data Standardization Strategy

To enable meaningful model comparisons within each task:
- Each task uses a single standard dataset
- All models for a task use identical train/test split (train_size=0.8, test_size=0.2, random_state=42)
- Metrics are computed on the same evaluation set for fair comparison

## Impact
- **Low**: No breaking changes to existing notebook outputs
- **Data**: Perceptron and SVM will use larger, standardized dataset (improvement)
- **Maintenance**: Reduces code duplication by ~30-40% per notebook
- **Quality**: Ensures metric consistency across all models
- **Reusability**: Evaluation logic centralized and testable

## Approval Status
- [x] Ready for implementation (2025-10-22)
  - ✅ Decision: Task-scoped comparison only (no cross-task)
  - ✅ Decision: Standardize spam task to sms_spam_no_header.csv
  - ✅ Decision: Linear Regression explicitly excluded
  - ✅ Decision: Binary classification only (no multi-class)
