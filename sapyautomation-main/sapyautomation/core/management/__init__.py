import os
import sys
import importlib
import argparse
from pathlib import Path

os.environ['SAPY_SETTINGS'] = str(Path.cwd().joinpath('settings.ini'))


def execute_from_command_line(argv=None):
    """Run a ManagementUtility."""
    utility = ManagementUtility(argv)
    utility.execute()


def load_command_class(name):
    """ Loads command class by name """
    command = importlib.import_module(
        'sapyautomation.core.management.commands.%s' % name)

    return command.Command()


class ManagementUtility:
    """ Encapsulate the logic of the sapyautomation utilities. """
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        if self.prog_name == '__main__.py':
            self.prog_name = 'python -m sapyautomation'
        self.settings_exception = None

    def execute(self):
        """
        Given the command-line arguments, figure out which subcommand is being
        run, create a parser appropriate to that command, and run it.
        """
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = 'help'

        parser = argparse.ArgumentParser(description='Run test cases and '
                                                     'generate html or xml '
                                                     'reports')
        parser.add_argument('args', nargs='*')  # catch-all

        if subcommand == 'help':
            pass
        elif self.argv[1:] in (['--help'], ['-h']):
            pass
        else:
            load_command_class(subcommand).run_from_argv(self.argv)
