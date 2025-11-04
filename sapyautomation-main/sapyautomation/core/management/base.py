import argparse


class BaseCommand:
    """ The base class from wich all commands will derive """
    help = ''

    def add_arguments(self, parser):
        """ Entry point for subclassed commands to add custom arguments.
        """

    def handle(self, **options):
        """ The actual logic of the command. Subclasses must implement
        this method.
        """
        raise NotImplementedError(
            'subclasses of BaseCommand must provide a handle() method')

    def execute(self, **options):
        """ Executes the command """

        output = self.handle(**options)

        return output

    def create_parser(self):
        """
        Create and return the ``ArgumentParser`` which will be used to
        parse the arguments to this command.
        """
        parser = argparse.ArgumentParser(description='Run test cases and '
                                                     'generate html or xml '
                                                     'reports')

        self.add_arguments(parser)
        return parser

    def run_from_argv(self, argv):
        """ Runs the command parsing the arguments """

        parser = self.create_parser()

        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)

        self.execute(**cmd_options)
