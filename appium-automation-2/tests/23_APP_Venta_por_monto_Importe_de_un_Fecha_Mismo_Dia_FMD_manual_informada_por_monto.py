"""
Casos de prueba para la aplicación Valmex Móvil
"""

from time import sleep
from conftest import driver
from pages.home_page import ValmexHomePage
from pages.login_page import ValmexLoginPage
from pages.operations_page import ValmexOperationsPage
from pages.vender_page import ValmexVenderPage
from sapyautomation.core.test_cases import TestData
import os


from utils.evidences import take_evidence
import subprocess


class TestValmexApp:
    """
    Apertura de la app de valmex y validar Textos
    """

    home_page: ValmexHomePage = None

    def test_23_APP_Venta_por_monto_Importe_de_un_FMD_manual_informada_por_monto(self, valmex_driver):
        """
        Ejecución de Todos los Pasos.
        """
        # Get the directory where this script is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to the project root and then to test_data
        project_root = os.path.dirname(current_dir)
        excel_path = os.path.join(
            project_root,
            "test_data",
            "23_APP_Venta_por_monto_Importe_de_un_Fecha_Mismo_Dia_FMD_manual_informada_por_monto.xlsx",
        )

        # Leer datos de prueba desde un archivo de Excel
        book = TestData(excel_path)
        self.data = book.data["data"]

        self.login_page = ValmexLoginPage(valmex_driver)
        self.home_page = ValmexHomePage(valmex_driver)
        self.operations_page = ValmexOperationsPage(valmex_driver)
        self.vender_page = ValmexVenderPage(valmex_driver)

        # get current location to verify
        current_location = valmex_driver.location
        print(f"Current location: {current_location}")
        # Ejecución de los pasos de prueba
        self.step_01_open_and_validate(valmex_driver)
        self.step_02_ingresar_password(valmex_driver)
        self.step_03_click_operaciones(valmex_driver)
        self.step_04_click_vender(valmex_driver)
        self.step_05_seleccionar_fondo(valmex_driver)
        self.step_06_ingreso_del_importe_de_venta(valmex_driver)
        self.step_07_Ejecucion_de_la_venta(valmex_driver)
        self.step_08_validacion_de_carga_de_token_movil(valmex_driver)
        self.step_09_validacion_de_datos_del_comprobante_de_venta(valmex_driver)

    def step_01_open_and_validate(self, driver):
        """
        Descripcion: Apertura de la aplicacion
        Resultado Esperado: Carga correctamente la aplicacion y se verifica un elemento clave.
        """
        print("step_01_open_and_validate")
        assert (
            self.login_page.verificar_existencia_texto01() is True
        ), "❌ FALLA DE ASSERT: El texto clave de inicio no se encontró después de 15s."
        take_evidence(driver)
        sleep(10)

    def step_02_ingresar_password(self, driver):
        """
        Descripcion: Ingresar password en la pantalla de login y acceder a la aplicación.
        Resultado Esperado: Carga la pantalla de inicio correctamente.
        """
        print("step_02_ingresar_password")
        assert (
            self.login_page.set_Access_with_credentials(self.data["password"], driver)
            is True
        ), " No fue posible realizar la accion de inicio de sesion."
        driver.hide_keyboard()
        take_evidence(driver)
        sleep(20)  # Espera para asegurar que la pantalla de inicio se haya cargado
        # Validar que la página de inicio se haya cargado correctamente
        assert (
            self.home_page.validate_home_page_loaded() is True
        ), "❌ FALLA DE ASSERT: La página de inicio no se cargó correctamente."

    def step_03_click_operaciones(self, driver):
        """
        Descripcion: Clic en Operaciones
        Resultado Esperado: Se debe navegar a la sección de Operaciones.
        """
        print("step_03_click_operaciones")
        self.home_page.click_operaciones()
        take_evidence(driver)
        sleep(5)  # Espera para asegurar que la pantalla de Operaciones se haya cargado
        # Validar que la página de Operaciones se haya cargado correctamente
        assert (
            self.operations_page.validate_operations_page_loaded() is True
        ), "❌ FALLA DE ASSERT: La página de Operaciones no se cargó correctamente."

    def step_04_click_vender(self, driver):
        """
        Descripcion: Clic en Vender
        Resultado Esperado: Se debe navegar a la sección de Vender.
        """
        print("step_04_click_vender")
        assert (
            self.operations_page.click_vender() is True
        ), " No fue posible realizar la accion de clic en vender."
        take_evidence(driver)
        sleep(5)  # Espera para asegurar que la pantalla de Vender se haya cargado
        # Validar que la página de Vender se haya cargado correctamente
        assert (
            self.vender_page.validate_vender_page_loaded() is True
        ), "❌ FALLA DE ASSERT: La página de Vender no se cargó correctamente."

    def step_05_seleccionar_fondo(self, driver):
        """
        Descripcion: Seleccionar un fondo por índice
        Resultado Esperado: Se debe seleccionar el fondo correctamente.
        """
        print("step_05_seleccionar_fondo")
        assert (
            self.vender_page.select_fund_by_name(
                self.data["fondo"] 
            )
            is True
        ), " No fue posible seleccionar el fondo por índice."
        take_evidence(driver)

    def step_06_ingreso_del_importe_de_venta(self, driver):
        """
        Descripcion: Ingresar monto
        Resultado Esperado: Se debe ingresar el monto y continuar correctamente.
        """
        print("step_06_ingreso_del_importe_de_venta")
        assert (
            self.vender_page.set_sell_amount(self.data["sell_amount"]) is True
        ), " No fue posible ingresar el monto y continuar."
        take_evidence(driver)
        self.vender_page._scroll_page_down()
        sleep(5)  # Espera para asegurar que la pantalla de confirmación se haya cargado

    def step_07_Ejecucion_de_la_venta(self, driver):
        """
        Descripcion: Ejecutar la venta
        Resultado Esperado: Se debe ejecutar la venta correctamente.
        """
        print("step_07_Ejecucion_de_la_venta")
        assert (
            self.vender_page.select_contract_by_number(self.data["contract"]) is True
        ), " No fue posible seleccionar el contrato por número."
        take_evidence(driver)
        sleep(5)  # Espera para asegurar que la pantalla de confirmación se haya cargado
        assert (
            self.vender_page.click_vender_button() is True
        ), " No fue posible ejecutar la venta."
        take_evidence(driver)
        sleep(5)  # Espera para asegurar que la pantalla de confirmación se haya cargado
        # Valida que la página de confirmación se haya cargado correctamente
        assert (
            self.vender_page.validate_confirmation_page_loaded() is True
        ), "❌ FALLA DE ASSERT: La página de Confirmación no se cargó correctamente."

    def step_08_validacion_de_carga_de_token_movil(self, driver):
        """
        Descripcion: Validar carga de token móvil
        Resultado Esperado: Se debe validar que el token móvil se haya cargado correctamente.
        """
        print("step_08_validacion_de_carga_de_token_movil")
        assert (
            self.vender_page.click_confirmar_operacion() is True
        ), " No fue posible confirmar la venta."
        take_evidence(driver)
        sleep(
            15
        )  # Espera para asegurar que la pantalla de confirmación se haya cargado

    def step_09_validacion_de_datos_del_comprobante_de_venta(self, driver):
        """
        Descripcion: Validar carga de detalle de operación
        Resultado Esperado: Se debe validar que el detalle de operación se haya cargado correctamente.
        """
        print("step_09_validacion_de_datos_del_comprobante_de_venta")
        # Valida que la página de detalle de operación se haya cargado correctamente
        assert (
            self.vender_page.validate_detalle_de_operacion_page_loaded() is True
        ), "❌ FALLA DE ASSERT: La página de Detalle de Operación no se cargó correctamente."
        take_evidence(driver)
        sleep(
            5
        ) 