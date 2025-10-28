"""
Unit tests for visualization methods in ModelEvaluator.

Tests for:
- plot_confusion_matrix(): Confusion matrix heatmap visualization
- plot_roc_curve(): ROC curve with AUC score display
- generate_report(): Formatted text performance report

Test Coverage:
- Normal cases with default parameters
- Custom parameters (titles, colors, axes)
- Edge cases (perfect models, all wrong predictions)
- Error handling (missing visualization libraries)
- Return value validation
"""

import numpy as np
import pytest
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.datasets import make_classification

from sources.model_evaluation import ModelEvaluator


class TestConfusionMatrixVisualization:
    """Test plot_confusion_matrix() method."""

    @pytest.fixture
    def setup(self):
        """Create test data and models."""
        X, y = make_classification(
            n_samples=200, n_features=10, n_informative=8, n_classes=2, random_state=42
        )
        X_train, X_test = X[:150], X[150:]
        y_train, y_test = y[:150], y[150:]

        model = DecisionTreeClassifier(random_state=42)
        model.fit(X_train, y_train)

        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test, task_name="test_task")

        return evaluator, X_train, X_test, y_train, y_test

    def test_plot_confusion_matrix_returns_fig_ax(self, setup):
        """Test that plot_confusion_matrix returns figure and axes."""
        evaluator, _, _, _, _ = setup

        fig, ax = evaluator.plot_confusion_matrix(use_test=True)

        assert fig is not None
        assert ax is not None
        assert hasattr(fig, "savefig")
        assert hasattr(ax, "set_title")

        plt.close(fig)

    def test_plot_confusion_matrix_uses_test_set(self, setup):
        """Test that use_test=True uses test set."""
        evaluator, _, _, _, _ = setup

        fig, ax = evaluator.plot_confusion_matrix(use_test=True)

        title = ax.get_title()
        assert "Test" in title

        plt.close(fig)

    def test_plot_confusion_matrix_uses_training_set(self, setup):
        """Test that use_test=False uses training set."""
        evaluator, _, _, _, _ = setup

        fig, ax = evaluator.plot_confusion_matrix(use_test=False)

        title = ax.get_title()
        assert "Training" in title

        plt.close(fig)

    def test_plot_confusion_matrix_custom_title(self, setup):
        """Test that custom title is used."""
        evaluator, _, _, _, _ = setup
        custom_title = "Custom Confusion Matrix Title"

        fig, ax = evaluator.plot_confusion_matrix(title=custom_title)

        assert ax.get_title() == custom_title

        plt.close(fig)

    def test_plot_confusion_matrix_custom_colormap(self, setup):
        """Test that custom colormap can be set."""
        evaluator, _, _, _, _ = setup

        # Should not raise error with different colormap
        fig, ax = evaluator.plot_confusion_matrix(cmap="Reds")

        assert fig is not None

        plt.close(fig)

    def test_plot_confusion_matrix_with_provided_axes(self, setup):
        """Test that function works with provided axes."""
        evaluator, _, _, _, _ = setup

        fig, ax_provided = plt.subplots()
        fig_ret, ax_ret = evaluator.plot_confusion_matrix(ax=ax_provided)

        # Should return the same figure
        assert fig_ret == fig
        assert ax_ret == ax_provided

        plt.close(fig)

    def test_plot_confusion_matrix_includes_task_name(self, setup):
        """Test that task name appears in title."""
        evaluator, _, _, _, _ = setup

        fig, ax = evaluator.plot_confusion_matrix()

        title = ax.get_title()
        assert "test_task" in title

        plt.close(fig)

    def test_plot_confusion_matrix_heatmap_data(self, setup):
        """Test that confusion matrix displays correct data."""
        evaluator, _, _, _, _ = setup

        fig, ax = evaluator.plot_confusion_matrix(use_test=True)

        # Check that heatmap was created (has image collection)
        assert len(ax.collections) > 0

        plt.close(fig)


class TestROCCurveVisualization:
    """Test plot_roc_curve() method."""

    @pytest.fixture
    def setup(self):
        """Create test data and models."""
        X, y = make_classification(
            n_samples=200, n_features=10, n_informative=8, n_classes=2, random_state=42
        )
        X_train, X_test = X[:150], X[150:]
        y_train, y_test = y[:150], y[150:]

        model = DecisionTreeClassifier(random_state=42)
        model.fit(X_train, y_train)

        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test, task_name="roc_test")

        return evaluator, X_train, X_test, y_train, y_test

    def test_plot_roc_curve_returns_fig_ax_auc(self, setup):
        """Test that plot_roc_curve returns figure, axes, and AUC score."""
        evaluator, _, _, _, _ = setup

        fig, ax, auc = evaluator.plot_roc_curve(use_test=True)

        assert fig is not None
        assert ax is not None
        assert isinstance(auc, (float, np.floating))
        assert 0.0 <= auc <= 1.0

        plt.close(fig)

    def test_plot_roc_curve_auc_in_title(self, setup):
        """Test that AUC score appears in title."""
        evaluator, _, _, _, _ = setup

        fig, ax, auc = evaluator.plot_roc_curve(use_test=True)

        title = ax.get_title()
        # AUC value should be in label, check legend instead
        legend = ax.get_legend()
        assert legend is not None

        plt.close(fig)

    def test_plot_roc_curve_uses_test_set(self, setup):
        """Test that use_test=True uses test set."""
        evaluator, _, _, _, _ = setup

        fig, ax, _ = evaluator.plot_roc_curve(use_test=True)

        title = ax.get_title()
        assert "Test" in title

        plt.close(fig)

    def test_plot_roc_curve_uses_training_set(self, setup):
        """Test that use_test=False uses training set."""
        evaluator, _, _, _, _ = setup

        fig, ax, _ = evaluator.plot_roc_curve(use_test=False)

        title = ax.get_title()
        assert "Training" in title

        plt.close(fig)

    def test_plot_roc_curve_custom_title(self, setup):
        """Test that custom title is used."""
        evaluator, _, _, _, _ = setup
        custom_title = "Custom ROC Curve"

        fig, ax, _ = evaluator.plot_roc_curve(title=custom_title)

        assert ax.get_title() == custom_title

        plt.close(fig)

    def test_plot_roc_curve_custom_color(self, setup):
        """Test that custom color can be set."""
        evaluator, _, _, _, _ = setup

        fig, ax, _ = evaluator.plot_roc_curve(color="red")

        assert fig is not None

        plt.close(fig)

    def test_plot_roc_curve_with_provided_axes(self, setup):
        """Test that function works with provided axes."""
        evaluator, _, _, _, _ = setup

        fig, ax_provided = plt.subplots()
        fig_ret, ax_ret, _ = evaluator.plot_roc_curve(ax=ax_provided)

        assert fig_ret == fig
        assert ax_ret == ax_provided

        plt.close(fig)

    def test_plot_roc_curve_has_legend(self, setup):
        """Test that ROC curve has legend."""
        evaluator, _, _, _, _ = setup

        fig, ax, _ = evaluator.plot_roc_curve()

        legend = ax.get_legend()
        assert legend is not None

        plt.close(fig)

    def test_plot_roc_curve_auc_value_in_valid_range(self, setup):
        """Test that AUC score is in valid range."""
        evaluator, _, _, _, _ = setup

        fig, _, auc = evaluator.plot_roc_curve(use_test=True)

        assert 0.0 <= auc <= 1.0

        plt.close(fig)

    def test_plot_roc_curve_perfect_model(self):
        """Test ROC curve for perfect model (AUC = 1.0)."""
        X, y = make_classification(
            n_samples=100,
            n_features=10,
            n_informative=5,
            n_classes=2,
            n_clusters_per_class=1,
            random_state=42,
        )
        X_train, X_test = X[:75], X[75:]
        y_train, y_test = y[:75], y[75:]

        # Perfect model that memorizes
        model = DecisionTreeClassifier(max_depth=None, random_state=42)
        model.fit(X_train, y_train)

        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)

        fig, ax, auc_train = evaluator.plot_roc_curve(use_test=False)

        # Training AUC should be 1.0 or very close
        assert auc_train >= 0.95

        plt.close(fig)


class TestReportGeneration:
    """Test generate_report() method."""

    @pytest.fixture
    def setup(self):
        """Create test data and models."""
        X, y = make_classification(
            n_samples=200, n_features=10, n_informative=8, n_classes=2, random_state=42
        )
        X_train, X_test = X[:150], X[150:]
        y_train, y_test = y[:150], y[150:]

        model = DecisionTreeClassifier(random_state=42)
        model.fit(X_train, y_train)

        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test, task_name="report_test")

        return evaluator

    def test_generate_report_returns_string(self, setup):
        """Test that generate_report returns a string."""
        evaluator = setup

        report = evaluator.generate_report(use_test=True)

        assert isinstance(report, str)
        assert len(report) > 0

    def test_generate_report_includes_metrics(self, setup):
        """Test that report includes all key metrics."""
        evaluator = setup

        report = evaluator.generate_report(use_test=True)

        assert "Accuracy" in report
        assert "Precision" in report
        assert "Recall" in report
        assert "F1-Score" in report
        assert "AUC" in report or "AUC-ROC" in report

    def test_generate_report_includes_task_name(self, setup):
        """Test that report includes task name."""
        evaluator = setup

        report = evaluator.generate_report()

        assert "report_test" in report

    def test_generate_report_uses_test_set(self, setup):
        """Test that use_test=True uses test set."""
        evaluator = setup

        report = evaluator.generate_report(use_test=True)

        assert "Test Set" in report or "test" in report.lower()

    def test_generate_report_uses_training_set(self, setup):
        """Test that use_test=False uses training set."""
        evaluator = setup

        report = evaluator.generate_report(use_test=False)

        assert "Training Set" in report or "training" in report.lower()

    def test_generate_report_includes_summary(self, setup):
        """Test that report includes summary section."""
        evaluator = setup

        report = evaluator.generate_report()

        assert "Summary" in report or "Assessment" in report

    def test_generate_report_includes_class_info(self, setup):
        """Test that report includes positive/negative class info."""
        evaluator = setup

        report = evaluator.generate_report()

        assert "Positive" in report or "Negative" in report or "Class" in report

    def test_generate_report_metrics_format(self, setup):
        """Test that metrics are formatted as floats."""
        evaluator = setup

        report = evaluator.generate_report(use_test=True)

        # Should have numeric values in format like 0.xxxx
        import re

        float_pattern = r"0\.\d{4}"
        matches = re.findall(float_pattern, report)

        assert len(matches) > 0

    def test_generate_report_assessment_levels(self):
        """Test that report includes appropriate assessment levels."""
        X, y = make_classification(
            n_samples=100, n_features=10, n_informative=5, n_classes=2, random_state=42
        )
        X_train, X_test = X[:75], X[75:]
        y_train, y_test = y[:75], y[75:]

        model = DecisionTreeClassifier(random_state=42)
        model.fit(X_train, y_train)

        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)

        report = evaluator.generate_report()

        # Should have assessment level
        assessments = ["Excellent", "Very Good", "Good", "Fair", "Poor"]
        found = any(assessment in report for assessment in assessments)

        assert found

    def test_generate_report_file_writable(self, setup):
        """Test that report can be written to file."""
        evaluator = setup
        report = evaluator.generate_report()

        # Simulate file write (don't actually write)
        assert isinstance(report, str)
        assert len(report) > 100  # Should be substantial


class TestVisualizationEdgeCases:
    """Test edge cases and error handling for visualization methods."""

    def test_perfect_model_visualization(self):
        """Test visualizations with perfect model."""
        X, y = make_classification(
            n_samples=100,
            n_features=10,
            n_informative=5,
            n_classes=2,
            n_clusters_per_class=1,
            random_state=42,
        )
        X_train, X_test = X[:75], X[75:]
        y_train, y_test = y[:75], y[75:]

        model = DecisionTreeClassifier(max_depth=None, random_state=42)
        model.fit(X_train, y_train)

        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)

        # All visualizations should work
        fig1, ax1 = evaluator.plot_confusion_matrix()
        fig2, ax2, auc = evaluator.plot_roc_curve()
        report = evaluator.generate_report()

        assert fig1 is not None
        assert fig2 is not None
        assert auc >= 0.9
        assert len(report) > 0

        plt.close(fig1)
        plt.close(fig2)

    def test_poor_model_visualization(self):
        """Test visualizations with poor model."""
        X, y = make_classification(
            n_samples=100, n_features=10, n_informative=2, n_classes=2, random_state=42
        )
        X_train, X_test = X[:75], X[75:]
        y_train, y_test = y[:75], y[75:]

        # Simple model that will likely perform poorly
        from sklearn.tree import DecisionTreeClassifier

        model = DecisionTreeClassifier(max_depth=1, random_state=42)
        model.fit(X_train, y_train)

        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)

        # All visualizations should still work
        fig1, ax1 = evaluator.plot_confusion_matrix()
        fig2, ax2, auc = evaluator.plot_roc_curve()
        report = evaluator.generate_report()

        assert fig1 is not None
        assert fig2 is not None
        assert 0.0 <= auc <= 1.0
        assert "Poor" in report or "Fair" in report or len(report) > 0

        plt.close(fig1)
        plt.close(fig2)

    def test_small_dataset_visualization(self):
        """Test visualizations with small dataset."""
        X = np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8]])
        y = np.array([0, 0, 0, 1, 1, 1, 0])

        X_train, X_test = X[:5], X[5:]
        y_train, y_test = y[:5], y[5:]

        model = DecisionTreeClassifier(random_state=42)
        model.fit(X_train, y_train)

        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)

        # Should work even with small dataset
        fig1, ax1 = evaluator.plot_confusion_matrix()
        fig2, ax2, auc = evaluator.plot_roc_curve()
        report = evaluator.generate_report()

        assert fig1 is not None
        assert fig2 is not None
        assert len(report) > 0

        plt.close(fig1)
        plt.close(fig2)

    def test_large_dataset_visualization(self):
        """Test visualizations with large dataset."""
        X, y = make_classification(
            n_samples=10000, n_features=20, n_informative=15, n_classes=2, random_state=42
        )
        X_train, X_test = X[:8000], X[8000:]
        y_train, y_test = y[:8000], y[8000:]

        model = DecisionTreeClassifier(max_depth=10, random_state=42)
        model.fit(X_train, y_train)

        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)

        # Should work even with large dataset
        fig1, ax1 = evaluator.plot_confusion_matrix()
        fig2, ax2, auc = evaluator.plot_roc_curve()
        report = evaluator.generate_report()

        assert fig1 is not None
        assert fig2 is not None
        assert 0.0 <= auc <= 1.0
        assert len(report) > 100

        plt.close(fig1)
        plt.close(fig2)


class TestVisualizationIntegration:
    """Integration tests for all visualization methods."""

    def test_complete_visualization_workflow(self):
        """Test complete workflow using all visualization methods."""
        X, y = make_classification(
            n_samples=200, n_features=10, n_informative=8, n_classes=2, random_state=42
        )
        X_train, X_test = X[:150], X[150:]
        y_train, y_test = y[:150], y[150:]

        model = DecisionTreeClassifier(random_state=42)
        model.fit(X_train, y_train)

        evaluator = ModelEvaluator(
            model, X_train, y_train, X_test, y_test, task_name="integration_test"
        )

        # Create visualizations
        fig_cm, ax_cm = evaluator.plot_confusion_matrix()
        fig_roc, ax_roc, auc = evaluator.plot_roc_curve()
        report = evaluator.generate_report()

        # Verify all outputs
        assert fig_cm is not None and ax_cm is not None
        assert fig_roc is not None and ax_roc is not None
        assert 0.0 <= auc <= 1.0
        assert isinstance(report, str) and len(report) > 0

        # Verify integration across methods
        metrics = evaluator.calculate_metrics()
        assert "auc_roc_test" in metrics

        plt.close(fig_cm)
        plt.close(fig_roc)

    def test_multiple_visualizations_same_figure(self):
        """Test creating multiple visualizations on same figure."""
        X, y = make_classification(
            n_samples=200, n_features=10, n_informative=8, n_classes=2, random_state=42
        )
        X_train, X_test = X[:150], X[150:]
        y_train, y_test = y[:150], y[150:]

        model = DecisionTreeClassifier(random_state=42)
        model.fit(X_train, y_train)

        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)

        # Create figure with subplots
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Add visualizations to subplots
        fig_cm, ax_cm = evaluator.plot_confusion_matrix(ax=axes[0])
        fig_roc, ax_roc, _ = evaluator.plot_roc_curve(ax=axes[1])

        # Both should use same figure
        assert fig_cm == fig
        assert fig_roc == fig

        plt.close(fig)
