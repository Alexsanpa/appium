"""Tomar como base el archivo start_browser.py de la carpeta vendors/web y modificarlo para que funcione con JavaFX"""
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.ie.service import Service as IeService
from pywinauto import Application
import time

from pywinauto import Desktop


class Browser:
    driver = None
    window_title = "Advertencia de Seguridad"
    button_name = "EjecutarButton"

    def __init__(self, browser, unsecure: bool = False, extra_options: list = None):
        """
        Constructor for Browser Class

        Args:
            browser (str): name browser what you want to start
        """
        if browser == "Chrome":
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_experimental_option("detach", True)

            if extra_options is not None:
                for opt in extra_options:
                    chrome_options.add_argument(opt)

            if unsecure:
                chrome_options.add_argument("--ignore-ssl-errors=yes")
                chrome_options.add_argument("--ignore-certificate-errors")

            self.driver = webdriver.Chrome(
                executable_path=ChromeDriverManager().install(), options=chrome_options
            )

        if browser == "Firefox":
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.set_preference("dom.webnotifications.enabled", False)
            profile = webdriver.FirefoxProfile()
            capabilities = webdriver.DesiredCapabilities().FIREFOX
            if extra_options is not None:
                for opt in extra_options:
                    firefox_options.set_preference(opt[0], opt[1])

            if unsecure:
                capabilities["acceptSslCerts"] = True
                profile.accept_untrusted_certs = True

            self.driver = webdriver.Firefox(
                firefox_profile=profile,
                executable_path=GeckoDriverManager().install(),
                options=firefox_options,
                capabilities=capabilities,
            )

        if browser == "IE":
            self.ie_options = webdriver.IeOptions()
            self.ie_options.attach_to_edge_chrome = True
            self.ie_options.add_argument("start-maximized")
            self.ie_options.add_argument("inprivate")
            self.ie_options.edge_executable_path = (
                r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
            )

            # profile = webdriver.IeProfile()
            if extra_options is not None:
                for opt in extra_options:
                    self.ie_options.set_preference(opt[0], opt[1])

            """ if unsecure:
                capabilities["acceptSslCerts"] = True
                profile.accept_untrusted_certs = True """

            self.service = webdriver.IeService(
                executable_path=r"C:\\Utils\\IEDriverServer.exe", log_level="TRACE"
            )
            self.driver = webdriver.Ie(service=self.service, options=self.ie_options)

    def handle_alert(self, accept: bool = True):
        """Handle browser's alert message on unsaved data

        Args:
            accept(bool): accepts if True or dismiss if False
        """
        try:
            if accept:
                self.driver.switch_to.alert.accept()

            else:
                self.driver.switch_to.alert.dismiss()

        except NoAlertPresentException:
            pass

    def start_browser(self, url) -> object:
        """Starts a browser

        Start a instance of specific browser

        Args:
            url (str): url of website

        Return:
            driver (object): driver to interface with the browser
        """

        self.driver.implicitly_wait(1)

        if url is not None:
            self.driver.get(url)

        new_window = self.driver.window_handles[0]
        self.driver.implicitly_wait(5)
        self.driver.switch_to.window(new_window)
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        return self.driver

    def close_browser(self):
        """Close your browser instance"""
        self.driver.close()
        self.driver.quit()

    def close_security_warning(
        self, window_title: str = window_title, button_name: str = button_name
    ):
        """Close Java security warning"""

        desktop = Desktop(backend="uia")
        window = desktop.window(title=window_title)
        window.wait("visible", timeout=120)

        app = Application(backend="uia").connect(title=window_title)
        dlg = app.window(title=window_title)
        try:
            dlg.wait("visible", timeout=120)

            checkbox = dlg.CheckBox
            # Check if the checkbox is found
            if checkbox.exists():
                if not checkbox.get_toggle_state():
                    checkbox.toggle()
                    print(f"Checkbox checked.")
                else:
                    print(f"Checkbox is already checked.")
            else:
                print(f"Checkbox not found.")

            dlg.__getattribute__(button_name).click()
        except:
            pass
        
