#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xander.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:donohoe_al@xander-lakes:~/xander_lakes/frontend$ sudo apt-get install

        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from except
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
