import sys
import inspect
import unittest

from sapyautomation.core.utils.general import PackedData, get_locks_by_name
from sapyautomation.core.management.commands.run_test import Command as RunTest
from sapyautomation.core.utils.exceptions import TestsNotFound


class Command(RunTest):
    """ This command allows the user to run tests creating reports by CLI

    Allows the user run tests by CLI with parameters to be able to get html
    or xml reports. You can also type multiple files in order to run
    everything in one execution. optional argument -h or --help, returns:

        python -m usage: cli.py [-h] [--html-report] [--xml-report]
        suites [suites ...]

    """
    help = "Run n test cases."

    def load_test_with_resume_data(self, member_name, member, group, index):
        for lockfile in get_locks_by_name(member_name):
            pdata = PackedData(lockfile.parts[-1][1:])
            data_file = self.test_data_groups[group][index]
            if not pdata.get('runned_steps') and \
                    pdata.get('status') == 'paused':
                pdata.clean_up()

            elif pdata.get('runned_steps') and \
                    pdata.get('status') == 'paused' and \
                    pdata.get('target_datetime') is not None and \
                    str(data_file) in pdata.get('data_file_name'):

                pdata.replace_or_append('status', 'resumed')
                methods = inspect.getmembers(
                    member, predicate=inspect.isfunction)
                test_methods = [tm[0] for tm in methods
                                if tm[0].startswith('test_')]
                data = (member, test_methods,
                        pdata.get('runned_steps')[:-1],
                        lockfile.parts[-1][1:],
                        data_file,
                        self.exec_id)

                if data not in self.loaded_tests:
                    self.loaded_tests[group].append(data)

    def load_tests(self):
        """ Loads the test cases to be run """
        testLoader = unittest.loader.defaultTestLoader
        test_groups, suite_groups = self.load_test_groups()

        for group, tests in enumerate(test_groups):
            testLoader.loadTestsFromNames(tests)
            for i, module_name in enumerate(tests):
                try:
                    for member_name, member in inspect.getmembers(
                            sys.modules[module_name],
                            inspect.isclass):
                        self.load_test_with_resume_data(member_name, member,
                                                        group, i)

                except KeyError:
                    raise TestsNotFound(module_name)

        return suite_groups
