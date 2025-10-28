"""
Unit tests for comparison tools in model_evaluation module.

Tests for:
- plot_model_comparison(): Multi-model comparison visualization

Test Coverage:
- Normal cases with multiple models
- Custom parameters (metrics, titles, axes)
- Edge cases (single model, many models)
- Error handling (invalid metrics, empty lists)
- Return value validation
"""

import numpy as np
import pytest
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

from sources.model_evaluation import ModelEvaluator, plot_model_comparison


class TestModelComparison:
    """Test plot_model_comparison() function."""

    @pytest.fixture
    def setup(self):
        """Create test data and multiple models."""
        X, y = make_classification(
            n_samples=200, n_features=10, n_informative=8, n_classes=2, random_state=42
        )
        X_train, X_test = X[:150], X[150:]
        y_train, y_test = y[:150], y[150:]

        # Create multiple models
        model1 = DecisionTreeClassifier(max_depth=3, random_state=42)
        model1.fit(X_train, y_train)

        model2 = DecisionTreeClassifier(max_depth=5, random_state=42)
        model2.fit(X_train, y_train)

        model3 = SVC(kernel="rbf", probability=True, random_state=42)
        model3.fit(X_train, y_train)

        eval1 = ModelEvaluator(
            model1,
            X_train,
            y_train,
            X_test,
            y_test,
            task_name="Decision Tree (depth=3)",
        )
        eval2 = ModelEvaluator(
            model2,
            X_train,
            y_train,
            X_test,
            y_test,
            task_name="Decision Tree (depth=5)",
        )
        eval3 = ModelEvaluator(
            model3, X_train, y_train, X_test, y_test, task_name="SVM"
        )

        return [eval1, eval2, eval3], X_train, X_test, y_train, y_test

    def test_plot_model_comparison_returns_fig_ax(self, setup):
        """Test that plot_model_comparison returns figure and axes."""
        evaluators, _, _, _, _ = setup

        fig, ax = plot_model_comparison(evaluators)

        assert fig is not None
        assert ax is not None
        assert hasattr(fig, "savefig")
        assert hasattr(ax, "set_title")

        plt.close(fig)

    def test_plot_model_comparison_default_metric(self, setup):
        """Test that default metric is accuracy_test."""
        evaluators, _, _, _, _ = setup

        fig, ax = plot_model_comparison(evaluators)

        title = ax.get_title()
        assert "accuracy" in title.lower() or "test" in title.lower()

        plt.close(fig)

    def test_plot_model_comparison_custom_metric(self, setup):
        """Test that custom metric can be specified."""
        evaluators, _, _, _, _ = setup

        fig, ax = plot_model_comparison(evaluators, metric="f1_test")

        title = ax.get_title()
        assert "f1" in title.lower()

        plt.close(fig)

    def test_plot_model_comparison_all_metrics(self, setup):
        """Test that all valid metrics work."""
        evaluators, _, _, _, _ = setup

        valid_metrics = [
            "accuracy_train",
            "accuracy_test",
            "precision_train",
            "precision_test",
            "recall_train",
            "recall_test",
            "f1_train",
            "f1_test",
            "auc_roc_train",
            "auc_roc_test",
        ]

        for metric in valid_metrics:
            fig, ax = plot_model_comparison(evaluators, metric=metric)
            assert fig is not None
            plt.close(fig)

    def test_plot_model_comparison_custom_title(self, setup):
        """Test that custom title is used."""
        evaluators, _, _, _, _ = setup
        custom_title = "Custom Comparison Title"

        fig, ax = plot_model_comparison(evaluators, title=custom_title)

        assert ax.get_title() == custom_title

        plt.close(fig)

    def test_plot_model_comparison_with_provided_axes(self, setup):
        """Test that function works with provided axes."""
        evaluators, _, _, _, _ = setup

        fig, ax_provided = plt.subplots()
        fig_ret, ax_ret = plot_model_comparison(evaluators, ax=ax_provided)

        assert fig_ret == fig
        assert ax_ret == ax_provided

        plt.close(fig)

    def test_plot_model_comparison_includes_task_names(self, setup):
        """Test that model task names appear in comparison."""
        evaluators, _, _, _, _ = setup

        fig, ax = plot_model_comparison(evaluators)

        # Get x-axis labels
        labels = [t.get_text() for t in ax.get_xticklabels()]
        labels_str = " ".join(labels)

        # At least one task name should appear
        found = any(ev.task_name in labels_str for ev in evaluators if ev.task_name)
        assert found

        plt.close(fig)

    def test_plot_model_comparison_bar_values(self, setup):
        """Test that comparison shows different values for different models."""
        evaluators, _, _, _, _ = setup

        fig, ax = plot_model_comparison(evaluators, metric="accuracy_test")

        # Get bar heights (metric values)
        bars = [patch for patch in ax.patches]
        heights = [bar.get_height() for bar in bars]

        # Should have 3 bars
        assert len(heights) == 3

        # Values should be between 0 and 1
        for height in heights:
            assert 0.0 <= height <= 1.0

        plt.close(fig)

    def test_plot_model_comparison_single_model(self):
        """Test comparison with single model."""
        X, y = make_classification(
            n_samples=100, n_features=10, n_informative=5, n_classes=2, random_state=42
        )
        X_train, X_test = X[:75], X[75:]
        y_train, y_test = y[:75], y[75:]

        model = DecisionTreeClassifier(random_state=42)
        model.fit(X_train, y_train)

        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)

        fig, ax = plot_model_comparison([evaluator])

        assert fig is not None
        bars = [patch for patch in ax.patches]
        assert len(bars) == 1

        plt.close(fig)

    def test_plot_model_comparison_many_models(self):
        """Test comparison with many models."""
        X, y = make_classification(
            n_samples=150, n_features=10, n_informative=8, n_classes=2, random_state=42
        )
        X_train, X_test = X[:100], X[100:]
        y_train, y_test = y[:100], y[100:]

        evaluators = []
        for i in range(5):
            model = DecisionTreeClassifier(max_depth=i + 1, random_state=42)
            model.fit(X_train, y_train)
            ev = ModelEvaluator(
                model, X_train, y_train, X_test, y_test, task_name=f"Model {i+1}"
            )
            evaluators.append(ev)

        fig, ax = plot_model_comparison(evaluators)

        assert fig is not None
        bars = [patch for patch in ax.patches]
        assert len(bars) == 5

        plt.close(fig)


class TestModelComparisonErrors:
    """Test error handling for plot_model_comparison()."""

    def test_empty_evaluators_list(self):
        """Test that empty list raises ValueError."""
        with pytest.raises(ValueError, match="empty"):
            plot_model_comparison([])

    def test_invalid_evaluators_type(self):
        """Test that non-list type raises TypeError."""
        X, y = make_classification(
            n_samples=100, n_features=10, n_informative=5, n_classes=2, random_state=42
        )
        X_train, X_test = X[:75], X[75:]
        y_train, y_test = y[:75], y[75:]

        model = DecisionTreeClassifier(random_state=42)
        model.fit(X_train, y_train)

        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)

        with pytest.raises(TypeError, match="must be a list"):
            plot_model_comparison(evaluator)  # Not a list

    def test_non_evaluator_in_list(self):
        """Test that non-ModelEvaluator in list raises TypeError."""
        with pytest.raises(TypeError, match="not a ModelEvaluator"):
            plot_model_comparison(["not_an_evaluator"])

    def test_invalid_metric_name(self):
        """Test that invalid metric name raises ValueError."""
        X, y = make_classification(
            n_samples=100, n_features=10, n_informative=5, n_classes=2, random_state=42
        )
        X_train, X_test = X[:75], X[75:]
        y_train, y_test = y[:75], y[75:]

        model = DecisionTreeClassifier(random_state=42)
        model.fit(X_train, y_train)

        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)

        with pytest.raises(ValueError, match="Invalid metric"):
            plot_model_comparison([evaluator], metric="invalid_metric")


class TestModelComparisonIntegration:
    """Integration tests for model comparison."""

    def test_comparison_workflow(self):
        """Test complete comparison workflow."""
        X, y = make_classification(
            n_samples=200, n_features=10, n_informative=8, n_classes=2, random_state=42
        )
        X_train, X_test = X[:150], X[150:]
        y_train, y_test = y[:150], y[150:]

        # Create different models
        models = {
            "Decision Tree (depth=3)": DecisionTreeClassifier(
                max_depth=3, random_state=42
            ),
            "Decision Tree (depth=5)": DecisionTreeClassifier(
                max_depth=5, random_state=42
            ),
            "Random Forest": RandomForestClassifier(n_estimators=10, random_state=42),
            "SVM": SVC(kernel="rbf", probability=True, random_state=42),
        }

        # Train models and create evaluators
        evaluators = []
        for name, model in models.items():
            model.fit(X_train, y_train)
            ev = ModelEvaluator(model, X_train, y_train, X_test, y_test, task_name=name)
            evaluators.append(ev)

        # Compare accuracy
        fig1, ax1 = plot_model_comparison(evaluators, metric="accuracy_test")
        assert fig1 is not None

        # Compare F1
        fig2, ax2 = plot_model_comparison(evaluators, metric="f1_test")
        assert fig2 is not None

        # Compare AUC
        fig3, ax3 = plot_model_comparison(evaluators, metric="auc_roc_test")
        assert fig3 is not None

        plt.close(fig1)
        plt.close(fig2)
        plt.close(fig3)

    def test_comparison_with_single_vs_multiple_metrics(self):
        """Test comparing models across different metrics."""
        X, y = make_classification(
            n_samples=150, n_features=8, n_informative=6, n_classes=2, random_state=42
        )
        X_train, X_test = X[:100], X[100:]
        y_train, y_test = y[:100], y[100:]

        # Create evaluators
        evaluators = []
        for i in range(3):
            model = DecisionTreeClassifier(max_depth=i + 2, random_state=42)
            model.fit(X_train, y_train)
            ev = ModelEvaluator(model, X_train, y_train, X_test, y_test)
            evaluators.append(ev)

        # Get metrics for comparison
        metrics = [
            "accuracy_train",
            "precision_test",
            "recall_test",
            "f1_test",
            "auc_roc_test",
        ]

        results = {}
        for metric in metrics:
            fig, ax = plot_model_comparison(evaluators, metric=metric)
            results[metric] = fig
            assert fig is not None

        # Close all figures
        for fig in results.values():
            plt.close(fig)

    def test_model_comparison_consistency(self):
        """Test that comparison values match individual evaluator metrics."""
        X, y = make_classification(
            n_samples=100, n_features=10, n_informative=5, n_classes=2, random_state=42
        )
        X_train, X_test = X[:75], X[75:]
        y_train, y_test = y[:75], y[75:]

        models = [
            DecisionTreeClassifier(max_depth=2, random_state=42),
            DecisionTreeClassifier(max_depth=4, random_state=42),
        ]

        evaluators = []
        for model in models:
            model.fit(X_train, y_train)
            ev = ModelEvaluator(model, X_train, y_train, X_test, y_test)
            evaluators.append(ev)

        # Get individual metrics
        individual_metrics = [ev.calculate_metrics() for ev in evaluators]

        # Create comparison chart
        fig, ax = plot_model_comparison(evaluators, metric="accuracy_test")

        # Get bar heights
        bars = [patch for patch in ax.patches]
        heights = [bar.get_height() for bar in bars]

        # Heights should match individual metrics
        for i, height in enumerate(heights):
            assert abs(height - individual_metrics[i]["accuracy_test"]) < 0.0001

        plt.close(fig)
