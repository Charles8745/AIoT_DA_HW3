# Specification: Visualization Suite

## Overview
This specification defines the comprehensive visualization suite for analyzing ML model training progress, performance metrics, and comparative results. The suite provides three interfaces: programmatic (Python API), terminal (CLI dashboard), and web (Streamlit app).

## ADDED Requirements

### Requirement: Training Curve Visualization
The system SHALL plot training and validation curves (loss, accuracy, F1) with smoothing and statistical context.

#### Scenario: Plot training history from multiple epochs
```python
from sources.visualization import plot_training_curves

history = {
    'loss': [0.5, 0.4, 0.3, 0.25, 0.22],
    'val_loss': [0.55, 0.45, 0.38, 0.35, 0.34],
    'accuracy': [0.75, 0.80, 0.85, 0.88, 0.89],
    'val_accuracy': [0.73, 0.78, 0.82, 0.85, 0.86]
}
fig, ax = plot_training_curves(history, metric='loss')
# Output: 2x2 subplots showing loss and accuracy curves with confidence bands
```

#### Scenario: Export training curves to PNG file
```python
fig, ax = plot_training_curves(history, figsize=(12, 8))
fig.savefig('training_curves.png', dpi=150, bbox_inches='tight')
# Output: High-resolution PNG with proper margins and labels
```

### Requirement: Feature Importance Visualization
The system SHALL display feature importance scores as ranked horizontal bar charts with optional filtering.

#### Scenario: Plot top 15 features from decision tree model
```python
from sources.visualization import plot_feature_importance

feature_names = ['word_count', 'url_count', 'exclamation_count', 'email_pattern', 'price_mention']
importance = [0.45, 0.25, 0.15, 0.10, 0.05]

fig, ax = plot_feature_importance(feature_names, importance, top_n=5)
# Output: Horizontal bar chart with top 5 features, sorted descending
```

#### Scenario: Customize colors and styling
```python
fig, ax = plot_feature_importance(
    feature_names, importance, 
    top_n=15, 
    color_palette='RdYlGn',
    figsize=(10, 8)
)
# Output: Custom-colored bar chart with 15 features
```

### Requirement: Metrics Heatmap Visualization
The system SHALL render model performance metrics as color-coded heatmaps comparing accuracy, precision, recall, F1, AUC across models.

#### Scenario: Compare metrics across 4 models on same dataset
```python
from sources.visualization import plot_metrics_heatmap

metrics_dict = {
    'DecisionTree': {'accuracy': 0.92, 'precision': 0.88, 'recall': 0.90, 'f1': 0.89, 'auc': 0.93},
    'LogisticReg': {'accuracy': 0.89, 'precision': 0.91, 'recall': 0.85, 'f1': 0.88, 'auc': 0.91},
    'SVM': {'accuracy': 0.91, 'precision': 0.89, 'recall': 0.88, 'f1': 0.88, 'auc': 0.92},
    'Perceptron': {'accuracy': 0.85, 'precision': 0.84, 'recall': 0.83, 'f1': 0.83, 'auc': 0.86}
}

fig, ax = plot_metrics_heatmap(metrics_dict, figsize=(12, 6))
# Output: 4x5 heatmap with color gradient (red=low, green=high)
```

### Requirement: Confusion Matrix Grid Visualization
The system SHALL display confusion matrices for multiple models in a grid layout with consistent scaling and annotations.

#### Scenario: Compare confusion matrices across 6 models
```python
from sources.visualization import plot_confusion_matrices_grid

fig, axes = plot_confusion_matrices_grid(
    evaluators=[dt_eval, lr_eval, svm_eval, perc_eval, nb_eval, rf_eval],
    figsize=(18, 10),
    annotations=True
)
# Output: 2x3 grid of confusion matrices with TP/FP/TN/FN labels
```

#### Scenario: Add normalization by row percentages
```python
fig, axes = plot_confusion_matrices_grid(
    evaluators=evaluators,
    normalize='true',  # Show percentages
    annotate_metrics=True  # Include accuracy in each subplot
)
# Output: Normalized confusion matrices with percentages
```

### Requirement: ROC Curves Overlay Visualization
The system SHALL overlay multiple ROC curves in a single plot with AUC scores, diagonal reference line, and legend.

#### Scenario: Compare ROC curves from 4 models on phishing dataset
```python
from sources.visualization import plot_roc_curves_overlay

evaluators = [dt_eval, lr_eval, svm_eval, perc_eval]
fig, ax = plot_roc_curves_overlay(
    evaluators,
    figsize=(8, 8),
    title='ROC Curves - Phishing Detection'
)
# Output: Single plot with 4 ROC curves, legend showing AUC scores
```

#### Scenario: Customize colors and line styles
```python
fig, ax = plot_roc_curves_overlay(
    evaluators,
    colors=['red', 'blue', 'green', 'orange'],
    line_styles=['-', '--', '-.', ':'],
    fill_under=True  # Shade AUC area
)
# Output: Styled ROC curves with custom colors and shading
```

### Requirement: Convergence Analysis Visualization
The system SHALL plot smoothed loss curves with moving average to analyze training convergence patterns.

#### Scenario: Analyze convergence of training loss with smoothing window
```python
from sources.visualization import plot_convergence_analysis

losses = [0.5, 0.45, 0.48, 0.40, 0.38, 0.42, 0.35, 0.33, 0.30, 0.28]

fig, ax = plot_convergence_analysis(
    losses,
    window=3,
    show_trend=True
)
# Output: Line plot of raw losses + moving average + trend line
```

#### Scenario: Detect overfitting with dual-curve analysis
```python
fig, ax = plot_convergence_analysis(
    losses={'train': train_losses, 'val': val_losses},
    window=5,
    highlight_divergence=True
)
# Output: Train and val curves with alert when divergence detected
```

### Requirement: CLI Metrics Dashboard
The system SHALL provide a command-line interface (CLI) for viewing, filtering, and exporting model metrics in table format.

#### Scenario: Display metrics for all trained models
```bash
python -m sources.cli_dashboard --show-all

# Output:
# ┌─────────────┬──────────┬───────────┬────────┬─────┬────────┐
# │ Model       │ Dataset  │ Accuracy  │ Recall │ F1  │ AUC    │
# ├─────────────┼──────────┼───────────┼────────┼─────┼────────┤
# │ DecisionTree│ Phishing │ 0.92 ████ │ 0.90   │ 0.89│ 0.93   │
# │ LogisticReg│ Phishing │ 0.89 ███  │ 0.85   │ 0.88│ 0.91   │
# │ SVM         │ SMS      │ 0.91 ████ │ 0.88   │ 0.90│ 0.92   │
# └─────────────┴──────────┴───────────┴────────┴─────┴────────┘
```

#### Scenario: Filter models by type and export to CSV
```bash
python -m sources.cli_dashboard --model-type=tree --export metrics.csv

# Output: CSV file with filtered results
```

#### Scenario: Sort by specific metric
```bash
python -m sources.cli_dashboard --sort-by=auc --desc
# Displays models sorted by AUC in descending order
```

### Requirement: Streamlit Interactive Dashboard
The system SHALL provide an interactive web application for exploring metrics with filters, comparisons, and downloads.

#### Scenario: Launch Streamlit dashboard
```bash
streamlit run sources/streamlit_app.py

# Launches web app with tabs:
# - Overview: Summary statistics, dataset info
# - Metrics: Interactive table with sorting/filtering
# - Comparison: Multi-model comparison with statistical tests
# - Training: Convergence curves with log scale options
# - Features: Feature importance analysis
```

#### Scenario: Filter models and compare side-by-side
```
User selects in web UI:
1. Filter: Dataset=Phishing, Model type=Tree
2. Compare: DecisionTree vs RandomForest
3. View: Side-by-side metrics + ROC curves
4. Export: Download comparison as JSON
```

#### Scenario: Analyze feature importance across all models
```
User navigates to Features tab:
1. Select metric: Feature importance
2. Group by: Model type
3. View: Top 10 features ranked across models
4. Interactive legend: Toggle models on/off
```

### Requirement: Data Overview Visualization
The system SHALL display comprehensive dataset statistics including class distribution, feature statistics, and data quality metrics.

#### Scenario: Display dataset overview for SMS spam detection
```python
from sources.visualization import plot_data_overview

overview_fig = plot_data_overview(
    X_data,
    y_labels,
    dataset_name='SMS Spam',
    class_names=['Ham', 'Spam']
)
# Output: Multi-panel visualization with:
# - Class distribution (pie/bar chart)
# - Feature statistics (mean/std for top features)
# - Missing values heatmap
# - Sample distribution over time (if applicable)
```

#### Scenario: Export dataset statistics to report
```python
from sources.visualization import DataOverviewAnalyzer

analyzer = DataOverviewAnalyzer(X_data, y_labels)
stats_report = analyzer.generate_report()
# Returns: DataFrame with feature-level statistics
```

### Requirement: Top-k Tokens by Class Visualization
The system SHALL identify and visualize the most discriminative tokens (words) for each class.

#### Scenario: Plot top 15 tokens for spam vs ham in SMS dataset
```python
from sources.visualization import plot_top_tokens_by_class

messages = df['text']  # Raw SMS messages
labels = df['label']   # Spam/Ham labels
class_names = ['Ham', 'Spam']

fig, axes = plot_top_tokens_by_class(
    messages,
    labels,
    class_names=class_names,
    top_k=15,
    figsize=(14, 8)
)
# Output: Side-by-side bar charts showing most frequent/distinctive tokens per class
```

#### Scenario: Analyze token importance across models
```python
fig, ax = plot_top_tokens_by_class(
    messages,
    labels,
    class_names=class_names,
    top_k=20,
    metric='tf-idf',  # Use TF-IDF instead of frequency
    show_importance=True
)
# Output: Tokens colored by importance score
```

### Requirement: Live Inference Playground
The system SHALL provide an interactive web interface for real-time model inference with dynamic parameter adjustment.

#### Scenario: Launch Live Inference Playground in Streamlit
```bash
streamlit run sources/streamlit_app.py --page=playground

# Playground Features:
# - Text input area for entering test messages
# - Model selector (dropdown to choose model)
# - Parameter sliders for preprocessing options
# - Real-time prediction output
# - Confidence scores visualization
# - Historical predictions log
```

#### Scenario: Adjust preprocessing parameters and observe prediction changes
```
User Experience:
1. User enters text: "Click here to win $$$"
2. Selects model: "Decision Tree"
3. Adjusts preprocessing:
   - Toggle: Remove URLs ✓
   - Toggle: Remove Numbers ✓
   - Slider: Stopword Removal (0-1)
   - Slider: Confidence Threshold (0.5-0.99)
4. Sees real-time prediction update
5. Views feature importance for this input
6. Inspects preprocessed text transformation
```

#### Scenario: Export inferred results
```
User can:
- Download single prediction as JSON
- Export batch of predictions (CSV)
- Share prediction permalink
- View prediction history with timestamps
```

### Requirement: Neumorphism UI Design
The system SHALL implement a modern, tactile Neumorphism design aesthetic for all web interfaces.

#### Design Principles
**Soft Shadows & Depth**:
```css
/* Neumorphic button styling */
button {
  background: linear-gradient(145deg, #f5f5f5, #e8e8e8);
  box-shadow: 8px 8px 16px #b8b8b8,
              -8px -8px 16px #ffffff;
  border-radius: 12px;
}
```

**Blurred Backgrounds**:
```css
/* Frosted glass effect for cards */
.card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
```

**Warm Color Palette**:
- Background: Soft beige/gray (#f5f5f5)
- Accents: Warm earth tones (sage green, warm brown)
- Text: Dark charcoal for readability

**Tactile Interactions**:
- Smooth transitions (300-500ms)
- Depth on hover/click (shadows shift)
- Haptic-like feedback with color shifts

#### Scenario: Neumorphic metrics display
```python
# Streamlit app renders metrics with neumorphic styling
st.markdown("""
    <style>
    .neumorphic-metric {
        background: linear-gradient(145deg, #f5f5f5, #e8e8e8);
        box-shadow: 8px 8px 16px rgba(0,0,0,0.1),
                    -8px -8px 16px rgba(255,255,255,0.8);
        border-radius: 12px;
        padding: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# All UI elements automatically styled
```

### Requirement: Metrics Export Functionality
The system SHALL export computed metrics to standard formats (CSV, JSON) with full reproducibility information.

#### Scenario: Export all metrics to JSON with metadata
```python
from sources.cli_dashboard import CliDashboard

dashboard = CliDashboard(evaluators)
dashboard.export('results.json', format='json', include_metadata=True)

# Output JSON structure:
# {
#   "export_date": "2025-10-23",
#   "models": [...],
#   "metrics": {...},
#   "comparison_summary": {...}
# }
```

#### Scenario: Export with timestamp for versioning
```python
dashboard.export('results', auto_timestamp=True)
# Creates: results_2025-10-23_143022.csv
```

## MODIFIED Requirements

### Requirement: Model Evaluation Framework
Enhanced ModelEvaluator class SHALL support serialization, metadata tracking, and live inference capabilities.

#### Current Behavior
```python
evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)
metrics = evaluator.calculate_metrics()
# Returns dict with metrics only
```

#### Improved Behavior
```python
evaluator = ModelEvaluator(
    model, X_train, y_train, X_test, y_test,
    model_name='DecisionTree',
    dataset_name='phishing',
    metadata={'version': '1.0', 'timestamp': '2025-10-23'}
)
# New methods:
data = evaluator.to_dict()                          # Serialize to JSON-compatible dict
summary = evaluator.summary_metrics()               # Quick stats
evaluator.export('model.json')                      # Direct export
prediction = evaluator.predict_single(text)         # Single prediction
probs = evaluator.predict_proba(text)               # Confidence scores
importance = evaluator.get_feature_importance()     # Feature importance
preprocessed = evaluator.get_preprocessed_text(text)  # Show preprocessing steps
```

**Note**: Function signature extended with optional parameters; backward compatibility maintained. New live inference methods added.

### Requirement: Streamlit Application Interface
Streamlit app SHALL include comprehensive Live Inference Playground with parameter control and Neumorphism UI design.

#### Current Behavior
```python
# Basic Streamlit pages:
# - Overview, Metrics, Comparison, Training, Features
```

#### Improved Behavior
```
Enhanced Streamlit pages:
├── Overview              (data statistics, class distribution)
├── Metrics Explorer      (interactive table)
├── Model Comparison      (side-by-side metrics)
├── Training Analysis     (convergence curves)
├── Feature Analysis      (feature importance & tokens)
└── Live Inference        (NEW - playground with:
    ├── Text input area
    ├── Model selector
    ├── Preprocessing parameter sliders
    ├── Real-time prediction output
    ├── Confidence visualization
    ├── Feature importance for input
    ├── Preprocessed text transformation view
    └── Prediction history log
)

All UI elements styled with Neumorphism design:
- Soft shadows and depth effects
- Blurred/frosted glass backgrounds
- Warm color palette (beige, earth tones)
- Tactile interactions with smooth transitions
```

**Note**: Streamlit styling applied via custom CSS in `streamlit_app.py`; UX improved with playground.

## REMOVED Requirements
None (purely additive change)

## Acceptance Criteria
✅ All plot functions tested with sample data (decision trees, SMS/phishing datasets)
✅ Data Overview and Top-k Tokens visualizations render correctly with real datasets
✅ Live Inference Playground responsive (<500ms response time per prediction)
✅ Neumorphism styling applied to all Streamlit UI elements (buttons, cards, metrics)
✅ CLI dashboard renders correctly in 80-col and 120-col terminals
✅ Streamlit app loads in <3 seconds on typical hardware
✅ Export formats (CSV, JSON) are valid and reproducible
✅ 95% of existing tests pass (new tests for visualization modules ≥90% coverage)
✅ Color-blind friendly palette used (no red-green-only indicators)
✅ Documentation with usage examples for each visualization type
✅ No performance degradation (<100ms for plot rendering on datasets ≤10K rows)
✅ Neumorphism design verified on desktop and mobile (responsive)
✅ Live Inference shows feature importance and preprocessed text transformations
