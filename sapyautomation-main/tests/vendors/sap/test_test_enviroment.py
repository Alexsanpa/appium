import os
import unittest
import pathlib
skip = os.environ.get('IGNORE_TESTS', False)
if not skip:
    path = pathlib.Path.cwd()
    settings_file = str(path.joinpath('settings.ini'))
    os.environ['SAPY_SETTINGS'] = settings_file

skip = os.environ.get('IGNORE_TESTS', False)
if not skip:
    path = pathlib.Path.cwd()
    settings_file = str(path.joinpath('settings.ini'))
    os.environ['SAPY_SETTINGS'] = settings_file

    with open(settings_file, 'w+') as fh:
        fh.writelines(['[ENV]\n', 'DEBUG = true\n',
                       'CUSTOM_SETTINGS_ENABLED = false'])

    from sapyautomation.core import LazySettings  # noqa: E402
    from sapyautomation.desktop.process import is_process_running, \
        kill_process  # noqa: E402
    from sapyautomation.vendors.sap.test_enviroment import SapTestSuite\
        # noqa: E402


class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if not skip:
            cls.sap_name = "saplogon"
            cls.sapSuite = SapTestSuite()

    def setUp(self) -> None:
        if skip:
            self.skipTest('Ignore tests variable enable')

    def test_sap_test_suite(self):
        self.assertIsNotNone(self.sapSuite)
        self.assertIsInstance(self.sapSuite, unittest.TestCase)

    def test_start_sap(self) -> None:
        self.assertFalse(is_process_running(self.sap_name))
        self.sapSuite.start_sap()
        self.assertTrue(is_process_running(self.sap_name))
        kill_process(self.sap_name)

    def test_close_sap(self):
        self.sapSuite.start_sap()
        self.sapSuite.close_sap()
        self.assertFalse(is_process_running(self.sap_name))

    def test_assert_path_exists(self) -> None:
        self.sapSuite.start_sap()
        self.sapSuite.assertSapPathExists()
        self.sapSuite.close_sap()

    @classmethod
    def tearDownClass(cls) -> None:
        if not skip:
            path = pathlib.Path(
                LazySettings().PROJECT_PATH).parent.joinpath('Outputs', 'logs')
            for file in path.iterdir():
                if file.is_file() and 'sapyautomation' in str(file):
                    file.unlink(True)

            pathlib.Path(os.getenv('SAPY_SETTINGS')).unlink(True)
