import os
import sys
import inspect
import unittest
import shutil
from pathlib import Path
from unidecode import unidecode
from sapyautomation.core import LazySettings, LazyReporter
from sapyautomation.core.utils import factories
from sapyautomation.core.utils.general import get_resource, PackedData, \
    get_locks
from sapyautomation.core.management.base import BaseCommand
from sapyautomation.core.backends.email import MailBackend
from sapyautomation.desktop.files import SpreadSheetData, \
    generate_unique_filename, test_path_format, path_to_module
from sapyautomation.core.utils.exceptions import TestsNotFound, DataSetNotFound


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
    exec_id = 0

    def add_arguments(self, parser):
        """ Registers the command arguments """
        parser.add_argument('suites', nargs='+', help='Test suites to be run')

        parser.add_argument('-extra-resources', nargs=1,
                            help='Extra resources path')
        parser.add_argument('-email-report', nargs='+',
                            help='Test suites to be run')
        parser.add_argument('--module-directory', '-m', nargs=1,
                            help='Test suites to be run')
        parser.add_argument('--data-directory', '-d', nargs=1,
                            help='Test suites to be run')

        parser.add_argument(
            '--html-report',
            help='Run the tests and create an html report them',
            action='store_true')
        parser.add_argument(
            '--xml-report',
            help='Run the tests and create an xml report of them',
            action='store_true')
        parser.add_argument(
            '--no-dataset',
            help='Flag for test cases without dataset',
            action='store_true')
        parser.add_argument(
            "--pathfinder",
            "-p",
            help="Map the test cases and the dataset files to run sequential tests",
            action="store_true",
        )

    def handle(self, **options):
        """ Command content """
        self.suites = options['suites']
        self.emails = options['email_report']
        self.data_dir = options['data_directory']
        html_report = options['html_report']
        self.no_dataset = options['no_dataset']
        self.pathfinder = options["pathfinder"]
        self.xml_report = options['xml_report']
        extra_resources = options['extra_resources']
        if extra_resources is not None:
            LazySettings().EXTRA_RESOURCES_PATH = extra_resources[0]

        if self.suites[0] == "discover":
            suites = []
            directory = options['module_directory'][0]
            directory = "./tests" if directory is None \
                else test_path_format(directory)

            for dirpath, _, filenames in os.walk(directory):
                for filename in [f for f in filenames if
                                 f.startswith("test_", 0) and
                                 f.endswith(".py")]:
                    suites.append(os.path.join(dirpath[2:], filename))
            self.suites = suites

        execs_info = get_locks(True)
        for lock in execs_info:
            try:
                # ignore corrupted files
                data = PackedData(lock.parts[-1][1:])
                _id = data.get('exec_id')

            except ValueError:
                _id = None

            if _id is not None:
                self.exec_id = 1 + (0 if _id is None else _id)

        if self.pathfinder:
            self.test_dict, self.dataset_dict = self.get_files_from_directory()
            self.suites = self.load_tests()
        else:
            self.suites = self.load_tests()
        self.loaded_tests = [test for test in self.loaded_tests if len(test) > 0]

        if len(self.loaded_tests) > 0:
            for i, test_group in enumerate(self.loaded_tests):
                if html_report:
                    template = get_resource(
                        'reports/combine_report_template.html'
                        if LazySettings().REPORT_COMBINE else
                        'reports/report_template.html')
                    self.run(factories.factory_runner(
                        "html", template=template,
                        combine_reports=LazySettings().REPORT_COMBINE),
                        (i, test_group))
                    print("Test report generated")
                elif self.xml_report:
                    self.run(factories.factory_runner("xml"), (i, test_group))
                    print("Test report generated")
                else:
                    self.run(factories.factory_runner("text"), (i, test_group))
                    print("Process finished")

        else:
            print('Tests not found')

        self.clean_up()

    def clean_up(self):
        # TODO: remove workaround for lock duplication pylint: disable=fixme
        for lock in get_locks():
            data = PackedData(lock.parts[-1][1:])
            if data.get('exec_id') is not self.exec_id:
                break
            if data.get('status') is None:
                data.clean_up()

    def run(self, runner, test_group_data):
        """ Runs tests
        Sends report via email if specified with '-email-report' parameter
        """
        LazyReporter(rebuild=True)
        runner.tests = []
        runner.create_suite(test_group_data[1])
        try:
            result = runner.run()

            self._tests = runner.tests

            if not self.xml_report:
                # TODO fix pdf generation with xml runner pylint: disable=fixme
                self.create_pdf_report(
                    test_group_data[0],
                    result.error_list("Error",
                                      result.errors + result.failures),
                    result.duration
                )

            if self.emails is not None and len(self.emails) > 0 \
                    and result.wasSuccessful():
                print("Tests reported to %s " % ', '.join(self.emails)
                      if self.create_3pa_report() else
                      "Tests can't be reported")
        except AttributeError as e:
            if "'suite' has no module 'run'" not in e.args[0]:
                raise e

    def create_pdf_report(self, group_index, errors, test_duration):
        """ Creates evidences report in pdf format
        """
        for i, test in enumerate(self._tests):
            LazyReporter(test).save_evidence_report(
                self.suites[group_index][i], errors, test_duration)

    def create_3pa_report(self):
        """ Creates and sends spreadsheet report file with
        3rd party applications data.
        """
        report_data = LazyReporter().generate_execution_report(keys=[
            'status', 'result_data', '_3pa_data'], test_classes=self._tests)

        if len(report_data) == 0:
            return False

        connection = MailBackend()
        connection.create_msg(self.emails,
                              "3pa Report",
                              "Content")
        report_file = LazySettings().PROJECT_PATH.joinpath(
            LazySettings().REPORT_FILES_PATH,
            generate_unique_filename('report_3pa.xlsx', add_timestamp=True))

        shutil.copy(get_resource('reports/3pa_report_template.xlsx'),
                    report_file)
        report_book = SpreadSheetData(report_file)

        for index, data in enumerate(report_data):
            report_book.append_row([data['process_team'], data['id'],
                                    data['name'], data['system'],
                                    data['category'], data['description'],
                                    ', '.join(data['data']), data['status']],
                                   offset=index)

        connection.attach_to_msg(documents=[report_file, ])
        connection.send_email()

        return True

    def load_test_groups(self):
        test_groups = []
        suite_groups = []
        test_data_groups = []
        loaded_tests = []

        for suite in self.suites:
            module_path = path_to_module(suite)
            test_path = Path(suite).parts[-1].split('.')[0]
            if self.pathfinder:
                suite_file_name = os.path.splitext(os.path.basename(suite))[0].lower()
                if suite_file_name in self.dataset_dict:
                    self.no_dataset = False
                    data_set_path = self.dataset_dict[suite_file_name]
                    data_set_path = data_set_path.rpartition("\\")
                    data_files_path = ""
                    for i in range(len(data_set_path) - 1):
                        data_files_path += data_set_path[i]
                        data_files_path = data_files_path.replace("\\", "/")

                elif not (suite in self.dataset_dict):
                    self.no_dataset = True
                    data_files_path = "resources/test_data/"

            else:
                data_files_path = (
                    "resources/test_data/"
                    if self.data_dir is None
                    else self.data_dir[0]
                )
            data_files_path = Path(data_files_path)

            data_files_patterns = ('*_%s.xlsx' % test_path,
                                   '%s.xlsx' % test_path,
                                   '*_%s.xls' % test_path,
                                   '%s.xls' % test_path)

            data_files_list = []
            for pattern in data_files_patterns:
                files = data_files_path.glob(pattern)
                data_files_list = data_files_list + list(files)

            if len(data_files_list) > 0:
                for i, file in enumerate(data_files_list):
                    if i > len(test_groups)-1:
                        test_groups.append([])
                        suite_groups.append([])
                        test_data_groups.append([])
                        loaded_tests.append([])

                    test_groups[i].append(module_path)
                    suite_groups[i].append(suite)
                    test_data_groups[i].append(file)
            elif self.no_dataset:
                test_groups.append([])
                suite_groups.append([])
                test_data_groups.append([])
                loaded_tests.append([])

                test_groups[0].append(module_path)
                suite_groups[0].append(suite)
                test_data_groups[0].append('')
            else:
                raise DataSetNotFound(test_path)

        self.loaded_tests = loaded_tests
        self.test_data_groups = test_data_groups

        return test_groups, suite_groups

    def load_tests(self):
        """ Loads the test cases to be run
        """
        testLoader = unittest.loader.defaultTestLoader
        test_groups, suite_groups = self.load_test_groups()
        for group, tests in enumerate(test_groups):
            testLoader.loadTestsFromNames(tests)
            for i, module_name in enumerate(tests):
                try:
                    for member in inspect.getmembers(
                            sys.modules[module_name],
                            inspect.isclass):
                        test_methods = [tm[0] for tm in inspect.getmembers(
                                    member[1], predicate=inspect.isfunction)
                                    if tm[0].startswith('test_')]
                        self.loaded_tests[group].append(
                            (member[1], test_methods,
                             None, None,
                             self.test_data_groups[group][i],
                             self.exec_id))
                except KeyError:
                    raise TestsNotFound(module_name)

        return suite_groups

    def recursive_pathfinder(
        self, current_path: str, path_dict: dict, file_type: str = ".py"
    ) -> dict:
        """
        Recursively searches for files with the specified file type in the given directory and its subdirectories.

        Args:
            current_path (str): The path of the directory to search in.
            path_dict (dict): A dictionary to store the file names and their corresponding paths.
            file_type (str, optional): The file type to search for. Defaults to ".py".

        Returns:
            dict: A dictionary containing the file names and their corresponding paths.
        """
        # If the current is a directory
        if os.path.isdir(current_path):
            # Get the list of files and directories in the current directory
            paths = os.listdir(current_path)
            # Recursively search for files in each subdirectory
            for path in paths:
                new_path = os.path.join(current_path, path)
                self.recursive_pathfinder(new_path, path_dict, file_type)
        else:
            # If the current path is a file with the specified file type and is not an __init__.py file
            if (
                os.path.isfile(current_path)
                and (current_path.endswith(file_type))
                and os.path.basename(current_path) != "__init__.py"
            ):
                # Get the file name and convert it to lowercase without spaces and accents
                file_name = os.path.basename(current_path)
                file_name, _ = os.path.splitext(file_name)
                file_name = unidecode(file_name.replace(" ", "").lower())

                # Add the file name and its path to the dictionary
                path_dict[file_name] = current_path

        return path_dict

    def get_files_from_directory(self) -> tuple:
        """
        Get test and dataset files from their respective directories.

        Returns:
            Tuple: A tuple containing two dictionaries. The first dictionary contains
            test files and their paths, while the second dictionary contains dataset
            files and their paths.
        """
        suites = []
        test_dict = {}
        dataset_dict = {}
        test_path = "./tests"
        dataset_path = "resources/test_data/"
        self.recursive_pathfinder(test_path, test_dict)
        self.recursive_pathfinder(
            dataset_path, dataset_dict, file_type=(".xlsx", ".xls")
        )
        for test_name in self.suites:
            test_name = unidecode(test_name.replace(" ", "").lower())
            if not test_name.startswith("test_"):
                test_name = "test_" + test_name
            if test_name.endswith(".py"):
                test_name = test_name[:-3]
            if not (test_name in test_dict):
                raise TestsNotFound(f"{test_name}, is not in the work directory")
            suites.append(test_dict[test_name])
        self.suites = suites

        return test_dict, dataset_dict
