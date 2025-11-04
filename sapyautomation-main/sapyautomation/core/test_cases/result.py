import os
import sys
import time
import traceback
from unittest import result
from HtmlTestRunner.result import (_TestInfo, _SubTestInfos,
                                   render_html,
                                   strip_module_names)

from sapyautomation.core.utils.general import unique_path


class TestResult(result.TestResult):
    """ Base test result class """

    def __init__(self, stream, descriptions, verbosity):
        super(TestResult, self).__init__(stream, descriptions, verbosity)
        self.paused = []

    def addPause(self, test, reason):
        """ Register a paused case """
        reason = reason.split('Paused')[1].strip()
        self.paused.append((test, reason))

        if self.showAll:  # pylint: disable=no-member
            self.stream.writeln(  # pylint: disable=no-member
                "paused {0!r}".format(reason))

        elif self.dots:  # pylint: disable=no-member
            self.stream.write("s")  # pylint: disable=no-member
            self.stream.flush()  # pylint: disable=no-member


class TextTestResult(TestResult):
    """A test result class that can print formatted text results to a stream.

    Used by TextTestRunner.
    """
    separator1 = '=' * 70
    separator2 = '-' * 70

    def __init__(self, stream, descriptions, verbosity):
        super(TextTestResult, self).__init__(stream, descriptions, verbosity)

        self.stream = stream
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        self.descriptions = descriptions

    def getDescription(self, test):
        """ Gets test description
        Args:
            test: Test object
        """
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return '\n'.join((str(test), doc_first_line))

        return str(test)

    def startTest(self, test):
        """ Starts test execution
        Args:
            test: Test object
        """
        super(TextTestResult, self).startTest(test)
        if self.showAll:
            self.stream.write(self.getDescription(test))
            self.stream.write(" ... ")
            self.stream.flush()

    def addSuccess(self, test):
        """ Registers a case success
        Args:
            test: Test object
        """
        super(TextTestResult, self).addSuccess(test)
        if self.showAll:
            self.stream.writeln("ok")
        elif self.dots:
            self.stream.write('.')
            self.stream.flush()

    def addError(self, test, err):
        """ Registers a case error
        Args:
            test: Test object
        """
        super(TextTestResult, self).addError(test, err)
        if self.showAll:
            self.stream.writeln("ERROR")
        elif self.dots:
            self.stream.write('E')
            self.stream.flush()

    def addFailure(self, test, err):
        """ Registers a case failure
        Args:
            test: Test object
        """
        super(TextTestResult, self).addFailure(test, err)
        if self.showAll:
            self.stream.writeln("FAIL")
        elif self.dots:
            self.stream.write('F')
            self.stream.flush()

    def addSkip(self, test, reason):
        """ Registers a case skip
        Args:
            test: Test object
        """
        super(TextTestResult, self).addSkip(test, reason)
        if 'Paused' in reason:
            self.addPause(test, reason)
        elif self.showAll:
            self.stream.writeln("skipped {0!r}".format(reason))
        elif self.dots:
            self.stream.write("s")
            self.stream.flush()

    def addExpectedFailure(self, test, err):
        """ Registers a expected case failure
        Args:
            test: Test object
        """
        super(TextTestResult, self).addExpectedFailure(test, err)
        if self.showAll:
            self.stream.writeln("expected failure")
        elif self.dots:
            self.stream.write("x")
            self.stream.flush()

    def addUnexpectedSuccess(self, test):
        """ Registers a unexpected case success
        Args:
            test: Test object
        """
        super(TextTestResult, self).addUnexpectedSuccess(test)
        if self.showAll:
            self.stream.writeln("unexpected success")
        elif self.dots:
            self.stream.write("u")
            self.stream.flush()

    def printErrors(self):
        """ Prints errors """
        if self.dots or self.showAll:
            self.stream.writeln()
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour, errors):
        """ Prints error list
        Args:
            flavor: type name
            errors: errors list
        """

        for line in self.error_list(flavour, errors):
            self.stream.writeln(line)

    def error_list(self, flavour, errors):

        self.data_list = []
        for test, err in errors:
            self.data_list.append(self.separator1)
            if flavour is None:
                self.data_list.append(self.getDescription(test))

            else:
                self.data_list.append("%s: %s" % (flavour,
                                                  self.getDescription(test)))

            self.data_list.append(self.separator2)
            self.data_list.append("%s" % err)

        return self.data_list


class HtmlTestResult(TextTestResult):\
        # pylint: disable=too-many-instance-attributes
    """ A test result class that express test results in Html. """

    start_time = None
    stop_time = None
    default_prefix = "TestResults_"

    def __init__(self, stream, descriptions, verbosity):
        TextTestResult.__init__(self, stream, descriptions, verbosity)
        self.buffer = True
        self._stdout_data = None
        self._stderr_data = None
        self.successes = []
        self.subtests = {}
        self.callback = None
        self.infoclass = _TestInfo
        self.report_files = []

    def _prepare_callback(self, test_info, target_list, verbose_str,
                          short_str):
        """ Appends a 'info class' to the given target list and sets a
            callback method to be called by stopTest method."""
        tlist = [target for target in target_list if isinstance(target, list)]
        if len(tlist) > 0:
            for target in tlist:
                target.append(test_info)
        else:
            target_list.append(test_info)

        def callback():
            """Print test method outcome to the stream and elapsed time too."""
            test_info.test_finished()

            if self.showAll:
                self.stream.writeln(
                    "{} ({:3f})s".format(verbose_str, test_info.elapsed_time))
            elif self.dots:
                self.stream.write(short_str)

        self.callback = callback

    def getDescription(self, test):
        """ Return the test description if not have test name. """
        return str(test)

    def startTest(self, test):
        """ Called before execute each method. """
        self.start_time = time.time()
        TestResult.startTest(self, test)

        if self.showAll:
            self.stream.write(" " + self.getDescription(test))
            self.stream.write(" ... ")

    def _save_output_data(self):
        try:
            self._stdout_data = sys.stdout.getvalue()
            self._stderr_data = sys.stderr.getvalue()
        except AttributeError:
            pass

    def stopTest(self, test):
        """ Called after excute each test method. """
        self._save_output_data()
        TextTestResult.stopTest(self, test)
        self.stop_time = time.time()

        if self.callback and callable(self.callback):
            self.callback()
            self.callback = None

    def addSuccess(self, test):
        """ Called when a test executes successfully. """
        self._save_output_data()
        self._prepare_callback(self.infoclass(self, test),
                               self.successes, "OK", ".")

    @result.failfast
    def addFailure(self, test, err):
        """ Called when a test method fails. """
        self._save_output_data()
        testinfo = self.infoclass(self, test, self.infoclass.FAILURE, err)
        self._prepare_callback(testinfo, self.failures, "FAIL", "F")

    @result.failfast
    def addError(self, test, err):
        """" Called when a test method raises an error. """
        self._save_output_data()
        testinfo = self.infoclass(self, test, self.infoclass.ERROR, err)
        self._prepare_callback(testinfo, self.errors, 'ERROR', 'E')

    def addSubTest(self, test, subtest, err):
        """ Called when a subTest completes. """
        self._save_output_data()
        if err is None:
            testinfo = self.infoclass(self, test, self.infoclass.SUCCESS,
                                      err, subTest=subtest)
            self._prepare_callback(testinfo, self.successes, "OK", ".")
        else:
            testinfo = self.infoclass(self, test, self.infoclass.FAILURE,
                                      err, subTest=subtest)
            self._prepare_callback(testinfo, self.failures, "FAIL", "F")

        test_id_components = str(test).rstrip(')').split(' (')
        test_id = test_id_components[1] + '.' + test_id_components[0]
        if test_id not in self.subtests:
            self.subtests[test_id] = []
        self.subtests[test_id].append(testinfo)

    def addSkip(self, test, reason):
        """" Called when a test method was skipped. """
        self._save_output_data()
        testinfo = self.infoclass(self, test, self.infoclass.SKIP, reason)
        if 'Paused' in reason:
            self._prepare_callback(testinfo, [self.paused, self.skipped],
                                   "PAUSED", "S")
        else:
            self._prepare_callback(testinfo, self.skipped, "SKIP", "S")

    def error_list(self, flavour, errors):

        self.data_list = []
        for test_info in errors:
            self.data_list.append(self.separator1)
            self.data_list.append(
                '{} [{:3f}s]: {}'.format(flavour, test_info.elapsed_time,
                                         test_info.test_id)
            )
            self.data_list.append(self.separator2)
            self.data_list.append('%s' % test_info.get_error_info())

        return self.data_list

    def _get_info_by_testcase(self):
        """ Organize test results by TestCase module. """

        tests_by_testcase = {}

        subtest_names = set(self.subtests.keys())
        for test_name, subtests in self.subtests.items():
            subtest_info = _SubTestInfos(test_name, subtests)
            testcase_name = ".".join(test_name.split(".")[:-1])
            if testcase_name not in tests_by_testcase:
                tests_by_testcase[testcase_name] = []
            tests_by_testcase[testcase_name].append(subtest_info)

        for tests in (self.successes, self.failures, self.errors,
                      self.skipped):
            for test_info in tests:
                if test_info.is_subtest or test_info.test_id in subtest_names:
                    continue
                if isinstance(test_info, tuple):
                    test_info = test_info[0]
                testcase_name = ".".join(test_info.test_id.split(".")[:-1])
                if testcase_name not in tests_by_testcase:
                    tests_by_testcase[testcase_name] = []
                tests_by_testcase[testcase_name].append(test_info)

        for testcase in tests_by_testcase.values():
            testcase.sort(key=lambda x: x.test_id)

        return tests_by_testcase

    @staticmethod
    def _format_duration(elapsed_time):
        """Format the elapsed time in seconds, or milliseconds if the duration
        is less than 1 second."""
        if elapsed_time > 1:
            duration = '{:2.2f} s'.format(elapsed_time)
        else:
            duration = '{:d} ms'.format(int(elapsed_time * 1000))
        return duration

    def get_results_summary(self, tests):
        """Create a summary of the outcomes of all given tests."""

        failures = errors = skips = successes = 0
        for test in tests:
            outcome = test.outcome
            if outcome == test.ERROR:
                errors += 1
            elif outcome == test.FAILURE:
                failures += 1
            elif outcome == test.SKIP:
                skips += 1
            elif outcome == test.SUCCESS:
                successes += 1

        elapsed_time = 0
        for testinfo in tests:
            if not isinstance(testinfo, _SubTestInfos):
                elapsed_time += testinfo.elapsed_time
            else:
                for subtest in testinfo.subtests:
                    elapsed_time += subtest.elapsed_time

        results_summary = {
            "total": len(tests),
            "error": errors,
            "failure": failures,
            "skip": skips,
            "success": successes,
            "duration": self._format_duration(elapsed_time)
        }
        self.duration = results_summary['duration']
        return results_summary

    def _get_header_info(self, tests, start_time):
        results_summary = self.get_results_summary(tests)

        header_info = {
            "start_time": start_time,
            "status": results_summary
        }
        return header_info

    def _get_report_summaries(self, all_results):
        """ Generate headers and summaries for all given test cases."""
        summaries = {}
        for test_case_class_name, test_case_tests in all_results.items():
            summaries[test_case_class_name] = self.get_results_summary(
                test_case_tests)

        return summaries

    def generate_reports(self, testRunner):
        """ Generate report(s) for all given test cases that have been run. """
        status_tags = ('success', 'danger', 'warning', 'info')
        all_results = self._get_info_by_testcase()
        summaries = self._get_report_summaries(all_results)

        if not testRunner.combine_reports:
            for test_case_class_name, test_case_tests in all_results.items():
                header_info = self._get_header_info(test_case_tests,
                                                    testRunner.start_time)
                html_file = render_html(
                    testRunner.template,
                    title=testRunner.report_title,
                    header_info=header_info,
                    all_results={test_case_class_name: test_case_tests},
                    status_tags=status_tags,
                    summaries=summaries,
                    **testRunner.template_args
                )
                if testRunner.report_name is None:
                    report_name_body = self.default_prefix +\
                        test_case_class_name
                else:
                    report_name_body = test_case_class_name
                self.generate_file(testRunner, report_name_body, html_file)

        else:
            header_info = self._get_header_info(
                [item for sublist in all_results.values() for item in sublist],
                testRunner.start_time
            )
            html_file = render_html(
                testRunner.template,
                title=testRunner.report_title,
                header_info=header_info,
                all_results=all_results,
                status_tags=status_tags,
                summaries=summaries,
                **testRunner.template_args
            )
            if testRunner.report_name is not None:
                report_name_body = testRunner.report_name
            else:
                report_name_body = "_".join(
                    strip_module_names(list(all_results.keys())))
            self.generate_file(testRunner, report_name_body, html_file)

    def generate_file(self, testRunner, report_name, report):
        """ Generate the report file in the given path. """
        dir_to = testRunner.output
        if not os.path.exists(dir_to):
            os.makedirs(dir_to)
        name_parts = report_name.split('.')
        if len(name_parts) > 1:
            report_name = name_parts[-2]
        if testRunner.timestamp:
            report_name = '%s_%s' % (testRunner.timestamp, report_name)

        report_name += ".html"
        path_file = os.path.abspath(os.path.join(dir_to, report_name))
        path_file = unique_path(path_file)

        self.stream.writeln(os.path.relpath(path_file))
        self.report_files.append(path_file)
        with open(path_file, 'w') as report_file:
            report_file.write(report)

    def _exc_info_to_string(self, err, test):
        """
        Converts a sys.exc_info()-style tuple of values into a string.
        This function is overwiting _exc_info_to_string from unittest.result.TestResult
        Updated for python 3.9.11

        Args:
            err (tuple): A tuple containing the exception type, exception value, and traceback.
            test: The test object associated with the exception.

        Returns:
            str: The formatted string representation of the exception.
        """
        exctype, value, tb = err
        tb = self._clean_tracebacks(exctype, value, tb, test)
        tb_e = traceback.TracebackException(
            exctype, value, tb,
            capture_locals=self.tb_locals, compact=True)
        msg_lines = list(tb_e.format())

        if self.buffer:
            try:
                error = sys.stderr.getvalue()
            except AttributeError:
                error = None
            if error:
                if not error.endswith('\n'):
                    error += '\n'
                msg_lines.append(error)
        encoding = getattr(sys.stdout, 'encoding', 'utf-8')
        lines = []
        for line in msg_lines:
            if not isinstance(line, str):
                line = line.encode(encoding)
            lines.append(line)

        return ''.join(lines)