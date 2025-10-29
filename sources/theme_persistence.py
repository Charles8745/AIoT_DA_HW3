"""Theme persistence system for browser and system preferences.

This module handles persisting theme preferences across sessions
and detecting system color scheme preferences.

Module contents:
    - ThemePersistence: Theme persistence manager
    - detect_system_theme: Detect system color scheme preference
"""

import streamlit as st
from typing import Literal


class ThemePersistence:
    """Handle theme persistence across sessions.
    
    Uses session state to store theme preferences and
    integrates with browser localStorage (via JavaScript).
    """
    
    def __init__(self):
        """Initialize theme persistence."""
        self._init_session_state()
    
    def _init_session_state(self) -> None:
        """Initialize session state for theme persistence."""
        if 'theme' not in st.session_state:
            # Try to detect system preference
            system_theme = self.detect_system_preference()
            st.session_state.theme = system_theme
        
        if 'theme_persistence_initialized' not in st.session_state:
            st.session_state.theme_persistence_initialized = True
    
    @staticmethod
    def detect_system_preference() -> Literal['light', 'dark']:
        """Detect system color scheme preference.
        
        Returns:
            'light' or 'dark' based on system preference
        """
        # Default to light if we can't detect
        # In a production app, this would use JavaScript to detect
        # navigator.mediaQueryList('(prefers-color-scheme: dark)').matches
        return 'light'
    
    def save_preference(self, theme: Literal['light', 'dark']) -> None:
        """Save theme preference to session state.
        
        Args:
            theme: Theme name to save ('light' or 'dark')
        """
        st.session_state.theme = theme
    
    def get_preference(self) -> Literal['light', 'dark']:
        """Get saved theme preference.
        
        Returns:
            Current theme preference
        """
        return st.session_state.get('theme', 'light')
    
    def inject_persistence_script(self) -> str:
        """Generate JavaScript code for localStorage persistence.
        
        This script should be injected into the page to persist
        theme choice in browser localStorage.
        
        Returns:
            JavaScript code as string
        """
        script = """
        <script>
            // Save theme preference to localStorage when changed
            function saveThemePreference(theme) {
                localStorage.setItem('app_theme', theme);
            }
            
            // Load theme preference from localStorage on page load
            function loadThemePreference() {
                const saved = localStorage.getItem('app_theme');
                if (saved) {
                    return saved;
                }
                // Fall back to system preference
                if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                    return 'dark';
                }
                return 'light';
            }
            
            // Export functions for Streamlit integration
            window.themeUtils = {
                save: saveThemePreference,
                load: loadThemePreference,
            };
        </script>
        """
        return script
    
    @staticmethod
    def get_persistence_info() -> dict:
        """Get information about current persistence.
        
        Returns:
            Dictionary with persistence information
        """
        return {
            'current_theme': st.session_state.get('theme', 'light'),
            'storage_backend': 'session_state',
            'has_localStorage': True,  # Should check with JS
            'system_preference_detected': False,
        }


def init_theme_persistence() -> ThemePersistence:
    """Initialize and return theme persistence manager.
    
    Returns:
        ThemePersistence instance
    """
    if 'theme_persistence' not in st.session_state:
        st.session_state.theme_persistence = ThemePersistence()
    return st.session_state.theme_persistence
