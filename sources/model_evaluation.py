"""
Unified Model Evaluation Framework for Binary Classification

This module provides a standardized evaluation framework for binary classification models.
It encapsulates common evaluation patterns across ML notebooks, enabling consistent 
metrics calculation and task-scoped model comparison.

Module Structure:
- ModelEvaluator: Main class for evaluating binary classification models
- _validate_model_compatibility(): Check model has required methods
- _validate_binary_classification(): Check y has exactly 2 classes
- _validate_data_shapes(): Check data dimensions match

Key Features:
- Binary classification only (2 classes)
- Supports sklearn-compatible classifiers with predict() and predict_proba()
- Calculates: accuracy, precision, recall, F1, AUC-ROC
- Task-scoped comparison only (same dataset required)
- Clear error messages for invalid inputs

Example Usage:
    from sklearn.tree import DecisionTreeClassifier
    from sources.model_evaluation import ModelEvaluator
    
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    
    evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test, 
                               task_name='phishing')
    metrics = evaluator.calculate_metrics()
    print(metrics)
"""

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    roc_curve,
)

try:
    import matplotlib.pyplot as plt
    import seaborn as sns

    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False


def _validate_model_compatibility(model):
    """
    Validate that model has required methods for classification evaluation.
    
    Args:
        model: sklearn-compatible classifier
        
    Raises:
        AttributeError: If model lacks predict() or predict_proba()
        
    Requirements:
        - Model must have predict() method
        - Model must have predict_proba() method (for ROC curve)
        - Linear Regression and other regression models will be rejected
    """
    if not hasattr(model, "predict"):
        raise AttributeError(f"Model must have predict() method. " f"Got: {type(model).__name__}")

    if not hasattr(model, "predict_proba"):
        raise AttributeError(
            f"Model must have predict_proba() method for ROC curve calculation. "
            f"Linear Regression and other regression models are not supported. "
            f"Got: {type(model).__name__}"
        )


def _validate_binary_classification(y_train, y_test):
    """
    Validate that y contains exactly 2 unique classes (binary classification).
    
    Args:
        y_train: Training labels
        y_test: Test labels
        
    Raises:
        ValueError: If not binary classification
        
    Requirements:
        - y_train must have exactly 2 unique classes
        - y_test must have exactly 2 unique classes
        - Multi-class classification is not supported in this version
    """
    unique_train = np.unique(y_train)
    unique_test = np.unique(y_test)

    if len(unique_train) != 2:
        raise ValueError(
            f"Only binary classification supported. "
            f"y_train has {len(unique_train)} classes: {unique_train}. "
            f"Expected: 2 classes"
        )

    if len(unique_test) != 2:
        raise ValueError(
            f"Only binary classification supported. "
            f"y_test has {len(unique_test)} classes: {unique_test}. "
            f"Expected: 2 classes"
        )


def _validate_data_shapes(X_train, y_train, X_test, y_test):
    """
    Validate that data dimensions are consistent.
    
    Args:
        X_train, y_train: Training data and labels
        X_test, y_test: Test data and labels
        
    Raises:
        ValueError: If dimensions don't match
        
    Requirements:
        - X_train.shape[0] == len(y_train)
        - X_test.shape[0] == len(y_test)
        - X_train.shape[1] == X_test.shape[1] (same number of features)
    """
    if X_train.shape[0] != len(y_train):
        raise ValueError(
            f"X_train and y_train shape mismatch: "
            f"X_train has {X_train.shape[0]} samples, "
            f"y_train has {len(y_train)} samples"
        )

    if X_test.shape[0] != len(y_test):
        raise ValueError(
            f"X_test and y_test shape mismatch: "
            f"X_test has {X_test.shape[0]} samples, "
            f"y_test has {len(y_test)} samples"
        )

    if X_train.shape[1] != X_test.shape[1]:
        raise ValueError(
            f"X_train and X_test feature count mismatch: "
            f"X_train has {X_train.shape[1]} features, "
            f"X_test has {X_test.shape[1]} features. "
            f"Both must have the same number of features"
        )


class ModelEvaluator:
    """
    Standardized evaluator for binary classification models.
    
    This class encapsulates evaluation logic for any sklearn-compatible binary
    classifier. It validates inputs, calculates metrics, generates visualizations,
    and supports task-scoped model comparison.
    
    Attributes:
        model: sklearn-compatible binary classifier
        X_train, y_train: Training data and labels
        X_test, y_test: Test data and labels
        task_name: Optional task identifier (e.g., 'phishing', 'spam')
        _y_pred_train: Cached training predictions
        _y_pred_test: Cached test predictions
        _y_proba_train: Cached training probabilities
        _y_proba_test: Cached test probabilities
        
    Parameters:
        model: sklearn-compatible classifier with predict() and predict_proba()
        X_train: Training feature matrix (n_samples, n_features)
        y_train: Training labels (n_samples,) with exactly 2 unique classes
        X_test: Test feature matrix (n_samples, n_features)
        y_test: Test labels (n_samples,) with exactly 2 unique classes
        task_name: Optional task identifier for reporting (default: None)
        
    Raises:
        AttributeError: If model lacks predict() or predict_proba() methods
        ValueError: If y is not binary classification or data shapes don't match
        
    Example:
        >>> from sklearn.tree import DecisionTreeClassifier
        >>> from sources.model_evaluation import ModelEvaluator
        >>> 
        >>> model = DecisionTreeClassifier()
        >>> model.fit(X_train, y_train)
        >>> 
        >>> evaluator = ModelEvaluator(model, X_train, y_train, X_test, y_test,
        ...                            task_name='phishing')
        >>> metrics = evaluator.calculate_metrics()
        >>> print(f"Test Accuracy: {metrics['accuracy_test']:.3f}")
    """

    def __init__(self, model, X_train, y_train, X_test, y_test, task_name=None):
        """
        Initialize ModelEvaluator with validation.
        
        Performs comprehensive validation:
        1. Model compatibility (has predict and predict_proba)
        2. Binary classification (y has exactly 2 classes)
        3. Data shape consistency (matching dimensions)
        
        Args:
            model: sklearn-compatible classifier
            X_train: Training features (n_samples, n_features)
            y_train: Training labels (n_samples,) with 2 unique classes
            X_test: Test features (n_samples, n_features)
            y_test: Test labels (n_samples,) with 2 unique classes
            task_name: Optional task identifier (default: None)
            
        Raises:
            AttributeError: If model lacks required methods
            ValueError: If y is not binary or data shapes don't match
        """
        # Validate model compatibility
        _validate_model_compatibility(model)

        # Validate binary classification
        _validate_binary_classification(y_train, y_test)

        # Validate data shapes
        _validate_data_shapes(X_train, y_train, X_test, y_test)

        # Store inputs
        self.model = model
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.task_name = task_name

        # Cache for predictions (lazy evaluation)
        self._y_pred_train = None
        self._y_pred_test = None
        self._y_proba_train = None
        self._y_proba_test = None

    def _get_predictions(self):
        """
        Get or compute predictions from model (lazy evaluation).
        
        Returns:
            Tuple of (y_pred_train, y_pred_test, y_proba_train, y_proba_test)
        """
        if self._y_pred_train is None:
            self._y_pred_train = self.model.predict(self.X_train)
            self._y_pred_test = self.model.predict(self.X_test)
            self._y_proba_train = self.model.predict_proba(self.X_train)
            self._y_proba_test = self.model.predict_proba(self.X_test)

        return (self._y_pred_train, self._y_pred_test, self._y_proba_train, self._y_proba_test)

    def calculate_metrics(self):
        """
        Calculate classification metrics for training and test sets.
        
        Metrics calculated:
        - Accuracy: (TP + TN) / (TP + TN + FP + FN)
        - Precision: TP / (TP + FP)
        - Recall: TP / (TP + FN)
        - F1-Score: 2 * (Precision * Recall) / (Precision + Recall)
        - AUC-ROC: Area under ROC curve
        
        Returns:
            dict with keys:
            - 'accuracy_train', 'accuracy_test'
            - 'precision_train', 'precision_test'
            - 'recall_train', 'recall_test'
            - 'f1_train', 'f1_test'
            - 'auc_roc_train', 'auc_roc_test'
            - 'task_name' (if provided during initialization)
            
        Example:
            >>> metrics = evaluator.calculate_metrics()
            >>> print(metrics['accuracy_test'])
            0.95
            >>> print(metrics['auc_roc_test'])
            0.97
        """
        y_pred_train, y_pred_test, y_proba_train, y_proba_test = self._get_predictions()

        # Calculate train metrics
        acc_train = accuracy_score(self.y_train, y_pred_train)
        prec_train = precision_score(self.y_train, y_pred_train, zero_division=0)
        rec_train = recall_score(self.y_train, y_pred_train, zero_division=0)
        f1_train = f1_score(self.y_train, y_pred_train, zero_division=0)

        # For AUC, use probability of positive class (second column)
        auc_train = roc_auc_score(self.y_train, y_proba_train[:, 1])

        # Calculate test metrics
        acc_test = accuracy_score(self.y_test, y_pred_test)
        prec_test = precision_score(self.y_test, y_pred_test, zero_division=0)
        rec_test = recall_score(self.y_test, y_pred_test, zero_division=0)
        f1_test = f1_score(self.y_test, y_pred_test, zero_division=0)

        # For AUC, use probability of positive class (second column)
        auc_test = roc_auc_score(self.y_test, y_proba_test[:, 1])

        # Return metrics dict
        metrics = {
            "accuracy_train": acc_train,
            "accuracy_test": acc_test,
            "precision_train": prec_train,
            "precision_test": prec_test,
            "recall_train": rec_train,
            "recall_test": rec_test,
            "f1_train": f1_train,
            "f1_test": f1_test,
            "auc_roc_train": auc_train,
            "auc_roc_test": auc_test,
        }

        if self.task_name is not None:
            metrics["task_name"] = self.task_name

        return metrics

    def compare_with(self, other):
        """
        Compare metrics with another ModelEvaluator.
        
        Validates that both evaluators use the same dataset (by checking shapes),
        then returns a comparison of their metrics.
        
        Args:
            other: Another ModelEvaluator instance
            
        Returns:
            dict mapping metric names to (self_value, other_value) tuples
            
        Raises:
            ValueError: If datasets have different sizes or feature counts
            TypeError: If other is not a ModelEvaluator instance
            
        Example:
            >>> eval1 = ModelEvaluator(model1, X_train, y_train, X_test, y_test)
            >>> eval2 = ModelEvaluator(model2, X_train, y_train, X_test, y_test)
            >>> comparison = eval1.compare_with(eval2)
            >>> print(f"Model1 Accuracy: {comparison['accuracy_test'][0]:.3f}")
            >>> print(f"Model2 Accuracy: {comparison['accuracy_test'][1]:.3f}")
        """
        if not isinstance(other, ModelEvaluator):
            raise TypeError(
                f"Can only compare with another ModelEvaluator. " f"Got: {type(other).__name__}"
            )

        # Check that test sets have same size
        if self.X_test.shape[0] != other.X_test.shape[0]:
            raise ValueError(
                f"Cannot compare: different test set sizes. "
                f"self: {self.X_test.shape[0]}, other: {other.X_test.shape[0]}"
            )

        # Check that both have same number of features
        if self.X_test.shape[1] != other.X_test.shape[1]:
            raise ValueError(
                f"Cannot compare: different feature counts. "
                f"self: {self.X_test.shape[1]}, other: {other.X_test.shape[1]}"
            )

        # Get metrics from both
        self_metrics = self.calculate_metrics()
        other_metrics = other.calculate_metrics()

        # Return comparison dict
        comparison = {}
        for key in self_metrics:
            if key != "task_name":
                comparison[key] = (self_metrics[key], other_metrics[key])

        return comparison

    def plot_confusion_matrix(self, ax=None, use_test=True, title=None, cmap="Blues"):
        """
        Plot confusion matrix for the model.
        
        Args:
            ax: matplotlib.axes.Axes object (default: None, creates new figure)
            use_test: If True, use test set; if False, use training set (default: True)
            title: Custom title for the plot (default: auto-generated)
            cmap: Colormap for heatmap (default: 'Blues')
            
        Returns:
            tuple: (fig, ax) matplotlib figure and axes objects
            
        Raises:
            ImportError: If matplotlib or seaborn not installed
            
        Example:
            >>> fig, ax = evaluator.plot_confusion_matrix(use_test=True)
            >>> plt.tight_layout()
            >>> plt.savefig('confusion_matrix.png', dpi=100)
            >>> plt.show()
        """
        if not VISUALIZATION_AVAILABLE:
            raise ImportError(
                "Visualization requires matplotlib and seaborn. "
                "Install with: pip install matplotlib seaborn"
            )

        y_pred_train, y_pred_test, _, _ = self._get_predictions()

        # Select data
        if use_test:
            y_true = self.y_test
            y_pred = y_pred_test
            data_label = "Test"
        else:
            y_true = self.y_train
            y_pred = y_pred_train
            data_label = "Training"

        # Calculate confusion matrix
        cm = confusion_matrix(y_true, y_pred)

        # Create figure if not provided
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 6))
        else:
            fig = ax.get_figure()

        # Plot heatmap
        sns.heatmap(
            cm, annot=True, fmt="d", cmap=cmap, ax=ax, cbar_kws={"label": "Count"}, square=True
        )

        # Labels
        class_labels = np.unique(y_true)
        ax.set_xlabel("Predicted Label", fontsize=12)
        ax.set_ylabel("True Label", fontsize=12)

        if title is None:
            task_suffix = f" ({self.task_name})" if self.task_name else ""
            title = f"Confusion Matrix - {data_label} Set{task_suffix}"

        ax.set_title(title, fontsize=14, fontweight="bold")

        # Set tick labels
        ax.set_xticklabels(class_labels)
        ax.set_yticklabels(class_labels)

        plt.tight_layout()

        return fig, ax

    def plot_roc_curve(self, ax=None, use_test=True, title=None, color="blue"):
        """
        Plot ROC curve for the model.
        
        Args:
            ax: matplotlib.axes.Axes object (default: None, creates new figure)
            use_test: If True, use test set; if False, use training set (default: True)
            title: Custom title for the plot (default: auto-generated)
            color: Line color for ROC curve (default: 'blue')
            
        Returns:
            tuple: (fig, ax, auc_score) matplotlib figure, axes, and AUC value
            
        Raises:
            ImportError: If matplotlib not installed
            
        Example:
            >>> fig, ax, auc = evaluator.plot_roc_curve(use_test=True)
            >>> print(f"AUC Score: {auc:.3f}")
            >>> plt.show()
        """
        if not VISUALIZATION_AVAILABLE:
            raise ImportError(
                "Visualization requires matplotlib. " "Install with: pip install matplotlib"
            )

        _, _, y_proba_train, y_proba_test = self._get_predictions()

        # Select data
        if use_test:
            y_true = self.y_test
            y_proba = y_proba_test
            data_label = "Test"
        else:
            y_true = self.y_train
            y_proba = y_proba_train
            data_label = "Training"

        # Calculate ROC curve
        fpr, tpr, _ = roc_curve(y_true, y_proba[:, 1])
        auc_score = roc_auc_score(y_true, y_proba[:, 1])

        # Create figure if not provided
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 6))
        else:
            fig = ax.get_figure()

        # Plot ROC curve
        ax.plot(fpr, tpr, color=color, lw=2, label=f"ROC curve (AUC = {auc_score:.3f})")

        # Plot random classifier
        ax.plot([0, 1], [0, 1], "k--", lw=1, label="Random classifier")

        # Labels and title
        ax.set_xlabel("False Positive Rate", fontsize=12)
        ax.set_ylabel("True Positive Rate", fontsize=12)

        if title is None:
            task_suffix = f" ({self.task_name})" if self.task_name else ""
            title = f"ROC Curve - {data_label} Set{task_suffix}"

        ax.set_title(title, fontsize=14, fontweight="bold")

        # Formatting
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.legend(loc="lower right", fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        return fig, ax, auc_score

    def generate_report(self, use_test=True):
        """
        Generate formatted text report of model performance.
        
        Args:
            use_test: If True, report test set metrics; if False, training set (default: True)
            
        Returns:
            str: Formatted report text
            
        Example:
            >>> report = evaluator.generate_report(use_test=True)
            >>> print(report)
            >>> 
            >>> # Save to file
            >>> with open('model_report.txt', 'w') as f:
            ...     f.write(report)
        """
        metrics = self.calculate_metrics()

        # Select metrics suffix
        suffix = "_test" if use_test else "_train"
        data_label = "Test" if use_test else "Training"

        # Build report
        lines = []
        lines.append("=" * 70)

        if self.task_name:
            lines.append(f"Model Performance Report - {self.task_name}")
        else:
            lines.append("Model Performance Report")

        lines.append("=" * 70)
        lines.append(f"\nDataset: {data_label} Set")
        lines.append(f"Samples: {len(self.y_test) if use_test else len(self.y_train)}")
        lines.append(f"Positive Class: {np.unique(self.y_test)[1]}")
        lines.append(f"Negative Class: {np.unique(self.y_test)[0]}")

        lines.append("\n" + "-" * 70)
        lines.append("Classification Metrics")
        lines.append("-" * 70)

        # Format metrics
        metric_names = {
            "accuracy": ("Accuracy", "correctness"),
            "precision": ("Precision", "positive predictive value"),
            "recall": ("Recall", "sensitivity / true positive rate"),
            "f1": ("F1-Score", "harmonic mean of precision and recall"),
            "auc_roc": ("AUC-ROC", "area under receiver operating characteristic"),
        }

        for key, (display_name, description) in metric_names.items():
            metric_key = f"{key}{suffix}"
            value = metrics[metric_key]
            lines.append(f"\n{display_name}: {value:.4f}")
            lines.append(f"  └─ {description}")

        lines.append("\n" + "-" * 70)
        lines.append("Summary")
        lines.append("-" * 70)

        acc = metrics[f"accuracy{suffix}"]
        auc = metrics[f"auc_roc{suffix}"]

        # Performance assessment
        if acc >= 0.95 and auc >= 0.95:
            assessment = "Excellent"
        elif acc >= 0.90 and auc >= 0.90:
            assessment = "Very Good"
        elif acc >= 0.80 and auc >= 0.80:
            assessment = "Good"
        elif acc >= 0.70 and auc >= 0.70:
            assessment = "Fair"
        else:
            assessment = "Poor"

        lines.append(f"\nOverall Assessment: {assessment}")
        lines.append(f"Model is performing at {acc*100:.1f}% accuracy")

        lines.append("\n" + "=" * 70)

        return "\n".join(lines)


def plot_model_comparison(evaluators, metric="accuracy_test", ax=None, title=None):
    """
    Plot comparison of multiple models on the same metric.

    Args:
        evaluators: List of ModelEvaluator instances to compare
        metric: Metric to compare (default: 'accuracy_test')
                Options: accuracy_train, accuracy_test, precision_train, precision_test,
                        recall_train, recall_test, f1_train, f1_test,
                        auc_roc_train, auc_roc_test
        ax: matplotlib.axes.Axes object (default: None, creates new figure)
        title: Custom title for the plot (default: auto-generated)

    Returns:
        tuple: (fig, ax) matplotlib figure and axes objects

    Raises:
        ImportError: If matplotlib not installed
        ValueError: If metric name is invalid or evaluators list is empty
        TypeError: If evaluators is not a list of ModelEvaluator instances

    Example:
        >>> eval1 = ModelEvaluator(model1, X_train, y_train, X_test, y_test, task_name='model1')
        >>> eval2 = ModelEvaluator(model2, X_train, y_train, X_test, y_test, task_name='model2')
        >>> fig, ax = plot_model_comparison([eval1, eval2], metric='accuracy_test')
        >>> plt.show()
    """
    if not VISUALIZATION_AVAILABLE:
        raise ImportError(
            "Visualization requires matplotlib. "
            "Install with: pip install matplotlib"
        )

    if not evaluators:
        raise ValueError("evaluators list cannot be empty")

    if not isinstance(evaluators, list):
        raise TypeError(f"evaluators must be a list. Got: {type(evaluators).__name__}")

    # Validate all evaluators
    for i, ev in enumerate(evaluators):
        if not isinstance(ev, ModelEvaluator):
            raise TypeError(
                f"evaluator[{i}] is not a ModelEvaluator. "
                f"Got: {type(ev).__name__}"
            )

    # Get metrics from all evaluators
    all_metrics = [ev.calculate_metrics() for ev in evaluators]

    # Check if metric exists
    if metric not in all_metrics[0]:
        valid_metrics = [k for k in all_metrics[0].keys() if k != "task_name"]
        raise ValueError(
            f"Invalid metric '{metric}'. "
            f"Valid metrics: {', '.join(valid_metrics)}"
        )

    # Extract metric values and labels
    values = [metrics[metric] for metrics in all_metrics]
    labels = [
        ev.task_name if ev.task_name else f"Model {i+1}"
        for i, ev in enumerate(evaluators)
    ]

    # Create figure if not provided
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    else:
        fig = ax.get_figure()

    # Create bar chart
    colors = plt.cm.viridis(np.linspace(0, 1, len(evaluators)))
    bars = ax.bar(labels, values, color=colors, alpha=0.7, edgecolor="black", linewidth=1.5)

    # Add value labels on bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{value:.3f}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    # Formatting
    ax.set_ylabel(metric.replace("_", " ").title(), fontsize=12, fontweight="bold")
    ax.set_ylim(0, 1.0)
    ax.grid(axis="y", alpha=0.3, linestyle="--")

    if title is None:
        title = f"Model Comparison - {metric.replace('_', ' ').title()}"

    ax.set_title(title, fontsize=14, fontweight="bold")

    plt.tight_layout()

    return fig, ax
