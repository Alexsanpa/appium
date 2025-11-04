import unittest
from pathlib import Path
from sapyautomation.core.test_cases import BasePom


class DemoPom(BasePom):

    @property
    def logger(self):
        return self._reporter._logger


class TestBasePom(unittest.TestCase):

    def setUp(self):
        self.pom = DemoPom()

    def test_logging(self):
        self.pom.log("log entry")
        self.pom.log_info("log entry")
        self.pom.log_warning("log entry")
        self.pom.log_error("log entry")

        log_file = Path(self.pom.logger._path,
                        self.pom.logger.file_name['debug'])
        flags = {'debug': False,
                 'info': False,
                 'warning': False,
                 'error': False}

        with log_file.open('r') as f:
            for line in f.readlines():
                if 'DEBUG[' in line:
                    flags['debug'] = True
                if 'INFO[' in line:
                    flags['info'] = True
                if 'WARNING[' in line:
                    flags['warning'] = True
                if 'ERROR[' in line:
                    flags['error'] = True

        for entry in flags:
            self.assertTrue(entry)
