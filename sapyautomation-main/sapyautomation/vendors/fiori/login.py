from selenium.common.exceptions import NoSuchElementException,\
    StaleElementReferenceException

from sapyautomation.web.elements import ElementById, ElementByXPath


class Login:
    """ Login object to manage fiori login actions
    """
    def __init__(self, driver):
        self.__driver = driver

    def logout(self):
        """ Logs out the user session
        Goes back through screens until it can logout

        Raises:
            SapNotSavedChanges: When there is changes that requires saving
        """

        for _ in range(30):
            btn_user = ElementById(self.__driver, 'meAreaHeaderButton')
            try:
                btn_user.element(10, True)
                btn_user.press()

            except StaleElementReferenceException:
                continue

            user_menu = ElementById(self.__driver, "leftViewPort")
            user_menu.element(10)
            if user_menu.exists(True):
                break

        for _ in range(30):
            btn_logout = ElementById(self.__driver, "logoutBtn-inner")
            btn_logout.element(10, True)
            btn_logout.press()

            btn_ok = ElementById(self.__driver, "__mbox-btn-0")
            btn_ok.element(10)
            if btn_ok.exists(True):
                btn_ok.press()
                break

    def login_vpn(self, user: str, password: str):
        """Fill the login fields and click 'login' in CBI VPN. only if the
        vpn login page is on screen otherwise pass.
        Args:
            secrets_section (str): credentials section in secrets file to
            use in vpn login.
        """
        txt_user_name = ElementById(self.__driver, "username")
        txt_user_name.input_text(user)

        txt_password = ElementById(self.__driver, "password")
        txt_password.input_text(password)

        btn_login = ElementByXPath(self.__driver,
                                   "//button[@type='submit']")
        btn_login.press()

        btn_rememberme = ElementByXPath(self.__driver,
                                        "//button[text()='Do ']")
        btn_rememberme.element(20)
        btn_rememberme.press()

    def login_home(self):
        """
        Click on the login button
        """
        btn_sap_login = ElementById(self.__driver, "LOGIN_LINK")
        btn_sap_login.press()

    def login_netweaver(self, client: str = '', user: str = '',
                        password: str = '', language: str = ''):
        """ Fills netweaver login form
        """
        txt_sap_user = ElementById(self.__driver, "sap-user")
        txt_sap_user.element(60)
        txt_sap_password = ElementById(self.__driver, "sap-password")
        txt_sap_user.input_text(user)
        txt_sap_password.input_text(password)

        if client != '':
            try:
                txt_sap_client = ElementById(self.__driver,
                                             "sap-client")
                txt_sap_client.input_text(client)

            except (NoSuchElementException, StaleElementReferenceException):
                pass

        if language != '':
            try:
                sel_language = ElementById(self.__driver, "sap-language")
                sel_language.select_combo_value(language)

            except (NoSuchElementException, StaleElementReferenceException):
                pass

        btn_sap_login = ElementById(self.__driver, "LOGON_BUTTON")
        btn_sap_login.element(60)
        btn_sap_login.press()

    def login(self, client: str = '', user: str = '', password: str = '',
              language: str = ''):
        """ Fills login form
        """
        txt_sap_user = ElementById(self.__driver, "USERNAME_FIELD-inner")
        txt_sap_user.element(60)
        txt_sap_password = ElementById(self.__driver,
                                       "PASSWORD_FIELD-inner")
        txt_sap_user.input_text(user)
        txt_sap_password.input_text(password)

        try:
            txt_sap_client = ElementById(self.__driver,
                                         "CLIENT_FIELD-inner")
            txt_sap_client.input_text(client)

        except (NoSuchElementException, StaleElementReferenceException):
            pass

        try:
            sel_language = ElementById(self.__driver, "LANGUAGE_SELECT")
            sel_language.select_combo_value(language)

        except (NoSuchElementException, StaleElementReferenceException):
            pass
