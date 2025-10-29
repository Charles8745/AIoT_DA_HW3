"""Enhanced navigation component for Streamlit application.

This module provides a flexible navigation system with active page
tracking and visual highlighting.

Module contents:
    - NavigationItem: Single navigation item data class
    - SidebarNavigator: Main navigation component
"""

from dataclasses import dataclass
from typing import Dict, Optional, Callable, Any
import streamlit as st


@dataclass
class NavigationItem:
    """Single navigation menu item.
    
    Attributes:
        label: Display label for the menu item
        icon: Emoji or icon for visual identification
        page_key: Unique key to identify this page
        page_func: Callable function to render the page
        section: Optional section/category for grouping
    """
    label: str
    icon: str
    page_key: str
    page_func: Callable
    section: Optional[str] = None
    
    def __repr__(self) -> str:
        """String representation of navigation item."""
        return f"{self.icon} {self.label}"


class SidebarNavigator:
    """Manage sidebar navigation with active page highlighting.
    
    This component handles page switching, active state tracking,
    and visual navigation hierarchy.
    """
    
    def __init__(self):
        """Initialize the sidebar navigator."""
        self.items: Dict[str, NavigationItem] = {}
        self.sections: Dict[str, list] = {}
        self._init_session_state()
    
    def _init_session_state(self) -> None:
        """Initialize session state for navigation."""
        if 'active_page' not in st.session_state:
            st.session_state.active_page = None
    
    def add_item(self, item: NavigationItem) -> None:
        """Add a navigation item.
        
        Args:
            item: NavigationItem to add
        """
        self.items[item.page_key] = item
        
        # Add to section
        section = item.section or 'Main'
        if section not in self.sections:
            self.sections[section] = []
        self.sections[section].append(item.page_key)
    
    def add_items(self, items: list) -> None:
        """Add multiple navigation items.
        
        Args:
            items: List of NavigationItem objects
        """
        for item in items:
            self.add_item(item)
    
    def get_active_page(self) -> Optional[str]:
        """Get the currently active page key.
        
        Returns:
            Active page key or None
        """
        return st.session_state.get('active_page')
    
    def set_active_page(self, page_key: str) -> None:
        """Set the active page.
        
        Args:
            page_key: Key of the page to activate
        """
        if page_key not in self.items:
            raise ValueError(f"Unknown page: {page_key}")
        
        st.session_state.active_page = page_key
    
    def render(self) -> None:
        """Render the sidebar navigation.
        
        Displays navigation menu grouped by section with
        visual highlighting for active page.
        """
        st.sidebar.markdown("### 🎯 Navigation")
        st.sidebar.markdown("---")
        
        # Group and display sections
        for section in self.sections:
            # Section header
            if section != 'Main':
                st.sidebar.markdown(f"#### {section}")
            
            # Items in section
            for page_key in self.sections[section]:
                item = self.items[page_key]
                is_active = st.session_state.get('active_page') == page_key
                
                # Create button style based on active state
                button_style = "👉 " if is_active else "   "
                label = f"{button_style}{item.icon} {item.label}"
                
                # Highlight active item
                if is_active:
                    st.sidebar.markdown(
                        f"<div style='background-color: rgba(52, 152, 219, 0.1); "
                        f"padding: 8px; border-radius: 4px; border-left: 3px solid #3498db;'>"
                        f"<b>{label}</b></div>",
                        unsafe_allow_html=True
                    )
                else:
                    if st.sidebar.button(label, key=f"nav_{page_key}", use_container_width=True):
                        self.set_active_page(page_key)
            
            st.sidebar.markdown("---")
    
    def render_active_page(self) -> bool:
        """Render the currently active page.
        
        Returns:
            True if a page was rendered, False otherwise
        """
        active_key = self.get_active_page()
        
        if not active_key or active_key not in self.items:
            return False
        
        item = self.items[active_key]
        item.page_func()
        return True
    
    def get_page_function(self, page_key: str) -> Optional[Callable]:
        """Get the page function for a key.
        
        Args:
            page_key: Key of the page
        
        Returns:
            Page rendering function or None
        """
        item = self.items.get(page_key)
        return item.page_func if item else None
    
    def get_all_pages(self) -> Dict[str, NavigationItem]:
        """Get all registered pages.
        
        Returns:
            Dictionary of all navigation items
        """
        return self.items.copy()
    
    def get_sections_summary(self) -> Dict[str, list]:
        """Get summary of sections and their items.
        
        Returns:
            Dictionary mapping sections to list of page keys
        """
        return self.sections.copy()


def init_navigator() -> SidebarNavigator:
    """Initialize and return the sidebar navigator singleton.
    
    Returns:
        SidebarNavigator instance
    """
    if 'sidebar_navigator' not in st.session_state:
        st.session_state.sidebar_navigator = SidebarNavigator()
    return st.session_state.sidebar_navigator
