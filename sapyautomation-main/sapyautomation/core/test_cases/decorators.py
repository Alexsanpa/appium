import functools
import types
from unittest import SkipTest
from datetime import datetime, timedelta

from sapyautomation.core import LazyReporter, LazySettings
from sapyautomation.core.utils.general import PackedData


def pause(reason: str):
    """ Unconditionally pause a test.

    Args:
        reason(str): pause reason message
    """
    def decorator(test_item):
        if not isinstance(test_item, type):
            @functools.wraps(test_item)
            def pause_wrapper(*args, **kwargs):
                raise SkipTest('Paused: %s' % reason)
            test_item = pause_wrapper
        parent_class = get_class_in_decorator(str(test_item))

        lock = PackedData('%s_%s' % (LazyReporter(parent_class).uid,
                                     parent_class), auto_save=True)
        test_item.__unittest_skip__ = True
        test_item.__unittest_skip_why__ = 'Paused: %s' % reason
        lock.replace_or_append('status', 'paused')
        if not lock.key_exists('pauses'):
            lock.append('pauses', [test_item.__name__, ])
        else:
            data = lock.get('pauses')
            if test_item.__name__ not in data:
                data.append(test_item.__name__)
                lock.replace('pauses', data)
        return test_item

    if isinstance(reason, types.FunctionType):
        test_item = reason
        reason = ''
        return decorator(test_item)

    return decorator


def get_class_in_decorator(func_str: str) -> str:
    """ Extracts parent class from object string

    Args:
        func_str(str): object string

    Returns(str): parent class name

    """
    obj_str = func_str.split(' ')[1]
    return obj_str.split('.')[0]


def pause_if(condition: bool, reason: str):
    """ Pause a test if the condition is true.

    Args:
        condition(bool): true or false condition value.
        reason(str):  pause reason message
    """
    def decorator(function):
        def wrapper(self):
            if self.resumed_test is None:
                lock = PackedData('%s_%s' % (
                    LazyReporter(self.__class__.__name__).uid,
                    self.__class__.__name__), auto_save=True)
            else:
                lock = PackedData(self.resumed_test, auto_save=True)

            if condition:
                lock.replace_or_append('status', 'paused')
                if not lock.key_exists('pauses'):
                    lock.append('pauses', [function.__name__, ])
                else:
                    data = lock.get('pauses')
                    if function.__name__ not in data:
                        data.append(function.__name__)
                        lock.replace('pauses', data)
                raise self.skipTest('Paused: %s' % reason)

            lock.clean_up()
            return function(self)
        return wrapper
    return decorator


def pause_until(days: int = 0, hours: int = 0, minutes: int = 0):
    """ Pause a test if paused execution been n days-hours-minutes ago.

    Args:
        days(int): day to pause.
        hours(int): hours to pause.
        minutes(int): minutes to pause.
    """
    def decorator(function):
        def wrapper(self):
            actual_dt = datetime.now()
            if self.resumed_test is None:
                lock = self._lock._lock
                target_dt = datetime.now() + timedelta(
                    days=days,
                    hours=hours,
                    minutes=minutes)
                lock.replace_or_append('target_datetime', target_dt.strftime(
                    LazySettings().TIMESTAMP_FORMAT))

            else:
                lock = PackedData(self.resumed_test, auto_save=True)
                target_dt = datetime.strptime(lock.get('target_datetime'),
                                              LazySettings().TIMESTAMP_FORMAT)

            difference = target_dt - actual_dt

            if difference.total_seconds() > 0:
                lock.replace_or_append('status', 'paused')
                if not lock.key_exists('pauses'):
                    lock.append('pauses', [function.__name__, ])
                else:
                    data = lock.get('pauses')
                    if function.__name__ not in data:
                        data.append(function.__name__)
                        lock.replace('pauses', data)
                raise self.skipTest('Paused until: %s' % target_dt)

            lock.clean_up()
            return function(self)
        return wrapper
    return decorator


def ignore_in_resume(_):
    """ This decorator gets func empty """
    return _id


def _id(obj=None):
    """ returns a callable object when needed
    """
    return obj
