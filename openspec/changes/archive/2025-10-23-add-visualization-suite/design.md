# Design: Richer Visualization Suite

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Visualization Suite                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Core Visualization Engine                  │   │
│  │        (sources/visualization.py)                    │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │  • plot_training_curves()                            │   │
│  │  • plot_feature_importance()                         │   │
│  │  • plot_metrics_heatmap()                            │   │
│  │  • plot_confusion_matrices_grid()                    │   │
│  │  • plot_roc_curves_overlay()                         │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ▲                                    │
│                          │                                    │
│          ┌───────────────┼───────────────┐                   │
│          │               │               │                   │
│          ▼               ▼               ▼                   │
│    ┌──────────┐   ┌──────────┐   ┌──────────┐              │
│    │   CLI    │   │Streamlit │   │ Notebook │              │
│    │Dashboard │   │   App    │   │Integration
 │              │
│    │(rich)    │   │(web UI)  │   │(embed)   │              │
│    └──────────┘   └──────────┘   └──────────┘              │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Module Design

### 1. Core Visualization Engine (`sources/visualization.py`)
**Purpose**: Centralized plotting library using matplotlib with consistent styling

**Key Functions**:
- `plot_training_curves(history, metric='loss', figsize=(12, 5))` - Line plot of training/validation curves
- `plot_feature_importance(feature_names, importance_scores, top_n=15)` - Horizontal bar chart
- `plot_metrics_heatmap(metrics_dict, figsize=(10, 6))` - Heatmap of model metrics
- `plot_confusion_matrices_grid(evaluators, figsize=(15, 5))` - Multiple confusion matrices side-by-side
- `plot_roc_curves_overlay(evaluators, figsize=(8, 8))` - Overlay ROC curves with AUC labels
- `plot_convergence_analysis(losses, window=50)` - Smoothed loss convergence
- `plot_data_overview(X_data, y_labels, figsize=(16, 10))` - Dataset statistics and quality metrics (NEW)
- `plot_top_tokens_by_class(messages, labels, top_k=15, figsize=(14, 8))` - Most discriminative tokens per class (NEW)

**Style Consistency**:
- Theme: Seaborn "darkgrid"
- Color palette: "Set2" for multi-line plots
- Font size: 10pt (labels), 12pt (titles)
- DPI: 100 (screen), 150 (export)

### 2. CLI Dashboard (`sources/cli_dashboard.py`)
**Purpose**: Terminal-based metrics viewer using `rich` library

**Features**:
- Tables with sortable columns (model name, dataset, accuracy, F1, AUC)
- Progress bars for metric ranges
- Color coding (red <0.6, yellow 0.6-0.8, green >0.8)
- Live update capability (re-fetch metrics on interval)
- Export to CSV/JSON

**API**:
```python
from sources.cli_dashboard import CliDashboard

dashboard = CliDashboard(models=[evaluator_dt, evaluator_lr])
dashboard.render()  # Display in terminal
dashboard.export('metrics.csv')
```

### 3. Streamlit App (`sources/streamlit_app.py`)
**Purpose**: Interactive web dashboard for exploring results

**Pages**:
1. **Overview** - Summary stats, model counts, dataset info
2. **Metrics Explorer** - Interactive table with sorting/filtering
3. **Model Comparison** - Side-by-side comparison with statistical tests
4. **Training Analysis** - Convergence curves with log scale options
5. **Feature Analysis** - Feature importance across models
6. **Live Inference** - (NEW) Real-time prediction playground with parameter control

**Live Inference Playground Features**:
- Text input area for entering test messages/emails
- Model selector dropdown (choose from trained models)
- Preprocessing parameter sliders:
  - Remove URLs (toggle)
  - Remove Numbers (toggle)
  - Stopword removal intensity (0-1)
  - Confidence threshold (0.5-0.99)
- Real-time prediction output with confidence scores
- Feature importance visualization for current input
- Preprocessed text transformation view
- Prediction history with timestamps
- Export individual predictions as JSON

**Interactivity**:
- Filters: Model type, dataset, date range
- Multi-select: Compare 2-5 models
- Download: Export filtered results
- Responsive: Mobile-friendly layout
- Neumorphism: All UI elements styled with soft shadows, blurred backgrounds

### Neumorphism UI Design System
**Design Philosophy**: Create a soft, tactile, inviting interface that mimics physical depth and material properties

**Core Principles**:
1. **Soft Shadows & Depth**
   - Outset shadows: box-shadow with light and dark layers
   - Inset shadows: for pressed/active states
   - Blur radius: 8-16px for soft appearance

2. **Frosted Glass Effect**
   - Semi-transparent backgrounds (70-80% opacity)
   - Backdrop blur: 10px minimum
   - Subtle border: 1px rgba white for frosted appearance

3. **Warm Color Palette**
   - Primary background: #f5f5f5 (soft off-white)
   - Secondary: #ebebeb (slightly darker)
   - Accent: Warm earth tones (#8b7d6b sage green, #d4a574 warm brown)
   - Text: #2c2c2c (charcoal for high readability)

4. **Tactile Interactions**
   - Smooth transitions: 300-500ms cubic-bezier(0.4, 0, 0.2, 1)
   - Depth on hover: shadows shift outward (expand effect)
   - Pressed state: shadows reverse/invert (indent effect)
   - Color shifts: Subtle saturation/lightness on hover

5. **Spacing & Scale**
   - Rounded corners: 12-16px for large elements
   - Padding: 20-24px for generous spacing
   - Gap between elements: 16-20px

**Implementation in Streamlit**:
```python
# Neumorphic CSS variables
NEUMORPHIC_STYLES = """
<style>
:root {
  --bg-primary: #f5f5f5;
  --bg-secondary: #ebebeb;
  --text-primary: #2c2c2c;
  --accent-green: #8b7d6b;
  --accent-brown: #d4a574;
  --shadow-light: 0 0 8px rgba(255,255,255,0.8);
  --shadow-dark: 0 0 8px rgba(0,0,0,0.1);
  --blur-bg: blur(10px);
}

.neumorphic-button {
  background: linear-gradient(145deg, var(--bg-primary), var(--bg-secondary));
  box-shadow: var(--shadow-dark), var(--shadow-light);
  border: none;
  border-radius: 12px;
  padding: 12px 24px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.neumorphic-button:hover {
  box-shadow: 0 0 16px rgba(0,0,0,0.15), 0 0 16px rgba(255,255,255,0.9);
  transform: translate(-2px, -2px);
}

.neumorphic-button:active {
  box-shadow: inset 0 0 8px rgba(0,0,0,0.1), inset 0 0 8px rgba(255,255,255,0.8);
  transform: translate(2px, 2px);
}

.neumorphic-card {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: var(--blur-bg);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 8px 8px 16px rgba(0,0,0,0.1),
              -8px -8px 16px rgba(255,255,255,0.8);
}

.neumorphic-metric {
  background: linear-gradient(145deg, var(--bg-primary), var(--bg-secondary));
  border-radius: 12px;
  padding: 20px;
  box-shadow: 8px 8px 16px rgba(0,0,0,0.1),
              -8px -8px 16px rgba(255,255,255,0.8);
}

.neumorphic-input {
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(0,0,0,0.05);
  border-radius: 12px;
  padding: 12px 16px;
  font-size: 14px;
}

.neumorphic-input:focus {
  box-shadow: inset 2px 2px 5px rgba(0,0,0,0.05),
              inset -2px -2px 5px rgba(255,255,255,0.8);
}
</style>
"""
```

### 4. Integration Points
**Existing `ModelEvaluator` enhancements**:
- Add `to_dict()` method for JSON serialization
- Add `summary_metrics()` for quick stats
- Add metadata tracking (model_type, dataset_name, timestamp)

**Notebook Integration**:
- Import and use `plot_*()` functions directly
- Option to embed Streamlit app via `streamlit.config.toml`

## Technology Stack

| Component | Library | Reason |
|-----------|---------|--------|
| Plotting | matplotlib + seaborn | Familiar, publication-quality output |
| CLI UI | rich | Beautiful tables, progress bars, colors |
| Web App | Streamlit | Rapid prototyping, no frontend needed |
| Data | pandas | Existing standard |
| Caching | functools.lru_cache | Fast repeated computations |

## Performance Considerations

**Rendering Speed**:
- Matplotlib plots: ~50-100ms (typical dataset)
- Streamlit re-renders: Cached via `@st.cache_data`
- CLI tables: <20ms (50 models)

**Memory**:
- Store plots as `.png` (serializable)
- Cache metrics in pandas DataFrame (~5MB for 100 models)
- Lazy-load feature importance (computed on-demand)

## Backward Compatibility

- ✅ Existing `defs.py` functions unchanged
- ✅ `ModelEvaluator` API backward-compatible (new methods only)
- ✅ Jupyter notebooks work without modification
- ✅ Optional dependencies: `rich` and `streamlit` only required for CLI/web

## Testing Strategy

**Unit Tests**:
- Test each plot function with mock data
- Verify output shape and labels
- Check color assignment, axis ranges

**Integration Tests**:
- Test CLI dashboard with sample evaluators
- Test Streamlit app page loading
- Verify export formats (CSV, JSON)

**Manual Tests**:
- Render on real datasets (phishing, SMS spam)
- Verify statistical annotations are correct
- Check responsive design on mobile

## Migration Path

**Phase 1**: Core visualization engine (no breaking changes)
**Phase 2**: CLI dashboard (optional, new feature)
**Phase 3**: Streamlit app (optional, new feature)
**Phase 4**: Integrate into notebooks (gradual adoption)

Users can adopt incrementally without disrupting existing workflows.
