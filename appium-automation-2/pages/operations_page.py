from time import sleep
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy


class ValmexOperationsPage:
    """
    Clase que describe los objetos y acciones para el flujo de la app móvil Valmex.
    """

    # ----------------------------------------------------
    # 1. LOCALIZADORES (Usando el patrón (By_Method, Value))
    # NOTA: Ajusta estos localizadores si NO son Accessibility ID o si la app NO usa Android
    # ----------------------------------------------------

    VENDER_BTN = (AppiumBy.XPATH, '//android.view.View[@content-desc="Vender"]')
    DEPOSITAR_BTN = (
        AppiumBy.XPATH,
        '//android.view.View[@content-desc="Depositar a mi contrato"]',
    )

    DEFAULT_WAIT_TIME = 5

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, self.DEFAULT_WAIT_TIME)

    def validate_operations_page_loaded(self):
        """
        Valida que la página de operaciones se haya cargado correctamente.
        """
        try:
            self.wait.until(EC.presence_of_element_located(self.DEPOSITAR_BTN))
            return True
        except TimeoutException:
            return False

    def click_vender(self):
        """
        Hace clic en el botón de vender.
        """
        try:
            vender_btn = self.wait.until(EC.element_to_be_clickable(self.VENDER_BTN))
            vender_btn.click()
            return True
        except TimeoutException:
            return False
