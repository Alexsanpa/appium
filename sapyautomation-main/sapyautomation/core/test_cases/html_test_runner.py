"""
Test runnner with HTML reporting
"""

import sys
import time
from datetime import datetime
from typing import List, Union

from sapyautomation.core import LazyReporter

from .result import HtmlTestResult
from .text_test_runner import TextTestRunner
from .bases import BaseRunner
from . import BaseTestCases

UTF8 = "UTF-8"


class HtmlRunner(BaseRunner):
    suite = None
    runner = None
    type_test_cases = Union[BaseTestCases, List[BaseTestCases]]

    def __init__(self, template: str, report_name: str = "SAPy",
                 combine_reports: bool = True, add_timestamp: bool = True):
        """Initialize method creates the html runner

        Args:
            combine_reports -- if we want one test for everything or one for
            each test (default True)
            report_name -- the name of the html file (default "SAPy")
            add_timestamp -- add time in the html file name (default True)
        """
        self.runner = HTMLTestRunner(
            output=LazyReporter().paths['report_path'],
            combine_reports=combine_reports,
            report_name=report_name,
            template=template,
            template_args=None,
            add_timestamp=add_timestamp,
            open_in_browser=False
        )

    def prepare_run(self):
        """ Makes preparations for the runner"""
        data = {'sapy_title': 'Testing Automation Results',
                'sapy_cases_source': {},
                'sapy_cases_log': {},
                'sapy_cases_evidence': {},
                'sapy_cases_evidence_report': {},
                'sapy_test_uid': LazyReporter().uid,
                'sapy_resumed_from': {}}

        for case in self.suite:
            rdata = LazyReporter(
                case.__class__.__name__).case_report(case)
            for dkey in rdata.keys():
                for ckey in rdata[dkey]:
                    if ckey not in data[dkey].keys():
                        data[dkey][ckey] = rdata[dkey][ckey]

        self.runner.template_args = data


class HTMLTestRunner(TextTestRunner):\
        # pylint: disable=too-many-instance-attributes
    """" A test runner class that output the results. """

    time_format = "%Y-%m-%d_%H-%M-%S"

    def __init__(self,  # pylint: disable=too-many-arguments
                 output="./reports/", verbosity=2, stream=sys.stderr,
                 descriptions=True, failfast=False, buffer=False,
                 report_title=None, report_name=None, template=None,
                 resultclass=None, add_timestamp=True, open_in_browser=False,
                 combine_reports=False, template_args=None):

        self.verbosity = verbosity
        self.output = output
        self.encoding = UTF8

        TextTestRunner.__init__(self, stream, descriptions, verbosity,
                                failfast=failfast, buffer=buffer)

        if add_timestamp:
            self.timestamp = time.strftime(self.time_format)
        else:
            self.timestamp = ""

        if resultclass is None:
            self.resultclass = HtmlTestResult
        else:
            self.resultclass = resultclass

        if template_args is not None and not isinstance(template_args, dict):
            raise ValueError("template_args must be a dict-like.")
        self.template_args = template_args or {}

        self.report_title = report_title or "Unittest Results"
        self.report_name = report_name
        self.template = template

        self.open_in_browser = open_in_browser
        self.combine_reports = combine_reports

        self.start_time = 0
        self.duration = 0

    def _make_result(self):
        """ Create a TestResult object which will be used to store
        information about the executed tests. """
        return self.resultclass(self.stream, self.descriptions, self.verbosity)

    def run(self, test):
        """ Runs the given testcase or testsuite. """
        try:

            result = self._make_result()
            result.failfast = self.failfast
            if hasattr(test, 'properties'):
                # junit testsuite properties
                result.properties = test.properties

            self.stream.writeln()
            self.stream.writeln("Running tests... ")
            self.stream.writeln(result.separator2)

            self.start_time = datetime.now()
            test(result)
            stop_time = datetime.now()
            self.duration = stop_time - self.start_time

            result.printErrors()
            self.stream.writeln(result.separator2)
            run = result.testsRun
            self.stream.writeln("Ran {} test{} in {}".format(
                run, run != 1 and "s" or "", str(self.duration)[:7]))
            self.stream.writeln()

            expectedFails = len(result.expectedFailures)
            unexpectedSuccesses = len(result.unexpectedSuccesses)
            skipped = len(result.skipped)
            paused = len(result.paused)

            infos = []
            if not result.wasSuccessful():
                self.stream.writeln("FAILED")
                failed, errors = map(len, (result.failures, result.errors))
                if failed:
                    infos.append("Failures={0}".format(failed))
                if errors:
                    infos.append("Errors={0}".format(errors))
                self.on_error(result.failures, result.errors)
            else:
                self.stream.writeln("OK")

            if skipped-paused > 0:
                infos.append("skipped=%d" % skipped)
            if paused:
                infos.append("paused=%d" % paused)
            if expectedFails:
                infos.append("Expected Failures={}".format(expectedFails))
            if unexpectedSuccesses:
                infos.append(
                    "Unexpected Successes={}".format(unexpectedSuccesses))

            if infos:
                self.stream.writeln(" ({})".format(", ".join(infos)))
            else:
                self.stream.writeln("\n")

            self.stream.writeln()
            self.stream.writeln('Generating HTML reports... ')
            result.generate_reports(self)
            if self.open_in_browser:
                import webbrowser
                for report in result.report_files:
                    webbrowser.open_new_tab('file://' + report)
        finally:
            pass

        return result
