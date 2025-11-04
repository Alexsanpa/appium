import os
from time import sleep
try:
    from sapyautomation.desktop.inputs.mouse import click_on_position
except KeyError:
    pass

try:
    from sapyautomation.vendors.sap.start_transaction import SapTransaction
    from sapyautomation.vendors.sap.connection import SAP
    from sapyautomation.vendors.sap.login import Login
except ImportError:
    pass

from sapyautomation.vendors.fiori.test_environment import FioriTestSuite
from sapyautomation.core import LazySettings
from sapyautomation.core.test_cases import BaseTestCases, BasePom
from sapyautomation.core.utils.exceptions import SapConnectionError
from sapyautomation.desktop.process import is_process_running, focus_on_window
from sapyautomation.vendors.sap.elements import Window


class SapTestSuite(BaseTestCases):
    """SAP test suite is used as parent class for the test cases

    In this class we created the basic methods to make SAP testing scripts
    easily adding methods as connect_sap() and custom asserts.
    """
    sap = None
    login_obj = None

    def change_login(self, secrets_section: str, client: str = '',
                     user: str = '', password: str = '',
                     language: str = '', get_evidence: bool = False):
        """ Logs out of the active session and starts a new one

        Args:
            secrets_section(str): section in secrets.ini
            client(str): client id
            user(str): username for the login process
            password(str): user's password
            language(str): language of the session
        """
        self.login_obj.logout()
        self.start_sap(self._connection_name)
        self.login(client, user, password, language, secrets_section,
                   get_evidence)

    def login(self, client: str = '', user: str = '',
              password: str = '', language: str = '',
              secrets_section: str = 'SAP', get_evidence: bool = True):
        """Login into SAP usisng credentials from settings.ini

        This methos loads credentials from a specific section in settings.ini
        to login into SAP.

        Args:
            secrets_section(str): section in secrets.ini
            client(str): client id
            user(str): username for the login process
            password(str): user's password
            language(str): language of the session
        """
        credentials = LazySettings().CREDENTIALS(secrets_section)
        if not hasattr(self, 'login_data'):
            self.login_data = None

        self.login_data = [
            credentials['CLIENT'] if client == '' else client,
            credentials['USER'] if user == '' else user,
            credentials['PASSWORD'] if password == '' else password,
            credentials['LANGUAGE'] if language == '' else language]

        self.add_to_result('login_data')

        try:
            self.login_obj = Login()
            self.login_obj.login(client=self.login_data[0],
                                 user=self.login_data[1],
                                 password=self.login_data[2],
                                 language=self.login_data[3])

            # status_menu = ElementById("wnd[0]/mbar/menu[4]/menu[11]",
            #                          SAP.get_current_connection(0))
            # status_menu.select()
            # TODO: a better session info retrieving pylint: disable=fixme
            click_on_position(1680, 30)

            if get_evidence:
                self.get_evidence(1)

            self.login_obj.identify_modal()
            sleep(2)
            focus_on_window('^SAP.+%s$' % self.login_data[1])

        except (AttributeError, OSError):
            pass

        return SAP.get_sap_information()

    def start_sap(self, connection_name: str = None) -> None:
        """Launch SAP logon and open a 'connection_name'

        This method creates a new SAP object and opens the connection by
        given name, this connection should be previously added manually.

        Args:
            connection_name (str): the connection name from SAP logon

        """
        # TODO: connection_name as first option  pylint: disable=fixme
        try:
            conn_data = LazySettings().CREDENTIALS("CONNECTION")
            self._connection_name = conn_data['NAME']

        except KeyError:
            self._connection_name = LazySettings().SAP_CONNECTION_NAME \
                if connection_name is None else connection_name

        if self._connection_name is None:
            raise SapConnectionError("Connection name no defined, "
                                     "please add it to settings.")

        self.sap = SAP(self._connection_name)
        self.sap.start()

    def close_sap(self) -> None:
        """Kill the 'saplogon.exe' process
        """
        try:
            sleep(1)
            self.sap.close()

        except AttributeError:
            pass

    def assertSapIsRunning(self) -> None:
        """Raise an exception if 'saplogon.exe' process is not running
        """
        if not is_process_running("saplogon.exe"):
            raise self.failureException("SAP is not currently running")

    def assertSapIsNotRunning(self) -> None:
        """Raise an exception if 'saplogon.exe' process is running
        """
        if is_process_running("saplogon.exe"):
            raise self.failureException("SAP is currently running")

    def assertSapPathExists(self) -> None:
        """Assert that the SAP path exists
        """
        if not os.path.exists(self.sap.path):
            raise self.failureException("SAP path does not exist")

    def start_transaction(self, name_transaction: str, msg: str = None,
                          num_connection: int = 0,
                          keep_session: str = "/n",
                          get_evidence: bool = True):
        """ Starts a transaction

        Args:
            name_transaction(str): transaction t-code
            num_connection(int): connection index which is gonna launch
                de transaction
            keep_session(str): session code for the launched transaction.

        """
        if msg is None:
            msg = f"Entering to the {name_transaction} transaction. " \
                "Note: some data from previous executions could be " \
                "pre-populated in the different fields"

        transaction = SapTransaction(num_connection, name_transaction)
        transaction_name = transaction.enter_transaction(keep_session)
        if get_evidence:
            self.get_evidence(label=msg)

        return transaction_name

    def on_resume(self):
        """ Setting up for test case resumming
        """
        self.login(get_evidence=False)
        self.assertIn("SAP Easy Access", Window(0).get_title(),
                      "The login did not load correctly")


class SapBasePom(BasePom):
    """ Base SAP POM
    """
    panel_id = "wnd[0]/sbar/pane[0]"
    title_id = "wnd[0]/titl"

    def __init__(self, connection=0):
        super().__init__()
        self.__connection = connection

    @property
    def session(self):
        """ Gets session object
        it creates a new session objetc if is the first call
        """
        if not hasattr(self, '__session'):
            self.__session = SAP.get_current_connection(self.__connection)

        return self.__session

    def window(self, index: int = 0, skip_shell: bool = False):
        """ Gets windows by index

        Args:
            index(int): windows index position.
            skip_shell(bool): skips shell generation and loads
                independent elements.

        Note:
            if you want to use `skip_shell` this method should be called
            before the load of the window/modal/etc... containing the shell.

        """
        return self._window(index, skip_shell).element

    def _window(self, index: int = 0, skip_shell: bool = False):
        """ Gets windows by index

        Args:
            index(int): windows index position.
            skip_shell(bool): skips shell generation and loads
                independent elements.

        Note:
            if you want to use `skip_shell` this method should be called
            before the load of the window/modal/etc... containing the shell.

        """
        window = Window(index, connection_index=self.__connection)
        if skip_shell:
            window.maximize()

        return window

    def exec_n_times(self, command_name: str, times: int,
                     window_index: int = 0):
        """ Execute n times a command from this class
        Args:
            command_name(str): Name of the command to be executed.
            times(int): Times to be executed
            window_index(int): sap window index
        """
        cmd = getattr(self, command_name)
        for _ in range(times):
            cmd(window_index)

    def get_id_from_panel(self) -> int:
        """Returns the identifier for any new document

        It also works for orders, requests, etc. if the number is on the
        'panel[0]'.

        Returns:
            The first number in the message showed after creating a new id
        """
        message = self._window().get_message_from_panel()
        return int([int(s) for s in message.split() if s.isdigit()][0])

    def get_message_from_panel(self) -> str:
        """Returns the message from panel

        Returns:
            The message text in the panel
        """
        message = self._window().get_message_from_panel()
        return message

    def enter(self, window_index: int = 0):
        """ Action to execute an enter
        """
        self._window(window_index).send_key(0)
        self.log('Action executed: Enter')

    def save(self, window_index: int = 0):
        """press the save key (F11) to SAP window
        """
        self._window(window_index).send_key(11)
        self.log('Action executed: Save')

    def back(self, window_index: int = 0):
        """ Action to go previous screen
        """
        self._window(window_index).send_key(3)
        self.log('Action executed: Back')

    def execute(self, window_index: int = 0):
        """Execute SAP action
        """
        self._window(window_index).send_key(8)
        self.log('Action executed: Execute')

    def get_title(self, window_index: int = 0):
        """get the title from screen.

        Args:
            window_index: the number of window to get the title (Default 0).
        Returns:
            The text in the title of screen by index.
        """
        title_element = self._window(window_index).get_title()
        return title_element

    @staticmethod
    def get_today_date(use_utc: bool = True, utc_timezone: int = 0) -> str:
        """Returns the actual date in SAP format

        Args:
                    use_utc(bool): flag to use utc or system date.
            utc_timezone(int): utc timezone value.

        Returns:
            date in string in SAP format i.e. 30.03.2020
        """
        return SAP.get_date(use_utc=use_utc, utc_timezone=utc_timezone)

    @staticmethod
    def get_date(offset_days: int = 0, use_utc: bool = False,
                 utc_timezone: int = 0) -> str:
        """Returns a date in SAP format based on actual date

        Args:
            offset_days(int): offset days to calculate with actual date.
            use_utc(bool): flag to use utc or system date.
            utc_timezone(int): utc timezone value.

        Returns:
            date in string in SAP format i.e. 30.03.2020
        """
        return SAP.get_date(offset_days, use_utc, utc_timezone)


class HybridTestSuite(SapTestSuite, FioriTestSuite):
    """Hybrid test suite is used as parent class for the test cases

    In this class we merged the basic methods to make SAP & Fiori testing
    scripts.
    """
    on_fiori = False

    def login_sap(self, client: str = '', user: str = '',
                  password: str = '', language: str = '',
                  secrets_section: str = 'SAP', get_evidence: bool = True):
        """Login into SAP usisng credentials from settings.ini

        This methos loads credentials from a specific section in settings.ini
        to login into SAP.

        Args:
            secrets_section(str): section in secrets.ini
            client(str): client id
            user(str): username for the login process
            password(str): user's password
            language(str): language of the session
        """
        self.on_fiori = False
        SapTestSuite.login(self, client, user, password, language,
                           secrets_section, get_evidence)

    def login_fiori(self, client: str = '', user: str = '',
                    password: str = '', language: str = '',
                    secrets_section: str = 'SAPFIORI',
                    get_evidence: bool = True,
                    secrets_vpn_section: str = 'VPN'):
        """Login into SAP usisng credentials from settings.ini

        This methos loads credentials from a specific section in settings.ini
        to login into SAP.

        Args:
            secrets_section(str): section in secrets.ini
            client(str): client id
            user(str): username for the login process
            password(str): user's password
            language(str): language of the session
        """
        self.on_fiori = True
        FioriTestSuite.login(self, client=client, user=user, password=password,
                             language=language, get_evidence=get_evidence,
                             secrets_section=secrets_section,
                             secrets_vpn_section=secrets_vpn_section)

    def change_login(  # pylint: disable=arguments-differ
            self, secrets_section: str, secrets_vpn_section: str = None,
            client: str = '', user: str = '', password: str = '',
            language: str = '', get_evidence: bool = False):
        """ Logs out of the active session and starts a new one

        Args:
            secrets_section(str): section in secrets.ini
            client(str): client id
            user(str): username for the login process
            password(str): user's password
            language(str): language of the session
        """
        if self.on_fiori:
            self.login_obj.logout()
            sleep(10)
            self.login_fiori(
                secrets_vpn_section=secrets_vpn_section, client=client,
                user=user, password=password, language=language,
                secrets_section=secrets_section, get_evidence=get_evidence)

        else:
            self.login_obj.logout()
            self.start_sap(self._connection_name)
            self.login_sap(client=client, user=user, password=password,
                           language=language, secrets_section=secrets_section,
                           get_evidence=get_evidence)

    def start_transaction(self, name_transaction: str, msg: str = None,
                          num_connection: int = 0,
                          keep_session: str = "/n",
                          get_evidence: bool = True):
        """ Starts a transaction

        Args:
            name_transaction(str): transaction t-code
            num_connection(int): connection index which is gonna launch
                de transaction
            keep_session(str): session code for the launched transaction.

        """
        if self.on_fiori:
            return FioriTestSuite.start_transaction(
                self, name_transaction=name_transaction, msg=msg,
                get_evidence=get_evidence)

        return SapTestSuite.start_transaction(
            self, name_transaction=name_transaction, msg=msg,
            num_connection=num_connection, keep_session=keep_session,
            get_evidence=get_evidence)

    def on_resume(self):
        """ Setting up for test case resumming
        """
        if self.on_fiori:
            self.login_fiori(get_evidence=False)

        else:
            self.login(get_evidence=False)
            self.assertIn("SAP Easy Access", Window(0).get_title(),
                          "The login did not load correctly")
