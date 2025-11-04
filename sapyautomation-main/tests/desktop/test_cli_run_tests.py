import os
import unittest
import subprocess
from pathlib import Path
import shutil


class TestCliRunTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.tests_path = 'tests/desktop/sapytest_dummie.py'
        path = Path.cwd()

        os.environ['SAPY_SETTINGS'] = str(path.joinpath('settings.ini'))

        with open(os.getenv('SAPY_SETTINGS'), 'w+') as fh:
            fh.writelines(['[ENV]\n', 'DEBUG = true\n',
                           'LOG_FILES_PATH = outputs_cli/logs\n',
                           'REPORT_FILES_PATH = outputs_cli/reports\n',
                           'CUSTOM_SETTINGS_ENABLED = false'])

    def setUp(self):
        skip = os.environ.get('IGNORE_TESTS', False)
        if skip:
            self.skipTest('Ignore tests variable enable')

    def test_show_help_text(self):
        cmd = "python -m sapyautomation run_test -h"
        result = subprocess.check_output(cmd, shell=True)
        self.assertTrue(b"usage:" in result)
        self.assertTrue(b"positional arguments:" in result)
        self.assertTrue(b"optional arguments:" in result)

    def test_validate_run_cli_no_report(self):
        cmd = r' '.join(('python -m sapyautomation run_test',
                        self.tests_path,
                        '-d tests/resources/test_files'))
        result = subprocess.check_output(cmd, shell=True)
        self.assertFalse(b"Test report generated" in result)
        self.assertTrue(b"Process finished" in result)

    def test_validate_run_cli_html_report(self):
        cmd = r' '.join(('python -m sapyautomation run_test',
                         self.tests_path,
                         '-d tests/resources/test_files',
                         '--html-report'))
        result = subprocess.check_output(cmd, shell=True)
        self.assertTrue(b"Test report generated" in result)

    def test_validate_run_cli_xml_report(self):
        cmd = r' '.join(('python -m sapyautomation run_test',
                         self.tests_path,
                         '-d tests/resources/test_files',
                         '--xml-report'))
        result = subprocess.check_output(cmd, shell=True)
        self.assertTrue(b"Test report generated" in result)

    @classmethod
    def tearDownClass(cls) -> None:
        settings_path = Path(os.getenv('SAPY_SETTINGS'))
        shutil.rmtree(settings_path.parent.joinpath('outputs_cli'),
                      ignore_errors=True)
        settings_path.unlink(True)


if __name__ == '__main__':
    unittest.main()
