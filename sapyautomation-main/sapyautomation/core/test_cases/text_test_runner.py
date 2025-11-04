"""
Test runnner with HTML reporting
"""
import time
import warnings
import unittest
from unittest.signals import registerResult

from .bases import BaseRunner
from .result import TextTestResult


class TextRunner(BaseRunner):
    """ Wrapper for test runner
    """

    def __init__(self):
        self.runner = TextTestRunner(resultclass=TextTestResult, verbosity=2)

    def prepare_run(self):
        """ Implementation to comply with BaseRunner """


class TextTestRunner(unittest.TextTestRunner):
    """ Runner for test executions
    """
    on_error = object

    def run(self, test):
        "Run the given test case or test suite."
        result = self._makeResult()
        registerResult(result)
        result.failfast = self.failfast
        result.buffer = self.buffer
        result.tb_locals = self.tb_locals
        with warnings.catch_warnings():
            if self.warnings:
                # if self.warnings is set, use it to filter all the warnings
                warnings.simplefilter(self.warnings)
                # if the filter is 'default' or 'always', special-case the
                # warnings from the deprecated unittest methods to show them
                # no more than once per module, because they can be fairly
                # noisy.  The -Wd and -Wa flags can be used to bypass this
                # only when self.warnings is None.
                if self.warnings in ['default', 'always']:
                    warnings.filterwarnings(
                        'module',
                        category=DeprecationWarning,
                        message=r'Please use assert\w+ instead.')
            startTime = time.perf_counter()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()
            try:
                test(result)
            finally:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()
            stopTime = time.perf_counter()
        self.duration = stopTime - startTime
        result.printErrors()
        if hasattr(result, 'separator2'):
            self.stream.writeln(result.separator2)
        run = result.testsRun
        self.stream.writeln("Ran %d test%s in %.3fs" %
                            (run, run != 1 and "s" or "", self.duration))
        self.stream.writeln()

        expectedFails = unexpectedSuccesses = skipped = paused = 0
        try:
            results = map(len, (result.expectedFailures,
                                result.unexpectedSuccesses,
                                result.skipped,
                                result.paused))
        except AttributeError:
            pass
        else:
            expectedFails, unexpectedSuccesses, skipped, paused = results

        infos = []
        if not result.wasSuccessful():
            self.stream.write("FAILED")
            failed, errored = len(result.failures), len(result.errors)
            if failed:
                infos.append("failures=%d" % failed)
            if errored:
                infos.append("errors=%d" % errored)
            self.on_error(result.failures, result.errors)
        else:
            self.stream.write("OK")
        if skipped-paused > 0:
            infos.append("skipped=%d" % skipped)
        if paused:
            infos.append("paused=%d" % paused)
        if expectedFails:
            infos.append("expected failures=%d" % expectedFails)
        if unexpectedSuccesses:
            infos.append("unexpected successes=%d" % unexpectedSuccesses)
        if infos:
            self.stream.writeln(" (%s)" % (", ".join(infos),))
        else:
            self.stream.write("\n")
        return result
