from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import StaleElementReferenceException,\
    NoAlertPresentException

from sapyautomation.web.start_browser import Browser
from sapyautomation.core.management.conf import LazySettings
from sapyautomation.vendors.fiori.login import Login
from sapyautomation.core.test_cases.bases import BaseTestCases, BasePom
from sapyautomation.vendors.sap.connection import SAP
from sapyautomation.web.elements import ElementByXPath, ElementById, _Element,\
    ElementByTag
from sapyautomation.core.utils.exceptions import FioriElementNotFound


class FioriTestSuite(BaseTestCases):
    """Fiori test suite is used as parent class for the test cases

    In this class we created the basic methods to make Fiori testing scripts.
    """
    def change_login(self, secrets_section: str,
                     secrets_vpn_section: str = None, client: str = '',
                     user: str = '', password: str = '',
                     language: str = '', get_evidence: bool = True):
        """ Logs out of the active session and starts a new one

        Args:
            secrets_vpn_section(str): vpn section in secrets.ini
            secrets_section(str): section in secrets.ini
            client(str): client id
            user(str): username for the login process
            password(str): user's password
            language(str): language of the session
        """
        self.login_obj.logout()
        sleep(10)
        self.login(secrets_vpn_section, client, user, password, language,
                   secrets_section, get_evidence)

    def login_netweaver(self, secrets_section: str = '', client: str = '',
                        user: str = '', password: str = '',
                        language: str = ''):
        """Login into SAP-netweaver usisng credentials from settings.ini

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

        self.login_obj.login_netweaver(
            client=credentials['CLIENT'] if client == '' else client,
            user=credentials['USER'] if user == '' else user,
            password=credentials['PASSWORD'] if password == '' else password,
            language=credentials['LANGUAGE'] if language == '' else language)

    def login(self, secrets_vpn_section: str = None, client: str = '',
              user: str = '', password: str = '', language: str = '',
              secrets_section: str = 'SAPFIORI', get_evidence: bool = True):
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
        self.login_obj = Login(self._driver)
        self._driver.get(credentials['FIORI'])

        if secrets_vpn_section is not None and secrets_vpn_section != '':
            try:
                vpn_credentials = LazySettings().CREDENTIALS(
                    secrets_vpn_section)

                if not hasattr(self, 'vpn_data'):
                    self.vpn_data = None

                self.vpn_data = [vpn_credentials['USER'],
                                 vpn_credentials['PASSWORD']]

                if get_evidence and \
                        self.login_obj.login_vpn(user=self.vpn_data[0],
                                                 password=self.vpn_data[1]):
                    self.get_evidence(1)

                self.add_to_result('vpn_data')
            except FioriElementNotFound:
                pass

        if not hasattr(self, 'login_data'):
            self.login_data = None

        self.login_data = [
            credentials['CLIENT'] if client == '' else client,
            credentials['USER'] if user == '' else user,
            credentials['PASSWORD'] if password == '' else password,
            credentials['LANGUAGE'] if language == '' else language]

        self.login_obj.login(client=self.login_data[0],
                             user=self.login_data[1],
                             password=self.login_data[2],
                             language=self.login_data[3])

        if get_evidence:
            self.get_evidence(1)

        self.login_obj.login_home()
        self.add_to_result('login_data')

        if get_evidence:
            self.__pom.toggle_usermenu()
            self.get_evidence(1)
            self.__pom.toggle_usermenu()

    def start_browser(self, browser: str = "Chrome", url: str = None,
                      unsecure: bool = False):
        """ Starts browser for fiori login

        Args:
            browser(str): browser name to be used
            url(str): if not specified loads the url in credentials
        """
        self._browser = Browser(browser, unsecure)
        self._driver = self._browser.start_browser(url)
        self.__pom = FioriBasePom(self._driver)

    def close_browser(self) -> None:
        """Kill the 'saplogon.exe' process
        """
        try:
            sleep(1)
            self._driver.quit()

        except AttributeError:
            pass

    def start_transaction(self, name_transaction: str,
                          result_index: int = 0, msg: str = None,
                          get_evidence: bool = True) -> str:
        """ Starts a transaction

        Args:
            name_transaction(str): transaction t-code
            num_connection(int): connection index which is gonna launch
                de transaction
            keep_session(str): session code for the launched transaction.

        Returns:
            transaction name.
        """
        result = None
        if msg is None:
            msg = f"Entering to the {name_transaction} transaction. " \
                "Note: some data from previous executions could be " \
                "pre-populated in the different fields"

        btn_search_xpath = "//a[@id='sf']"
        btn_t_search_id = "searchFieldInShell-button"
        lst_results_id = "AppSearchContainerResultListItem"
        txt_transaction_xpath = "//input[@id='searchFieldInShell-input-inner']"
        btn_search = ElementByXPath(self._driver, btn_search_xpath)
        if self.__pom.await_element(btn_search):
            btn_search.press()

        transaction_input = ElementByXPath(self._driver, txt_transaction_xpath)
        for _ in range(5):
            if self.__pom.await_element(transaction_input):
                try:
                    transaction_input.input_text(name_transaction, False)
                    if transaction_input.value == name_transaction:
                        break

                except StaleElementReferenceException:
                    pass

        btn_t_search = ElementById(self._driver, btn_t_search_id)
        if self.__pom.await_element(btn_t_search):
            btn_t_search.press()

        self.__pom.await_loading()

        container = ElementById(self._driver, lst_results_id)
        if self.__pom.await_element(container):
            tile = container.children(by_class="sapMGTScopeDisplay")
            title = tile[result_index].get_attribute('aria-label').split('\n')
            tile[result_index].click()
            self.__pom.switch_tab(-1)
            try:
                self.__pom.enter_frame(by_xpath="//iframe[contains(@class,"
                                       "'sapUShellApplicationContainer')]")

            except FioriElementNotFound:
                pass

            result = ' '.join(title[1:])[:-2]

        if get_evidence:
            self.get_evidence(label=msg)

        return result

    def on_resume(self):
        """ Setting up for test case resumming
        """
        self.login(get_evidence=False)
        self.assertIn("Home", self.pom.get_title(),
                      "Home page is not displayed")


class FioriBasePom(BasePom):
    """ Base Fiori POM
    """
    title_id = "shellAppTitle"
    div_loading_screen_id = "sap-ui-blocklayer-popup"

    def __init__(self, driver: WebDriver, browser: Browser = None):
        super().__init__()
        self._driver = driver
        self._browser = browser

    def toggle_usermenu(self):
        """ Toggle show/hide user menu in fiori

        Returns:
            boolean on toggle success
        """
        btn_user = ElementById(self._driver, 'meAreaHeaderButton')
        user_menu = ElementById(self._driver, "leftViewPort")
        for _ in range(30):
            try:
                prev = self.await_element(user_menu, 10)

            except FioriElementNotFound:
                prev = False

            try:
                if self.await_element(btn_user, 10):
                    btn_user.press()

                if prev is not self.await_element(user_menu, 10):
                    return True

            except (StaleElementReferenceException, FioriElementNotFound):
                if prev is True:
                    return True

        return False

    def enter_frame(self, by_id: str = None, by_xpath: str = None):
        """ Enters iframe context
        The method will enter the first iframe if no parameter is defined.

        Args:
            by_id(str): id of the wanted iframe
            by_xpath(str): xpath of the wanted iframe
        """
        if by_id is not None:
            frame = ElementById(self._driver, by_id)

        elif by_xpath is not None:
            frame = ElementByXPath(self._driver, by_xpath)

        else:
            frame = ElementByTag(self._driver, "iframe")

        if self.await_element(frame):
            self._driver.switch_to.frame(frame.element())
            return True

        return False

    def exit_frame(self):
        """ Leaves iframe context
        """
        self._driver.switch_to.default_content()

    @staticmethod
    def await_element(element: _Element, max_wait: int = 60):
        """ Awaits for element to be visible

        Args:
            element(_Element): wanted element
            max_wait(int): maximun time in seconds for the await
        """
        for _ in range(max_wait):
            sleep(1)
            try:
                element.element(force=True)
                if element.exists(True):
                    element.set_focus()
                    return True

            except (FioriElementNotFound, StaleElementReferenceException):
                pass

        raise FioriElementNotFound()

    def await_loading(self, max_wait: int = 60):
        """ Awaits for loading page to disapear

        Args:
            max_wait(int): maximun time in seconds for the await
        """
        for _ in range(max_wait):
            sleep(1)
            try:
                if not self.is_loading:
                    return True

            except FioriElementNotFound:
                pass

        return False

    def switch_tab(self, tab_index: int):
        """ Switch to specified tab

        Args:
            tab_index(int): index of wanted tab
        """
        window_new = self._driver.window_handles[tab_index]
        self._driver.switch_to.window(window_new)

        return self.get_title()

    def handle_alert(self, accept: bool = True):
        """ Handle browser's alert message on unsaved data

        Args:
            accept(bool): accepts if True or dismiss if False
        """
        try:
            if accept:
                self._driver.switch_to.alert.accept()

            else:
                self._driver.switch_to.alert.dismiss()

        except NoAlertPresentException:
            pass

    def close_current_tab(self):
        """ Closes current tab and goes to first tab remaining
        """
        self._driver.close()
        self.switch_tab(0)

    def get_title(self):
        """ Get the title from screen.

        Args:
            window_index: the number of window to get the title (Default 0).

        Returns:
            The text in the title of screen by index.
        """
        for _ in range(30):
            sleep(1)
            if self._driver.title != '' and \
                    self._driver.title != 'SAP GUI for HTML':
                break

        return self._driver.title

    @property
    def is_loading(self):
        """ Checks if fiori page/app is loading
        """
        element = ElementById(self._driver, self.div_loading_screen_id)

        return element.element(5).is_displayed()

    @staticmethod
    def get_today_date(use_utc: bool = True, utc_timezone: int = 0) -> str:
        """ Returns the actual date in SAP format

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
