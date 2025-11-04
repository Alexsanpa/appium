from time import sleep
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy


class ValmexLoginPage:
    """
    Clase que describe los objetos y acciones para el flujo de la app móvil Valmex.
    """

    # ----------------------------------------------------
    # 1. LOCALIZADORES (Usando el patrón (By_Method, Value))
    # NOTA: Ajusta estos localizadores si NO son Accessibility ID o si la app NO usa Android
    # ----------------------------------------------------
    LOCATOR_TEXTO_ACTIVACION = (
        AppiumBy.XPATH,
        '//android.widget.EditText[@hint="Contraseña"]',
    )

    # Localizador para el campo de contraseña (usa hint porque no tiene accessibility ID ni resource-id)
    PASSWORD_FIELD = (AppiumBy.XPATH, '//android.widget.EditText[@hint="Contraseña"]')
    ENTRAR_BUTTON = (AppiumBy.XPATH, '//android.widget.Button[@content-desc="Entrar"]')

    DEFAULT_WAIT_TIME = 5

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, self.DEFAULT_WAIT_TIME)

    def verificar_existencia_texto01(self):
        """
        Valida que el text "Si ya eres cliente y aún.." esté visible.
        Retorna True si lo encuentra, False en caso de Timeout.
        """
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.LOCATOR_TEXTO_ACTIVACION)
            )
            return True
        except TimeoutException:
            return False

    def set_Access_with_credentials(self, password, driver):
        """
        Establece la contraseña en el campo correspondiente.
        """
        try:
            password_field = self.wait.until(
                EC.visibility_of_element_located(self.PASSWORD_FIELD)
            )
            password_field.click()
            password_field.send_keys(password)
            entrar_button = self.wait.until(
                EC.element_to_be_clickable(self.ENTRAR_BUTTON)
            )
            driver.hide_keyboard()
            entrar_button.click()
            return True
        except TimeoutException:
            return False

    def validar_campo_termino_condiciones(self, driver):
        """
        Captura el texto del elemento 'Términos y Condiciones' y lo valida.
        """
        texto_esperado = "Ver términos y condiciones"

        try:
            sleep(3)
            terminos_link_element = driver.find_element(self.TERMINOS_LINK_SELECTOR)
            texto_capturado = terminos_link_element.text

            # 3. Realizar la aserción
            assert (
                texto_capturado == texto_esperado
            ), f"El texto no coincide. Esperado: '{texto_esperado}', Obtenido: '{texto_capturado}'"

        except AttributeError:
            # Esto captura si 'self.TERMINOS_LINK_SELECTOR' no existe.
            print("❌ Error: El selector TERMINOS_LINK_SELECTOR no está definido.")
            return False
        except Exception as e:
            # Esto captura si el elemento no se encuentra o cualquier otro error de Appium.
            print(f"❌ Falló la validación del texto de términos. Error: {e}")
            return False
