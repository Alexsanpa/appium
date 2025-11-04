"""
General utils
"""
import sys
import inspect
from time import sleep
from pathlib import Path
import msgpack

from sapyautomation.core.management.conf import LazySettings


def unique_path(path: str):
    """ Validates if the path doesn't exist, if it exists adds an index
    until the path becomes unique.
    Args:
        path: absolute path to validate as unique.
    """
    original_path = Path(path)
    unique_name = original_path.parts[-1]
    original_path = original_path.parent

    new_path = original_path.joinpath(unique_name)
    original_parts = len(unique_name.split('_'))

    index = 0
    while new_path.exists():
        parts = unique_name.split('_')
        if len(parts) >= original_parts:
            parts = parts[1:]

        unique_name = '%s_%s' % (index, '_'.join(parts))
        new_path = original_path.joinpath(unique_name)

    return str(new_path)


def wait(seconds=None):
    """
    Wait run time N seconds.
    """
    sleep(seconds)


def get_resource(file_name: str, skip_user_res: bool = False) -> str:
    """ Looks if a resource exists

    First this method looks for the resource in user's project and
    if it does not exist would look on framework's default resources.

    Args:
        file_name(str): resource's filename with extension to look for.
        skip_user_res(bool): if 'True' skips lookup in user's project path.

    Returns:
        resource absolute path

    Raises:
        FileExistsError if resource doesn't exists.

    """
    user_path = Path(LazySettings().PROJECT_PATH).joinpath('resources')
    extra_path = LazySettings().EXTRA_RESOURCES_PATH
    default_path = Path(__file__).parent.parent.joinpath('management',
                                                         'resources')

    user_path = user_path.joinpath(file_name)
    extra_path = None if extra_path is None \
        else Path(extra_path).joinpath(file_name)
    default_path = default_path.joinpath(file_name)

    if not skip_user_res and user_path.exists():
        resource_path = str(user_path.absolute())
    elif extra_path is not None and extra_path.exists():
        resource_path = str(extra_path.absolute())
    elif default_path.exists():
        resource_path = str(default_path.absolute())
    else:
        raise FileExistsError("resource '%s' don't exists" % file_name)

    return resource_path


def get_locks(only_last: bool = False):
    files = [f for f in LazySettings().LOCK_PATH.iterdir() if f.is_file()]

    if only_last and len(files) > 0:
        return [sorted(files)[-1], ]

    return files


def get_locks_by_name(name: str, only_last: bool = False):
    """ Returns all lockfiles that contains 'name'
    Args:
        name(str): class name of test
        only_last(bool): flag to retrieve only last lock file
    """
    files = [file for file in get_locks(only_last)
             if name == str(file).split('_')[-1]]

    return files


def get_source_lines(method):
    """ Gets source code from specific method

    Gets source code from method and class-relative line number.

    Args:
        method: method object to analyze
    """
    class_source = inspect.getsource(
        sys.modules[method.__module__]).split('\n')
    case_source = inspect.getsource(
        getattr(method, method._testMethodName)).split('\n')
    i = 1
    for line in class_source:
        if case_source[0] in line:
            break
        i += 1

    source_list = []
    for line in case_source:
        line = line.split('#')[0].strip()
        if line != '' or None:
            source_list.append('%s:%s' % (i, line))
        i += 1

    return [line.split(':') for line in source_list if 'def ' not in line]


class PackedData:
    """ Serialize data

    Args:
        name(str): name of the file where the data can be saved
        data(dict): data to be serialized
        auto_save(bool): flag to do auto save on every change.
    """
    def __init__(self, name: str, data: dict = None, auto_save: bool = False):
        self._data = {} if data is None else data
        self._path = LazySettings().LOCK_PATH.joinpath('.%s' % name)
        self._auto_save = auto_save
        if self.file_exists:
            self.readFromFile()

    @property
    def file_exists(self):
        return self._path.exists()

    def get(self, key):
        """ gets the value of a key from data
        Args:
            key(str): key to look for.
        """
        if self.key_exists(key):
            return self._data[key]

        return None

    def remove(self, key):
        """ removes a key from data
        Args:
            key(str): key to remove.
        """
        self._data.pop(key)
        if self._auto_save:
            self.saveToFile()

    def append(self, key, value):
        """ append a kay and value to data
        Args:
            key(str): key to append.
            value(str): value of key
        """
        if key not in self._data.keys():
            self._data[key] = value

        if self._auto_save:
            self.saveToFile()

    def replace_or_append(self, key, value):
        """ replace or append a value of a key from data
        Args:
            key(str): key to append or replace.
            value(str): value of key
        """
        if self.get(key) is None:
            self.append(key, value)

        else:
            self.replace(key, value)

    def key_exists(self, key: str) -> bool:
        """ returns boolean if key exists
        Args:
            key(str): key to check.
        """
        if key in self._data.keys():
            return True

        return False

    def keys(self) -> list:
        """ returns a list of keys """
        return self._data.keys()

    def replace(self, key, value):
        """ replace a value of a key from data
        Args:
            key(str): key to replace.
            value(str): value to replace with
        """
        if key in self._data.keys():
            self._data[key] = value

        if self._auto_save:
            self.saveToFile()

    def saveToFile(self):
        """ saves data to bin file"""
        with open(str(self._path), 'wb') as out_file:
            msgpack.pack(self._data, out_file)

    def readFromFile(self):
        """ reads bin data from file """
        with open(str(self._path), 'rb') as out_file:
            self._data = msgpack.unpack(out_file)

    def clean_up(self):
        """
        Wipe all data
        """
        self._data = {}
        if self.file_exists:
            self._path.unlink()
