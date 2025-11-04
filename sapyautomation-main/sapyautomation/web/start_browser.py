from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class Browser:
    driver = None

    def __init__(self, browser, unsecure: bool = False,
                 extra_options: list = None):
        """
        Constructor for Browser Class

        Args:
            browser (str): name browser what you want to start
        """
        if browser == "Chrome":
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--disable-notifications')
            chrome_options.add_experimental_option('detach', True)

            if extra_options is not None:
                for opt in extra_options:
                    chrome_options.add_argument(opt)

            if unsecure:
                chrome_options.add_argument('--ignore-ssl-errors=yes')
                chrome_options.add_argument('--ignore-certificate-errors')

            self.driver = webdriver.Chrome(
                executable_path=ChromeDriverManager().install(),
                options=chrome_options)

        if browser == "Firefox":
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.set_preference("dom.webnotifications.enabled",
                                           False)
            profile = webdriver.FirefoxProfile()
            capabilities = webdriver.DesiredCapabilities().FIREFOX
            if extra_options is not None:
                for opt in extra_options:
                    firefox_options.set_preference(opt[0], opt[1])

            if unsecure:
                capabilities['acceptSslCerts'] = True
                profile.accept_untrusted_certs = True

            self.driver = webdriver.Firefox(
                firefox_profile=profile,
                executable_path=GeckoDriverManager().install(),
                options=firefox_options,
                capabilities=capabilities)

    def handle_alert(self, accept: bool = True):
        """ Handle browser's alert message on unsaved data

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

        self.driver.maximize_window()

        return self.driver

    def close_browser(self):
        """Close your browser instance"""
        self.driver.close()
        self.driver.quit()
