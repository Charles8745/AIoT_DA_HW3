# Implementation Tasks: Unified Model Evaluation Framework

## Phase 1: Core Module Development

### Task 1.1: Create ModelEvaluator Class
- [ ] Create `sources/model_evaluation.py`
- [ ] Implement class definition with docstring
- [ ] Implement `__init__` method with parameters:
  - `model` (sklearn-compatible classifier)
  - `X_train, y_train, X_test, y_test` (data and labels)
  - `task_name` (optional, for identification)

### Task 1.2: Input Validation
- [ ] Implement `_validate_model_compatibility(model)`
  - Check for `predict()` method
  - Check for `predict_proba()` method
  - Raise `AttributeError` if missing with clear message
  - Explicitly check for Linear Regression and reject
  
- [ ] Implement `_validate_binary_classification(y_train, y_test)`
  - Check `y_train` has exactly 2 unique classes
  - Check `y_test` has exactly 2 unique classes
  - Raise `ValueError` if not binary with clear message
  
- [ ] Implement `_validate_data_shapes(X_train, y_train, X_test, y_test)`
  - Verify shapes are consistent
  - Raise `ValueError` if mismatched

### Task 1.3: Implement calculate_metrics()
- [ ] Calculate train metrics:
  - Generate predictions on training data
  - Calculate: accuracy, precision, recall, F1-score, AUC-ROC
  - Store in dict with keys: accuracy_train, precision_train, etc.
  
- [ ] Calculate test metrics:
  - Generate predictions on test data
  - Calculate: accuracy, precision, recall, F1-score, AUC-ROC
  - Store in dict with keys: accuracy_test, precision_test, etc.
  
- [ ] Add task_name to output dict if provided
- [ ] Verify results match scikit-learn exactly

### Task 1.4: Core Module Testing (30+ tests)
- [ ] Test valid binary classifier initialization ✅
- [ ] Test invalid classifier (no predict_proba) raises error ✅
- [ ] Test non-binary y raises error ✅
- [ ] Test mismatched data shapes raise error ✅
- [ ] Test metrics calculation accuracy (vs sklearn) ✅
- [ ] Test edge cases:
  - [ ] All predictions correct (perfect model)
  - [ ] All predictions wrong (zero model)
  - [ ] Imbalanced classes
  - [ ] Very small datasets (n < 10)

## Phase 2: Visualization Methods

### Task 2.1: Implement plot_confusion_matrix()
- [ ] Generate confusion matrix using sklearn
- [ ] Create 2x2 heatmap using matplotlib
- [ ] Add labels for TP, TN, FP, FN
- [ ] Add class labels if available
- [ ] Add title: "Confusion Matrix - [task_name]"
- [ ] Use appropriate colormap
- [ ] Return matplotlib figure object

### Task 2.2: Implement plot_roc_curve()
- [ ] Get probability predictions from model
- [ ] Calculate FPR and TPR using sklearn
- [ ] Calculate AUC score
- [ ] Plot ROC curve with AUC in legend
- [ ] Add diagonal reference line
- [ ] Add labels and title
- [ ] Return matplotlib figure object

### Task 2.3: Implement generate_report()
- [ ] Format metrics as readable text
- [ ] Include train and test metrics
- [ ] Format numbers to 2-3 decimal places
- [ ] Return formatted string

### Task 2.4: Visualization Testing (15+ tests)
- [ ] Test confusion matrix rendering ✅
- [ ] Test ROC curve AUC calculation ✅
- [ ] Test on various classifier types ✅
- [ ] Test on different dataset sizes ✅
- [ ] Test report format and completeness ✅

## Phase 3: Comparison Tools

### Task 3.1: Implement compare_with()
- [ ] Check that both evaluators use same test set size
  - Get test_size from both evaluators
  - Raise `ValueError` if mismatch
  
- [ ] Check that both evaluators use same feature count
  - Get feature count from X_test
  - Raise `ValueError` if mismatch
  
- [ ] Combine metrics into DataFrame with models as columns
- [ ] Return comparison DataFrame

### Task 3.2: Implement plot_model_comparison()
- [ ] Accept dict or list of evaluators
- [ ] Extract key metrics: accuracy, precision, recall, F1, AUC
- [ ] Create grouped bar chart:
  - X-axis: metrics
  - Y-axis: scores (0-1)
  - Grouped by model
  - Different colors per model
  
- [ ] Add title, legend, axis labels
- [ ] Return matplotlib figure object

### Task 3.3: Comparison Testing (10+ tests)
- [ ] Test compare_with() with compatible evaluators ✅
- [ ] Test compare_with() raises error for different datasets ✅
- [ ] Test plot_model_comparison() with 2+ models ✅
- [ ] Test comparison accuracy ✅

## Phase 4: Data Standardization

### Task 4.1: Verify/Prepare Phishing Detection Task
- [ ] Confirm phishing_dataset.csv has 11,054 samples ✅
- [ ] Define standard split: train_size=0.8, test_size=0.2, random_state=42
- [ ] Verify Decision Tree uses this split
- [ ] Verify Logistic Regression uses this split
- [ ] Document in integration guide

### Task 4.2: Standardize Spam Detection Task
- [ ] Confirm sms_spam_no_header.csv has 5,574 samples ✅
- [ ] Define standard split: train_size=0.8, test_size=0.2, random_state=42
- [ ] **Create data processing guide for Perceptron notebook**
  - Show migration from sms_spam_perceptron.csv to sms_spam_no_header.csv
  - Explain feature extraction from text
  - Provide sample code
  
- [ ] **Create data processing guide for SVM notebook**
  - Show migration from sms_spam_svm.csv to sms_spam_no_header.csv
  - Explain feature extraction
  - Provide sample code
  
- [ ] Document deprecation of old datasets

### Task 4.3: Verification Tests
- [ ] Verify Bayesian uses sms_spam_no_header.csv ✅
- [ ] Verify Perceptron can use sms_spam_no_header.csv ✅
- [ ] Verify SVM can use sms_spam_no_header.csv ✅
- [ ] Verify train/test splits are identical ✅

## Phase 5: Notebook Integration

### Task 5.1: Bayesian Spam Detector Integration
- [ ] Import ModelEvaluator at top of notebook
- [ ] Replace existing evaluation code with:
  ```python
  evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test, 
                             task_name='spam')
  metrics = evaluator.calculate_metrics()
  evaluator.plot_confusion_matrix()
  evaluator.plot_roc_curve()
  ```
- [ ] Verify results match original evaluation
- [ ] Test notebook runs without errors

### Task 5.2: Decision Tree Integration
- [ ] Import ModelEvaluator
- [ ] Replace evaluation code (same as above but task_name='phishing')
- [ ] Verify results match original
- [ ] Test notebook runs

### Task 5.3: Perceptron Integration
- [ ] **First**: Update to use sms_spam_no_header.csv
- [ ] Import ModelEvaluator
- [ ] Replace evaluation code
- [ ] Verify results
- [ ] Test notebook runs

### Task 5.4: SVM Integration
- [ ] **First**: Update to use sms_spam_no_header.csv
- [ ] Import ModelEvaluator
- [ ] Replace evaluation code
- [ ] Verify results
- [ ] Test notebook runs

### Task 5.5: Logistic Regression Integration
- [ ] Import ModelEvaluator
- [ ] Replace evaluation code
- [ ] Verify results
- [ ] Test notebook runs

### Task 5.6: Cross-Model Comparison Demo
- [ ] Create comparison between all spam models:
  ```python
  eval_bayes = ModelEvaluator(bayes_model, ..., task_name='spam')
  eval_perceptron = ModelEvaluator(perceptron_model, ..., task_name='spam')
  eval_svm = ModelEvaluator(svm_model, ..., task_name='spam')
  
  comparison = eval_bayes.compare_with(eval_perceptron).compare_with(eval_svm)
  ```
- [ ] Create comparison for phishing models:
  ```python
  eval_dt = ModelEvaluator(dt_model, ..., task_name='phishing')
  eval_lr = ModelEvaluator(lr_model, ..., task_name='phishing')
  comparison = eval_dt.compare_with(eval_lr)
  ```

## Phase 6: Documentation

### Task 6.1: Code Documentation
- [ ] Add comprehensive module docstring
- [ ] Document all public methods:
  - Parameters with types
  - Return types
  - Raises (exceptions)
  - Example usage
  
- [ ] Document validation functions
- [ ] Add inline comments for complex logic

### Task 6.2: Usage Guide
- [ ] Create UNIFIED_MODEL_EVALUATION_GUIDE.md with:
  - Overview of framework
  - Supported models list
  - Basic usage example
  - Advanced usage example
  - API reference
  - Troubleshooting section
  
- [ ] Document supported tasks:
  - Phishing: which notebooks use it
  - Spam: which notebooks use it (with dataset migration notes)

### Task 6.3: Integration Examples
- [ ] Document how to integrate into new notebooks
- [ ] Provide copy-paste code snippets
- [ ] Show before/after code comparison

## Phase 7: Testing & Validation

### Task 7.1: Unit Test Suite (60+ tests total)
- [ ] Run all tests in test_model_evaluation.py
- [ ] Verify >90% code coverage
- [ ] Test on multiple Python versions if available

### Task 7.2: End-to-End Testing
- [ ] Run all 5 notebooks sequentially
- [ ] Verify all produce valid evaluation results
- [ ] Verify metrics are consistent across runs
- [ ] Check for no errors or warnings

### Task 7.3: Data Consistency Verification
- [ ] Verify all phishing models use identical train/test split
- [ ] Verify all spam models use identical train/test split
- [ ] Confirm sms_spam_perceptron.csv and sms_spam_svm.csv are deprecated
- [ ] Document any data migration issues

## Phase 8: Quality Assurance

### Task 8.1: Code Review Checklist
- [ ] All code follows openspec/project.md conventions ✅
- [ ] All functions have docstrings ✅
- [ ] All parameters have type hints ✅
- [ ] Error messages are clear and helpful ✅
- [ ] No unused imports or variables ✅
- [ ] Code is DRY (no duplication) ✅

### Task 8.2: Performance Verification
- [ ] Calculate metrics in <100ms per model ✅
- [ ] Visualizations render in <500ms ✅
- [ ] Comparison works for 10+ models without slowdown ✅

### Task 8.3: Backward Compatibility
- [ ] Verify no existing notebooks are broken ✅
- [ ] Verify existing model files still work ✅
- [ ] Verify defs.py integration unchanged ✅

## Phase 9: Final Validation

### Task 9.1: Feature Validation
- [ ] All R requirements from spec.md are met ✅
- [ ] All acceptance criteria are satisfied ✅
- [ ] All design decisions documented ✅

### Task 9.2: Documentation Validation
- [ ] README/guide is clear and complete ✅
- [ ] API documentation is comprehensive ✅
- [ ] Integration examples are correct ✅

### Task 9.3: Archival Readiness
- [ ] All code is production-ready ✅
- [ ] All tests pass ✅
- [ ] All documentation complete ✅
- [ ] Ready for archival to openspec/changes/archive/ ✅

---

## Definition of Done

✅ All phases 1-9 completed
✅ 60+ unit tests with >90% pass rate
✅ All 5 notebooks integrated and tested
✅ Phishing models use unified framework
✅ Spam models use standardized dataset and unified framework
✅ Cross-model comparison works within tasks
✅ Linear Regression explicitly excluded
✅ Binary classification only (multi-class rejected)
✅ Task-scoped comparison only (cross-task rejected)
✅ Comprehensive documentation and usage guides
✅ No breaking changes to existing code
✅ Code review passed with no issues
