"""
Generic class to abstract communication with COM objects using the win32com
APGeneric class to abstract communication with COM objects using the
win32com AP
"""
import win32com.client  # pylint: disable=import-error
from win32com.universal import com_error  # pylint: disable=import-error

from sapyautomation.core.utils.exceptions import InvalidComException


class Com:
    """
    Parent class for ComDispath and Combject as wrapper

    """
    instance = None

    def destroy(self):
        """
        Set the instance variable no None
        """
        self.instance = None

    def get(self):
        """
        Returns the instance variable (com object or com dispatch)
        """
        return self.instance


class ComDispatch(Com):
    """" Create COM dispatch
    Creates a Dispatch based COM object.

    Args:
        name (str): The name of the COM application.

    Raises:
        InvalidComException: If there is an error creating the COM object
    """

    def __init__(self, name: str = "SAPGUI.Application"):
        try:
            self.instance = win32com.client.Dispatch(name)
        except com_error:
            raise InvalidComException("Invalid COM dispatch")


class ComObject(Com):
    """Connect to COM object
     Will connect to an already running instance of the COM object.

    Args:
        name (str): The name of the COM application.

    Raises:
        InvalidComException: If there is an error connecting to the COM object
    """

    def __init__(self, name: str = "SAPGUI"):
        try:
            self.instance = win32com.client.GetObject(name)
        except com_error:
            # TODO refactor catch SAP exceptions # pylint: disable=fixme
            raise InvalidComException()
