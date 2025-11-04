import pathlib
import logging

from pathlib import WindowsPath
from sapyautomation.core.management.conf import LazySettings


class Logger:
    """ A class to manage logging """
    current_test = None
    test_errors = []

    def __init__(self, name: str, uid: str):
        path = pathlib.Path(LazySettings().PROJECT_PATH).joinpath(
            LazySettings().LOG_FILES_PATH, uid)

        self._path = path
        self._path.mkdir(parents=True, exist_ok=True)
        self.configure(name)

    def configure(self, name):
        """ Initiates the logger

        Args:
            name(str): The name for the logger
        """
        self.file_name = {}

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        path = self._path.joinpath('%s.log' % name)
        i = 0
        while path.exists():
            i += 1
            path = path.parent.joinpath('%s_%s.log' % (i, name))

        self.file_name['debug'] = str(path.parts[-1])

        path_err = self._path.joinpath('%s_err.log' % name)
        i = 0
        while path_err.exists():
            i += 1
            path_err = path.parent.joinpath('%s_%s_err.log' % (i, name))

        self.file_name['error'] = str(path_err.parts[-1])

        fh = logging.FileHandler(str(path.absolute()))
        fh.setLevel(logging.DEBUG)
        fh_err = logging.FileHandler(str(path_err.absolute()))
        fh_err.setLevel(logging.ERROR)

        formatter = logging.Formatter('%(levelname)s[%(asctime)s]%(message)s',
                                      datefmt='%m/%d/%Y_%H:%M:%S')
        fh.setFormatter(formatter)
        fh_err.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(fh_err)

        self._logger = logger

    def _close(self):
        """ Closes all the handlers
        """
        for handler in self._logger.handlers:
            handler.close()

    def _newLogEntry(self, message: str, level: str):
        """ Add a log with specific level

        Args:
            message(str): the message to be logged.
            module(str): The origin module(test case, etc...) of the message.
            level(str): The level of the logged message.
        """

        if level is logging.ERROR:
            self._logger.error(message)
            self.test_errors.append(message)
        elif level is logging.DEBUG:
            self._logger.debug(message)
        elif level is logging.INFO:
            self._logger.info(message)
        elif level is logging.WARNING:
            self._logger.warning(message)
        self._close()

    def debug(self, message: str):
        """ Add a log with DEBUG level

        Args:
            message(str): the message to be logged.
            module(str): The origin module(test case, etc...) of the message.
        """
        self._newLogEntry(message, logging.DEBUG)

    def info(self, message: str):
        """ Add a log with INFO level

        Args:
            message(str): the message to be logged.
            module(str): The origin module(test case, etc...) of the message.
        """
        self._newLogEntry(message, logging.INFO)

    def warning(self, message: str):
        """ Add a log with WARNING level

        Args:
            message(str): the message to be logged.
            module(str): The origin module(test case, etc...) of the message.
        """
        self._newLogEntry(message, logging.WARNING)

    def error(self, message: str, error_at: str):
        """ Add a log with ERROR level

        Args:
            message(str): the message to be logged.
        """
        self._newLogEntry("%s at %s " % (message, error_at),
                          logging.ERROR)

    def file_path(self, type_name: str = None, is_relative: bool = False):
        """ Returns full path to specified logger file
        Args:
            type_name(str): type of logger (debug, error)
        """
        if type_name is None:
            path = [self._path.joinpath(self.file_name['debug']),
                    self._path.joinpath(self.file_name['error'])]
        else:
            path = self._path.joinpath(self.file_name[type_name])

        if is_relative:
            if isinstance(path, WindowsPath):
                path = "/".join(path.parts[-3:])
            else:
                path[0] = "/".join(path[0].parts[-3:])
                path[1] = "/".join(path[1].parts[-3:])

        return path
