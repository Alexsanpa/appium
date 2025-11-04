"""
Clase para manejar la conexión con Appium Server
"""

from appium import webdriver
from appium.options.android import UiAutomator2Options
import time


class AppiumDriver:
    """
    Clase para inicializar y manejar el driver de Appium
    """

    def __init__(self, capabilities):
        """
        Inicializa el driver de Appium

        Args:
            capabilities (dict): Diccionario con las capabilities del dispositivo
        """
        self.capabilities = capabilities
        self.driver = None
        self.appium_server_url = "http://localhost:4723"

    def start_driver(self):
        """
        Inicia el driver de Appium y conecta con el dispositivo

        Returns:
            driver: Instancia del driver de Appium
        """
        try:
            print("🚀 Iniciando conexión con Appium Server...")
            print(f"📱 URL del servidor: {self.appium_server_url}")

            # Crear opciones usando UiAutomator2Options
            options = UiAutomator2Options()
            options.load_capabilities(self.capabilities)

            # Inicializar el driver
            self.driver = webdriver.Remote(
                command_executor=self.appium_server_url, options=options
            )

            print("✅ Conexión establecida exitosamente")
            print(f"📱 Dispositivo: {self.capabilities.get('appium:deviceName')}")

            # Esperar a que el dispositivo esté listo
            time.sleep(2)

            return self.driver

        except Exception as e:
            print(f"❌ Error al conectar con Appium Server: {str(e)}")
            print("\n💡 Asegúrate de que:")
            print("   1. Appium Server está corriendo (appium)")
            print("   2. El emulador/dispositivo está conectado")
            print("   3. Las capabilities son correctas")
            raise

    def stop_driver(self):
        """
        Detiene el driver y cierra la sesión
        """
        if self.driver:
            try:
                print("🛑 Cerrando conexión con Appium...")
                self.driver.quit()
                print("✅ Conexión cerrada exitosamente")
            except Exception as e:
                print(f"⚠️ Error al cerrar el driver: {str(e)}")

    def get_driver(self):
        """
        Retorna la instancia del driver

        Returns:
            driver: Instancia del driver de Appium
        """
        return self.driver
