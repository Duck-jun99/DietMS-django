#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.core.management import call_command


def main():
    from django.conf import settings
    from django.core.management import execute_from_command_line
    
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
        
    call_command('makemigrations', check=True)
    call_command('migrate', check=True)
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
