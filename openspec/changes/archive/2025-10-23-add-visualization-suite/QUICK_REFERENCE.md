# Quick Reference: Visualization Suite

# Quick Reference: Visualization Suite (Enhanced)

## Overview
Comprehensive visualization capabilities including training curve plots, data insights, CLI metrics dashboard, interactive Streamlit web app with Neumorphism design, and Live Inference Playground.

## Key Features

| Feature | Interface | File | Command |
|---------|-----------|------|---------|
| **Training Curves** | Python API | `visualization.py` | `plot_training_curves()` |
| **Feature Importance** | Python API | `visualization.py` | `plot_feature_importance()` |
| **Metrics Heatmap** | Python API | `visualization.py` | `plot_metrics_heatmap()` |
| **Confusion Matrices** | Python API | `visualization.py` | `plot_confusion_matrices_grid()` |
| **ROC Overlay** | Python API | `visualization.py` | `plot_roc_curves_overlay()` |
| **Convergence Plot** | Python API | `visualization.py` | `plot_convergence_analysis()` |
| **Data Overview** | Python API | `visualization.py` | `plot_data_overview()` |
| **Top-k Tokens** | Python API | `visualization.py` | `plot_top_tokens_by_class()` |
| **Metrics Viewer** | CLI | `cli_dashboard.py` | `python -m sources.cli_dashboard` |
| **Interactive Dashboard** | Web | `streamlit_app.py` | `streamlit run sources/streamlit_app.py` |
| **Live Inference** | Web | `streamlit_app.py` | Access "Playground" tab |

## Usage Examples

### Python API
```python
from sources.visualization import (
    plot_training_curves, plot_metrics_heatmap,
    plot_data_overview, plot_top_tokens_by_class
)

# Plot training history
fig, ax = plot_training_curves(history_dict, metric='loss')
fig.savefig('output.png')

# Show dataset insights
fig = plot_data_overview(X_data, y_labels, dataset_name='SMS Spam')
plt.show()

# Analyze discriminative tokens
fig, axes = plot_top_tokens_by_class(
    messages, labels,
    class_names=['Ham', 'Spam'],
    top_k=15
)
plt.show()

# Plot metrics heatmap
fig, ax = plot_metrics_heatmap(metrics_dict, figsize=(12, 6))
plt.show()
```

### Streamlit Web App (with Neumorphism Design)
```bash
# Launch interactive dashboard
streamlit run sources/streamlit_app.py

# Navigate to: http://localhost:8501
# Tabs: Overview, Metrics, Comparison, Training, Features, Playground
# Design: Neumorphism (soft shadows, frosted glass, warm colors)
```

### Live Inference Playground
```
Steps:
1. Open Streamlit app and go to "Playground" tab
2. Enter test message: "Click here to win $$$"
3. Select model from dropdown: "Decision Tree"
4. Adjust preprocessing:
   - Toggle: Remove URLs ✓
   - Toggle: Remove Numbers ✓
   - Slider: Stopword Removal
5. View prediction in real-time
6. Inspect feature importance
7. See preprocessed text transformation
8. Check prediction history
```

## Integration Points

**Existing `ModelEvaluator`**:
- ✅ Unchanged API (backward compatible)
- ✅ Optional new parameters: `model_name`, `dataset_name`, `metadata`
- ✅ New methods: `to_dict()`, `summary_metrics()`, `export()`
- ✅ NEW: `predict_single()`, `predict_proba()`, `get_feature_importance()`, `get_preprocessed_text()`

**Jupyter Notebooks**:
- Import `plot_*()` functions directly
- Replace matplotlib calls with new visualization API
- Add data overview and token analysis cells

## Design: Neumorphism UI
All Streamlit pages styled with modern Neumorphism aesthetic:
- **Soft Shadows**: Dual-layer shadows for depth (light + dark)
- **Frosted Glass**: Semi-transparent cards with backdrop blur
- **Warm Palette**: Soft beige background (#f5f5f5) with earth tone accents
- **Tactile Feel**: Smooth transitions (300-500ms), depth on hover/click
- **Responsive**: Works on desktop and mobile devices

## Dependencies
- New: `rich` (CLI UI), `streamlit` (web app)
- Existing: matplotlib, seaborn, pandas, numpy, nltk

## Performance Targets
- Plot rendering: <100ms (typical dataset)
- CLI dashboard: <20ms
- Streamlit startup: <3 seconds
- Live Inference: <500ms per prediction
- Memory: <100MB for 100 models

## File Structure
```
openspec/changes/add-visualization-suite/
├── proposal.md           # This proposal
├── design.md             # Architecture decisions
├── tasks.md              # Implementation checklist
└── specs/
    └── visualization/
        └── spec.md       # Detailed requirements
```

## Next Steps
1. Review proposal.md and design.md
2. Run `openspec validate add-visualization-suite --strict` ✓
3. Request code review
4. Implement tasks.md sequentially
5. Run validation before archival

## Status
✅ Proposal created and validated
✅ Enhancements added (Data Overview, Top-k Tokens, Live Inference, Neumorphism)
⏳ Ready for implementation
