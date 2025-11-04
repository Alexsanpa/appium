import os
import unittest
import inspect
from pathlib import Path
import shutil

skip = os.environ.get('IGNORE_TESTS', False)
if not skip:
    path = Path.cwd()
    settings_file = str(path.joinpath('settings.ini'))
    os.environ['SAPY_SETTINGS'] = settings_file

    with open(settings_file, 'w+') as fh:
        fh.writelines(['[ENV]\n', 'DEBUG = true\n',
                       'LOG_FILES_PATH = Outputs_report/logs\n'
                       'REPORT_FILES_PATH = Outputs_report/reports\n'
                       'CUSTOM_SETTINGS_ENABLED = false'])

    from sapyautomation.core import LazyReporter  # noqa: E402
    from sapyautomation.core.test_cases import BaseTestCases  # noqa: E402

    class XTestCase(BaseTestCases):
        pass

    class DummyTestCase(XTestCase):

        def test_dummy_a(self):
            self.assertTrue(True)

        def test_dummy_b(self):
            self.assertTrue(True)


class TrackingReporterTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not skip:
            cls.test_case_name = DummyTestCase.__name__
            cls.tests_in_report = LazyReporter(DummyTestCase.__name__)\
                .get_test_data(XTestCase.__name__)
            cls.tests_in_case = [test[0]
                                 for test in inspect.getmembers(DummyTestCase)
                                 if test[0][:4] == 'test']

    def setUp(self):
        if skip:
            self.skipTest('Ignore tests variable enable')

    def test_previous_tests_captured(self):
        self.assertTrue(self.test_case_name in self.tests_in_report.keys(), '')
        self.assertEqual(self.tests_in_report[self.test_case_name],
                         self.tests_in_case, '')

    @classmethod
    def tearDownClass(cls) -> None:
        settings_path = Path(os.getenv('SAPY_SETTINGS'))
        shutil.rmtree(settings_path.parent.joinpath('Outputs_report'),
                      ignore_errors=True)
        settings_path.unlink(True)
