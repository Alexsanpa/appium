from time import sleep
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy


class ValmexHomePage:
    """
    Clase que describe los objetos y acciones para el flujo de la app móvil Valmex.
    """

    # ----------------------------------------------------
    # 1. LOCALIZADORES (Usando el patrón (By_Method, Value))
    # NOTA: Ajusta estos localizadores si NO son Accessibility ID o si la app NO usa Android
    # ----------------------------------------------------
    OPERACIONES_BTN = (
        AppiumBy.XPATH,
        '//android.view.View[@content-desc="Operaciones"]',
    )

    DEFAULT_WAIT_TIME = 5

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, self.DEFAULT_WAIT_TIME)

    def click_operaciones(self):
        """
        Hace clic en el botón de operaciones.
        """
        try:
            operaciones_btn = self.wait.until(
                EC.element_to_be_clickable(self.OPERACIONES_BTN)
            )
            operaciones_btn.click()
            return True
        except TimeoutException:
            return False

    def validate_home_page_loaded(self):
        """
        Valida que la página de inicio se haya cargado correctamente.
        """
        try:
            self.wait.until(EC.presence_of_element_located(self.OPERACIONES_BTN))
            return True
        except TimeoutException:
            return False
