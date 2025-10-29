"""Theme management system for Streamlit application.

This module provides a theme manager for handling light and dark modes
across the Streamlit application. It includes theme configuration,
switching, and color management.

Module contents:
    - Theme: Data class for theme configuration
    - ThemeManager: Main theme manager class
    - LIGHT_THEME: Light theme preset
    - DARK_THEME: Dark theme preset
"""

from dataclasses import dataclass
from typing import Dict, Literal
import streamlit as st


@dataclass
class Theme:
    """Theme configuration data class.
    
    Attributes:
        name: Theme identifier (e.g., 'light', 'dark')
        primary_color: Primary brand color (hex)
        secondary_color: Secondary color (hex)
        background_color: Main background color (hex)
        surface_color: Surface/card background color (hex)
        text_color: Primary text color (hex)
        text_secondary_color: Secondary text color (hex)
        border_color: Border color (hex)
        success_color: Success state color (hex)
        warning_color: Warning state color (hex)
        error_color: Error state color (hex)
        info_color: Info state color (hex)
    """
    name: str
    primary_color: str
    secondary_color: str
    background_color: str
    surface_color: str
    text_color: str
    text_secondary_color: str
    border_color: str
    success_color: str
    warning_color: str
    error_color: str
    info_color: str
    
    def to_dict(self) -> Dict[str, str]:
        """Convert theme to dictionary.
        
        Returns:
            Dictionary of theme colors
        """
        return {
            'name': self.name,
            'primary_color': self.primary_color,
            'secondary_color': self.secondary_color,
            'background_color': self.background_color,
            'surface_color': self.surface_color,
            'text_color': self.text_color,
            'text_secondary_color': self.text_secondary_color,
            'border_color': self.border_color,
            'success_color': self.success_color,
            'warning_color': self.warning_color,
            'error_color': self.error_color,
            'info_color': self.info_color,
        }


# Light theme configuration
LIGHT_THEME = Theme(
    name='light',
    primary_color='#3498db',           # Blue
    secondary_color='#e74c3c',          # Red
    background_color='#f5f5f5',         # Light gray
    surface_color='#ffffff',            # White
    text_color='#2c3e50',               # Dark gray
    text_secondary_color='#7f8c8d',     # Medium gray
    border_color='#ecf0f1',             # Light border
    success_color='#2ecc71',            # Green
    warning_color='#f39c12',            # Orange
    error_color='#e74c3c',              # Red
    info_color='#3498db',               # Blue
)

# Dark theme configuration
DARK_THEME = Theme(
    name='dark',
    primary_color='#3498db',           # Blue (same as light)
    secondary_color='#e74c3c',          # Red (same as light)
    background_color='#1a1a1a',         # Very dark gray
    surface_color='#2d2d2d',            # Dark gray
    text_color='#ecf0f1',               # Light gray
    text_secondary_color='#95a5a6',     # Medium gray
    border_color='#404040',             # Dark border
    success_color='#2ecc71',            # Green
    warning_color='#f39c12',            # Orange
    error_color='#e74c3c',              # Red
    info_color='#3498db',               # Blue
)


class ThemeManager:
    """Manage application themes and colors.
    
    This class handles theme switching, color management, and
    persistence of user preferences.
    """
    
    def __init__(self):
        """Initialize the theme manager."""
        self._themes = {
            'light': LIGHT_THEME,
            'dark': DARK_THEME,
        }
        self._current_theme: Literal['light', 'dark'] = 'light'
    
    def get_theme(self) -> Theme:
        """Get the current theme.
        
        Returns:
            Current theme object
        """
        if 'theme' not in st.session_state:
            st.session_state.theme = 'light'
        
        theme_name = st.session_state.theme
        return self._themes.get(theme_name, LIGHT_THEME)
    
    def set_theme(self, theme_name: Literal['light', 'dark']) -> None:
        """Set the current theme.
        
        Args:
            theme_name: Theme name ('light' or 'dark')
        """
        if theme_name not in self._themes:
            raise ValueError(f"Unknown theme: {theme_name}")
        
        st.session_state.theme = theme_name
        self._current_theme = theme_name
    
    def get_colors(self) -> Dict[str, str]:
        """Get current theme colors as dictionary.
        
        Returns:
            Dictionary of theme colors
        """
        return self.get_theme().to_dict()
    
    def toggle_theme(self) -> str:
        """Toggle between light and dark theme.
        
        Returns:
            New theme name
        """
        current = st.session_state.get('theme', 'light')
        new_theme = 'dark' if current == 'light' else 'light'
        self.set_theme(new_theme)
        return new_theme
    
    def get_css_variables(self) -> str:
        """Generate CSS variables string for current theme.
        
        Returns:
            CSS string with theme variables
        """
        colors = self.get_colors()
        
        css_vars = f"""
        :root {{
            --primary-color: {colors['primary_color']};
            --secondary-color: {colors['secondary_color']};
            --background-color: {colors['background_color']};
            --surface-color: {colors['surface_color']};
            --text-color: {colors['text_color']};
            --text-secondary-color: {colors['text_secondary_color']};
            --border-color: {colors['border_color']};
            --success-color: {colors['success_color']};
            --warning-color: {colors['warning_color']};
            --error-color: {colors['error_color']};
            --info-color: {colors['info_color']};
        }}
        """
        return css_vars
    
    def get_available_themes(self) -> list:
        """Get list of available theme names.
        
        Returns:
            List of theme names
        """
        return list(self._themes.keys())
    
    def get_theme_name(self) -> str:
        """Get current theme name.
        
        Returns:
            Current theme name
        """
        return st.session_state.get('theme', 'light')


def get_theme_manager() -> ThemeManager:
    """Get or create the theme manager singleton.
    
    Returns:
        ThemeManager instance
    """
    if 'theme_manager' not in st.session_state:
        st.session_state.theme_manager = ThemeManager()
    return st.session_state.theme_manager
