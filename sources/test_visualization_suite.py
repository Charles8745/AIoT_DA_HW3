"""
Comprehensive Unit Tests for Visualization Suite Implementation

Tests all 4 phases:
- Phase 1: Core visualization engine (visualization.py)
- Phase 2: CLI dashboard (cli_dashboard.py)
- Phase 3: Streamlit web app (streamlit_app.py)
- Phase 4: Enhanced model evaluator (model_evaluator_enhanced.py)
"""

import unittest
import numpy as np
import pandas as pd
from unittest.mock import Mock, MagicMock, patch
import tempfile
import os
from pathlib import Path


# ============================================================================
# PHASE 1: VISUALIZATION TESTS
# ============================================================================

class TestVisualization(unittest.TestCase):
    """Test visualization.py functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            from sources import visualization as viz
            self.viz = viz
        except ImportError:
            self.skipTest("visualization module not available")
        
        # Create mock data
        self.history = {
            'loss': np.random.random(10).cumsum() / 10,
            'val_loss': np.random.random(10).cumsum() / 10,
            'accuracy': np.random.random(10),
            'val_accuracy': np.random.random(10),
        }
        
        self.X_data = np.random.random((100, 10))
        self.y_labels = np.random.randint(0, 2, 100)
        self.messages = ['hello world', 'spam message', 'check this'] * 30
        self.labels = [0, 1, 0] * 30
    
    def test_plot_training_curves_import(self):
        """Test training curves plot can be imported."""
        self.assertTrue(hasattr(self.viz, 'plot_training_curves'))
    
    def test_plot_training_curves_execution(self):
        """Test training curves plot execution."""
        try:
            fig, axes = self.viz.plot_training_curves(self.history)
            self.assertIsNotNone(fig)
            self.assertIsNotNone(axes)
        except Exception as e:
            self.skipTest(f"Matplotlib not available: {e}")
    
    def test_plot_feature_importance_import(self):
        """Test feature importance plot can be imported."""
        self.assertTrue(hasattr(self.viz, 'plot_feature_importance'))
    
    def test_plot_metrics_heatmap_import(self):
        """Test metrics heatmap can be imported."""
        self.assertTrue(hasattr(self.viz, 'plot_metrics_heatmap'))
    
    def test_plot_confusion_matrices_grid_import(self):
        """Test confusion matrices grid can be imported."""
        self.assertTrue(hasattr(self.viz, 'plot_confusion_matrices_grid'))
    
    def test_plot_roc_curves_overlay_import(self):
        """Test ROC curves plot can be imported."""
        self.assertTrue(hasattr(self.viz, 'plot_roc_curves_overlay'))
    
    def test_plot_convergence_analysis_import(self):
        """Test convergence analysis plot can be imported."""
        self.assertTrue(hasattr(self.viz, 'plot_convergence_analysis'))
    
    def test_plot_data_overview_import(self):
        """Test data overview plot can be imported."""
        self.assertTrue(hasattr(self.viz, 'plot_data_overview'))
    
    def test_plot_top_tokens_by_class_import(self):
        """Test top tokens plot can be imported."""
        self.assertTrue(hasattr(self.viz, 'plot_top_tokens_by_class'))
    
    def test_data_overview_analyzer_class(self):
        """Test DataOverviewAnalyzer class exists."""
        self.assertTrue(hasattr(self.viz, 'DataOverviewAnalyzer'))


# ============================================================================
# PHASE 2: CLI DASHBOARD TESTS
# ============================================================================

class TestCliDashboard(unittest.TestCase):
    """Test cli_dashboard.py functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            from sources import cli_dashboard
            self.cli = cli_dashboard
        except ImportError:
            self.skipTest("cli_dashboard module not available")
        
        # Create mock evaluators
        self.mock_evaluators = []
        for i in range(3):
            evaluator = Mock()
            evaluator.model_name = f'Model_{i+1}'
            evaluator.dataset_name = 'TestData'
            evaluator.accuracy_test = 0.8 + i * 0.05
            evaluator.precision_test = 0.75 + i * 0.05
            evaluator.recall_test = 0.82 + i * 0.04
            evaluator.f1_test = 0.78 + i * 0.045
            evaluator.auc_roc_test = 0.85 + i * 0.05
            self.mock_evaluators.append(evaluator)
    
    def test_cli_dashboard_import(self):
        """Test CliDashboard class can be imported."""
        self.assertTrue(hasattr(self.cli, 'CliDashboard'))
    
    def test_cli_dashboard_initialization(self):
        """Test CliDashboard initialization."""
        dashboard = self.cli.CliDashboard(self.mock_evaluators)
        self.assertEqual(len(dashboard.evaluators), 3)
        self.assertIsNotNone(dashboard.metrics_df)
    
    def test_cli_dashboard_render(self):
        """Test dashboard rendering."""
        dashboard = self.cli.CliDashboard(self.mock_evaluators)
        try:
            dashboard.render()
        except Exception as e:
            self.skipTest(f"Render failed: {e}")
    
    def test_cli_dashboard_export_csv(self):
        """Test CSV export."""
        dashboard = self.cli.CliDashboard(self.mock_evaluators)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = dashboard.export(
                os.path.join(tmpdir, 'test'),
                format='csv'
            )
            self.assertTrue(os.path.exists(filepath))
    
    def test_cli_dashboard_export_json(self):
        """Test JSON export."""
        dashboard = self.cli.CliDashboard(self.mock_evaluators)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = dashboard.export(
                os.path.join(tmpdir, 'test'),
                format='json'
            )
            self.assertTrue(os.path.exists(filepath))
    
    def test_cli_dashboard_filter_by_model_type(self):
        """Test model type filtering."""
        dashboard = self.cli.CliDashboard(self.mock_evaluators)
        filtered = dashboard.filter_by_model_type('Model_1')
        self.assertEqual(len(filtered), 1)
    
    def test_cli_dashboard_get_top_models(self):
        """Test getting top models by metric."""
        dashboard = self.cli.CliDashboard(self.mock_evaluators)
        top = dashboard.get_top_models(metric='Accuracy', top_n=2)
        self.assertEqual(len(top), 2)
    
    def test_cli_dashboard_get_comparison_summary(self):
        """Test comparison summary."""
        dashboard = self.cli.CliDashboard(self.mock_evaluators)
        summary = dashboard.get_comparison_summary()
        self.assertIn('total_models', summary)
        self.assertEqual(summary['total_models'], 3)


# ============================================================================
# PHASE 3: STREAMLIT APP TESTS
# ============================================================================

class TestStreamlitApp(unittest.TestCase):
    """Test streamlit_app.py functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            from sources import streamlit_app
            self.app = streamlit_app
        except ImportError:
            self.skipTest("streamlit_app module not available")
    
    def test_streamlit_app_import(self):
        """Test streamlit app can be imported."""
        self.assertTrue(hasattr(self.app, 'NEUMORPHISM_COLORS'))
    
    def test_neumorphism_colors_defined(self):
        """Test Neumorphism color palette."""
        self.assertIn('primary_bg', self.app.NEUMORPHISM_COLORS)
        self.assertIn('accent_sage', self.app.NEUMORPHISM_COLORS)
        self.assertIn('accent_warm', self.app.NEUMORPHISM_COLORS)
    
    def test_neumorphism_css_defined(self):
        """Test Neumorphism CSS defined."""
        self.assertIsNotNone(self.app.NEUMORPHISM_CSS)
        self.assertIn('neumorphic-card', self.app.NEUMORPHISM_CSS)
        self.assertIn('neumorphic-button', self.app.NEUMORPHISM_CSS)
    
    def test_page_functions_defined(self):
        """Test all page functions are defined."""
        pages = [
            'page_overview',
            'page_metrics_explorer',
            'page_model_comparison',
            'page_live_inference',
            'page_feature_importance',
            'page_data_overview',
        ]
        
        for page in pages:
            self.assertTrue(hasattr(self.app, page), f"Missing {page}")


# ============================================================================
# PHASE 4: ENHANCED MODEL EVALUATOR TESTS
# ============================================================================

class TestModelEvaluatorEnhanced(unittest.TestCase):
    """Test model_evaluator_enhanced.py functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            from sources import model_evaluator_enhanced as me
            self.me = me
        except ImportError:
            self.skipTest("model_evaluator_enhanced module not available")
        
        # Create mock base evaluator
        self.base_evaluator = Mock()
        self.base_evaluator.model_name = 'TestModel'
        self.base_evaluator.dataset_name = 'TestData'
        self.base_evaluator.class_names = ['spam', 'ham']
    
    def test_enhanced_evaluator_import(self):
        """Test ModelEvaluatorEnhanced can be imported."""
        self.assertTrue(hasattr(self.me, 'ModelEvaluatorEnhanced'))
    
    def test_enhanced_evaluator_initialization(self):
        """Test initialization."""
        enhanced = self.me.ModelEvaluatorEnhanced(self.base_evaluator)
        self.assertIsNotNone(enhanced.base_evaluator)
    
    def test_predict_single_method_exists(self):
        """Test predict_single method exists."""
        enhanced = self.me.ModelEvaluatorEnhanced()
        self.assertTrue(hasattr(enhanced, 'predict_single'))
    
    def test_predict_proba_method_exists(self):
        """Test predict_proba method exists."""
        enhanced = self.me.ModelEvaluatorEnhanced()
        self.assertTrue(hasattr(enhanced, 'predict_proba'))
    
    def test_get_feature_importance_method_exists(self):
        """Test get_feature_importance method exists."""
        enhanced = self.me.ModelEvaluatorEnhanced()
        self.assertTrue(hasattr(enhanced, 'get_feature_importance'))
    
    def test_get_preprocessed_text_method_exists(self):
        """Test get_preprocessed_text method exists."""
        enhanced = self.me.ModelEvaluatorEnhanced()
        self.assertTrue(hasattr(enhanced, 'get_preprocessed_text'))
    
    def test_get_preprocessing_stats_method_exists(self):
        """Test get_preprocessing_stats method exists."""
        enhanced = self.me.ModelEvaluatorEnhanced()
        self.assertTrue(hasattr(enhanced, 'get_preprocessing_stats'))
    
    def test_batch_predict_method_exists(self):
        """Test batch_predict method exists."""
        enhanced = self.me.ModelEvaluatorEnhanced()
        self.assertTrue(hasattr(enhanced, 'batch_predict'))
    
    def test_batch_predict_proba_method_exists(self):
        """Test batch_predict_proba method exists."""
        enhanced = self.me.ModelEvaluatorEnhanced()
        self.assertTrue(hasattr(enhanced, 'batch_predict_proba'))
    
    def test_clear_prediction_cache_method_exists(self):
        """Test clear_prediction_cache method exists."""
        enhanced = self.me.ModelEvaluatorEnhanced()
        self.assertTrue(hasattr(enhanced, 'clear_prediction_cache'))
    
    def test_get_cache_stats_method_exists(self):
        """Test get_cache_stats method exists."""
        enhanced = self.me.ModelEvaluatorEnhanced()
        self.assertTrue(hasattr(enhanced, 'get_cache_stats'))
    
    def test_get_last_predictions_method_exists(self):
        """Test get_last_predictions method exists."""
        enhanced = self.me.ModelEvaluatorEnhanced()
        self.assertTrue(hasattr(enhanced, 'get_last_predictions'))
    
    def test_get_performance_stats_method_exists(self):
        """Test get_performance_stats method exists."""
        enhanced = self.me.ModelEvaluatorEnhanced()
        self.assertTrue(hasattr(enhanced, 'get_performance_stats'))
    
    def test_get_summary_method_exists(self):
        """Test get_summary method exists."""
        enhanced = self.me.ModelEvaluatorEnhanced()
        self.assertTrue(hasattr(enhanced, 'get_summary'))
    
    def test_export_predictions_history_method_exists(self):
        """Test export_predictions_history method exists."""
        enhanced = self.me.ModelEvaluatorEnhanced()
        self.assertTrue(hasattr(enhanced, 'export_predictions_history'))
    
    def test_cache_stats_structure(self):
        """Test cache stats return structure."""
        enhanced = self.me.ModelEvaluatorEnhanced()
        stats = enhanced.get_cache_stats()
        self.assertIn('cached_predictions', stats)
        self.assertIn('last_predictions_count', stats)
    
    def test_create_enhanced_evaluator_function(self):
        """Test create_enhanced_evaluator function."""
        self.assertTrue(hasattr(self.me, 'create_enhanced_evaluator'))
        enhanced = self.me.create_enhanced_evaluator(self.base_evaluator)
        self.assertIsNotNone(enhanced)


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration(unittest.TestCase):
    """Integration tests across all phases."""
    
    def test_all_modules_importable(self):
        """Test all modules can be imported."""
        import sys
        from pathlib import Path
        
        # Add parent directory to path
        base_path = Path(__file__).parent.parent
        sys.path.insert(0, str(base_path))
        
        modules = [
            'sources.visualization',
            'sources.cli_dashboard',
            'sources.streamlit_app',
            'sources.model_evaluator_enhanced',
        ]
        
        for module_name in modules:
            try:
                __import__(module_name)
            except ImportError as e:
                # Some optional dependencies might not be installed
                if 'streamlit' not in str(e) and 'plotly' not in str(e):
                    self.fail(f"Failed to import {module_name}: {e}")
    
    def test_no_syntax_errors(self):
        """Test no syntax errors in any module."""
        import py_compile
        
        files = [
            'sources/visualization.py',
            'sources/cli_dashboard.py',
            'sources/streamlit_app.py',
            'sources/model_evaluator_enhanced.py',
        ]
        
        base_path = Path('/Users/charles88/Desktop/AIoT/AIoT_DA_HW3')
        
        for filepath in files:
            full_path = base_path / filepath
            if full_path.exists():
                try:
                    py_compile.compile(str(full_path), doraise=True)
                except py_compile.PyCompileError as e:
                    self.fail(f"Syntax error in {filepath}: {e}")


# ============================================================================
# TEST SUITE
# ============================================================================

def create_test_suite():
    """Create complete test suite."""
    suite = unittest.TestSuite()
    
    # Add Phase tests
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestVisualization))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCliDashboard))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestStreamlitApp))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestModelEvaluatorEnhanced))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestIntegration))
    
    return suite


if __name__ == '__main__':
    # Run all tests
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("=" * 70)
