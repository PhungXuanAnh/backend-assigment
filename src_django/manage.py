#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def initialize_debugger(sys_args):
    if os.getenv("RUN_MAIN") and (sys_args[1] == "runserver" or sys_args[1] == "runserver_skip_check"):
        try:
            import debugpy

            debugpy.listen(("0.0.0.0", 5678))
            sys.stdout.write("=======> Started the VS Code debugger")
            sys.stdout.write('\n')
        except Exception as ex:
            sys.stdout.write("=======> Start the VS Code debugger FAILED: %" % ex)
            sys.stdout.write('\n')


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings.base")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    initialize_debugger(sys.argv)
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
