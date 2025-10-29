"""Caching layer for performance optimization.

This module provides caching utilities to reduce redundant computations
and improve application performance.

Module contents:
    - CacheManager: Main cache management class
    - get_cache_manager: Singleton accessor
"""

import streamlit as st
from functools import wraps
from typing import Callable, Any, Dict
from datetime import datetime, timedelta
import hashlib
import json


class CacheManager:
    """Manage application caching with TTL support."""
    
    def __init__(self, default_ttl_minutes: int = 5):
        """Initialize cache manager.
        
        Args:
            default_ttl_minutes: Default time-to-live in minutes
        """
        self.default_ttl = timedelta(minutes=default_ttl_minutes)
        self._init_session_state()
    
    def _init_session_state(self) -> None:
        """Initialize session state for caching."""
        if 'cache_store' not in st.session_state:
            st.session_state.cache_store = {}
        if 'cache_stats' not in st.session_state:
            st.session_state.cache_stats = {
                'hits': 0,
                'misses': 0,
                'total_saved_ms': 0,
            }
    
    def _get_cache_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generate cache key from function and arguments.
        
        Args:
            func_name: Name of the function
            args: Positional arguments
            kwargs: Keyword arguments
        
        Returns:
            Cache key string
        """
        # Create hashable representation of arguments
        key_data = {
            'func': func_name,
            'args': str(args),
            'kwargs': str(sorted(kwargs.items())),
        }
        
        key_str = json.dumps(key_data, sort_keys=True)
        key_hash = hashlib.md5(key_str.encode()).hexdigest()
        
        return f"{func_name}_{key_hash}"
    
    def get(self, key: str) -> tuple[bool, Any]:
        """Get value from cache.
        
        Args:
            key: Cache key
        
        Returns:
            Tuple of (found, value)
        """
        if key not in st.session_state.cache_store:
            st.session_state.cache_stats['misses'] += 1
            return False, None
        
        cache_entry = st.session_state.cache_store[key]
        
        # Check if expired
        created_at = datetime.fromisoformat(cache_entry['created_at'])
        if datetime.now() - created_at > self.default_ttl:
            # Expired
            del st.session_state.cache_store[key]
            st.session_state.cache_stats['misses'] += 1
            return False, None
        
        st.session_state.cache_stats['hits'] += 1
        return True, cache_entry['value']
    
    def set(self, key: str, value: Any, ttl: timedelta = None) -> None:
        """Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live (uses default if None)
        """
        st.session_state.cache_store[key] = {
            'value': value,
            'created_at': datetime.now().isoformat(),
            'ttl': (ttl or self.default_ttl).total_seconds(),
        }
    
    def clear_all(self) -> None:
        """Clear all cache entries."""
        st.session_state.cache_store = {}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Cache statistics dictionary
        """
        stats = st.session_state.cache_stats.copy()
        total = stats['hits'] + stats['misses']
        stats['hit_rate'] = stats['hits'] / total if total > 0 else 0
        stats['total_requests'] = total
        
        return stats
    
    def cache_function(
        self,
        ttl: timedelta = None
    ) -> Callable:
        """Decorator for caching function results.
        
        Args:
            ttl: Time-to-live for cache entries
        
        Returns:
            Decorator function
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key
                key = self._get_cache_key(func.__name__, args, kwargs)
                
                # Check cache
                found, value = self.get(key)
                if found:
                    return value
                
                # Compute and cache result
                result = func(*args, **kwargs)
                self.set(key, result, ttl or self.default_ttl)
                
                return result
            
            return wrapper
        
        return decorator


def get_cache_manager() -> CacheManager:
    """Get or create the cache manager singleton.
    
    Returns:
        CacheManager instance
    """
    if 'cache_manager' not in st.session_state:
        st.session_state.cache_manager = CacheManager()
    return st.session_state.cache_manager


def cache_data(ttl_minutes: int = 5) -> Callable:
    """Decorator to cache function data with TTL.
    
    Args:
        ttl_minutes: Time-to-live in minutes
    
    Returns:
        Decorator function
    """
    manager = get_cache_manager()
    ttl = timedelta(minutes=ttl_minutes)
    return manager.cache_function(ttl)
