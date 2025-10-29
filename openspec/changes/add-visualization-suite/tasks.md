# Tasks: Add Richer Visualization Suite

Implementation checklist for the visualization suite. Complete tasks in order; each is a verifiable unit of work.

## Phase 1: Core Visualization Engine

- [ ] **T1.1**: Create `sources/visualization.py` with basic structure
  - [ ] Define imports (matplotlib, seaborn, numpy, nltk for token analysis)
  - [ ] Set up consistent style/theme
  - [ ] Create function stubs for all 8 plot functions
  - **Verification**: File exists, imports work, no runtime errors on import

- [ ] **T1.2**: Implement `plot_training_curves()` function
  - [ ] Accept history dict with loss/accuracy keys
  - [ ] Support train and validation curves
  - [ ] Add confidence bands (optional)
  - [ ] Return matplotlib figure and axes
  - **Verification**: 
    - Test with sample history dict
    - Verify output has 2x2 subplots (loss train/val, accuracy train/val)
    - Check axis labels and legend

- [ ] **T1.3**: Implement `plot_feature_importance()` function
  - [ ] Accept feature names and importance scores
  - [ ] Sort by importance descending
  - [ ] Support `top_n` parameter
  - [ ] Create horizontal bar chart
  - **Verification**:
    - Test with 20 features, top_n=10
    - Verify correct features in correct order
    - Check color gradient (optional)

- [ ] **T1.4**: Implement `plot_metrics_heatmap()` function
  - [ ] Accept dict of dicts (models → metrics)
  - [ ] Create color-coded heatmap
  - [ ] Use diverging colormap (red=low, green=high)
  - [ ] Add text annotations (metric values)
  - **Verification**:
    - Test with 4 models × 5 metrics
    - Verify correct color mapping
    - Check annotations readable

- [ ] **T1.5**: Implement `plot_confusion_matrices_grid()` function
  - [ ] Accept list of ModelEvaluator objects
  - [ ] Create MxN grid of subplots
  - [ ] Draw heatmap for each confusion matrix
  - [ ] Add labels (TP, FP, TN, FN)
  - [ ] Support normalization option
  - **Verification**:
    - Test with 6 evaluators (2x3 grid)
    - Verify grid layout correct
    - Check confusion matrix values match evaluator

- [ ] **T1.6**: Implement `plot_roc_curves_overlay()` function
  - [ ] Accept list of ModelEvaluator objects
  - [ ] Draw ROC curve for each model
  - [ ] Add diagonal reference line
  - [ ] Display AUC in legend
  - [ ] Support custom colors/line styles
  - **Verification**:
    - Test with 4 evaluators
    - Verify ROC curves from (0,0) to (1,1)
    - Check AUC values in legend match evaluator.auc_roc_test

- [ ] **T1.7**: Implement `plot_convergence_analysis()` function
  - [ ] Accept loss values (list or dict)
  - [ ] Calculate moving average with window
  - [ ] Plot raw + smoothed curves
  - [ ] Optional: Add trend line
  - [ ] Optional: Highlight overfitting divergence
  - **Verification**:
    - Test with 20 epoch losses
    - Verify moving average correct
    - Check plot has both raw and smoothed lines

- [ ] **T1.8**: Implement `plot_data_overview()` function (NEW)
  - [ ] Accept X_data, y_labels, dataset_name, class_names
  - [ ] Create multi-panel visualization with:
    - [ ] Class distribution (pie or bar chart)
    - [ ] Feature statistics (mean/std for top N features)
    - [ ] Missing values heatmap (if applicable)
    - [ ] Data sample distribution visualization
  - [ ] Return matplotlib figure with 4 subplots
  - **Verification**:
    - Test with SMS spam dataset
    - Verify class labels correct
    - Check feature stats calculation

- [ ] **T1.9**: Implement `plot_top_tokens_by_class()` function (NEW)
  - [ ] Accept messages (list of strings), labels, class_names
  - [ ] Tokenize and count word frequencies per class
  - [ ] Compute TF-IDF or frequency-based importance
  - [ ] Create side-by-side bar charts (one per class)
  - [ ] Show top_k tokens for each class
  - [ ] Support custom metrics (frequency, tf-idf, etc.)
  - **Verification**:
    - Test with SMS spam/ham messages
    - Verify tokens are class-discriminative
    - Check top_k selection and ordering

- [ ] **T1.10**: Write unit tests for visualization.py
  - [ ] Test each plot function with mock data
  - [ ] Verify output dimensions and types
  - [ ] Test edge cases (empty data, single model, etc.)
  - [ ] Test figure saving to PNG
  - [ ] Test data overview with real SMS dataset
  - [ ] Test token analysis with real text data
  - **Verification**: ≥90% code coverage for visualization module

## Phase 2: CLI Dashboard

- [ ] **T2.1**: Create `sources/cli_dashboard.py` with `CliDashboard` class
  - [ ] Accept list of ModelEvaluator objects in `__init__`
  - [ ] Implement `render()` method (displays table in terminal)
  - [ ] Use `rich` library for table styling
  - [ ] Support color-coded metrics (red/yellow/green)
  - [ ] Add progress bars for metric ranges
  - **Verification**:
    - Test with 3-5 evaluators
    - Run `python -m sources.cli_dashboard` (requires test data)
    - Verify table renders in 80 and 120 column terminals
    - Check colors display correctly

- [ ] **T2.2**: Implement filtering in CLI dashboard
  - [ ] Add `--filter-by-model-type` parameter
  - [ ] Add `--filter-by-dataset` parameter
  - [ ] Implement filtering logic
  - [ ] Update table display based on filters
  - **Verification**:
    - Test `--model-type=tree` shows only tree models
    - Test `--dataset=phishing` shows only phishing results
    - Test chaining filters together

- [ ] **T2.3**: Implement sorting in CLI dashboard
  - [ ] Add `--sort-by` parameter (default: model name)
  - [ ] Add `--desc` flag for descending order
  - [ ] Support sorting by any metric column
  - **Verification**:
    - Test `--sort-by=auc --desc`
    - Verify correct sort order
    - Test with all numeric metrics

- [ ] **T2.4**: Implement export to CSV
  - [ ] Add `export(filename, format='csv')` method
  - [ ] Write filtered/sorted results to CSV
  - [ ] Include header row with column names
  - [ ] Add `--export` CLI parameter
  - **Verification**:
    - Test CSV output readable by pandas
    - Verify all rows and columns present
    - Check data types preserved

- [ ] **T2.5**: Implement export to JSON
  - [ ] Add `format='json'` support in export method
  - [ ] Include metadata (export date, models count, etc.)
  - [ ] Structure results in nested JSON
  - **Verification**:
    - Test JSON valid and parseable
    - Verify metadata included
    - Check all metrics present

- [ ] **T2.6**: Write tests for CLI dashboard
  - [ ] Test table rendering (no crashes)
  - [ ] Test filtering logic
  - [ ] Test sorting logic
  - [ ] Test CSV/JSON export
  - **Verification**: ≥85% code coverage for cli_dashboard module

## Phase 3: Streamlit App

- [ ] **T3.1**: Create `sources/streamlit_app.py` with basic structure
  - [ ] Set up Streamlit app with session state
  - [ ] Create navigation tabs/pages
  - [ ] Load evaluators from file/memory
  - [ ] Implement Neumorphism CSS styling framework
  - **Verification**:
    - Test `streamlit run sources/streamlit_app.py`
    - Verify app loads without errors
    - Check all tabs present
    - Verify Neumorphism styling applied

- [ ] **T3.2**: Implement Overview page
  - [ ] Display model count, dataset info
  - [ ] Show summary statistics with data overview visualization
  - [ ] Display distribution of metrics (histograms)
  - [ ] Add class distribution chart
  - [ ] Style with Neumorphism cards
  - **Verification**:
    - Tab loads correctly
    - Metrics display properly
    - Histograms render
    - Data overview shows class distribution

- [ ] **T3.3**: Implement Metrics Explorer page
  - [ ] Create interactive table with all models/metrics
  - [ ] Implement sorting by clicking column headers
  - [ ] Implement filtering (model type, dataset, metric range)
  - [ ] Show/hide columns
  - [ ] Apply Neumorphism styling to table
  - **Verification**:
    - Table displays all data
    - Filtering works (try selecting subset)
    - Sorting works (click column header)
    - Performance <1 second for typical dataset
    - UI follows Neumorphism design

- [ ] **T3.4**: Implement Model Comparison page
  - [ ] Multi-select dropdown to choose 2-5 models
  - [ ] Display metrics side-by-side
  - [ ] Show performance difference
  - [ ] Optional: Statistical tests (t-test)
  - [ ] Draw ROC curves for selected models
  - [ ] Draw confusion matrices for selected models
  - [ ] Apply Neumorphism styling
  - **Verification**:
    - Select 2 models, verify side-by-side display
    - Select 5 models, verify all comparison metrics shown
    - ROC curves overlay correctly
    - Confusion matrices display side-by-side

- [ ] **T3.5**: Implement Training Analysis page
  - [ ] Load training history data (loss curves)
  - [ ] Plot training/validation curves
  - [ ] Support log scale for loss
  - [ ] Zoom and pan options
  - [ ] Optional: Convergence analysis
  - [ ] Neumorphism styling for controls
  - **Verification**:
    - Curves display correctly
    - Log scale toggle works
    - Zoom/pan responsive

- [ ] **T3.6**: Implement Feature Analysis page
  - [ ] Load feature importance from models (if available)
  - [ ] Plot top N features
  - [ ] Support filtering by model
  - [ ] Group by model type
  - [ ] Interactive legend
  - [ ] Add top-k tokens visualization
  - [ ] Neumorphism card styling
  - **Verification**:
    - Features display with importance scores
    - Filtering works
    - Legend toggle toggles features on/off
    - Top-k tokens display for each class

- [ ] **T3.7**: Implement Live Inference Playground page (NEW)
  - [ ] Create text input area for test messages
  - [ ] Model selector dropdown (choose from trained models)
  - [ ] Preprocessing parameter sliders:
    - [ ] Remove URLs (toggle)
    - [ ] Remove Numbers (toggle)
    - [ ] Stopword removal (slider 0-1)
    - [ ] Confidence threshold (slider 0.5-0.99)
  - [ ] Real-time prediction display
  - [ ] Show confidence scores with progress bar
  - [ ] Display feature importance for input
  - [ ] Show preprocessed text transformation
  - [ ] Prediction history log with timestamps
  - [ ] Apply Neumorphism styling to all elements
  - **Verification**:
    - Text input works
    - Model selection updates prediction
    - Parameter sliders adjust preprocessing
    - Prediction updates in real-time (<500ms)
    - Feature importance displays correctly
    - Preprocessed text shows transformations clearly
    - History log maintains entries

- [ ] **T3.8**: Implement Neumorphism UI Design System (NEW)
  - [ ] Create CSS styling with Neumorphism principles:
    - [ ] Soft shadows (outset/inset states)
    - [ ] Frosted glass backgrounds (blur + transparency)
    - [ ] Warm color palette (#f5f5f5, earth tones)
    - [ ] Rounded corners (12-16px)
    - [ ] Smooth transitions (300-500ms)
    - [ ] Depth on hover/active states
  - [ ] Create reusable component classes:
    - [ ] .neumorphic-button
    - [ ] .neumorphic-card
    - [ ] .neumorphic-metric
    - [ ] .neumorphic-input
    - [ ] .neumorphic-select
  - [ ] Apply styling to all pages consistently
  - **Verification**:
    - All buttons have Neumorphic appearance
    - Cards have soft shadows and blur effect
    - Metrics display with depth effect
    - Hover states work smoothly
    - Mobile responsive

- [ ] **T3.9**: Add download functionality
  - [ ] Add "Download Results" button on each page
  - [ ] Support formats: CSV, JSON, PDF (optional)
  - [ ] Include metadata in export
  - [ ] Neumorphic styling for download button
  - **Verification**:
    - Download button appears
    - Downloaded file valid and complete
    - Format correct

- [ ] **T3.10**: Write tests for Streamlit app
  - [ ] Test page loading
  - [ ] Test filtering/sorting logic
  - [ ] Test visualization rendering
  - [ ] Test Live Inference prediction
  - [ ] Test parameter adjustment effects
  - [ ] Test export functionality
  - [ ] Test Neumorphism styling renders
  - **Verification**: ≥80% code coverage for streamlit_app module

## Phase 4: Integration & Enhancement

- [ ] **T4.1**: Enhance `ModelEvaluator` for dashboard integration
  - [ ] Add optional `model_name`, `dataset_name` parameters to `__init__`
  - [ ] Add optional `metadata` dict parameter
  - [ ] Implement `to_dict()` method (JSON-serializable)
  - [ ] Implement `summary_metrics()` method
  - [ ] Implement `export(filename)` method
  - [ ] Implement `predict_single(text)` for live inference
  - [ ] Implement `predict_proba(text)` for confidence scores
  - [ ] Implement `get_feature_importance()` method
  - [ ] Implement `get_preprocessed_text(text)` to show transformations
  - **Verification**:
    - Backward compatibility: old code works unchanged
    - New parameters accept string/dict values
    - Methods return expected types
    - Live inference works with single test input

- [ ] **T4.2**: Integrate visualization into notebooks
  - [ ] Update "Linear Regression.ipynb" to use new plots + data overview
  - [ ] Update "Logistic Regression Phishing Detector.ipynb"
  - [ ] Update "SVM.ipynb"
  - [ ] Update "Decision Tree Phishing Detector.ipynb"
  - [ ] Import and use `plot_*()` functions where applicable
  - [ ] Add data overview analysis cells
  - [ ] Add top-k tokens analysis cells
  - **Verification**:
    - Notebooks run without errors
    - New plots appear in output
    - No cell failures
    - Data insights visible

- [ ] **T4.3**: Create example scripts
  - [ ] Create `examples/example_cli_dashboard.py`
  - [ ] Create `examples/example_streamlit_app.py`
  - [ ] Create `examples/example_live_inference.py`
  - [ ] Document how to run each
  - **Verification**:
    - Scripts run without errors
    - Generate expected output
    - Live inference example shows parameter adjustment

- [ ] **T4.4**: Write integration tests
  - [ ] Test full pipeline: train model → compute metrics → visualize
  - [ ] Test all three interfaces (API, CLI, web)
  - [ ] Test end-to-end export workflow
  - [ ] Test Live Inference prediction pipeline
  - [ ] Test data overview with real datasets
  - [ ] Test token analysis with SMS/phishing data
  - **Verification**: ≥85% code coverage for entire module

## Phase 5: Documentation & Validation

- [ ] **T5.1**: Create comprehensive documentation
  - [ ] Document API for each plot function (docstrings)
  - [ ] Write usage guide for CLI dashboard
  - [ ] Write usage guide for Streamlit app
  - [ ] Create troubleshooting guide
  - **Verification**: All functions have complete docstrings

- [ ] **T5.2**: Create example notebooks
  - [ ] Create "Visualization Examples.ipynb"
  - [ ] Demonstrate each plot function
  - [ ] Show CLI dashboard usage
  - [ ] Show Streamlit app features
  - **Verification**: Notebook runs end-to-end

- [ ] **T5.3**: Performance validation
  - [ ] Measure plot rendering time (<100ms)
  - [ ] Measure Streamlit app startup (<3s)
  - [ ] Measure CLI dashboard render (<20ms)
  - [ ] Profile memory usage
  - **Verification**: All benchmarks met

- [ ] **T5.4**: Validate backward compatibility
  - [ ] Run all existing tests (target: ≥95% pass rate)
  - [ ] Verify existing notebooks still work
  - [ ] Check API compatibility with existing code
  - **Verification**: ≥95% existing tests pass

- [ ] **T5.5**: Final validation with `openspec validate`
  - [ ] Run `openspec validate add-visualization-suite --strict`
  - [ ] Resolve any issues
  - [ ] Prepare for archival
  - **Verification**: `openspec validate` passes with no errors

- [ ] **T5.6**: Code review and approval
  - [ ] Request code review
  - [ ] Address review feedback
  - [ ] Receive approval from maintainers
  - **Verification**: Approval received

## Summary

**Total Tasks**: 40 (updated from 32)
**Estimated Duration**: 11 working days
**Key Dependencies**: 
- Phase 1 must complete before Phase 2
- Phase 2 can be parallel with Phase 3
- Phase 4 integration requires Phases 1-3 complete
- Phase 5 validation happens throughout

**Completion Criteria**:
✅ All tasks marked complete (checkboxes)
✅ All code tests passing (≥85% coverage)
✅ All existing tests passing (≥95% pass rate)
✅ `openspec validate add-visualization-suite --strict` passing
✅ Code review approval received
