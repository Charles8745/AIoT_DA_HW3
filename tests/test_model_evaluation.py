"""
Unit Tests for Model Evaluation Framework

Tests cover:
- Phase 1.1: Model initialization and validation (6 tests)
- Phase 1.2: Binary classification validation (3 tests)
- Phase 1.3: Data shape validation (3 tests)
- Phase 1.4: Metrics calculation (6 tests)

Total: 18 tests
Target: 100% pass rate, >90% code coverage
"""

import pytest
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sources.model_evaluation import (
    ModelEvaluator,
    _validate_model_compatibility,
    _validate_binary_classification,
    _validate_data_shapes,
)


# ============================================================================
# Test Fixtures - Data generation
# ============================================================================


@pytest.fixture
def binary_classification_data():
    """Generate binary classification dataset."""
    X, y = make_classification(
        n_samples=200, n_features=10, n_informative=8, n_redundant=2, n_classes=2, random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    return X_train, X_test, y_train, y_test


@pytest.fixture
def trained_classifier(binary_classification_data):
    """Train a classifier on binary classification data."""
    X_train, X_test, y_train, y_test = binary_classification_data
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    return model, X_train, X_test, y_train, y_test


@pytest.fixture
def multiclass_data():
    """Generate multi-class classification dataset."""
    X, y = make_classification(
        n_samples=150,
        n_features=10,
        n_informative=8,
        n_redundant=2,
        n_classes=3,
        n_clusters_per_class=1,
        random_state=42,
    )
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    return X_train, X_test, y_train, y_test


# ============================================================================
# Test Group 1: Model Initialization Validation (6 tests)
# ============================================================================


class TestModelInitialization:
    """Tests for ModelEvaluator initialization and model validation."""

    def test_valid_model_initialization(self, trained_classifier):
        """Test successful initialization with valid model and data."""
        model, X_train, X_test, y_train, y_test = trained_classifier

        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)

        assert evaluator.model is model
        assert evaluator.X_train is X_train
        assert evaluator.y_train is y_train
        assert evaluator.X_test is X_test
        assert evaluator.y_test is y_test
        assert evaluator.task_name is None

    def test_initialization_with_task_name(self, trained_classifier):
        """Test initialization with optional task_name parameter."""
        model, X_train, X_test, y_train, y_test = trained_classifier

        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test, task_name="phishing")

        assert evaluator.task_name == "phishing"

    def test_model_without_predict_method_raises_error(self, binary_classification_data):
        """Test that model without predict() raises AttributeError."""
        X_train, X_test, y_train, y_test = binary_classification_data

        class InvalidModel:
            def predict_proba(self, X):
                return np.random.rand(len(X), 2)

        with pytest.raises(AttributeError) as exc_info:
            ModelEvaluator(InvalidModel(), X_train, y_train, X_test, y_test)

        assert "predict()" in str(exc_info.value)

    def test_model_without_predict_proba_raises_error(self, binary_classification_data):
        """Test that model without predict_proba() raises AttributeError."""
        X_train, X_test, y_train, y_test = binary_classification_data

        class InvalidModel:
            def predict(self, X):
                return np.zeros(len(X))

        with pytest.raises(AttributeError) as exc_info:
            ModelEvaluator(InvalidModel(), X_train, y_train, X_test, y_test)

        assert "predict_proba()" in str(exc_info.value)

    def test_linear_regression_raises_error(self, binary_classification_data):
        """Test that Linear Regression (regression model) raises AttributeError."""
        X_train, X_test, y_train, y_test = binary_classification_data
        model = LinearRegression()
        model.fit(X_train, y_train)

        with pytest.raises(AttributeError) as exc_info:
            ModelEvaluator(model, X_train, y_train, X_test, y_test)

        assert "predict_proba()" in str(exc_info.value)
        assert "Linear Regression" in str(exc_info.value)

    def test_model_with_valid_methods_succeeds(self, binary_classification_data):
        """Test that model with both predict and predict_proba works."""
        X_train, X_test, y_train, y_test = binary_classification_data
        model = DecisionTreeClassifier(random_state=42)
        model.fit(X_train, y_train)

        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)

        assert evaluator is not None


# ============================================================================
# Test Group 2: Binary Classification Validation (3 tests)
# ============================================================================


class TestBinaryClassificationValidation:
    """Tests for binary classification enforcement."""

    def test_binary_classification_accepted(self, binary_classification_data):
        """Test that binary classification is accepted."""
        X_train, X_test, y_train, y_test = binary_classification_data
        model = LogisticRegression(random_state=42)
        model.fit(X_train, y_train)

        # Should not raise
        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)
        assert evaluator is not None

    def test_multiclass_training_raises_error(self, multiclass_data):
        """Test that multi-class y_train raises ValueError."""
        X_train, X_test, y_train, y_test = multiclass_data
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)

        with pytest.raises(ValueError) as exc_info:
            ModelEvaluator(model, X_train, y_train, X_test, y_test)

        assert "binary" in str(exc_info.value).lower()
        assert "3 classes" in str(exc_info.value)

    def test_multiclass_test_raises_error(self, binary_classification_data, multiclass_data):
        """Test that multi-class y_test raises ValueError."""
        X_train, X_test_bin, y_train, y_test_bin = binary_classification_data
        X_train_mc, X_test_mc, y_train_mc, y_test_mc = multiclass_data

        model = LogisticRegression(random_state=42)
        model.fit(X_train, y_train)

        # Mix binary train with multi-class test (shape-matching)
        # Use test data from multiclass but add binary from somewhere
        X_test = X_test_bin[: X_test_mc.shape[0]]
        y_test = y_test_mc  # This is multi-class

        with pytest.raises(ValueError) as exc_info:
            ModelEvaluator(model, X_train, y_train, X_test, y_test)

        assert "binary" in str(exc_info.value).lower()


# ============================================================================
# Test Group 3: Data Shape Validation (3 tests)
# ============================================================================


class TestDataShapeValidation:
    """Tests for data shape consistency validation."""

    def test_valid_data_shapes_accepted(self, trained_classifier):
        """Test that valid data shapes are accepted."""
        model, X_train, X_test, y_train, y_test = trained_classifier

        # Should not raise
        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)
        assert evaluator is not None

    def test_x_train_y_train_mismatch_raises_error(self, trained_classifier):
        """Test that X_train and y_train sample count mismatch raises ValueError."""
        model, X_train, X_test, y_train, y_test = trained_classifier

        # Create mismatch
        y_train_wrong = y_train[:-5]  # Remove 5 samples

        with pytest.raises(ValueError) as exc_info:
            ModelEvaluator(model, X_train, y_train_wrong, X_test, y_test)

        assert "X_train and y_train" in str(exc_info.value)

    def test_train_test_feature_count_mismatch_raises_error(self, trained_classifier):
        """Test that different feature counts in X_train and X_test raises ValueError."""
        model, X_train, X_test, y_train, y_test = trained_classifier

        # Create feature mismatch
        X_test_wrong = X_test[:, :-1]  # Remove 1 feature column

        with pytest.raises(ValueError) as exc_info:
            ModelEvaluator(model, X_train, y_train, X_test_wrong, y_test)

        assert "feature count" in str(exc_info.value).lower()


# ============================================================================
# Test Group 4: Metrics Calculation (6 tests)
# ============================================================================


class TestMetricsCalculation:
    """Tests for metrics calculation accuracy."""

    def test_calculate_metrics_returns_dict(self, trained_classifier):
        """Test that calculate_metrics returns a dict with all required keys."""
        model, X_train, X_test, y_train, y_test = trained_classifier
        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)

        metrics = evaluator.calculate_metrics()

        assert isinstance(metrics, dict)
        assert "accuracy_train" in metrics
        assert "accuracy_test" in metrics
        assert "precision_train" in metrics
        assert "precision_test" in metrics
        assert "recall_train" in metrics
        assert "recall_test" in metrics
        assert "f1_train" in metrics
        assert "f1_test" in metrics
        assert "auc_roc_train" in metrics
        assert "auc_roc_test" in metrics

    def test_metrics_are_floats(self, trained_classifier):
        """Test that all metric values are floats in valid range [0, 1]."""
        model, X_train, X_test, y_train, y_test = trained_classifier
        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)

        metrics = evaluator.calculate_metrics()

        for key, value in metrics.items():
            if key != "task_name":
                assert isinstance(value, (float, np.floating))
                assert 0 <= value <= 1, f"{key} = {value} out of range [0, 1]"

    def test_metrics_with_perfect_model(self, binary_classification_data):
        """Test metrics with perfect model (train accuracy = 1.0)."""
        X_train, X_test, y_train, y_test = binary_classification_data

        # Use simple model on simple data
        model = DecisionTreeClassifier(max_depth=10, random_state=42)
        model.fit(X_train, y_train)

        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)
        metrics = evaluator.calculate_metrics()

        # Perfect model should have train accuracy = 1.0
        assert metrics["accuracy_train"] == 1.0
        assert metrics["precision_train"] == 1.0
        assert metrics["recall_train"] == 1.0
        assert metrics["f1_train"] == 1.0
        assert metrics["auc_roc_train"] == 1.0

    def test_metrics_include_task_name_if_provided(self, trained_classifier):
        """Test that task_name is included in metrics if provided."""
        model, X_train, X_test, y_train, y_test = trained_classifier
        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test, task_name="phishing")

        metrics = evaluator.calculate_metrics()

        assert "task_name" in metrics
        assert metrics["task_name"] == "phishing"

    def test_metrics_exclude_task_name_if_not_provided(self, trained_classifier):
        """Test that task_name is not in metrics if not provided."""
        model, X_train, X_test, y_train, y_test = trained_classifier
        evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test)

        metrics = evaluator.calculate_metrics()

        assert "task_name" not in metrics


# ============================================================================
# Test Group 5: Model Comparison (3 tests - bonus)
# ============================================================================


class TestModelComparison:
    """Tests for model comparison functionality."""

    def test_compare_with_valid_evaluators(self, binary_classification_data):
        """Test comparing two evaluators on same dataset."""
        X_train, X_test, y_train, y_test = binary_classification_data

        model1 = LogisticRegression(random_state=42)
        model1.fit(X_train, y_train)

        model2 = DecisionTreeClassifier(random_state=42)
        model2.fit(X_train, y_train)

        eval1 = ModelEvaluator(model1, X_train, y_train, X_test, y_test)
        eval2 = ModelEvaluator(model2, X_train, y_train, X_test, y_test)

        comparison = eval1.compare_with(eval2)

        assert isinstance(comparison, dict)
        assert "accuracy_test" in comparison
        # Each metric should be a tuple of (eval1_value, eval2_value)
        assert isinstance(comparison["accuracy_test"], tuple)
        assert len(comparison["accuracy_test"]) == 2

    def test_compare_with_different_test_sizes_raises_error(self, binary_classification_data):
        """Test that comparing evaluators with different test set sizes raises error."""
        X_train, X_test, y_train, y_test = binary_classification_data

        model1 = LogisticRegression(random_state=42)
        model1.fit(X_train, y_train)

        model2 = DecisionTreeClassifier(random_state=42)
        model2.fit(X_train, y_train)

        eval1 = ModelEvaluator(model1, X_train, y_train, X_test, y_test)

        # Create evaluator with different test set size
        X_test_small = X_test[:10]
        y_test_small = y_test[:10]
        eval2 = ModelEvaluator(model2, X_train, y_train, X_test_small, y_test_small)

        with pytest.raises(ValueError) as exc_info:
            eval1.compare_with(eval2)

        assert "test set size" in str(exc_info.value).lower()

    def test_compare_with_different_feature_counts_raises_error(self, binary_classification_data):
        """Test that comparing evaluators with different feature counts raises error."""
        X_train, X_test, y_train, y_test = binary_classification_data

        model1 = LogisticRegression(random_state=42)
        model1.fit(X_train, y_train)

        model2 = DecisionTreeClassifier(random_state=42)
        model2.fit(X_train, y_train)

        eval1 = ModelEvaluator(model1, X_train, y_train, X_test, y_test)

        # Create evaluator with different feature count
        X_train_small = X_train[:, :-1]
        X_test_small = X_test[:, :-1]
        eval2 = ModelEvaluator(model2, X_train_small, y_train, X_test_small, y_test)

        with pytest.raises(ValueError) as exc_info:
            eval1.compare_with(eval2)

        assert "feature count" in str(exc_info.value).lower()


# ============================================================================
# Test Validation Functions Directly
# ============================================================================


class TestValidationFunctions:
    """Tests for validation helper functions."""

    def test_validate_model_compatibility_success(self, trained_classifier):
        """Test _validate_model_compatibility with valid model."""
        model, _, _, _, _ = trained_classifier
        # Should not raise
        _validate_model_compatibility(model)

    def test_validate_binary_classification_success(self, binary_classification_data):
        """Test _validate_binary_classification with valid data."""
        X_train, X_test, y_train, y_test = binary_classification_data
        # Should not raise
        _validate_binary_classification(y_train, y_test)

    def test_validate_data_shapes_success(self, binary_classification_data):
        """Test _validate_data_shapes with valid data."""
        X_train, X_test, y_train, y_test = binary_classification_data
        # Should not raise
        _validate_data_shapes(X_train, y_train, X_test, y_test)


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
