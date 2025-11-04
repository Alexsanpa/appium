# config/settings.py
"""
Sistema de configuración centralizado para el proyecto de automatización
Soporta múltiples entornos: dev, qa, staging, prod
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Literal

# Cargar variables de entorno desde .env
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
    print(f"✅ Configuración cargada desde: {ENV_FILE}")
else:
    print("⚠️ Archivo .env no encontrado, usando valores por defecto")


class AppiumConfig:
    """Configuración de Appium Server"""

    HOST = os.getenv("APPIUM_HOST", "localhost")
    PORT = int(os.getenv("APPIUM_PORT", 4723))

    @property
    def url(self):
        return f"http://{self.HOST}:{self.PORT}/wd/hub"

    # Timeouts
    NEW_COMMAND_TIMEOUT = int(os.getenv("APPIUM_NEW_COMMAND_TIMEOUT", 300))
    IMPLICIT_WAIT = int(os.getenv("APPIUM_IMPLICIT_WAIT", 10))
    EXPLICIT_WAIT = int(os.getenv("APPIUM_EXPLICIT_WAIT", 15))

    # Instalación
    INSTALL_TIMEOUT = int(os.getenv("APPIUM_INSTALL_TIMEOUT", 60000))
    ADB_EXEC_TIMEOUT = int(os.getenv("APPIUM_ADB_TIMEOUT", 60000))


class DeviceConfig:
    """Configuración del dispositivo móvil"""

    # Execution platform
    EMULATED_OR_PHYSICAL = os.getenv("DEVICE_EMULATED_OR_PHYSICAL", "emulated")

    PLATFORM_NAME = os.getenv("DEVICE_PLATFORM", "Android")
    PLATFORM_VERSION = os.getenv("DEVICE_PLATFORM_VERSION", "16")
    DEVICE_NAME = os.getenv("DEVICE_NAME", "emulator-5554")
    AUTOMATION_NAME = os.getenv("DEVICE_AUTOMATION", "UiAutomator2")
    # AVD configuration
    DEVICE_AVD = os.getenv("DEVICE_AVD", "Medium_Phone_API_36.1")

    # Configuraciones de reset
    NO_RESET = os.getenv("DEVICE_NO_RESET", "True").lower() == "true"
    FULL_RESET = os.getenv("DEVICE_FULL_RESET", "False").lower() == "true"
    AUTO_GRANT_PERMISSIONS = (
        os.getenv("DEVICE_AUTO_GRANT_PERMISSIONS", "True").lower() == "true"
    )


class AppConfig:
    """Configuración de la aplicación bajo prueba"""

    PACKAGE_NAME = os.getenv("APP_PACKAGE", "com.valmex.valmexcb")
    ACTIVITY_NAME = os.getenv("APP_ACTIVITY", "com.valmex.valmexcb.MainActivity")

    # Ruta del APK
    APK_FILENAME = os.getenv("APP_APK_FILENAME", "app-release.apk")
    APK_PATH = BASE_DIR / "apk" / APK_FILENAME

    # Modo de instalación
    INSTALL_APP = os.getenv("APP_INSTALL", "False").lower() == "true"


class EvidenceConfig:
    """Configuración del sistema de evidencias"""

    # Rutas de salida
    BASE_OUTPUT_DIR = BASE_DIR / os.getenv("EVIDENCE_BASE_DIR", "evidencias")
    VIDEO_DIR = BASE_OUTPUT_DIR / os.getenv("EVIDENCE_VIDEO_DIR", "videos")
    PHOTO_DIR = BASE_OUTPUT_DIR / os.getenv("EVIDENCE_PHOTO_DIR", "fotos")
    HTML_DIR = BASE_OUTPUT_DIR / os.getenv("EVIDENCE_HTML_DIR", "reportes_html")
    PDF_DIR = BASE_OUTPUT_DIR / os.getenv("EVIDENCE_PDF_DIR", "reportes_pdf")

    # Configuración de video
    VIDEO_ENABLED = os.getenv("EVIDENCE_VIDEO_ENABLED", "True").lower() == "true"
    VIDEO_CODEC = os.getenv("EVIDENCE_VIDEO_CODEC", "vp8")
    VIDEO_TIME_LIMIT = int(os.getenv("EVIDENCE_VIDEO_TIME_LIMIT", 600))
    VIDEO_TIMEOUT = int(os.getenv("EVIDENCE_VIDEO_TIMEOUT", 180))

    # Configuración de capturas
    SCREENSHOT_ON_FAILURE = (
        os.getenv("EVIDENCE_SCREENSHOT_ON_FAILURE", "True").lower() == "true"
    )
    IMAGE_MAX_DIMENSION = int(os.getenv("EVIDENCE_IMAGE_MAX_DIM", 1400))
    IMAGE_QUALITY = int(os.getenv("EVIDENCE_IMAGE_QUALITY", 75))

    # Reportes
    GENERATE_HTML = os.getenv("EVIDENCE_GENERATE_HTML", "True").lower() == "true"
    GENERATE_PDF = os.getenv("EVIDENCE_GENERATE_PDF", "True").lower() == "true"

    # Allure
    ATTACH_TO_ALLURE = os.getenv("EVIDENCE_ATTACH_ALLURE", "True").lower() == "true"


class TestConfig:
    """Configuración de pruebas"""

    ENVIRONMENT = os.getenv("TEST_ENVIRONMENT", "dev")  # dev, qa, staging, prod

    # Configuración de reintentos
    MAX_RETRIES = int(os.getenv("TEST_MAX_RETRIES", 0))
    RETRY_DELAY = int(os.getenv("TEST_RETRY_DELAY", 2))

    # Configuración de logs
    LOG_LEVEL = os.getenv("TEST_LOG_LEVEL", "INFO")
    VERBOSE = os.getenv("TEST_VERBOSE", "False").lower() == "true"

    # Delays entre acciones
    DEFAULT_SLEEP = float(os.getenv("TEST_DEFAULT_SLEEP", 0.5))
    ACTION_DELAY = float(os.getenv("TEST_ACTION_DELAY", 1.0))


class CompanyConfig:
    """Configuración de la empresa (para reportes)"""

    NAME = os.getenv("COMPANY_NAME", "Mi Empresa")
    PROJECT_NAME = os.getenv("PROJECT_NAME", "Valmex Mobile Testing")
    TEAM_NAME = os.getenv("TEAM_NAME", "QA Team")

    # Logo (ruta o base64)
    LOGO_PATH = os.getenv("COMPANY_LOGO_PATH", "")


# Instancias singleton
appium = AppiumConfig()
device = DeviceConfig()
app = AppConfig()
evidence = EvidenceConfig()
test = TestConfig()
company = CompanyConfig()


# Función helper para validar configuración
def validate_config():
    """Valida que la configuración esté correcta"""
    errors = []

    # Validar que el APK existe si se requiere instalación
    if app.INSTALL_APP and not app.APK_PATH.exists():
        errors.append(f"APK no encontrado en: {app.APK_PATH}")

    # Validar timeouts
    if appium.NEW_COMMAND_TIMEOUT < 60:
        errors.append("APPIUM_NEW_COMMAND_TIMEOUT debe ser >= 60 segundos")

    # Validar directorios
    for dir_path in [
        evidence.VIDEO_DIR,
        evidence.PHOTO_DIR,
        evidence.HTML_DIR,
        evidence.PDF_DIR,
    ]:
        dir_path.mkdir(parents=True, exist_ok=True)

    if errors:
        print("❌ Errores de configuración:")
        for error in errors:
            print(f"  - {error}")
        return False

    print("✅ Configuración validada correctamente")
    return True


def print_config_summary():
    """Imprime un resumen de la configuración actual"""
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE CONFIGURACIÓN")
    print("=" * 60)

    print(f"\n🌍 ENTORNO: {test.ENVIRONMENT.upper()}")

    print(f"\n🔧 APPIUM:")
    print(f"  └─ URL: {appium.url}")
    print(f"  └─ Timeout: {appium.NEW_COMMAND_TIMEOUT}s")

    print(f"\n📱 DISPOSITIVO:")
    print(f"  └─ Nombre: {device.DEVICE_NAME}")
    print(f"  └─ Platform: {device.PLATFORM_NAME} {device.PLATFORM_VERSION}")
    print(f"  └─ No Reset: {device.NO_RESET}")

    print(f"\n📦 APLICACIÓN:")
    print(f"  └─ Package: {app.PACKAGE_NAME}")
    print(f"  └─ Activity: {app.ACTIVITY_NAME}")
    print(f"  └─ Instalar APK: {app.INSTALL_APP}")
    if app.INSTALL_APP:
        print(f"  └─ APK Path: {app.APK_PATH}")

    print(f"\n📸 EVIDENCIAS:")
    print(f"  └─ Video: {'✅' if evidence.VIDEO_ENABLED else '❌'}")
    print(f"  └─ HTML Report: {'✅' if evidence.GENERATE_HTML else '❌'}")
    print(f"  └─ PDF Report: {'✅' if evidence.GENERATE_PDF else '❌'}")
    print(f"  └─ Base Dir: {evidence.BASE_OUTPUT_DIR}")

    print(f"\n🏢 EMPRESA:")
    print(f"  └─ Nombre: {company.NAME}")
    print(f"  └─ Proyecto: {company.PROJECT_NAME}")

    print("=" * 60 + "\n")


if __name__ == "__main__":
    # Validar y mostrar configuración
    validate_config()
    print_config_summary()
