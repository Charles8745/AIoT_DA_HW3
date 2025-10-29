"""Form validation components for enhanced user input.

This module provides validated input components with real-time
validation, error handling, and success indicators.

Module contents:
    - ValidationResult: Validation result data class
    - ValidatedInput: Text input with validation
    - ValidatedSlider: Slider with validation
    - FormValidator: Form-level validation
"""

from dataclasses import dataclass
from typing import Callable, Optional, Any, List
import streamlit as st
import re


@dataclass
class ValidationResult:
    """Result of input validation.
    
    Attributes:
        is_valid: Whether input is valid
        error_message: Error message if invalid
        warning_message: Optional warning message
        suggestions: List of helpful suggestions
    """
    is_valid: bool
    error_message: Optional[str] = None
    warning_message: Optional[str] = None
    suggestions: List[str] = None
    
    def __post_init__(self):
        """Initialize defaults."""
        if self.suggestions is None:
            self.suggestions = []


class ValidatedInput:
    """Text input with validation support."""
    
    def __init__(
        self,
        label: str,
        key: str,
        validators: Optional[List[Callable]] = None,
        help_text: str = "",
        placeholder: str = "",
    ):
        """Initialize validated input.
        
        Args:
            label: Input label
            key: Unique identifier
            validators: List of validation functions
            help_text: Help text to display
            placeholder: Placeholder text
        """
        self.label = label
        self.key = key
        self.validators = validators or []
        self.help_text = help_text
        self.placeholder = placeholder
    
    def add_validator(self, validator: Callable) -> None:
        """Add a validation function.
        
        Args:
            validator: Function that takes value and returns ValidationResult
        """
        self.validators.append(validator)
    
    def validate(self, value: str) -> ValidationResult:
        """Validate input value.
        
        Args:
            value: Value to validate
        
        Returns:
            ValidationResult object
        """
        for validator in self.validators:
            result = validator(value)
            if not result.is_valid:
                return result
        
        return ValidationResult(is_valid=True)
    
    def render(self) -> tuple[str, ValidationResult]:
        """Render input and return value and validation result.
        
        Returns:
            Tuple of (value, validation_result)
        """
        value = st.text_input(
            self.label,
            key=self.key,
            help=self.help_text,
            placeholder=self.placeholder
        )
        
        validation_result = self.validate(value) if value else ValidationResult(is_valid=True)
        
        # Display validation feedback
        if value and validation_result.error_message:
            st.error(f"❌ {validation_result.error_message}")
        elif value and validation_result.warning_message:
            st.warning(f"⚠️ {validation_result.warning_message}")
        elif value and validation_result.is_valid:
            st.success(f"✅ Valid input")
        
        # Display suggestions
        if validation_result.suggestions:
            with st.expander("💡 Suggestions"):
                for suggestion in validation_result.suggestions:
                    st.write(f"• {suggestion}")
        
        return value, validation_result


class ValidatedSlider:
    """Slider with validation and constraints."""
    
    def __init__(
        self,
        label: str,
        min_value: float,
        max_value: float,
        default_value: float,
        key: str,
        step: float = 1.0,
        help_text: str = "",
    ):
        """Initialize validated slider.
        
        Args:
            label: Slider label
            min_value: Minimum value
            max_value: Maximum value
            default_value: Default value
            key: Unique identifier
            step: Step size
            help_text: Help text to display
        """
        self.label = label
        self.min_value = min_value
        self.max_value = max_value
        self.default_value = default_value
        self.key = key
        self.step = step
        self.help_text = help_text
    
    def render(self) -> float:
        """Render slider and return value.
        
        Returns:
            Selected value
        """
        value = st.slider(
            self.label,
            min_value=self.min_value,
            max_value=self.max_value,
            value=self.default_value,
            step=self.step,
            key=self.key,
            help=self.help_text
        )
        return value


class FormValidator:
    """Validate entire form with multiple fields."""
    
    def __init__(self):
        """Initialize form validator."""
        self.validators: dict = {}
        self.results: dict = {}
    
    def add_field_validator(
        self,
        field_name: str,
        validator: Callable
    ) -> None:
        """Add validator for a form field.
        
        Args:
            field_name: Name of the field
            validator: Validation function
        """
        self.validators[field_name] = validator
    
    def validate_field(
        self,
        field_name: str,
        value: Any
    ) -> ValidationResult:
        """Validate a single field.
        
        Args:
            field_name: Name of field to validate
            value: Value to validate
        
        Returns:
            ValidationResult
        """
        validator = self.validators.get(field_name)
        if not validator:
            return ValidationResult(is_valid=True)
        
        result = validator(value)
        self.results[field_name] = result
        return result
    
    def validate_all(self, data: dict) -> bool:
        """Validate all fields in data dictionary.
        
        Args:
            data: Dictionary of field values
        
        Returns:
            True if all fields are valid
        """
        for field_name, value in data.items():
            result = self.validate_field(field_name, value)
            if not result.is_valid:
                return False
        return True
    
    def get_errors(self) -> dict:
        """Get all validation errors.
        
        Returns:
            Dictionary of field errors
        """
        return {
            field: result.error_message
            for field, result in self.results.items()
            if not result.is_valid
        }
    
    def display_errors(self) -> None:
        """Display all validation errors in UI."""
        errors = self.get_errors()
        if errors:
            st.error("❌ Form validation errors:")
            for field, message in errors.items():
                st.write(f"• **{field}**: {message}")


# Common validators
def email_validator(email: str) -> ValidationResult:
    """Validate email format.
    
    Args:
        email: Email address to validate
    
    Returns:
        ValidationResult
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return ValidationResult(
            is_valid=False,
            error_message="Invalid email format"
        )
    return ValidationResult(is_valid=True)


def min_length_validator(min_len: int) -> Callable:
    """Create validator for minimum length.
    
    Args:
        min_len: Minimum length required
    
    Returns:
        Validator function
    """
    def validator(value: str) -> ValidationResult:
        if len(value) < min_len:
            return ValidationResult(
                is_valid=False,
                error_message=f"Minimum {min_len} characters required"
            )
        return ValidationResult(is_valid=True)
    
    return validator


def max_length_validator(max_len: int) -> Callable:
    """Create validator for maximum length.
    
    Args:
        max_len: Maximum length allowed
    
    Returns:
        Validator function
    """
    def validator(value: str) -> ValidationResult:
        if len(value) > max_len:
            return ValidationResult(
                is_valid=False,
                error_message=f"Maximum {max_len} characters allowed"
            )
        return ValidationResult(is_valid=True)
    
    return validator


def numeric_validator(value: str) -> ValidationResult:
    """Validate numeric input.
    
    Args:
        value: Value to validate
    
    Returns:
        ValidationResult
    """
    try:
        float(value)
        return ValidationResult(is_valid=True)
    except ValueError:
        return ValidationResult(
            is_valid=False,
            error_message="Must be a valid number"
        )
