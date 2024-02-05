import os
import sys
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'protected.settings')

def run_daphne():
    # Import Daphne only when needed to avoid import errors
    from daphne.cli import CommandLineInterface
    sys.argv = ["daphne", "protected.asgi:application"]
    CommandLineInterface.entrypoint()

if __name__ == "__main__":
    execute_from_command_line(sys.argv)
