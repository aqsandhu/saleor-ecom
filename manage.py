#!/usr/bin/env python3
"""
Django's command-line utility for administrative tasks.
This is the main entry point for Saleor e-commerce platform.
It sets up Django environment and provides command-line utilities.
"""
import os
import sys

if __name__ == "__main__":
    # Default Django settings module for the 'manage.py' command
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saleor.settings")

    from django.core.management import execute_from_command_line

    # Execute command from command line arguments
    execute_from_command_line(sys.argv)
