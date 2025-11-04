import os
import unittest
from pathlib import Path
from sapyautomation.core.management.conf import LazySettings


class TestSettingsCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path = Path.cwd()
        cls.settings_files = {
            'default': str(path.joinpath('default_settings.ini')),
            'custom': str(path.joinpath('custom_settings.ini')),
            'bad': str(path.joinpath('bad_settings.ini'))}

        with open(cls.settings_files['default'], 'w+') as fh:
            fh.writelines(['[ENV]\n', 'CUSTOM_SETTINGS_ENABLED = false'])

        with open(cls.settings_files['custom'], 'w+') as fh:
            fh.writelines(['[ENV]\n', 'DEBUG = true\n',
                           'CUSTOM_SETTINGS_ENABLED = true\n',
                           '[CUSTOM]\n', 'DEMO = data'])

        with open(cls.settings_files['bad'], 'w+') as fh:
            fh.writelines(['[ENV]\n', 'DEBU = true\n'])

        cls.secrets_file = str(path.joinpath('secrets.ini'))

        with open(cls.secrets_file, 'w+') as fh:
            fh.writelines(['[SAP]\n', 'USER = user0\n',
                           'PASSWORD = pass0\n', 'SYSTEM = NS5\n'
                           '[OTHER]\n', 'USER = user1\n',
                           'PASSWORD = pass1\n'])

    def setUp(self):
        os.environ['SAPY_SETTINGS'] = self.settings_files['default']

    def test_unique_inmutable_instance_settings(self):
        settings = LazySettings(rebuild=True)
        os.environ['SAPY_SETTINGS'] = self.settings_files['bad']
        settings2 = LazySettings()

        self.assertIsNotNone(settings, 'settings module found.')
        self.assertEqual(settings, settings2)

    def test_load_default_settings(self):
        settings = LazySettings(rebuild=True)

        self.assertFalse(settings.CUSTOM_SETTINGS_ENABLED)

    def test_override_default_settings(self):
        os.environ['SAPY_SETTINGS'] = self.settings_files['custom']
        settings = LazySettings(rebuild=True)

        self.assertTrue(settings.DEBUG)

    def test_custom_settings_not_enabled(self):
        settings = LazySettings(rebuild=True)

        self.assertFalse(settings.CUSTOM_SETTINGS_ENABLED)

        with self.assertRaises(Exception):
            settings.CUSTOM_DEMO

    def test_custom_settings_enabled(self):
        os.environ['SAPY_SETTINGS'] = self.settings_files['custom']
        settings = LazySettings(rebuild=True)
        self.assertTrue(settings.CUSTOM_SETTINGS_ENABLED)

        self.assertIsNotNone(settings.CUSTOM_DEMO)

    def test_error_not_expected_setting(self):
        os.environ['SAPY_SETTINGS'] = self.settings_files['bad']
        with self.assertRaises(Exception):
            LazySettings(rebuild=True)

    def test_credentials(self):
        settings = LazySettings(rebuild=True)
        sap_credentials = settings.CREDENTIALS('SAP')
        other_credentials = settings.CREDENTIALS('OTHER')
        self.assertTrue(sap_credentials is not None)
        self.assertTrue(other_credentials is not None)

        self.assertTrue('SYSTEM' in sap_credentials.keys())
        self.assertTrue('USER' in other_credentials.keys())

    @classmethod
    def tearDownClass(cls):
        for file in cls.settings_files.keys():
            Path(cls.settings_files[file]).unlink(True)
        Path(cls.secrets_file).unlink(True)


if __name__ == '__main__':
    unittest.main()
