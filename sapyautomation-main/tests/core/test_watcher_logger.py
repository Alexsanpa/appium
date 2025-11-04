import os
import unittest
from pathlib import Path
import shutil

from sapyautomation.core.watchers.logger import Logger


class LoggerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path.cwd()
        os.environ['SAPY_SETTINGS'] = str(path.joinpath('settings.ini'))

        with open(os.getenv('SAPY_SETTINGS'), 'w+') as fh:
            fh.writelines(['[ENV]\n', 'DEBUG = true\n',
                           'LOG_FILES_PATH = Outputs_log/logs\n'
                           'REPORT_FILES_PATH = Outputs_log/reports\n'
                           'CUSTOM_SETTINGS_ENABLED = false'])

        cls.logger = Logger('unittest', 'myuid')

    def test_path_created(self):
        path = self.logger.file_path('debug').parent
        self.assertTrue(path.exists())

    def test_logfile_created(self):
        logfile_debug = self.logger.file_path('debug')
        logfile_error = self.logger.file_path('error')
        self.assertTrue(logfile_debug.exists())
        self.assertTrue(logfile_error.exists())

    def test_log_entries(self):
        self.logger.debug('message')
        self.logger.info('message')
        self.logger.warning('message')
        self.logger.error('message', 'step')

        logfile_debug = self.logger.file_path('debug')
        logfile_error = self.logger.file_path('error')

        entries_error = 0
        with logfile_error.open() as f:
            for line in f.readlines():
                if line.startswith('ERROR'):
                    entries_error += 1

        entries_debug = 0
        with logfile_debug.open() as f:
            for line in f.readlines():
                if line.startswith('DEBUG') or \
                        line.startswith('INFO') or \
                        line.startswith('WARNING'):
                    entries_debug += 1

        self.assertEqual(entries_debug, 3)
        self.assertEqual(entries_error, 1)

    @classmethod
    def tearDownClass(cls) -> None:
        settings_path = Path(os.getenv('SAPY_SETTINGS'))
        shutil.rmtree(settings_path.parent.joinpath('Outputs_log'),
                      ignore_errors=True)
        settings_path.unlink(True)
