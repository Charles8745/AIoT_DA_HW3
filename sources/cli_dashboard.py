"""
CLI Dashboard for Model Metrics Visualization

Provides terminal-based metrics viewer with filtering, sorting, and export capabilities.
Uses the rich library for styled tables and interactive features.
"""

import pandas as pd
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class CliDashboard:
    """Terminal-based metrics dashboard for model evaluation results."""
    
    def __init__(self, evaluators: List, dataset_name: str = "Results"):
        """
        Initialize CLI Dashboard.
        
        Parameters:
        -----------
        evaluators : list
            List of ModelEvaluator objects
        dataset_name : str
            Name of the dataset or experiment
        """
        self.evaluators = evaluators
        self.dataset_name = dataset_name
        self.metrics_df = self._build_metrics_dataframe()
    
    def _build_metrics_dataframe(self) -> pd.DataFrame:
        """Build metrics dataframe from evaluators."""
        records = []
        
        for i, evaluator in enumerate(self.evaluators):
            record = {
                'Model': getattr(evaluator, 'model_name', f'Model {i+1}'),
                'Dataset': getattr(evaluator, 'dataset_name', self.dataset_name),
                'Accuracy': getattr(evaluator, 'accuracy_test', 0),
                'Precision': getattr(evaluator, 'precision_test', 0),
                'Recall': getattr(evaluator, 'recall_test', 0),
                'F1': getattr(evaluator, 'f1_test', 0),
                'AUC': getattr(evaluator, 'auc_roc_test', 0),
            }
            records.append(record)
        
        return pd.DataFrame(records)
    
    def render(self, sort_by: str = 'Model', ascending: bool = True, 
               filter_model_type: Optional[str] = None,
               filter_dataset: Optional[str] = None) -> None:
        """
        Display metrics table in terminal.
        
        Parameters:
        -----------
        sort_by : str
            Column to sort by
        ascending : bool
            Sort order
        filter_model_type : str, optional
            Filter by model type
        filter_dataset : str, optional
            Filter by dataset name
        """
        df = self.metrics_df.copy()
        
        # Apply filters
        if filter_model_type:
            df = df[df['Model'].str.contains(filter_model_type, case=False, na=False)]
        
        if filter_dataset:
            df = df[df['Dataset'].str.contains(filter_dataset, case=False, na=False)]
        
        # Sort
        if sort_by in df.columns:
            df = df.sort_values(by=sort_by, ascending=ascending)
        
        # Display table
        print("\n" + "=" * 100)
        print(f"  MODEL METRICS DASHBOARD - {self.dataset_name}")
        print("=" * 100 + "\n")
        
        # Format and print dataframe
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        
        print(df.to_string(index=False))
        print("\n" + "=" * 100)
        print(f"  Total Models: {len(df)} | Columns: {', '.join(df.columns)}")
        print("=" * 100 + "\n")
    
    def export(self, filename: str, format: str = 'csv', 
               include_metadata: bool = True,
               auto_timestamp: bool = False) -> str:
        """
        Export metrics to file.
        
        Parameters:
        -----------
        filename : str
            Output filename (without extension)
        format : str
            Export format ('csv' or 'json')
        include_metadata : bool
            Include metadata in export
        auto_timestamp : bool
            Automatically add timestamp to filename
        
        Returns:
        --------
        str : Path to exported file
        """
        if auto_timestamp:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
            filename = f"{filename}_{timestamp}"
        
        output_path = Path(filename).with_suffix(f'.{format}')
        
        if format == 'csv':
            self.metrics_df.to_csv(output_path, index=False)
            return str(output_path)
        
        elif format == 'json':
            export_data = {
                'export_date': datetime.now().isoformat(),
                'dataset': self.dataset_name,
                'metrics': self.metrics_df.to_dict(orient='records'),
            }
            
            if include_metadata:
                export_data['metadata'] = {
                    'n_models': len(self.evaluators),
                    'n_metrics': len(self.metrics_df.columns),
                    'columns': list(self.metrics_df.columns),
                }
            
            with open(output_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            return str(output_path)
        
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'csv' or 'json'.")
    
    def filter_by_model_type(self, model_type: str) -> pd.DataFrame:
        """Filter metrics by model type."""
        return self.metrics_df[self.metrics_df['Model'].str.contains(model_type, case=False, na=False)]
    
    def filter_by_dataset(self, dataset_name: str) -> pd.DataFrame:
        """Filter metrics by dataset."""
        return self.metrics_df[self.metrics_df['Dataset'].str.contains(dataset_name, case=False, na=False)]
    
    def get_top_models(self, metric: str = 'AUC', top_n: int = 5) -> pd.DataFrame:
        """Get top N models by specified metric."""
        return self.metrics_df.nlargest(top_n, metric)
    
    def get_comparison_summary(self) -> Dict:
        """Get summary statistics for all models."""
        numeric_cols = self.metrics_df.select_dtypes(include=['float', 'int']).columns
        
        summary = {
            'total_models': len(self.metrics_df),
            'metrics_count': len(numeric_cols),
        }
        
        for col in numeric_cols:
            summary[f'{col}_mean'] = self.metrics_df[col].mean()
            summary[f'{col}_std'] = self.metrics_df[col].std()
            summary[f'{col}_max'] = self.metrics_df[col].max()
            summary[f'{col}_min'] = self.metrics_df[col].min()
        
        return summary
    
    def display_summary(self) -> None:
        """Display summary statistics."""
        summary = self.get_comparison_summary()
        
        print("\n" + "=" * 50)
        print("  SUMMARY STATISTICS")
        print("=" * 50)
        print(f"Total Models: {summary['total_models']}")
        print(f"Metrics Tracked: {summary['metrics_count']}\n")
        
        for key, value in summary.items():
            if key not in ['total_models', 'metrics_count']:
                if isinstance(value, float):
                    print(f"  {key}: {value:.4f}")
        
        print("=" * 50 + "\n")


def main():
    """Main function for CLI dashboard (for testing)."""
    import argparse
    
    parser = argparse.ArgumentParser(description='CLI Metrics Dashboard')
    parser.add_argument('--show-all', action='store_true', help='Show all metrics')
    parser.add_argument('--model-type', type=str, help='Filter by model type')
    parser.add_argument('--dataset', type=str, help='Filter by dataset')
    parser.add_argument('--sort-by', type=str, default='Model', help='Sort by column')
    parser.add_argument('--desc', action='store_true', help='Sort descending')
    parser.add_argument('--export', type=str, help='Export to file (csv or json)')
    parser.add_argument('--format', type=str, default='csv', choices=['csv', 'json'])
    
    args = parser.parse_args()
    
    print("CLI Dashboard would render here with provided arguments")
    print(f"Arguments: {args}")


if __name__ == '__main__':
    main()
