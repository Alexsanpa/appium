class Error(Exception):
    """Base class for exceptions."""

    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, self.message)

    def __repr__(self):
        return self.message

    __str__ = __repr__

# Command execptions


class CommandError(Exception):
    """ Exception class indicating a problem while executing a management
    command.
    """


class TestsNotFound(CommandError):
    """ Exception launched when no tests can be found
    """

    def __init__(self, test: str = None):
        message = 'Tests not found'
        if test is not None:
            message = "Tests '%s' doesn't exist or not a test." % test

        super().__init__(self, message)


class DataSetNotFound(CommandError):
    """ Exception launched when no data set can be found
    """

    def __init__(self, test: str = None):
        message = 'Data sets not found'
        if test is not None:
            message = "Data set for test '%s' missing." % test

        super().__init__(self, message)


class CollectionNotFound(CommandError):
    """ Exception launched when no test collection can be found
    """

# SAP execptions


class SapError(Error):
    """Base exception for sap errors"""


class SapSessionNotFound(SapError):
    """Exception lauched by get_sap_information() when the given session is
    not found
    """


class SapElementNotFound(SapError):
    """Exception lauched by sap elements not found by id
    """


class SapTransactionError(SapError):
    """Exception lauched by sap transactions when can't be loaded.
    """


class SapConnectionError(SapError):
    """Exception lauched by sap connection fails or don't exists.
    """

# Project exceptions


class ProjectError(Error):
    """Base exception for project errors"""


class SettingNotFound(ProjectError):
    """Exception lauched by LazySettings when the requested attribute is
    not found
    """


class MissingSettingsFile(ProjectError):
    """Exception lauched when there is not settings.ini in the project
    """


class BadSettings(ProjectError):
    """Exception lauched when there is not a valid setting in the project
    """


class EvidenceOutOfStep(ProjectError):
    """ Exception launched in report generation when get_evidence was called
    before any test's step.
    """

# Communication exceptions


class ComError(Error):
    """Base exception for com errors"""


class SMTPError(ComError):
    """Exception lauched when there is an smtp error
    """


class InvalidComException(ComError):
    """Exception launched by COM errors.
    """

# Fiori exceptions


class FioriError(Error):
    """ Base exception for fiori error
    """


class FioriElementNotFound(FioriError):
    """Exception lauched by fiori elements not found by id
    """


class FioriLoginError(FioriError):
    """ Exception launched when login fails
    """
