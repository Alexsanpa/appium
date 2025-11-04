"""
Configuración de pytest para las pruebas de Appium
"""
from time import sleep
import pytest
from utils.appium_driver import AppiumDriver
from capabilities.valmex_caps import get_valmex_capabilities_installed
from utils.evidences import (
    start_video_recording,
    stop_and_save_video_if_recording,
    generate_html_report,
    take_evidence,
)


@pytest.fixture(scope="function")
def valmex_driver(request):
    """
    Fixture específico para la app Valmex.
    Inicia y cierra el driver de Appium para cada función de prueba.
    Gestiona automáticamente:
    - Inicio del driver
    - Grabación de video
    - Capturas de evidencia en caso de fallo
    - Generación de reportes HTML/PDF
    """
    print("\n" + "="*50)
    print("SETUP: Iniciando driver para Valmex App")
    print("="*50)

    # 1. Obtener las capacidades necesarias
    caps = get_valmex_capabilities_installed()
    
    # 2. Inicializar tu gestor de driver
    appium_driver = AppiumDriver(caps)

    # 3. Iniciar la sesión de Appium
    driver_instance = appium_driver.start_driver()

    # 4. Obtener el nombre del test
    test_name = request.node.name 

    # 5. Configuración de video
    VIDEO_ENABLED = True 

    # 6. Establecer el estado de la evidencia ANTES del yield
    setattr(driver_instance, 'evidence_state', {
        'is_recording': False,
        'test_name': test_name, 
        'step_count': 0
    })
    
    # 7. Iniciar la grabación si está habilitada
    if VIDEO_ENABLED:
        start_video_recording(driver_instance, test_name) 

    # 8. Entregar el driver al test
    yield driver_instance
    
    sleep(2)

    # ============================================
    # TEARDOWN: Gestión post-ejecución
    # ============================================
    
    # 9. Obtener el resultado del test
    rep = getattr(request.node, "rep_call", None)
    status = "PASSED"
    error_text = None

    if rep is not None and rep.failed:
        status = "FAILED"
        try:
            error_text = str(rep.longrepr)
        except Exception:
            error_text = repr(rep)

    # 10. Guardar estado final y error en el evidence_state del driver
    state = getattr(driver_instance, "evidence_state", {}) or {}
    state['final_status'] = status
    if error_text:
        state['error'] = error_text
    setattr(driver_instance, 'evidence_state', state)

    # 11. Tomar captura del error si existe
    if error_text:
        try:
            take_evidence(driver_instance, step_log=error_text)
            print("📸 Captura del paso fallido tomada y añadida con el log de error.")
        except Exception as e:
            print(f"⚠️ No se pudo tomar captura del paso fallido: {e}")

    print("\n" + "="*50)
    print("TEARDOWN: Cerrando driver y gestionando video")
    print("="*50)

    # 12. Detener video y generar reportes
    stop_and_save_video_if_recording(driver_instance, test_name)
    appium_driver.stop_driver()
    generate_html_report(driver_instance, status=status)


@pytest.fixture(scope="function")
def driver():
    """
    Fixture simple sin gestión de evidencias (para pruebas básicas)
    """
    print("\n" + "="*50)
    print("🔧 SETUP: Iniciando driver de Appium")
    print("="*50)
    
    caps = get_valmex_capabilities_installed()
    appium_driver = AppiumDriver(caps)
    driver_instance = appium_driver.start_driver()
    
    yield driver_instance
    
    print("\n" + "="*50)
    print("🧹 TEARDOWN: Cerrando driver de Appium")
    print("="*50)
    appium_driver.stop_driver()


@pytest.fixture(scope="session")
def appium_server_check():
    """
    Fixture que verifica si el servidor de Appium está corriendo
    antes de ejecutar las pruebas
    """
    import requests
    
    try:
        print("\n🔍 Verificando si Appium Server está corriendo...")
        response = requests.get("http://localhost:4723/status", timeout=5)
        if response.status_code == 200:
            print("✅ Appium Server está corriendo correctamente")
        else:
            print("⚠️ Appium Server respondió pero con un estado inesperado")
    except requests.exceptions.RequestException:
        print("\n" + "="*60)
        print("❌ ERROR: Appium Server NO está corriendo")
        print("="*60)
        print("\n💡 Para iniciar Appium Server, ejecuta en otra terminal:")
        print("   appium")
        print("\n")
        pytest.exit("Appium Server no está disponible", returncode=1)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook que guarda el resultado del test para usarlo en la fixture
    """
    outcome = yield
    rep = outcome.get_result()
    # Guarda solo la fase "call" (ejecución del test)
    if rep.when == "call":
        setattr(item, "rep_call", rep)

        
# Configuración de pytest
def pytest_configure(config):
    """
    Configuración inicial de pytest
    """
    config.addinivalue_line(
        "markers", "smoke: marca pruebas de smoke testing"
    )
    config.addinivalue_line(
        "markers", "regression: marca pruebas de regresión"
    )