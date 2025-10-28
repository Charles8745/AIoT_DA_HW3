# Proposal: Add Richer Visualization Suite

## Why
Current visualization capabilities are limited to basic plots embedded in Jupyter notebooks:
- No centralized dashboard for viewing all metrics and results
- Step outputs (training curves, feature importance) not visualized
- No interactive CLI for quick analysis
- Streamlit integration missing for stakeholder demos
- Limited ability to compare model performance across runs
- No dataset-level insights (class distribution, feature statistics)
- No analysis of discriminative tokens/words per class
- No live inference capability for testing models in real-time
- No modern UI design for professional presentation

This proposal adds a comprehensive visualization suite with:
1. **Step Output Visualizations** - Training curves, convergence plots, feature analysis
2. **Data Insights** - Dataset overview and top-k tokens by class analysis
3. **Unified Metrics Dashboard** - CLI-based metrics viewer with tabular summaries
4. **Live Inference Playground** - Interactive parameter adjustment and real-time predictions
5. **Streamlit Interactive App** - Web UI with Neumorphism design for exploring results
6. **Enhanced Comparison Views** - Side-by-side model performance with statistical annotations

## What Changes
- **NEW**: `sources/visualization.py` - Core visualization engine
- **NEW**: `sources/cli_dashboard.py` - CLI metrics viewer (terminal UI)
- **NEW**: `sources/streamlit_app.py` - Streamlit web dashboard with Neumorphism design
- **ENHANCED**: `sources/model_evaluation.py` - Add live inference and preprocessing visibility methods
- **ENHANCED**: Jupyter notebooks - Integrate new visualization utilities

## Scope
This change scopes to visualization infrastructure only. Implementation details:
- Step outputs (e.g., training losses) are collected during model training via callbacks
- Metrics are computed and cached using existing `ModelEvaluator` framework
- Data overview and token analysis use existing text preprocessing pipeline
- Live Inference uses ModelEvaluator for single-instance predictions
- CLI dashboard uses `rich` library for terminal styling
- Streamlit app provides interactive filtering, live inference, and Neumorphism UI design
- No changes to model algorithms or core training logic

## Success Criteria
✅ All step outputs visualized with appropriate chart types (line, histogram, heatmap)
✅ Data Overview shows class distribution, feature statistics, missing values
✅ Top-k Tokens visualization displays discriminative words per class
✅ Live Inference Playground responds in <500ms per prediction
✅ Neumorphism UI applied to all Streamlit pages (buttons, cards, metrics)
✅ CLI dashboard runs in terminal with `python -m sources.cli_dashboard`
✅ Streamlit app launches with `streamlit run sources/streamlit_app.py`
✅ Comparison views include statistical annotations (error bars, p-values)
✅ 95% of existing tests still pass (new tests for visualization modules)
✅ Performance: rendering <100ms for typical dataset sizes
✅ Documentation with usage examples for each visualization type

## Timeline
- **Phase 1**: Core visualization engine + step output plots + data overview (4 days)
- **Phase 2**: CLI dashboard implementation (2 days)
- **Phase 3**: Streamlit app + Neumorphism design + Live Inference Playground (4 days)
- **Phase 4**: Documentation and examples (1 day)

## Acceptance Gates
1. ✅ `openspec validate add-visualization-suite --strict` passes
2. ✅ All tasks in `tasks.md` marked complete
3. ✅ CLI dashboard and Streamlit app both working in local environment
4. ✅ Code review approval from project maintainers
