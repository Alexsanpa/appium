from datetime import datetime
from datetime import timedelta
import win32com  # pylint: disable=import-error
from win32com.client import GetObject  # pylint: disable=import-error
from sapyautomation.vendors.sap.connection import SAP
from sapyautomation.vendors.sap.find_modal import identify_modal
from sapyautomation.vendors.sap.find_modal import actions_modal
from sapyautomation.core.utils.exceptions import SapTransactionError,\
    SapSessionNotFound
from sapyautomation.vendors.sap.elements import ElementById


class SapTransaction:
    """Starts transaction

    Start a transaction what you want use and return True if transaction has
    been started or false otherwise

    Args:
       num_connection (int): number connection what you want to access
       name_transaction (str): name transaction what you want to use
       keep_session (str): if you use "/o", system open a new session with
                            your transaction and if you use "/n", system not
                            open a new session.

    Returns:
          bool: True if successful, False otherwise.

    Raises:
        SapSessionNotFound: If you want to start a transaction on a new
            session and you have five sessions opened
        SapTransactionError: If you want to start an incorrect transaction or a
            transaction without authorization
    """
    _title_id = "wnd[0]/titl"
    _message_id = "wnd[0]/sbar"
    _input_transaction_id = "wnd[0]/tbar[0]/okcd"

    def __init__(self, num_connection: int, name: str):
        self._sap_gui = GetObject("SAPGUI").GetScriptingEngine
        self._session = SAP.get_current_connection(num_connection)
        self._num_connection = num_connection
        self._name = name

    @property
    def title(self):
        if self._keep_session == "/o":
            title = self._session.findById(self._title_id).text

        else:
            title = self._sap_gui.Connections.Item(self._num_connection)\
                .Sessions(self._session_active - 1).\
                findById(self._title_id).text

        return title

    @property
    def msg(self):
        if self._keep_session == "/o":
            msg = self._session.findById(self._message_id).text

        else:
            msg = self._sap_gui.Connections.Item(self._num_connection)\
                .Sessions(self._session_active - 1).\
                findById(self._message_id).text

        return msg

    def enter_transaction(self, keep_session: str = "/n"):
        self._keep_session = keep_session
        input_transaction = ElementById(self._input_transaction_id,
                                        self._session)
        input_transaction.input_text(self._keep_session + self._name)
        self._session.findById("wnd[0]").sendVKey(0)

        return self.validate_transaction()

    def validate_transaction(self):
        current_time = datetime.now()
        num_sessions = self._sap_gui.Connections.Item(self._num_connection)\
            .Sessions.Count
        self._session_active = num_sessions

        if self._keep_session == "/o":
            while num_sessions == self._session_active:
                now = datetime.now()
                self._session_active = self._sap_gui.Connections.Item(
                    self._num_connection).Sessions.Count

                if now >= (current_time + timedelta(seconds=3)):
                    identify_modal(self._session)
                    raise SapSessionNotFound("Session has not been created")

        if self.msg != '':
            if self._session_active > 1:
                self._sap_gui.Connections.Item(self._num_connection)\
                    .Sessions(self._session_active - 1)\
                    .findById(self._input_transaction_id).text = "/n"
                self._sap_gui.Connections.Item(self._num_connection)\
                    .Sessions(self._session_active - 1).findById("wnd[0]").\
                    sendVKey(0)

            if "SAP Easy Access" in self.title:
                raise SapTransactionError(self.msg)

        if "SAP Easy Access" not in self.title:
            return True

        return False


def click_exit_system(num_connection: int) -> bool:
    """ Closes SAP System.

    Identifies all active windows and close all of them, return True if
    session has been closed or false otherwise

    Args:
    num_connection (int): number connection what you want to access

    Returns:
        bool: True if successful, False otherwise.
    """

    sap_gui = win32com.client.GetObject("SAPGUI").GetScriptingEngine
    connections = sap_gui.Connections.Count
    session = SAP.get_current_connection(num_connection)
    num_sessions = sap_gui.Connections.Item(num_connection).Sessions.Count

    if num_sessions > 1:
        num_session = 1
        while num_sessions != num_session:
            sap_gui.Connections.Item(num_connection).Sessions.Item(
                1).findbyid(
                "wnd[0]/tbar[0]/btn[15]").press()
            num_session = num_session + 1

        session.findById("wnd[0]/tbar[0]/btn[15]").press()
    else:
        session.findById("wnd[0]/tbar[0]/btn[15]").press()

    list_elements = identify_modal(session)
    if len(list_elements) != 0:
        actions_modal(list_elements, session)

    connections_current = connections

    while connections_current == connections:
        connections_current = sap_gui.Connections.Count

    connections = connections - 1
    if connections_current == connections:
        return True


def create_new_mode(num_connection: int) -> bool:
    """Creates a new mode(new session)

    Opens a new session and return True if session has been created or false
    otherwise

    Args:
    num_connection (int): number connection what you want to access

    Returns:
        bool: True if successful, False otherwise.

    Raises:
        SystemError: If you want to create more than five sessions
    """

    sap_gui = win32com.client.GetObject("SAPGUI").GetScriptingEngine
    num_sessions = sap_gui.Connections.Item(num_connection).Sessions.Count

    session = SAP.get_current_connection(num_connection)
    session.createSession()

    session_active = num_sessions
    current_time = datetime.now()
    while num_sessions == session_active:
        now = datetime.now()
        session_active = sap_gui.Connections.Item(num_connection)\
            .Sessions.Count
        if now >= (current_time + timedelta(seconds=3)):
            identify_modal(session)
            raise SystemError("Maximum number of GUI sessions "
                              "reached")

    title = sap_gui.Connections.Item(num_connection)\
        .Sessions(session_active - 1).findById("wnd[0]/titl").text

    if title == "SAP Easy Access":
        return True


def start_transaction(num_connection: int, name_transaction: str,
                      keep_session: str = "/n") -> bool:
    """Starts transaction

    Start a transaction what you want use and return True if transaction has
    been started or false otherwise

    Args:
       num_connection (int): number connection what you want to access
       name_transaction (str): name transaction what you want to use
       keep_session (str): if you use "/o", system open a new session with
                            your transaction and if you use "/n", system not
                            open a new session.

    Returns:
          bool: True if successful, False otherwise.

    Raises:
        SapSessionNotFound: If you want to start a transaction on a new
            session and you have five sessions opened
        SapTransactionError: If you want to start an incorrect transaction or a
            transaction without authorization
    """
    transaction = SapTransaction(num_connection, name_transaction)

    return transaction.enter_transaction(keep_session)
