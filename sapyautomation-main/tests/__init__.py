import unittest
import pathlib
import shutil


class BaseTest(unittest.TestCase):
    """ Base test case for unittest
    """
    _resources = pathlib.Path(__file__).parent.joinpath('resources')
    _working_dir = pathlib.Path.cwd()
    _test_dirs = []
    _test_files = []

    @classmethod
    def get_test_resource(cls, resource_path: str) -> pathlib.Path:
        """ Returns absolute path of resource
        Args:
            resource_path(str): relite resource path
        """
        return cls._resources.joinpath(resource_path)

    def add_to_clean_up(self, test_file_path: str = None,
                        test_dir_path: str = None):
        """ Adds file or dir to clean list to be deleted
        when clean_test_data is called
        Warning:
            test_dir_path is idependant to test_file_path.
        Args:
            test_file_path(str): absolute path to file to be added
            test_dir_path(str): absolute path to dir to be added
        """
        if test_file_path:
            self._test_files.append(self._working_dir.joinpath(test_file_path))

        if test_dir_path:
            self._test_dirs.append(self._working_dir.joinpath(test_dir_path))

    def clean_test_data(self):
        """ Deletes files and dirs in clean up list """
        for file in self._test_files:
            pathlib.Path(file).unlink(missing_ok=True)

        for directory in self._test_dirs:
            shutil.rmtree(directory, ignore_errors=True)
