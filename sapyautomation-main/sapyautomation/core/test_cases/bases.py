import abc
import inspect
import unittest
from unittest import TestCase, TestSuite
from typing import List, Union
from logging import ERROR, DEBUG, INFO, WARNING
from datetime import datetime

from sapyautomation.core.watchers.tracker import TrackerMeta
from sapyautomation.core import LazyReporter
from sapyautomation.core.utils.general import PackedData, get_locks_by_name,\
    get_resource
from sapyautomation.core.test_cases.decorators import ignore_in_resume
from sapyautomation.core.utils.strings import string_to_pep_convention,\
    Convention, wrap_text
from sapyautomation.core.management.conf import LazySettings
from sapyautomation.desktop.files import SpreadSheetData


class BaseLock:
    """ Base lock object
    """
    def __init__(self, uid: str, name: str):
        self._lock = PackedData(f"{uid}_{name}", auto_save=True)
        self._uid = uid
        self._name = name

    @property
    def status(self):
        """ Returns status
        """
        return self._lock.get('status')

    def add_attribute(self, name: str, value: str):
        """ Adds custom attribute to lock file
        """
        try:
            self._lock.replace_or_append(name, value)

        except TypeError:
            print(f"'{name}' isn't a serializeable element.")
            self._lock.replace_or_append(name, None)

    def get_attribute(self, name: str):
        """ Adds custom attribute to lock file
        """
        return self._lock.get(name)

    def add_step(self, step: str):
        """ Registers a step
        """
        data = self.get_steps()

        if step not in data:
            data.append(step)

        self._lock.replace_or_append('steps', data)

    def add_runned_step(self, step: str, description: str):
        """ Registers a runned step
        """
        steps, info = self.get_runned_steps()

        if step not in steps:
            self.last_step = step
            steps.append(step)
            info[step] = description

        self._lock.replace_or_append('runned_steps', steps)
        self._lock.replace_or_append('runned_steps_info', info)

    def get_steps(self):
        """ Gets a list of test's steps
        """
        return self._lock.get('steps') \
            if self._lock.key_exists('steps') else []

    def get_runned_steps(self):
        """ Gets a list of runned steps
        """
        steps = self._lock.get('runned_steps') \
            if self._lock.key_exists('runned_steps') else []
        info = self._lock.get('runned_steps_info') \
            if self._lock.key_exists('runned_steps_info') else {}

        return steps, info

    def set_pause(self):
        """ Set status to 'paused'
        """
        self._lock.replace_or_append('status', 'pause')

    def set_resume_status(self):
        """ Set status to resumed execution status
        """
        status = self._lock.get('resume_status')

        if status is not None and status == 'success':
            self.set_success()

        elif status is not None and status == 'failed':
            self.set_failed(self.last_step, 'Resume failed')

    def get_resume(self, previous_run: str) -> tuple:
        """ Gets necesary data to resume execution

        Args:
            previous_run(str): Execution name to be resumed.

        """
        self._lock.replace_or_append('previous_run', previous_run)
        self.resume_lock = PackedData(previous_run, auto_save=True)

        return ((attr, self.resume_lock.get(attr))
                for attr in self.resume_lock.keys()
                if attr not in ('status', 'steps', 'target_datetime',
                                'pauses'))

    def set_success(self):
        """ Set status to 'success'
        """
        self._lock.replace_or_append('status', 'success')

    def set_failed(self, failed_step: str, msg: str):
        """ Set status to 'failed'

        Args:
            failed_step(str): name of the failed step.

        """
        self._lock.replace_or_append('status', 'failed')
        self._lock.replace_or_append('failure', failed_step)
        self._lock.replace_or_append('failure_msg', msg)


class BaseTestCases(TestCase, metaclass=TrackerMeta):
    """ Base class for test cases.

    Args:
        methodName(`str`): required argument for `TestCase` override.
    """
    _current_step = (None, True)

    def __init__(self, methodName='runTest', ignore_steps=None,
                 resumed_test=None, data_file=None, exec_id=None):
        if data_file is not None or data_file == '':
            self._lock = BaseLock(self.__reporter.uid, self._testcase)

            self.build_case_data(methodName, data_file)
            self.build_resume_case_data(resumed_test, ignore_steps)

            self._lock.add_attribute('exec_id', exec_id)
            self._lock.add_attribute('test_id', self.test_id)
            self._lock.add_attribute('test_name', self.test_name)
            self._lock.add_attribute('test_video', '')
            test_report = "%s_%s.%s" % (
                self.__reporter.uid, self._testcase,
                'docx' if LazySettings().REPORT_DOCX_FORMAT else 'pdf')
            self._lock.add_attribute('test_report', test_report)

            self.__reporter.add_registry_data(self._testcase, self.__index)
            self.__reporter.save_evidence_report()

            TestCase.__init__(self, methodName=methodName)

    def build_case_data(self, test_method: str, data_file: str):
        """ Gathers test case data

        Args:
            test_method(str): test method name.
            data_file(str): data file path.

        """
        self.__index = 0

        try:
            while self.__index in self.__reporter.get_test_data(
                    self._testcase):
                self.__index += 1
        except KeyError:
            pass

        raw_id = self.__module__.split('.')[-1].split('_')[1]
        try:
            self.test_id = float(raw_id)

        except ValueError:
            self.test_id = raw_id

        self.test_name = None
        try:
            data = SpreadSheetData(get_resource(LazySettings().TESTS_DATA))
            self.test_name = data.get_row_by_value(0, self.test_id)[1]

        except (FileExistsError, TypeError):
            pass

        try:
            doc = self.__doc__
            if self.test_name is None and doc != "":
                self.test_name = doc

        except TypeError:
            pass

        if self.test_name is None:
            self.test_name = self.__module__.split('.')[-1]

        steps = [line.strip()
                 for line in inspect.getsource(
                     getattr(self, test_method)).split('\n')
                 if 'step_' in line]

        for step in steps:
            self._lock.add_step(step[5:-2])

        if data_file == '':
            msg = "Data set: Using environment parameters"

        elif data_file is not None:
            msg = 'Data set: %s' % data_file
            self.log(msg)
            self.data_file = data_file.absolute()
            self.data_file_name = str(self.data_file)
            self.add_to_result('data_file_name')
            self._lock.add_attribute('test_description',
                                     self.get_test_description())

    def get_test_description(self):
        description = self.data_file_name.split('\\')[-1].split('_')[0]
        description = ' '.join(description.split('-'))

        return description

    def build_resume_case_data(self, resumed_test: str, ignore_steps: list):
        """ Gathers resumed test data

        Args:
            resumed_test(str): resumed test uuid.
            ignore_steps(str): steps to be ignored.

        """
        self.resumed_test = resumed_test
        self.__ignore_steps = ignore_steps if ignore_steps else []
        if resumed_test is not None:
            self.__resume_case()

    def _callSetUp(self):
        """ Set Up caller
        """
        self.setUp()
        if self.resumed_test is not None:
            self.on_resume()

    def __getattribute__(self, item):
        """ Override to catch 'assert' methods.

        This override would gather evidence from every 'assert'.

        Args:
            item(`str`): the called attribute's name by `__get__`.

        Returns:
            The requested attribute. If the attribute is an assert is
            returned wrapped with `get_evidence`
        """
        attr = object.__getattribute__(self, item)
        # TODO log attribus that are variable definitions pylint: disable=fixme
        lock_data = None
        if item == 'run':
            self.__reporter.current_test = self._testMethodName
            self.__reporter.add_to_log('', DEBUG)
            self.__reporter.add_to_log("Test '%s' started from '%s'" %
                                       (self._testMethodName,
                                        self._testcase),
                                       DEBUG)
            if self._lock.status is None:
                self._lock.set_success()  # is a success unless another pops

            if LazySettings().TEST_RECORDING_ENABLED:
                self.start_record()
        elif item == 'failureException':
            self._current_step = (self._current_step[0], False)

        elif item == 'doCleanups':
            self._current_step = (self._current_step[0], False)
            for attr_name in dir(self.__class__):
                if attr_name not in dir(self.__class__.__bases__[0]) \
                        and not callable(getattr(self, attr_name)) \
                        and not attr_name.startswith('tearDown') \
                        and not attr_name.startswith('_'):
                    _attr = getattr(self, attr_name)
                    if 'BasePom' not in [
                            base.__name__
                            for base in inspect.getmro(_attr.__class__)]:

                        self._lock.add_attribute(attr_name, _attr)

            if LazySettings().TEST_RECORDING_ENABLED:
                self.stop_record()

        elif 'step_' in item and self._current_step[1] is True:
            # TODO: optimize if-statements
            if self._current_step[1] is True:
                if item in self.__ignore_steps:
                    self.__reporter.add_to_log('Step skipped: %s' % ' '.join(
                        item.split('_')[1:]), DEBUG)
                    attr = ignore_in_resume(attr)

                else:
                    self._current_step = (item, True)
                    step_parts = item.split('_')
                    self.__reporter.add_to_log(
                        f"Step {step_parts[1]}: {' '.join(step_parts[2:])}",
                        DEBUG)

                    self._lock.add_runned_step(item, attr.__doc__)

            elif item not in self.__ignore_steps:
                self._lock.add_runned_step(item, attr.__doc__)

        if lock_data is not None and self._lock.status != 'paused':
            self._lock.set_resume_status()

        return attr

    @abc.abstractmethod
    def on_resume(self):
        """ Hook method for setting up the test case for resumming execution
        """

    def on_error(self, failures, errors):
        """ Actions to be taken if test fails or error rises
        """
        try:
            lines = errors[0].test_exception_info.split('\n')

        except IndexError:
            lines = failures[0].get_error_info().split('\n')

        for i in range(len(lines)):
            line = lines[-i]
            if 'step_' in line:
                self._current_step = (f"step_{line.split('step_')[1]}", False)
                break

        # self.get_evidence(logger_level=ERROR)
        if LazySettings().TEST_RECORDING_ENABLED:
            self.stop_record()

        self.__reporter.add_to_log(lines[-2], ERROR, self._current_step[0])
        errors_msg = []
        for item in failures + errors:
            try:
                errors_msg.append(str(item.err[1]))

            except AttributeError:
                errors_msg.append(item[1].split('\n')[-2])

        self._lock.set_failed(self._current_step[0], errors_msg[-1])

    def start_record(self):
        """ Starts evidence recorder
        """
        record_path = self.__reporter.start_record(self._testcase,
                                                   self._testMethodName,
                                                   self.__index)
        record_path = '/'.join(record_path.split('/')[-2:])
        self._lock.add_attribute('test_video', record_path)
        self.__reporter.add_to_log("Evidence: recording started", DEBUG)

    def stop_record(self):
        """ Stops evidence recorder
        """
        evidence = self.__reporter.stop_record()
        self.__reporter.add_to_log("Evidence: record saved in "
                                   f"'{evidence['path']}'", DEBUG)
        self.__reporter.add_to_log(
            f"Evidence: record saved with {evidence['framerate']} fps and "
            f"{evidence['lostframes']} frames lost", DEBUG)

    def get_evidence(self, await_before: float = 0.1,
                     label: str = "",
                     await_after: float = 0.1, logger_level=DEBUG,
                     asynchronous: bool = False):
        """ Takes evidence

        Args:
            await_before(float): seconds to await before taking evidence
            await_after(float): seconds to await after taking evidence
            logger_level: logger level to be used when logging evidence

        """
        evidence = self.__reporter.save_evidence(self._testcase,
                                                 self._testMethodName,
                                                 await_before, await_after,
                                                 self.__index, asynchronous)
        label = label.replace('\n', ' ')
        self.__reporter.add_to_log(
            f"Evidence: screenshot saved in '{evidence}' |{label}",
            logger_level)

    def add_label(self, label: str = "", logger_level=DEBUG, newline=False):
        """ Add text/label to a specific step on the log debug

        Args:
            label(string): label/text to add on step
            logger_level: logger level to be used when logging evidence

        """
    
        if newline:
            label = label.split('\n')
            for line in label:
                line = line.replace('\n', ' ')
                self.__reporter.add_to_log(
                    f"Label: added text | {line}",
                    logger_level)
        else:
            label = label.replace('\n', ' ')
            self.__reporter.add_to_log(
                    f"Label: added text | {label}",
                    logger_level)

    def add_3pa_data(self, test_id: str, name: str, system: str,
                     description: str, category: str, team: str):
        """ Adds registry of 3rd party application

        Args:
            test_id(str): test id
            name(str): test name
            system(str): system/platform name of test
            description(str): description of 3pa
            category(str): category of 3pa
            team(str): Process team of the test

        """
        self.__3pa_data = True
        self._3pa_data = {
            'id': test_id,
            'name': name,
            'system': system,
            'description': description,
            'category': category,
            'process_team': team
        }

        self.add_to_result('_3pa_data')

    def add_to_result(self, attribute: str):
        """ Saves attribute to lockfile

        Args:
            attribute(str): attribute name to save
        """
        if hasattr(self, attribute):
            self._lock.add_attribute(attribute, getattr(self, attribute))

    def __resume_case(self):
        """ Adds attributes from resumed case """
        resume_data = self._lock.get_resume(self.resumed_test)

        for attr in resume_data:
            setattr(self, attr[0], attr[1])

    @staticmethod
    def get_case_data(case_class: str):
        """ Returns data from last success execution from specific case.

        Args:
            case_class(str): class name of the required test.
        """
        timestamp = None
        file = None

        for lockfile in get_locks_by_name(case_class):
            lockfile = lockfile.parts[-1][1:]
            data = PackedData(lockfile)
            time = datetime.strptime(' '.join(lockfile.split('_')[:-1]),
                                     "%Y-%m-%d %H-%M-%S")
            if timestamp is None:
                timestamp = time
            if data.get('status') == 'success' and \
                    timestamp <= time:
                timestamp = time
                file = lockfile

        data = PackedData(file)

        return data

    def log(self, msg: str):
        """ Logger access for user test case

        Arg:
            msg(str): The message that will be logged.
        """
        self.__reporter.add_to_log(msg, self._current_step[0])

    @property
    def _testcase(self):
        """ Test case class name """
        return self.__class__.__name__

    @property
    def __reporter(self):
        """ Dynamic load of reporter object """

        return LazyReporter(self._testcase)


class BaseRunner:
    """ Base object for runners
    """
    suite = None
    runner = None
    type_test_cases = Union[unittest.TestCase, List[unittest.TestCase]]
    tests = []

    def create_suite(self, test_cases: type_test_cases):
        """Returns a test suite from a test_load.

        Args:
            test_case(type_test_cases) the test cases suite from a
            unittest.TestCase subclass
        """
        self.suite = TestSuite()
        for test_case in test_cases:
            for case in test_case[1]:
                self.suite.addTest(test_case[0](methodName=case,
                                                ignore_steps=test_case[2],
                                                resumed_test=test_case[3],
                                                data_file=test_case[4],
                                                exec_id=test_case[5]))
                if test_case[0].__name__ not in self.tests:
                    self.tests.append(test_case[0].__name__)
                self.runner.on_error = self.suite._tests[-1].on_error

    def prepare_run(self):
        """ The preparations necessary before run. Subclasses must implement
        this method.
        """
        raise NotImplementedError(
            'subclasses of BaseRunner must provide a prepare_run() method')

    def run(self):
        """Runs a specific test suite with specific HTML runner.

        Raises:
            AttributeError: if the given object 'runner' has no module
            called 'run' to check if it is a valid runner

        """
        try:
            self.prepare_run()
            return self.runner.run(self.suite)

        except AttributeError:
            raise AttributeError("'suite' has no module 'run'")

        except KeyboardInterrupt:
            self.runner.on_error()
            raise KeyboardInterrupt()


class BasePom:
    """ Base class for POM objects

    Args:
        test_case_class_name(str): Name of the base test case class
            (SapTestCase)
    """
    def __init__(self):
        self._reporter = LazyReporter()

    def log(self, message: str):
        """ Adds a DEBUG entry to the logger
        Args:
            message(str): message to be added.
        """
        self._reporter.add_to_log(message, DEBUG)

    def log_info(self, message: str):
        """ Adds a INFO entry to the logger
        Args:
            message(str): message to be added.
        """
        self._reporter.add_to_log(message, INFO)

    def log_warning(self, message: str):
        """ Adds a WARNING entry to the logger
        Args:
            message(str): message to be added.
        """
        self._reporter.add_to_log(message, WARNING)

    def log_error(self, message: str):
        """ Adds a ERROR entry to the logger
        Args:
            message(str): message to be added.
        """
        self._reporter.add_to_log(message, ERROR)


class BaseTestData:
    """ Base class to manage data for test data

    Args:
        test_name(str): Test name to be used for module and class naming.
        module_docstring(str): docstring text for module.
        class_docstring(str): docstring text for class.

    """
    data = {}

    def __init__(self, test_name: str, module_docstring: str,
                 class_docstring: str):
        module_name = string_to_pep_convention(test_name,
                                               Convention.under_score)
        class_name = string_to_pep_convention(test_name,
                                              Convention.camel_case).title()
        self.data['module'] = (module_name, self._wrap_doc(module_docstring,
                                                           80))
        self.data['class'] = (class_name, self._wrap_doc(class_docstring, 76))
        self.data['steps'] = []

    @staticmethod
    def _wrap_doc(text: str, char_count: int = 71) -> list:
        """ Wraps docstring text to code conventions

        Args:
            text(str): text to be wrapped.
            char_count(int): max char count for line wrapping.

        Returns: wrapped text lines

        """
        doc_lines = []
        first_line = True
        for line in text.split('\n'):
            if first_line:
                doc_lines = doc_lines + wrap_text(line, char_count-4)
                first_line = False
            else:
                doc_lines = doc_lines + wrap_text(line, char_count)

        return doc_lines

    def add_step(self, name: str, description: str, expected_result: str):
        """ Registers step data

        Args:
            name(str): step name.
            description(str): description of step.
            expected_result(str): description of expected result.

        """
        docstring = self._wrap_doc(
            "Description: %s\nExpected result: %s" % (description,
                                                      expected_result))

        self.data['steps'].append((name.lower(), docstring))

    def get_module(self):
        """ Gets module data (name, docstring)
        """
        return self.data['module']

    def get_class(self):
        """ Gets class data (name, docstring)
        """
        return self.data['class']

    def get_steps(self):
        """ Gets step data list (name, docstring)
        """
        return self.data['steps']

    def get_step(self, index: int):
        """ Gets step data (name, docstring)

        Args:
            index(int): index of the step.

        """
        return self.data['steps'][index]
