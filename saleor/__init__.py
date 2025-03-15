"""
Saleor E-Commerce Platform

This is the main package for the Saleor e-commerce platform.
It provides a modular, API-first e-commerce solution built with Python, Django, and GraphQL.
"""

import pillow_avif  # noqa: F401 # imported for side effects - enables AVIF image support

from .celeryconf import app as celery_app

__all__ = ["celery_app"]
__version__ = "3.21.0-a.0"


class PatchedSubscriberExecutionContext:
    """
    A patched execution context for GraphQL subscribers.
    
    This class wraps the original execution context and provides error tracking
    for GraphQL subscription operations.
    """
    __slots__ = "exe_context", "errors"

    def __init__(self, exe_context):
        """
        Initialize with an execution context.
        
        Args:
            exe_context: The original GraphQL execution context
        """
        self.exe_context = exe_context
        self.errors = self.exe_context.errors

    def reset(self):
        """Reset the errors list."""
        self.errors = []

    def __getattr__(self, name):
        """Delegate attribute access to the wrapped execution context."""
        return getattr(self.exe_context, name)


# Extract major and minor version components for API versioning
_major, _minor, _ = __version__.split(".", 2)
schema_version = f"{_major}.{_minor}"
user_agent_version = f"Saleor/{schema_version}"
