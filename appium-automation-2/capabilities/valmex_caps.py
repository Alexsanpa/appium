"""
Configuración de capabilities para la aplicación Valmex
Ahora usa el sistema de configuración centralizado
"""

from config.settings import appium, device, app


def get_valmex_capabilities():
    """
    Retorna las capabilities para la aplicación Valmex (con instalación de APK)
    """
    caps = {
        # Configuración básica de Appium
        "platformName": device.PLATFORM_NAME,
        "appium:platformVersion": device.PLATFORM_VERSION,
        "appium:deviceName": device.DEVICE_NAME,
        "appium:automationName": device.AUTOMATION_NAME,
        # Configuración de la app Valmex
        "appium:app": str(app.APK_PATH),
        "appium:appPackage": app.PACKAGE_NAME,
        "appium:appActivity": app.ACTIVITY_NAME,
        # Configuración adicional
        "appium:noReset": False,
        "appium:fullReset": device.FULL_RESET,
        "appium:newCommandTimeout": appium.NEW_COMMAND_TIMEOUT,
        "appium:autoGrantPermissions": device.AUTO_GRANT_PERMISSIONS,
        # Configuración de espera
        "appium:uiautomator2ServerInstallTimeout": appium.INSTALL_TIMEOUT,
        "appium:adbExecTimeout": appium.ADB_EXEC_TIMEOUT,
    }

    return caps


def get_valmex_capabilities_installed():
    """
    Retorna las capabilities para usar la app Valmex ya instalada
    (No reinstala el APK, más rápido para testing)
    """
    if device.EMULATED_OR_PHYSICAL.lower() == "emulated":
        caps = {
            "platformName": device.PLATFORM_NAME,
            "appium:platformVersion": device.PLATFORM_VERSION,
            "appium:deviceName": device.DEVICE_NAME,
            "appium:automationName": device.AUTOMATION_NAME,
            # AVD and Snapshot configuration
            "appium:avd": device.DEVICE_AVD,
            # Solo usar la app ya instalada
            "appium:appPackage": app.PACKAGE_NAME,
            "appium:appActivity": app.ACTIVITY_NAME,
            "appium:noReset": device.NO_RESET,
            "appium:fullReset": device.FULL_RESET,
            "appium:newCommandTimeout": appium.NEW_COMMAND_TIMEOUT,
            "appium:autoGrantPermissions": device.AUTO_GRANT_PERMISSIONS,
            # GPS/Location configuration for Mexico
            "appium:gpsEnabled": True,
            "appium:setGeoLocation": True,
            "appium:locationServicesEnabled": True,
            "appium:locationServicesAuthorized": True,
        }
    if device.EMULATED_OR_PHYSICAL.lower() == "physical":
        caps = {
            "platformName": device.PLATFORM_NAME,
            "appium:platformVersion": device.PLATFORM_VERSION,
            "appium:deviceName": device.DEVICE_NAME,
            "appium:automationName": device.AUTOMATION_NAME,
            # Solo usar la app ya instalada
            "appium:appPackage": app.PACKAGE_NAME,
            "appium:appActivity": app.ACTIVITY_NAME,
            "appium:noReset": device.NO_RESET,
            "appium:fullReset": device.FULL_RESET,
            "appium:newCommandTimeout": appium.NEW_COMMAND_TIMEOUT,
            "appium:autoGrantPermissions": device.AUTO_GRANT_PERMISSIONS,
            # GPS/Location configuration for Mexico
            "appium:gpsEnabled": True,
            "appium:setGeoLocation": True,
            "appium:locationServicesEnabled": True,
            "appium:locationServicesAuthorized": True,
        }

    return caps


def get_capabilities_by_mode(install_app: bool = None):
    """
    Retorna las capabilities según el modo especificado o la configuración

    Args:
        install_app: Si es True, instala el APK. Si es None, usa la config.

    Returns:
        dict: Capabilities de Appium
    """
    if install_app is None:
        install_app = app.INSTALL_APP

    if install_app:
        return get_valmex_capabilities()
    else:
        return get_valmex_capabilities_installed()
