"""
Celery Configuration for Saleor E-Commerce platform.

This module configures Celery for asynchronous task processing in Saleor.
It sets up the Celery application, connects it to Django settings,
and configures task discovery.
"""

import logging
import os

from celery import Celery
from celery.signals import setup_logging
from django.conf import settings

from .plugins import discover_plugins_modules

# Logger name used by Celery
CELERY_LOGGER_NAME = "celery"


@setup_logging.connect
def setup_celery_logging(loglevel=None, **kwargs):
    """Skip default Celery logging configuration.

    Will rely on Django to set up the base root logger.
    Celery loglevel will be set if provided as Celery command argument.
    
    Args:
        loglevel: Log level passed from Celery command
        kwargs: Additional arguments passed from the signal
    """
    if loglevel:
        logging.getLogger(CELERY_LOGGER_NAME).setLevel(loglevel)


# Set Django settings module for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saleor.settings")

# Initialize Celery application with custom task class
app = Celery("saleor", task_cls="saleor.core.tasks:RestrictWriterDBTask")

# Load configuration from Django settings (with CELERY prefix)
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()

# Discover tasks from specific migrations
app.autodiscover_tasks(
    packages=[
        "saleor.order.migrations.tasks",
    ],
    related_name="saleor3_21",
)

# Discover tasks from installed plugins
app.autodiscover_tasks(lambda: discover_plugins_modules(settings.PLUGINS))  # type: ignore[misc] # circular import # noqa: E501

# Discover search-related tasks
app.autodiscover_tasks(related_name="search_tasks")
