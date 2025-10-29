"""Toast notification system for user feedback.

This module provides a flexible toast notification system for displaying
success, error, warning, and info messages to users.

Module contents:
    - NotificationLevel: Enum for notification types
    - Toast: Toast notification class
    - ToastManager: Manages toast queue and display
    - show_toast: Convenience function for showing toasts
"""

from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, List
import streamlit as st


class NotificationLevel(Enum):
    """Notification severity levels."""
    SUCCESS = 'success'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'


@dataclass
class Toast:
    """Single toast notification.
    
    Attributes:
        message: Notification message text
        level: Severity level (success, info, warning, error)
        duration: Display duration in seconds (0 = permanent)
        timestamp: When the toast was created
        id: Unique identifier for the toast
    """
    message: str
    level: NotificationLevel
    duration: float = 3.0
    timestamp: datetime = None
    id: str = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.id is None:
            self.id = f"toast_{int(self.timestamp.timestamp() * 1000)}"
    
    def is_expired(self) -> bool:
        """Check if toast has expired.
        
        Returns:
            True if toast duration has elapsed, False otherwise
        """
        if self.duration == 0:  # Permanent
            return False
        
        elapsed = (datetime.now() - self.timestamp).total_seconds()
        return elapsed > self.duration
    
    def get_color(self) -> str:
        """Get color for this notification level.
        
        Returns:
            Hex color code
        """
        colors = {
            NotificationLevel.SUCCESS: '#2ecc71',  # Green
            NotificationLevel.INFO: '#3498db',     # Blue
            NotificationLevel.WARNING: '#f39c12',  # Orange
            NotificationLevel.ERROR: '#e74c3c',    # Red
        }
        return colors.get(self.level, '#3498db')
    
    def get_icon(self) -> str:
        """Get emoji icon for this notification level.
        
        Returns:
            Emoji string
        """
        icons = {
            NotificationLevel.SUCCESS: '✅',
            NotificationLevel.INFO: 'ℹ️',
            NotificationLevel.WARNING: '⚠️',
            NotificationLevel.ERROR: '❌',
        }
        return icons.get(self.level, 'ℹ️')


class ToastManager:
    """Manage toast notifications.
    
    Handles toast creation, queuing, and display.
    """
    
    def __init__(self):
        """Initialize toast manager."""
        self.toasts: List[Toast] = []
        self._init_session_state()
    
    def _init_session_state(self) -> None:
        """Initialize session state for toasts."""
        if 'toasts' not in st.session_state:
            st.session_state.toasts = []
    
    def add_toast(
        self,
        message: str,
        level: NotificationLevel = NotificationLevel.INFO,
        duration: float = 3.0
    ) -> Toast:
        """Add a toast notification.
        
        Args:
            message: Message text
            level: Notification level
            duration: Display duration in seconds (0 = permanent)
        
        Returns:
            Toast object that was added
        """
        toast = Toast(message=message, level=level, duration=duration)
        st.session_state.toasts.append(toast)
        return toast
    
    def show_success(self, message: str, duration: float = 3.0) -> Toast:
        """Show success toast.
        
        Args:
            message: Message text
            duration: Display duration in seconds
        
        Returns:
            Toast object
        """
        return self.add_toast(message, NotificationLevel.SUCCESS, duration)
    
    def show_error(self, message: str, duration: float = 5.0) -> Toast:
        """Show error toast.
        
        Args:
            message: Message text
            duration: Display duration in seconds
        
        Returns:
            Toast object
        """
        return self.add_toast(message, NotificationLevel.ERROR, duration)
    
    def show_warning(self, message: str, duration: float = 4.0) -> Toast:
        """Show warning toast.
        
        Args:
            message: Message text
            duration: Display duration in seconds
        
        Returns:
            Toast object
        """
        return self.add_toast(message, NotificationLevel.WARNING, duration)
    
    def show_info(self, message: str, duration: float = 3.0) -> Toast:
        """Show info toast.
        
        Args:
            message: Message text
            duration: Display duration in seconds
        
        Returns:
            Toast object
        """
        return self.add_toast(message, NotificationLevel.INFO, duration)
    
    def get_active_toasts(self) -> List[Toast]:
        """Get all active (non-expired) toasts.
        
        Returns:
            List of active Toast objects
        """
        active = [t for t in st.session_state.toasts if not t.is_expired()]
        st.session_state.toasts = active
        return active
    
    def clear_all(self) -> None:
        """Clear all toasts."""
        st.session_state.toasts = []
    
    def render(self) -> None:
        """Render all active toasts to the page.
        
        Should be called once at the top of each page.
        """
        toasts = self.get_active_toasts()
        
        if not toasts:
            return
        
        # Render toasts as a container
        with st.container():
            for toast in toasts:
                self._render_single_toast(toast)
    
    @staticmethod
    def _render_single_toast(toast: Toast) -> None:
        """Render a single toast.
        
        Args:
            toast: Toast to render
        """
        color = toast.get_color()
        icon = toast.get_icon()
        
        st.markdown(
            f"""
            <div style='
                background-color: {color}20;
                border-left: 4px solid {color};
                padding: 12px;
                border-radius: 4px;
                margin-bottom: 8px;
                display: flex;
                align-items: center;
                gap: 12px;
            '>
                <span style='font-size: 18px;'>{icon}</span>
                <span style='color: #2c3e50;'>{toast.message}</span>
            </div>
            """,
            unsafe_allow_html=True
        )


def get_toast_manager() -> ToastManager:
    """Get or create the toast manager singleton.
    
    Returns:
        ToastManager instance
    """
    if 'toast_manager' not in st.session_state:
        st.session_state.toast_manager = ToastManager()
    return st.session_state.toast_manager


def show_toast(
    message: str,
    level: NotificationLevel = NotificationLevel.INFO,
    duration: float = 3.0
) -> Toast:
    """Show a toast notification.
    
    Convenience function for showing toasts without explicit manager.
    
    Args:
        message: Message text
        level: Notification level
        duration: Display duration in seconds
    
    Returns:
        Toast object
    """
    manager = get_toast_manager()
    return manager.add_toast(message, level, duration)
