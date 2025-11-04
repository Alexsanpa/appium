import unittest.runner

from sapyautomation.core.test_cases.html_test_runner import HtmlRunner
from sapyautomation.core.test_cases.xml_test_runner import XmlRunner
from sapyautomation.core.test_cases.text_test_runner import TextRunner


def factory_runner(report_type: str = "text", **kwargs) -> unittest.runner:
    """
    Returns a runner based on the type (html or xml)

    Keyword arguments:
    type -- type of test runner to return(default "text")
    """
    if report_type == "text":
        return TextRunner(**kwargs)

    if report_type == "html":
        return HtmlRunner(**kwargs)

    if report_type == "xml":
        return XmlRunner(**kwargs)

    raise TypeError("The valid types of reports are 'text', 'html' and 'xml'.")
