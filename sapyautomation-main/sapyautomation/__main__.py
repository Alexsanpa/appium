"""
Invokes sapyautomation when the sapyautomation module is run as a script.

Example: python -m sapyautomation -h
"""
import os
from pathlib import Path
from sapyautomation.core import management


def main():
    os.environ['SAPY_SETTINGS'] = str(Path.cwd().joinpath('settings.ini'))
    management.execute_from_command_line()


if __name__ == "__main__":
    main()
