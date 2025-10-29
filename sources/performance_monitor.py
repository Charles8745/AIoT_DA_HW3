"""Performance monitoring and profiling utilities.

This module provides performance monitoring capabilities including
function timing, bottleneck detection, and metrics reporting.

Module contents:
    - PerformanceMonitor: Main performance monitoring class
    - timeit: Decorator for function timing
"""

import streamlit as st
from functools import wraps
from typing import Callable, Dict, Any, List
from datetime import datetime
import time


class PerformanceMetrics:
    """Store performance metrics for a function call.
    
    Attributes:
        function_name: Name of the function
        execution_time_ms: Execution time in milliseconds
        timestamp: When the function was called
        status: 'success' or 'error'
        memory_used: Memory used (if available)
    """
    
    def __init__(self, function_name: str):
        """Initialize metrics.
        
        Args:
            function_name: Name of the function being monitored
        """
        self.function_name = function_name
        self.start_time = time.time()
        self.execution_time_ms = 0.0
        self.timestamp = datetime.now()
        self.status = 'pending'
        self.memory_used = 0
    
    def finish(self, status: str = 'success') -> None:
        """Mark monitoring as complete.
        
        Args:
            status: 'success' or 'error'
        """
        self.execution_time_ms = (time.time() - self.start_time) * 1000
        self.status = status
    
    def __repr__(self) -> str:
        """String representation."""
        return (f"PerformanceMetrics({self.function_name}, "
                f"{self.execution_time_ms:.2f}ms, {self.status})")


class PerformanceMonitor:
    """Monitor and analyze application performance."""
    
    def __init__(self):
        """Initialize performance monitor."""
        self._init_session_state()
    
    def _init_session_state(self) -> None:
        """Initialize session state for monitoring."""
        if 'performance_metrics' not in st.session_state:
            st.session_state.performance_metrics = []
        if 'performance_summary' not in st.session_state:
            st.session_state.performance_summary = {}
    
    def record_metric(self, metric: PerformanceMetrics) -> None:
        """Record a performance metric.
        
        Args:
            metric: PerformanceMetrics object to record
        """
        st.session_state.performance_metrics.append(metric)
        
        # Update summary
        if metric.function_name not in st.session_state.performance_summary:
            st.session_state.performance_summary[metric.function_name] = {
                'calls': 0,
                'total_time_ms': 0,
                'min_time_ms': float('inf'),
                'max_time_ms': 0,
                'avg_time_ms': 0,
            }
        
        summary = st.session_state.performance_summary[metric.function_name]
        summary['calls'] += 1
        summary['total_time_ms'] += metric.execution_time_ms
        summary['min_time_ms'] = min(summary['min_time_ms'], metric.execution_time_ms)
        summary['max_time_ms'] = max(summary['max_time_ms'], metric.execution_time_ms)
        summary['avg_time_ms'] = summary['total_time_ms'] / summary['calls']
    
    def get_metrics(self, function_name: str = None) -> List[PerformanceMetrics]:
        """Get recorded metrics.
        
        Args:
            function_name: Filter by function name (None = all)
        
        Returns:
            List of PerformanceMetrics
        """
        if function_name is None:
            return st.session_state.performance_metrics
        
        return [m for m in st.session_state.performance_metrics
                if m.function_name == function_name]
    
    def get_summary(self) -> Dict[str, Dict[str, float]]:
        """Get performance summary.
        
        Returns:
            Dictionary of performance summaries by function
        """
        return st.session_state.performance_summary.copy()
    
    def get_bottlenecks(self, limit: int = 5) -> List[tuple]:
        """Get slowest functions (bottlenecks).
        
        Args:
            limit: Number of bottlenecks to return
        
        Returns:
            List of (function_name, avg_time_ms) tuples
        """
        summary = self.get_summary()
        bottlenecks = sorted(
            [(name, data['avg_time_ms']) for name, data in summary.items()],
            key=lambda x: x[1],
            reverse=True
        )
        return bottlenecks[:limit]
    
    def clear_metrics(self) -> None:
        """Clear all recorded metrics."""
        st.session_state.performance_metrics = []
        st.session_state.performance_summary = {}
    
    def timeit(self, func: Callable) -> Callable:
        """Decorator for timing function execution.
        
        Args:
            func: Function to time
        
        Returns:
            Wrapped function
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            metric = PerformanceMetrics(func.__name__)
            
            try:
                result = func(*args, **kwargs)
                metric.finish('success')
                return result
            except Exception as e:
                metric.finish('error')
                raise
            finally:
                self.record_metric(metric)
        
        return wrapper
    
    def display_metrics(self, function_name: str = None) -> None:
        """Display performance metrics in Streamlit UI.
        
        Args:
            function_name: Show metrics for specific function
        """
        summary = self.get_summary()
        
        if not summary:
            st.info("No performance metrics recorded yet.")
            return
        
        if function_name:
            if function_name not in summary:
                st.warning(f"No metrics for {function_name}")
                return
            
            data = summary[function_name]
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Calls", data['calls'])
            with col2:
                st.metric("Avg Time (ms)", f"{data['avg_time_ms']:.2f}")
            with col3:
                st.metric("Min Time (ms)", f"{data['min_time_ms']:.2f}")
            with col4:
                st.metric("Max Time (ms)", f"{data['max_time_ms']:.2f}")
        else:
            # Display all functions
            import pandas as pd
            
            data = []
            for name, metrics in summary.items():
                data.append({
                    'Function': name,
                    'Calls': metrics['calls'],
                    'Avg (ms)': f"{metrics['avg_time_ms']:.2f}",
                    'Min (ms)': f"{metrics['min_time_ms']:.2f}",
                    'Max (ms)': f"{metrics['max_time_ms']:.2f}",
                    'Total (ms)': f"{metrics['total_time_ms']:.2f}",
                })
            
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
    
    def display_bottlenecks(self, limit: int = 5) -> None:
        """Display performance bottlenecks.
        
        Args:
            limit: Number of bottlenecks to show
        """
        bottlenecks = self.get_bottlenecks(limit)
        
        if not bottlenecks:
            st.info("No performance bottlenecks detected.")
            return
        
        st.markdown("### 🔴 Performance Bottlenecks")
        
        import pandas as pd
        
        data = []
        for func_name, avg_time in bottlenecks:
            status = "🟢 Good" if avg_time < 500 else "🟡 Slow" if avg_time < 1000 else "🔴 Very Slow"
            data.append({
                'Function': func_name,
                'Avg Time (ms)': f"{avg_time:.2f}",
                'Status': status,
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)


def get_performance_monitor() -> PerformanceMonitor:
    """Get or create the performance monitor singleton.
    
    Returns:
        PerformanceMonitor instance
    """
    if 'performance_monitor' not in st.session_state:
        st.session_state.performance_monitor = PerformanceMonitor()
    return st.session_state.performance_monitor


def timeit(func: Callable) -> Callable:
    """Decorator to time function execution.
    
    Args:
        func: Function to time
    
    Returns:
        Wrapped function
    """
    monitor = get_performance_monitor()
    return monitor.timeit(func)
