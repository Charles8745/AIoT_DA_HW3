"""Data pagination utilities for large datasets.

This module provides pagination components for efficiently displaying
large datasets without freezing the UI.

Module contents:
    - Paginator: Main pagination class
"""

from dataclasses import dataclass
from typing import List, Tuple
import streamlit as st
import pandas as pd


@dataclass
class PaginationState:
    """State of pagination.
    
    Attributes:
        page: Current page number (1-indexed)
        page_size: Number of items per page
        total_items: Total number of items
    """
    page: int = 1
    page_size: int = 50
    total_items: int = 0
    
    @property
    def total_pages(self) -> int:
        """Calculate total number of pages."""
        if self.page_size == 0:
            return 0
        return (self.total_items + self.page_size - 1) // self.page_size
    
    @property
    def start_idx(self) -> int:
        """Get start index for current page."""
        return (self.page - 1) * self.page_size
    
    @property
    def end_idx(self) -> int:
        """Get end index for current page."""
        return min(self.page * self.page_size, self.total_items)


class Paginator:
    """Paginate large datasets for efficient display."""
    
    def __init__(self, items_per_page: int = 50):
        """Initialize paginator.
        
        Args:
            items_per_page: Number of items to show per page
        """
        self.items_per_page = items_per_page
        self._init_session_state()
    
    def _init_session_state(self) -> None:
        """Initialize session state for pagination."""
        if 'pagination_state' not in st.session_state:
            st.session_state.pagination_state = PaginationState(
                page_size=self.items_per_page
            )
    
    def paginate(self, data: pd.DataFrame) -> pd.DataFrame:
        """Paginate dataframe and return current page.
        
        Args:
            data: DataFrame to paginate
        
        Returns:
            DataFrame for current page
        """
        state = st.session_state.pagination_state
        state.total_items = len(data)
        
        start = state.start_idx
        end = state.end_idx
        
        return data.iloc[start:end].reset_index(drop=True)
    
    def render_controls(self) -> None:
        """Render pagination controls."""
        state = st.session_state.pagination_state
        
        if state.total_pages <= 1:
            return
        
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
        
        with col1:
            if st.button("⬅️ Previous", use_container_width=True):
                if state.page > 1:
                    state.page -= 1
                    st.rerun()
        
        with col2:
            page_input = st.number_input(
                "Page",
                min_value=1,
                max_value=state.total_pages,
                value=state.page,
                step=1,
            )
            if page_input != state.page:
                state.page = page_input
                st.rerun()
        
        with col3:
            if st.button("Next ➡️", use_container_width=True):
                if state.page < state.total_pages:
                    state.page += 1
                    st.rerun()
        
        with col4:
            page_size = st.selectbox(
                "Per page",
                [10, 20, 50, 100],
                index=1,
            )
            if page_size != state.page_size:
                state.page_size = page_size
                state.page = 1
                st.rerun()
        
        with col5:
            st.markdown(
                f"📄 Page **{state.page}** of **{state.total_pages}** "
                f"({state.total_items} total items)",
                unsafe_allow_html=True
            )
    
    def display_with_pagination(self, data: pd.DataFrame) -> None:
        """Display dataframe with pagination controls.
        
        Args:
            data: DataFrame to display
        """
        state = st.session_state.pagination_state
        state.total_items = len(data)
        
        # Show controls
        self.render_controls()
        
        # Show current page
        st.markdown("---")
        paginated = self.paginate(data)
        st.dataframe(paginated, use_container_width=True)


def get_paginator(items_per_page: int = 50) -> Paginator:
    """Get or create paginator instance.
    
    Args:
        items_per_page: Items per page
    
    Returns:
        Paginator instance
    """
    if 'paginator' not in st.session_state:
        st.session_state.paginator = Paginator(items_per_page)
    return st.session_state.paginator
