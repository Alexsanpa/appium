from pathlib import Path

from sapyautomation.core.management.base import BaseCommand
from sapyautomation.desktop.builders import TestBuilder
from sapyautomation.desktop.files import SpreadSheetData, test_path_format
from sapyautomation.core.management.conf import LazySettings
from sapyautomation.core.utils.exceptions import CollectionNotFound
from sapyautomation.core.test_cases.bases import BaseTestData


class Command(BaseCommand):
    """ This command allows the user to run tests creating reports by CLI

    Allows the user run tests by CLI with parameters to be able to get html
    or xml reports. You can also type multiple files in order to run
    everything in one execution. optional argument -h or --help, returns:

        python -m usage: cli.py [-h] [--html-report] [--xml-report]
        suites [suites ...]

    """
    help = "Run n cases."
    _3pa_data = []

    def add_arguments(self, parser):
        """ Registers the command arguments """
        parser.add_argument('tests', nargs='+',
                            help='Tests id to be generated')
        parser.add_argument('--collection', '-c', nargs=1,
                            help='Test collection name')
        parser.add_argument('--module-directory', '-m', nargs=1,
                            help='Test suites to be run')
        parser.add_argument('--data-directory', '-d', nargs=1,
                            help='Test suites to be run')
        parser.add_argument('--target-environment', '-t', nargs=1,
                            help='Test suites to be run')

    def handle(self, **options):
        """ Command content """
        tests = options['tests']

        collection = options['collection']
        collection = None if collection is None else collection[0]

        data_dir = options['data_directory']
        data_dir = 'resources/test_data/' if data_dir is None else data_dir[0]

        module_dir = options['module_directory']
        module_dir = "tests" if module_dir is None \
            else test_path_format(module_dir[0])

        target_env = options['target_environment']
        target_env = "desktop" if target_env is None \
            else target_env[0]

        test_collection = self.get_tests_collection_file(data_dir, collection)
        collection_data = SpreadSheetData(test_collection)

        errors = []
        success = []

        for test in tests:
            test_constructor = None
            test_name = "test"

            first_step = True

            test_data = None
            for i, value in enumerate(collection_data.get_column_data(0, 0)):
                if test in str(value):
                    data = collection_data.get_row_data(i, 0)
                    if first_step:
                        first_step = False
                        test_data = BaseTestData(
                            '_'.join((test_name, test,
                                      Path(module_dir).parts[-1],
                                      target_env)),
                            '\n'.join([data[1],
                                       'Test id: %s' % int(data[0]),
                                       'Process team: %s' % data[3],
                                       'Description: %s' % data[2]]),
                            data[1])

                        test_constructor = TestBuilder(
                            test_data.get_module()[0],
                            test_data.get_module()[1],
                            test_data.get_class()[1])
                    test_data.add_step('_'.join(data[5].split(' ')),
                                       data[6], data[7])

                    test_constructor.add_method(test_data.get_step(-1)[0],
                                                test_data.get_step(-1)[1])

            result = test_constructor.save(
                LazySettings().PROJECT_PATH.joinpath(
                    module_dir, '%s.py' % test_data.get_module()[0]))

            if "' already exists." in result:
                errors.append(result)
            else:
                success.append(result)

        for item in success:
            print(' Success: %s' % item)
        for item in errors:
            print('   Error: %s' % item)

    @staticmethod
    def get_tests_collection_file(data_dir, collection):
        data_files_path = Path(data_dir)
        data_files_patterns = ('collection_*.xlsx',
                               'collection_*.xls')
        data_files_list = []
        for pattern in data_files_patterns:
            files = data_files_path.glob(pattern)
            data_files_list = data_files_list + list(files)

        for test_collection in data_files_list:
            if collection is None or 'collection_%s' % collection \
                    in test_collection.parts[-1]:
                return test_collection

        raise CollectionNotFound("No collection found.")
