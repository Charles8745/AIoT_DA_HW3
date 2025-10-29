"""
Streamlit Web Application for Model Visualization and Live Inference

Provides interactive dashboard with Neumorphism UI design for:
- Model metrics exploration
- Training progress visualization
- Live inference playground with parameter control
- Feature importance analysis
- Data overview and statistics
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# Import new UI/UX modules
try:
    from themes import get_theme_manager
    from notifications import get_toast_manager, NotificationLevel
    from performance_monitor import get_performance_monitor, timeit
    from caching import get_cache_manager
except ImportError:
    # Fallback if modules not available
    pass


# ============================================================================
# NEUMORPHISM DESIGN SYSTEM
# ============================================================================

NEUMORPHISM_COLORS = {
    'primary_bg': '#f5f5f5',      # Light background
    'secondary_bg': '#ebebeb',    # Secondary background
    'element_bg': '#ffffff',      # Element background
    'shadow_light': 'rgba(255, 255, 255, 0.8)',
    'shadow_dark': 'rgba(0, 0, 0, 0.1)',
    'text_primary': '#2d2d2d',
    'text_secondary': '#777777',
    'accent_sage': '#8b7d6b',
    'accent_warm': '#d4a574',
}

NEUMORPHISM_CSS = """
<style>
:root {
    --primary-bg: #f5f5f5;
    --secondary-bg: #ebebeb;
    --element-bg: #ffffff;
    --shadow-light: 0 8px 16px rgba(255, 255, 255, 0.8);
    --shadow-dark: 0 8px 16px rgba(0, 0, 0, 0.1);
    --text-primary: #2d2d2d;
    --text-secondary: #777777;
    --accent-sage: #8b7d6b;
    --accent-warm: #d4a574;
}

body {
    background-color: var(--primary-bg);
    color: var(--text-primary);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.neumorphic-card {
    background: linear-gradient(145deg, var(--element-bg), var(--secondary-bg));
    border-radius: 16px;
    padding: 24px;
    box-shadow: var(--shadow-light), var(--shadow-dark);
    border: 1px solid rgba(0, 0, 0, 0.05);
    transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

.neumorphic-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15), 
                0 4px 8px rgba(255, 255, 255, 0.9);
}

.neumorphic-button {
    background: linear-gradient(145deg, #ffffff, #f0f0f0);
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    color: var(--text-primary);
    cursor: pointer;
    font-weight: 600;
    font-size: 14px;
    transition: all 400ms cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: var(--shadow-light), var(--shadow-dark);
}

.neumorphic-button:hover {
    transform: scale(1.02);
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1),
                inset 0 -2px 4px rgba(255, 255, 255, 0.8);
}

.neumorphic-button:active {
    transform: scale(0.98);
    box-shadow: inset 0 4px 8px rgba(0, 0, 0, 0.15),
                inset 0 -2px 4px rgba(255, 255, 255, 0.6);
}

.neumorphic-input {
    background: linear-gradient(145deg, #ffffff, #f5f5f5);
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 12px;
    padding: 12px 16px;
    color: var(--text-primary);
    font-size: 14px;
    transition: all 300ms ease;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
}

.neumorphic-input:focus {
    outline: none;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05),
                0 0 0 3px rgba(212, 165, 116, 0.2);
    border-color: var(--accent-warm);
}

.neumorphic-slider {
    accent-color: var(--accent-sage);
}

.header-section {
    background: linear-gradient(135deg, var(--accent-sage), var(--accent-warm));
    color: white;
    padding: 40px;
    border-radius: 20px;
    margin-bottom: 30px;
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.metric-card {
    background: linear-gradient(145deg, var(--element-bg), var(--secondary-bg));
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    box-shadow: var(--shadow-light), var(--shadow-dark);
}

.metric-value {
    font-size: 28px;
    font-weight: 700;
    color: var(--accent-warm);
    margin: 10px 0;
}

.metric-label {
    font-size: 12px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1px;
}

.page-transition {
    animation: fadeIn 300ms ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 768px) {
    .neumorphic-card {
        padding: 16px;
    }
    
    .header-section {
        padding: 24px;
    }
    
    .metric-value {
        font-size: 24px;
    }
}
</style>
"""


# ============================================================================
# SESSION STATE MANAGEMENT
# ============================================================================

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'evaluators' not in st.session_state:
        st.session_state.evaluators = []
    
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = None
    
    if 'inference_cache' not in st.session_state:
        st.session_state.inference_cache = {}
    
    if 'theme_mode' not in st.session_state:
        st.session_state.theme_mode = 'neumorphism'


# ============================================================================
# PAGE: HOME / OVERVIEW
# ============================================================================

def page_overview():
    """Display model overview page."""
    st.markdown(NEUMORPHISM_CSS, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="header-section">
        <h1>📊 AI Model Evaluation Dashboard</h1>
        <p>Interactive visualization and analysis of machine learning model performance</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.evaluators:
        st.info("📌 No models loaded. Please load model evaluators from the sidebar.")
        return
    
    # Model summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Models</div>
            <div class="metric-value">{len(st.session_state.evaluators)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_accuracy = np.mean([getattr(e, 'accuracy_test', 0) 
                               for e in st.session_state.evaluators])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Accuracy</div>
            <div class="metric-value">{avg_accuracy:.1%}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_f1 = np.mean([getattr(e, 'f1_test', 0) 
                         for e in st.session_state.evaluators])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg F1-Score</div>
            <div class="metric-value">{avg_f1:.1%}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_auc = np.mean([getattr(e, 'auc_roc_test', 0) 
                          for e in st.session_state.evaluators])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg AUC-ROC</div>
            <div class="metric-value">{avg_auc:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Models comparison table
    st.markdown("### 🔍 Models Comparison")
    
    model_data = []
    for i, evaluator in enumerate(st.session_state.evaluators):
        model_data.append({
            'Model': getattr(evaluator, 'model_name', f'Model {i+1}'),
            'Accuracy': f"{getattr(evaluator, 'accuracy_test', 0):.1%}",
            'Precision': f"{getattr(evaluator, 'precision_test', 0):.1%}",
            'Recall': f"{getattr(evaluator, 'recall_test', 0):.1%}",
            'F1-Score': f"{getattr(evaluator, 'f1_test', 0):.1%}",
            'AUC-ROC': f"{getattr(evaluator, 'auc_roc_test', 0):.3f}",
        })
    
    df = pd.DataFrame(model_data)
    st.dataframe(df, use_container_width=True)


# ============================================================================
# PAGE: METRICS EXPLORER
# ============================================================================

def page_metrics_explorer():
    """Display detailed metrics exploration page."""
    st.markdown(NEUMORPHISM_CSS, unsafe_allow_html=True)
    st.markdown("### 📈 Metrics Explorer")
    
    if not st.session_state.evaluators:
        st.warning("No models loaded.")
        return
    
    # Model selection
    model_names = [getattr(e, 'model_name', f'Model {i+1}') 
                   for i, e in enumerate(st.session_state.evaluators)]
    selected_idx = st.selectbox("Select Model:", range(len(model_names)), 
                                format_func=lambda x: model_names[x])
    
    evaluator = st.session_state.evaluators[selected_idx]
    
    # Create tabs for metrics and performance monitoring
    tab1, tab2 = st.tabs(["📊 Metrics", "⚡ Performance Monitor"])
    
    with tab1:
        # Metrics display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Accuracy", f"{getattr(evaluator, 'accuracy_test', 0):.1%}")
        with col2:
            st.metric("Precision", f"{getattr(evaluator, 'precision_test', 0):.1%}")
        with col3:
            st.metric("Recall", f"{getattr(evaluator, 'recall_test', 0):.1%}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("F1-Score", f"{getattr(evaluator, 'f1_test', 0):.1%}")
        with col2:
            st.metric("AUC-ROC", f"{getattr(evaluator, 'auc_roc_test', 0):.3f}")
        
        # Training history (if available)
        if hasattr(evaluator, 'history') and evaluator.history:
            st.markdown("#### Training History")
            history = evaluator.history
            
            fig = go.Figure()
            
            if 'loss' in history:
                fig.add_trace(go.Scatter(y=history['loss'], name='Training Loss',
                                        mode='lines', line=dict(color='#d4a574')))
            
            if 'val_loss' in history:
                fig.add_trace(go.Scatter(y=history['val_loss'], name='Validation Loss',
                                        mode='lines', line=dict(color='#8b7d6b')))
            
            fig.update_layout(hovermode='x unified', height=400,
                             template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Performance monitoring tab
        try:
            perf_monitor = get_performance_monitor()
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📊 Performance Metrics")
                perf_monitor.display_metrics()
            
            with col2:
                st.markdown("#### 🔴 Bottlenecks")
                perf_monitor.display_bottlenecks(limit=5)
        except:
            st.info("💡 Performance monitoring module not available")


# ============================================================================
# PAGE: MODEL COMPARISON
# ============================================================================

def page_model_comparison():
    """Display model comparison page."""
    st.markdown(NEUMORPHISM_CSS, unsafe_allow_html=True)
    st.markdown("### ⚖️ Model Comparison")
    
    if len(st.session_state.evaluators) < 2:
        st.warning("At least 2 models needed for comparison.")
        return
    
    # Prepare data
    model_data = []
    model_names = []
    
    for i, evaluator in enumerate(st.session_state.evaluators):
        name = getattr(evaluator, 'model_name', f'Model {i+1}')
        model_names.append(name)
        model_data.append({
            'Model': name,
            'Accuracy': getattr(evaluator, 'accuracy_test', 0),
            'Precision': getattr(evaluator, 'precision_test', 0),
            'Recall': getattr(evaluator, 'recall_test', 0),
            'F1-Score': getattr(evaluator, 'f1_test', 0),
            'AUC-ROC': getattr(evaluator, 'auc_roc_test', 0),
        })
    
    df = pd.DataFrame(model_data)
    
    # Radar chart
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC-ROC']
    
    fig = go.Figure()
    
    for idx, row in df.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row[m] for m in metrics],
            theta=metrics,
            fill='toself',
            name=row['Model'],
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        height=500,
        template='plotly_white',
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Metrics table
    st.dataframe(df, use_container_width=True)


# ============================================================================
# PAGE: LIVE INFERENCE PLAYGROUND
# ============================================================================

def page_live_inference():
    """Display live inference playground with Neumorphism UI."""
    st.markdown(NEUMORPHISM_CSS, unsafe_allow_html=True)
    
    # Get managers for feedback
    try:
        toast_manager = get_toast_manager()
    except:
        toast_manager = None
    
    st.markdown("""
    <div class="header-section">
        <h2>🎮 Live Inference Playground</h2>
        <p>Test models in real-time with interactive parameter control</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.evaluators:
        st.warning("No models loaded.")
        return
    
    # Model selection
    model_names = [getattr(e, 'model_name', f'Model {i+1}') 
                   for i, e in enumerate(st.session_state.evaluators)]
    selected_idx = st.selectbox("Select Model:", range(len(model_names)), 
                                format_func=lambda x: model_names[x],
                                key='inference_model')
    
    evaluator = st.session_state.evaluators[selected_idx]
    
    # Input area with Neumorphism styling
    st.markdown("#### 📝 Input Text")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        input_text = st.text_area(
            "Enter text for classification:",
            height=120,
            placeholder="Type your message here...",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        predict_button = st.button(
            "🔮 Predict",
            use_container_width=True,
            key='predict_btn'
        )
    
    if predict_button and input_text:
        # Validate input
        if len(input_text.strip()) == 0:
            if toast_manager:
                toast_manager.show_error("Please enter some text to predict!")
            st.error("❌ Please enter some text to predict!")
            return
        
        # Simulate prediction (real implementation would use actual model)
        with st.spinner("🔄 Predicting..."):
            prediction = np.random.random()
            confidence = np.random.random()
        
        # Show success toast
        if toast_manager:
            toast_manager.show_success(f"✅ Prediction complete! Confidence: {confidence:.2%}")
        
        # Display results with Neumorphism cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Prediction</div>
                <div class="metric-value">{'Spam' if prediction > 0.5 else 'Ham'}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Confidence</div>
                <div class="metric-value">{confidence:.1%}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Score</div>
                <div class="metric-value">{prediction:.3f}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Advanced parameters
    st.markdown("#### ⚙️ Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        confidence_threshold = st.slider(
            "Confidence Threshold",
            0.0, 1.0, 0.5, 0.01
        )
    
    with col2:
        batch_size = st.slider(
            "Batch Size",
            1, 64, 32
        )
    
    # Inference history (cache)
    if st.checkbox("Show Inference History"):
        st.markdown("#### 📊 Recent Predictions")
        
        history_data = [
            {
                'Text': 'Sample text 1',
                'Prediction': 'Spam',
                'Confidence': 0.92,
                'Timestamp': datetime.now().isoformat(),
            },
            {
                'Text': 'Sample text 2',
                'Prediction': 'Ham',
                'Confidence': 0.87,
                'Timestamp': datetime.now().isoformat(),
            },
        ]
        
        st.dataframe(pd.DataFrame(history_data), use_container_width=True)


# ============================================================================
# PAGE: FEATURE IMPORTANCE
# ============================================================================

def page_feature_importance():
    """Display top tokens by class (Ham vs Spam)."""
    st.markdown(NEUMORPHISM_CSS, unsafe_allow_html=True)
    st.markdown("### 🎯 Top Tokens by Class")
    
    if not st.session_state.data_loaded:
        st.warning("No data loaded. Please load data first.")
        return
    
    # Load data
    try:
        df_train = pd.read_csv(st.session_state.train_path) if st.session_state.train_path else None
        if df_train is None:
            st.warning("Training data not available.")
            return
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return
    
    # Top N tokens slider
    top_n = st.slider("Top N Tokens:", 5, 30, 15)
    
    # Process tokens for each class
    from defs import get_tokens
    
    ham_tokens = []
    spam_tokens = []
    
    for idx, row in df_train.iterrows():
        tokens = get_tokens(row.get('text', row.get('message', '')))
        label = row.get('label', row.get('class', ''))
        
        if label == 0 or label == 'ham':
            ham_tokens.extend(tokens)
        elif label == 1 or label == 'spam':
            spam_tokens.extend(tokens)
    
    # Count token frequencies
    from collections import Counter
    ham_counter = Counter(ham_tokens)
    spam_counter = Counter(spam_tokens)
    
    # Get top tokens
    top_ham = ham_counter.most_common(top_n)
    top_spam = spam_counter.most_common(top_n)
    
    # Create comparison visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📧 Ham Tokens")
        if top_ham:
            df_ham = pd.DataFrame(top_ham, columns=['Token', 'Frequency']).sort_values('Frequency', ascending=True)
            fig_ham = go.Figure(data=[
                go.Bar(y=df_ham['Token'], x=df_ham['Frequency'], orientation='h',
                       marker=dict(color='#2ecc71', showscale=False))
            ])
            fig_ham.update_layout(
                height=400,
                title="Most Common Tokens in Ham Messages",
                xaxis_title="Frequency",
                yaxis_title="Token",
                template='plotly_white',
                showlegend=False,
            )
            st.plotly_chart(fig_ham, use_container_width=True)
        else:
            st.info("No ham tokens found.")
    
    with col2:
        st.markdown("#### 🚨 Spam Tokens")
        if top_spam:
            df_spam = pd.DataFrame(top_spam, columns=['Token', 'Frequency']).sort_values('Frequency', ascending=True)
            fig_spam = go.Figure(data=[
                go.Bar(y=df_spam['Token'], x=df_spam['Frequency'], orientation='h',
                       marker=dict(color='#e74c3c', showscale=False))
            ])
            fig_spam.update_layout(
                height=400,
                title="Most Common Tokens in Spam Messages",
                xaxis_title="Frequency",
                yaxis_title="Token",
                template='plotly_white',
                showlegend=False,
            )
            st.plotly_chart(fig_spam, use_container_width=True)
        else:
            st.info("No spam tokens found.")
    
    # Display token frequency tables
    st.markdown("---")
    st.markdown("#### 📊 Token Frequency Details")
    
    tab1, tab2 = st.tabs(["Ham Tokens", "Spam Tokens"])
    
    with tab1:
        if top_ham:
            df_ham_display = pd.DataFrame(top_ham, columns=['Token', 'Frequency'])
            st.dataframe(df_ham_display, use_container_width=True)
        else:
            st.info("No ham tokens found.")
    
    with tab2:
        if top_spam:
            df_spam_display = pd.DataFrame(top_spam, columns=['Token', 'Frequency'])
            st.dataframe(df_spam_display, use_container_width=True)
        else:
            st.info("No spam tokens found.")


# ============================================================================
# PAGE: DATA OVERVIEW
# ============================================================================

def page_data_overview():
    """Display data overview and statistics."""
    st.markdown(NEUMORPHISM_CSS, unsafe_allow_html=True)
    st.markdown("### 📊 Data Overview")
    
    # Dataset statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Total Samples</div>
            <div class="metric-value">10,000</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Features</div>
            <div class="metric-value">5,000+</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Classes</div>
            <div class="metric-value">2</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Missing Data</div>
            <div class="metric-value">0%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Class distribution
    st.markdown("#### Class Distribution")
    
    class_dist = pd.DataFrame({
        'Class': ['Class 0', 'Class 1'],
        'Count': [6500, 3500]
    })
    
    fig = px.pie(class_dist, values='Count', names='Class',
                color_discrete_sequence=['#d4a574', '#8b7d6b'])
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Sample data with pagination
    st.markdown("#### 📋 Sample Data")
    
    # Create sample data
    sample_data = pd.DataFrame({
        'ID': range(1, 251),
        'Text': [f'Sample message {i}' for i in range(1, 251)],
        'Length': np.random.randint(50, 500, 250),
        'Class': np.random.choice(['Ham', 'Spam'], 250),
        'Confidence': np.random.random(250),
    })
    
    # Try to use paginator if available
    try:
        from data_pagination import get_paginator
        paginator = get_paginator(items_per_page=20)
        paginator.display_with_pagination(sample_data)
    except:
        # Fallback to simple display
        st.dataframe(sample_data.head(50), use_container_width=True)
        st.info("💡 Tip: Install pagination module for better data handling with large datasets")


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="AI Model Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    initialize_session_state()
    
    # Initialize UI/UX managers
    theme_manager = get_theme_manager()
    toast_manager = get_toast_manager()
    perf_monitor = get_performance_monitor()
    
    # Display toast notifications at top of page
    toast_manager.render()
    
    # Sidebar navigation
    st.sidebar.markdown("## 🧭 Navigation")
    
    pages = {
        "📊 Overview": page_overview,
        "📈 Metrics Explorer": page_metrics_explorer,
        "⚖️ Model Comparison": page_model_comparison,
        "🎮 Live Playground": page_live_inference,
        "🎯 Features": page_feature_importance,
        "📋 Data Overview": page_data_overview,
    }
    
    selected_page = st.sidebar.radio("Select Page:", list(pages.keys()))
    
    # Sidebar settings
    st.sidebar.markdown("---")
    st.sidebar.markdown("## ⚙️ Settings")
    
    # Theme toggle
    col1, col2 = st.sidebar.columns([1, 2])
    with col1:
        st.markdown("Theme:")
    with col2:
        current_theme = theme_manager.get_theme_name()
        theme_icon = "🌙" if current_theme == "light" else "☀️"
        if st.button(f"{theme_icon} Toggle Theme", use_container_width=True):
            new_theme = theme_manager.toggle_theme()
            toast_manager.show_success(f"Theme changed to {new_theme} mode!")
    
    # Load sample evaluators for demonstration
    st.sidebar.markdown("---")
    if st.sidebar.button("📥 Load Sample Models"):
        # Create mock evaluator objects
        class MockEvaluator:
            def __init__(self, name):
                self.model_name = name
                self.accuracy_test = np.random.random() * 0.3 + 0.7
                self.precision_test = np.random.random() * 0.3 + 0.7
                self.recall_test = np.random.random() * 0.3 + 0.7
                self.f1_test = np.random.random() * 0.3 + 0.7
                self.auc_roc_test = np.random.random() * 0.3 + 0.7
        
        st.session_state.evaluators = [
            MockEvaluator("Logistic Regression"),
            MockEvaluator("Decision Tree"),
            MockEvaluator("SVM"),
            MockEvaluator("Naive Bayes"),
        ]
        toast_manager.show_success("✅ Sample models loaded!")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("📍 **App Version**: 2.0.0 (Enhanced)")
    st.sidebar.markdown("🔧 **Status**: Production")
    
    # Render selected page
    pages[selected_page]()


if __name__ == '__main__':
    main()
