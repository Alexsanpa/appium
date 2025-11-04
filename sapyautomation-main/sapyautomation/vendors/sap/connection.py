import subprocess
from datetime import datetime, timedelta

try:
    from win32com.universal import com_error  # pylint: disable=import-error
    from sapyautomation.core.com import ComObject

except ModuleNotFoundError:
    pass

from sapyautomation.core.management.conf import LazySettings
from sapyautomation.vendors.sap.models import session_data
from sapyautomation.desktop.process import kill_process
from sapyautomation.core.utils.exceptions import InvalidComException,\
    SapSessionNotFound, SapError, SapConnectionError


class SAP:
    """
    Constructor for SAP Class

    Keyword arguments:
    connection_name -- connection name what you want to connect
    path -- SAP system path
    time -- wait on seconds for connect to SAP (default 10 seconds)
    """
    __sap_gui_name = LazySettings().SAP_GUI_NAME
    __sap_path = LazySettings().SAP_PATH

    def __init__(self, connection_name: str, path: str = None, time: int = 10):
        assert connection_name != '', 'Invalid connection name'
        self.connection_name = connection_name
        self.path = path if path else self.__sap_path
        self.time = time

    @staticmethod
    def count_connections():
        """ Counts active sap connections
        """
        sap_gui = ComObject("SAPGUI").get().GetScriptingEngine
        return sap_gui.Connections.Count

    @staticmethod
    def get_date(offset_days: int = 0, use_utc: bool = False,
                 utc_timezone: int = 0):
        """Returns a date in SAP format based on actual date

        Args:
            offset_days(int): offset days to calculate with actual date.
            use_utc(bool): flag to use utc or system date.
            utc_timezone(int): utc timezone value.

        Returns:
            date in string in SAP format i.e. 30.03.2020
        """
        offset = timedelta(days=offset_days)
        tz_offset = timedelta(hours=utc_timezone)

        if use_utc:
            date = datetime.utcnow() + tz_offset
        else:
            date = datetime.now()

        date = date + offset

        return date.strftime("%d.%m.%Y")

    @staticmethod
    def get_current_connection(num_connection: int = 0,
                               num_session: int = 0) -> object:
        """
        Get current connection and return active session

        Keyword arguments:
        num_connection -- number connection what you want to connect
        """

        try:
            sap_gui = ComObject("SAPGUI").get().GetScriptingEngine
            connection = sap_gui.Children(num_connection)
            session = connection.Children(num_session)

            return session

        except (com_error, InvalidComException) as e:
            if e.args[2][2] in ("The control could not be found by id.",
                                "The enumerator of the collection "
                                "cannot find en element with the "
                                "specified index."):
                raise SapSessionNotFound(
                    "It was not possible to connect to the session")

    def start(self) -> object:
        """ Start SAP System and return session created
        """
        try:
            subprocess.Popen(self.path)
        except FileNotFoundError as e:
            if e.args[1] == 'The system cannot find the file specified':
                raise FileNotFoundError

        current_time = datetime.now()
        name_object = None
        now = current_time
        while name_object is None:
            try:
                now = datetime.now()
                name_object = ComObject(self.__sap_gui_name).get()

            except InvalidComException as e:
                if now >= (current_time + timedelta(seconds=self.time)):
                    if e.args[0] == -2147221020:
                        raise SystemError("The System has not been opened")
                    break

        try:
            sap_gui_auto = ComObject(self.__sap_gui_name).get()
            application = sap_gui_auto.GetScriptingEngine
            connection = application.openConnection(self.connection_name)
            session = connection.Children(0)

            return session

        except (com_error, InvalidComException) as e:
            if len(e.args) > 2 and e.args[2] is not None:
                if e.args[2][2] == "The enumerator of the collection " \
                                   "cannot find en element with the " \
                                   "specified index.":
                    raise SapSessionNotFound(
                        "It was not possible to connect to the session")

                if e.args[2][2] == "SAP Logon connection entry not found":
                    raise SapConnectionError("'%s' connection entry not found "
                                             % self.connection_name)

                if e.args[2][2] == 'The \'Sapgui Component\' could not be ' \
                                   'instantiated.':
                    raise SapError("The object has not been instantiated")

            elif e.args[0] == -2147221020:  # sapguiauto
                raise SapError("The provided SAP GUI Name is incorrect ")

    @staticmethod
    def get_sap_information(session: int = 0) -> session_data:
        """Returns information about SAP session.

        Returns a named tuple with SAP session information from GuiSessionInfo,
        the information is:

            application_server: The name of the application server is set only
            if the session belongs to a connection that was started without
            load balancing, by specifying an application server.

            system_name: This is the name of the SAP system.

            system_number: The system number is set only if the session belongs
            to a connection that was started without load balancing,
            by specifying an application server

            language: The language specified on the login screen.

            client: The client selected on the login screen.

            session: The number of the session is also displayed in SAP GUI on
            the status bar.

            group:The login group information is available only if the session
            belongs to a connection which was started using load balancing
            program: The name of the source program that is currently being
            executed.

            response_time(milliseconds): The time that is spent on network
            communication from the moment data are sent to the server to the
            moment the server response arrives.

            sap_path: sap_logon.exe where SAP was launched from

        Args:
            session(int): connection you want to connect to (default 0)

        Raises:
            SapSessionNotFound: if the given session is not found

        Returns:
            SapSession: a named tuple with the SAP session information:

        """
        try:
            session = SAP.get_current_connection(session).Info

        except (InvalidComException, com_error):
            raise SapSessionNotFound()

        sap_info = session_data(session.ApplicationServer,
                                session.SystemName,
                                session.SystemNumber,
                                session.Language,
                                session.Client,
                                session.SessionNumber,
                                session.Group,
                                session.Program,
                                session.ResponseTime)

        return sap_info

    @staticmethod
    def close_windows() -> bool:
        """ Close SAP Window and return True if menu  been clicked or false
        otherwise
        """

        sap_gui = ComObject("SAPGUI").get().GetScriptingEngine
        connection = sap_gui.Connections.Count
        num_connection = 0
        while connection != num_connection and connection > 0:
            connections = sap_gui.Children(num_connection)
            session = connections.Children(0)
            session.findbyid("wnd[0]").close()
            num_connection = num_connection + 1

        new_connections = connection
        while new_connections == 1:
            new_connections = sap_gui.Connections.Count

        if new_connections == 0:
            return True

    @staticmethod
    def close() -> bool:
        """ Close SAP application
        """
        value = kill_process(name="saplogon.exe")
        return value
