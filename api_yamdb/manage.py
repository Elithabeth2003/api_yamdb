#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """
    Run the Django management command line interface.

    This function sets the DJANGO_SETTINGS_MODULE environment
    variable to 'api_yamdb.settings', which specifies the settings module
    for the Django project. Then it attempts to import
    execute_from_command_line function from django.core.management module.

    If Django is not installed or not available on the PYTHONPATH environment
    variable, it raises an ImportError with a helpful error message.

    Usage:
        Call this function to execute Django management command line interface.

    Raises:
        ImportError: If Django is not installed or not available on
        the PYTHONPATH environment variable.

    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
