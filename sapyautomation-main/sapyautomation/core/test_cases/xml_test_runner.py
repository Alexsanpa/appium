"""
Test runnner with XML reporting
"""
import xmlrunner

from sapyautomation.core import LazyReporter
from .bases import BaseRunner


class XmlRunner(BaseRunner):

    def __init__(self):
        """Initialize method creates the xml runner"""
        self.runner = xmlrunner.XMLTestRunner(
            output=str(LazyReporter().paths['report_path']))

    def prepare_run(self):
        """ Implementation to comply with BaseRunner """
