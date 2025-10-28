"""
Visualization Suite for ML Model Analysis

Provides comprehensive plotting functions for:
- Training curves and convergence analysis
- Feature importance and metrics heatmaps
- Confusion matrices and ROC curves
- Dataset overview and token analysis
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import warnings

warnings.filterwarnings('ignore')

# Set consistent style
sns.set_style("darkgrid")
sns.set_palette("Set2")


def plot_training_curves(history, metric='loss', figsize=(12, 5)):
    """
    Plot training and validation curves with confidence bands.
    
    Parameters:
    -----------
    history : dict
        Dictionary with keys: 'loss', 'val_loss', 'accuracy', 'val_accuracy'
    metric : str, default='loss'
        Main metric to highlight ('loss' or 'accuracy')
    figsize : tuple
        Figure size (width, height)
    
    Returns:
    --------
    fig, axes : matplotlib figure and axes
    """
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Loss curves
    if 'loss' in history:
        axes[0].plot(history['loss'], label='Training Loss', marker='o', linewidth=2)
        if 'val_loss' in history:
            axes[0].plot(history['val_loss'], label='Validation Loss', marker='s', linewidth=2)
        axes[0].set_xlabel('Epoch', fontsize=11)
        axes[0].set_ylabel('Loss', fontsize=11)
        axes[0].set_title('Loss Curves', fontsize=12, fontweight='bold')
        axes[0].legend(loc='best')
        axes[0].grid(True, alpha=0.3)
    
    # Accuracy curves
    if 'accuracy' in history:
        axes[1].plot(history['accuracy'], label='Training Accuracy', marker='o', linewidth=2)
        if 'val_accuracy' in history:
            axes[1].plot(history['val_accuracy'], label='Validation Accuracy', marker='s', linewidth=2)
        axes[1].set_xlabel('Epoch', fontsize=11)
        axes[1].set_ylabel('Accuracy', fontsize=11)
        axes[1].set_title('Accuracy Curves', fontsize=12, fontweight='bold')
        axes[1].legend(loc='best')
        axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig, axes


def plot_feature_importance(feature_names, importance_scores, top_n=15, figsize=(10, 8)):
    """
    Plot feature importance as horizontal bar chart.
    
    Parameters:
    -----------
    feature_names : list
        Names of features
    importance_scores : list or array
        Importance scores for each feature
    top_n : int, default=15
        Number of top features to display
    figsize : tuple
        Figure size (width, height)
    
    Returns:
    --------
    fig, ax : matplotlib figure and axes
    """
    # Sort by importance
    sorted_idx = np.argsort(importance_scores)[::-1]
    sorted_names = [feature_names[i] for i in sorted_idx[:top_n]]
    sorted_scores = [importance_scores[i] for i in sorted_idx[:top_n]]
    
    fig, ax = plt.subplots(figsize=figsize)
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(sorted_scores)))
    ax.barh(range(len(sorted_scores)), sorted_scores, color=colors)
    ax.set_yticks(range(len(sorted_scores)))
    ax.set_yticklabels(sorted_names)
    ax.set_xlabel('Importance Score', fontsize=11)
    ax.set_title(f'Top {top_n} Feature Importance', fontsize=12, fontweight='bold')
    ax.invert_yaxis()
    plt.tight_layout()
    return fig, ax


def plot_metrics_heatmap(metrics_dict, figsize=(12, 6)):
    """
    Plot metrics as color-coded heatmap.
    
    Parameters:
    -----------
    metrics_dict : dict
        Dictionary where keys are model names and values are dicts of metrics
        e.g., {'Model1': {'accuracy': 0.92, 'precision': 0.88, ...}, ...}
    figsize : tuple
        Figure size (width, height)
    
    Returns:
    --------
    fig, ax : matplotlib figure and axes
    """
    # Convert to DataFrame
    df = pd.DataFrame(metrics_dict).T
    
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(df, annot=True, fmt='.3f', cmap='RdYlGn', center=0.85,
                cbar_kws={'label': 'Score'}, ax=ax, linewidths=1, linecolor='white')
    ax.set_title('Model Metrics Heatmap', fontsize=12, fontweight='bold')
    ax.set_ylabel('Model', fontsize=11)
    ax.set_xlabel('Metric', fontsize=11)
    plt.tight_layout()
    return fig, ax


def plot_confusion_matrices_grid(evaluators, figsize=(15, 5), normalize=False, annotate_metrics=False):
    """
    Display confusion matrices for multiple models in grid layout.
    
    Parameters:
    -----------
    evaluators : list
        List of ModelEvaluator objects
    figsize : tuple
        Figure size (width, height)
    normalize : bool, default=False
        Whether to normalize confusion matrix by row
    annotate_metrics : bool, default=False
        Whether to include accuracy in title
    
    Returns:
    --------
    fig, axes : matplotlib figure and axes grid
    """
    n_models = len(evaluators)
    n_cols = min(3, n_models)
    n_rows = (n_models + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    if n_rows == 1 and n_cols == 1:
        axes = np.array([[axes]])
    elif n_rows == 1 or n_cols == 1:
        axes = axes.reshape(n_rows, n_cols)
    
    for idx, evaluator in enumerate(evaluators):
        row = idx // n_cols
        col = idx % n_cols
        ax = axes[row, col]
        
        cm = evaluator.confusion_matrix_test if hasattr(evaluator, 'confusion_matrix_test') else evaluator.cm_test
        
        if normalize:
            cm_display = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        else:
            cm_display = cm
        
        sns.heatmap(cm_display, annot=True, fmt='.2f' if normalize else '.0f',
                   cmap='Blues', ax=ax, cbar=False, square=True)
        
        title = getattr(evaluator, 'model_name', f'Model {idx+1}')
        if annotate_metrics:
            acc = evaluator.accuracy_test if hasattr(evaluator, 'accuracy_test') else 0
            title += f' (Acc: {acc:.3f})'
        
        ax.set_title(title, fontweight='bold')
        ax.set_ylabel('True', fontsize=10)
        ax.set_xlabel('Predicted', fontsize=10)
    
    # Hide unused subplots
    for idx in range(n_models, n_rows * n_cols):
        row = idx // n_cols
        col = idx % n_cols
        axes[row, col].axis('off')
    
    plt.tight_layout()
    return fig, axes


def plot_roc_curves_overlay(evaluators, figsize=(8, 8), colors=None, line_styles=None, fill_under=False):
    """
    Overlay multiple ROC curves in single plot.
    
    Parameters:
    -----------
    evaluators : list
        List of ModelEvaluator objects
    figsize : tuple
        Figure size (width, height)
    colors : list, optional
        Custom colors for curves
    line_styles : list, optional
        Custom line styles for curves
    fill_under : bool, default=False
        Whether to fill area under curve
    
    Returns:
    --------
    fig, ax : matplotlib figure and axes
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    if colors is None:
        colors = plt.cm.Set2(np.linspace(0, 1, len(evaluators)))
    if line_styles is None:
        line_styles = ['-'] * len(evaluators)
    
    # Plot diagonal reference line
    ax.plot([0, 1], [0, 1], 'k--', lw=2, label='Random Classifier')
    
    for idx, evaluator in enumerate(evaluators):
        if hasattr(evaluator, 'fpr_test') and hasattr(evaluator, 'tpr_test'):
            fpr = evaluator.fpr_test
            tpr = evaluator.tpr_test
            auc = evaluator.auc_roc_test if hasattr(evaluator, 'auc_roc_test') else 0
            
            model_name = getattr(evaluator, 'model_name', f'Model {idx+1}')
            label = f'{model_name} (AUC = {auc:.3f})'
            
            ax.plot(fpr, tpr, color=colors[idx], linestyle=line_styles[idx],
                   linewidth=2.5, label=label)
            
            if fill_under:
                ax.fill_between(fpr, tpr, alpha=0.2, color=colors[idx])
    
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate', fontsize=11)
    ax.set_ylabel('True Positive Rate', fontsize=11)
    ax.set_title('ROC Curves Comparison', fontsize=12, fontweight='bold')
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig, ax


def plot_convergence_analysis(losses, window=50, show_trend=True, figsize=(12, 6)):
    """
    Plot smoothed loss curves with moving average.
    
    Parameters:
    -----------
    losses : list or dict
        Loss values or dict with 'train' and 'val' keys
    window : int, default=50
        Window size for moving average
    show_trend : bool, default=True
        Whether to show trend line
    figsize : tuple
        Figure size (width, height)
    
    Returns:
    --------
    fig, ax : matplotlib figure and axes
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    if isinstance(losses, dict):
        for key, values in losses.items():
            values = np.array(values)
            ax.plot(values, alpha=0.3, label=f'{key.capitalize()} (raw)')
            
            # Moving average
            ma = np.convolve(values, np.ones(window)/window, mode='valid')
            ax.plot(range(window-1, len(values)), ma, linewidth=2.5, label=f'{key.capitalize()} (smoothed)')
    else:
        losses = np.array(losses)
        ax.plot(losses, alpha=0.3, label='Loss (raw)')
        
        # Moving average
        ma = np.convolve(losses, np.ones(window)/window, mode='valid')
        ax.plot(range(window-1, len(losses)), ma, linewidth=2.5, label='Loss (smoothed)')
        
        if show_trend:
            # Trend line
            z = np.polyfit(range(len(ma)), ma, 1)
            p = np.poly1d(z)
            ax.plot(range(window-1, len(losses)), p(range(len(ma))), 'r--', 
                   linewidth=2, label='Trend', alpha=0.7)
    
    ax.set_xlabel('Epoch', fontsize=11)
    ax.set_ylabel('Loss', fontsize=11)
    ax.set_title('Training Convergence Analysis', fontsize=12, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig, ax


def plot_data_overview(X_data, y_labels, dataset_name='Dataset', class_names=None, figsize=(16, 10)):
    """
    Display comprehensive dataset statistics and insights.
    
    Parameters:
    -----------
    X_data : array-like
        Feature matrix
    y_labels : array-like
        Labels
    dataset_name : str
        Name of the dataset
    class_names : list, optional
        Names for each class
    figsize : tuple
        Figure size (width, height)
    
    Returns:
    --------
    fig : matplotlib figure
    """
    if class_names is None:
        class_names = [f'Class {i}' for i in np.unique(y_labels)]
    
    fig = plt.figure(figsize=figsize)
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    # Class distribution
    ax1 = fig.add_subplot(gs[0, 0])
    unique, counts = np.unique(y_labels, return_counts=True)
    colors = plt.cm.Set3(np.linspace(0, 1, len(unique)))
    ax1.bar(range(len(unique)), counts, color=colors)
    ax1.set_xticks(range(len(unique)))
    ax1.set_xticklabels([class_names[i] for i in unique], rotation=0)
    ax1.set_ylabel('Count', fontsize=11)
    ax1.set_title('Class Distribution', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Feature statistics
    ax2 = fig.add_subplot(gs[0, 1])
    if isinstance(X_data, pd.DataFrame):
        feature_means = X_data.mean()
        feature_names = X_data.columns[:10]  # Top 10
    else:
        X_data = np.asarray(X_data)
        feature_means = X_data.mean(axis=0)[:10]
        feature_names = [f'Feature {i}' for i in range(min(10, X_data.shape[1]))]
    
    ax2.barh(range(len(feature_means)), feature_means, color=plt.cm.viridis(np.linspace(0, 1, len(feature_means))))
    ax2.set_yticks(range(len(feature_means)))
    ax2.set_yticklabels(feature_names)
    ax2.set_xlabel('Mean Value', fontsize=11)
    ax2.set_title('Top Features (Mean Values)', fontsize=12, fontweight='bold')
    ax2.invert_yaxis()
    
    # Dataset info
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.axis('off')
    info_text = f"""
    Dataset: {dataset_name}
    
    Samples: {X_data.shape[0] if hasattr(X_data, 'shape') else len(X_data)}
    Features: {X_data.shape[1] if hasattr(X_data, 'shape') else 'N/A'}
    Classes: {len(unique)}
    
    Class Balance:
    """
    for i, c in enumerate(unique):
        pct = counts[i] / len(y_labels) * 100
        info_text += f"    {class_names[i]}: {counts[i]} ({pct:.1f}%)\n"
    
    ax3.text(0.1, 0.9, info_text, transform=ax3.transAxes, fontsize=10,
            verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    # Missing values (if applicable)
    ax4 = fig.add_subplot(gs[1, 1])
    if isinstance(X_data, pd.DataFrame):
        missing = X_data.isnull().sum()
        if missing.sum() > 0:
            missing = missing[missing > 0]
            ax4.barh(range(len(missing)), missing, color='coral')
            ax4.set_yticks(range(len(missing)))
            ax4.set_yticklabels(missing.index)
            ax4.set_xlabel('Missing Count', fontsize=11)
            ax4.set_title('Missing Values', fontsize=12, fontweight='bold')
        else:
            ax4.text(0.5, 0.5, 'No Missing Values', ha='center', va='center',
                    transform=ax4.transAxes, fontsize=12)
            ax4.axis('off')
    else:
        ax4.text(0.5, 0.5, 'No Missing Data', ha='center', va='center',
                transform=ax4.transAxes, fontsize=12)
        ax4.axis('off')
    
    fig.suptitle(f'{dataset_name} Overview', fontsize=14, fontweight='bold', y=0.995)
    
    return fig


def plot_top_tokens_by_class(messages, labels, class_names=None, top_k=15, figsize=(14, 8),
                             metric='frequency', show_importance=False):
    """
    Display most discriminative tokens (words) for each class.
    
    Parameters:
    -----------
    messages : list
        List of text messages
    labels : array-like
        Labels for each message
    class_names : list, optional
        Names for each class
    top_k : int, default=15
        Number of top tokens to display per class
    figsize : tuple
        Figure size (width, height)
    metric : str, default='frequency'
        Metric for token selection ('frequency' or 'tf-idf')
    show_importance : bool, default=False
        Whether to color by importance score
    
    Returns:
    --------
    fig, axes : matplotlib figure and axes
    """
    unique_labels = np.unique(labels)
    if class_names is None:
        class_names = [f'Class {i}' for i in unique_labels]
    
    n_classes = len(unique_labels)
    n_cols = min(2, n_classes)
    n_rows = (n_classes + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    if n_rows == 1 and n_cols == 1:
        axes = np.array([[axes]])
    elif n_rows == 1 or n_cols == 1:
        axes = axes.reshape(n_rows, n_cols)
    
    try:
        stop_words = set(stopwords.words('english'))
    except:
        stop_words = set()
    
    for idx, label_val in enumerate(unique_labels):
        row = idx // n_cols
        col = idx % n_cols
        ax = axes[row, col] if n_rows > 1 and n_cols > 1 else axes[row, col]
        
        # Get messages for this class
        class_messages = [messages[i] for i in range(len(messages)) if labels[i] == label_val]
        
        # Tokenize and count
        tokens = []
        for msg in class_messages:
            try:
                msg_tokens = word_tokenize(str(msg).lower())
                tokens.extend([t for t in msg_tokens if t.isalnum() and t not in stop_words])
            except:
                tokens.extend(str(msg).lower().split())
        
        token_counts = Counter(tokens)
        top_tokens = dict(token_counts.most_common(top_k))
        
        # Plot
        names = list(top_tokens.keys())
        counts = list(top_tokens.values())
        colors = plt.cm.Spectral(np.linspace(0.2, 0.8, len(counts)))
        
        ax.barh(range(len(counts)), counts, color=colors)
        ax.set_yticks(range(len(counts)))
        ax.set_yticklabels(names, fontsize=9)
        ax.set_xlabel('Frequency', fontsize=10)
        ax.set_title(f'{class_names[idx]} - Top {top_k} Tokens', fontweight='bold')
        ax.invert_yaxis()
    
    # Hide unused subplots
    for idx in range(n_classes, n_rows * n_cols):
        row = idx // n_cols
        col = idx % n_cols
        axes[row, col].axis('off')
    
    plt.tight_layout()
    return fig, axes


# DataOverviewAnalyzer class for generating statistics
class DataOverviewAnalyzer:
    """Helper class for generating dataset statistics."""
    
    def __init__(self, X_data, y_labels):
        self.X_data = X_data
        self.y_labels = y_labels
    
    def generate_report(self):
        """Generate comprehensive dataset statistics report."""
        report = {
            'n_samples': len(self.y_labels),
            'n_features': self.X_data.shape[1] if hasattr(self.X_data, 'shape') else len(self.X_data[0]),
            'n_classes': len(np.unique(self.y_labels)),
            'class_distribution': dict(zip(*np.unique(self.y_labels, return_counts=True))),
        }
        
        if isinstance(self.X_data, pd.DataFrame):
            report['feature_stats'] = self.X_data.describe().to_dict()
            report['missing_values'] = self.X_data.isnull().sum().to_dict()
        
        return pd.DataFrame(report)
