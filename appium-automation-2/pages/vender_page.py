from time import sleep
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from appium.webdriver.common.appiumby import AppiumBy


class ValmexVenderPage:
    """
    Clase que describe los objetos y acciones para el flujo de la app móvil Valmex.
    """

    # ----------------------------------------------------
    # 1. LOCALIZADORES (Usando el patrón (By_Method, Value))
    # NOTA: Ajusta estos localizadores si NO son Accessibility ID o si la app NO usa Android
    # ----------------------------------------------------

    SELECCIONE_FONDO = (AppiumBy.ACCESSIBILITY_ID, "Fondo\nSeleccione un fondo")
    IMPORTE_FIELD = (AppiumBy.XPATH, '//android.widget.EditText[@hint="Importe"]')
    CONTRACT_BY_NUMBER = lambda self, contract_number: (
        AppiumBy.XPATH,
        f'//android.view.View[contains(@content-desc, "Contrato - {contract_number}")]',
    )
    VENDER_BUTTON = (AppiumBy.XPATH, '//android.widget.Button[@content-desc="Vender"]')
    CONFIRMAR_OPERACION_BTN = (AppiumBy.ACCESSIBILITY_ID, "Confirmar operación")
    DETALLE_DE_OPERACION_LABEL = (
        AppiumBy.XPATH,
        '//android.view.View[@content-desc="Detalle de operación"]',
    )

    DEFAULT_WAIT_TIME = 5

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, self.DEFAULT_WAIT_TIME)

    def validate_vender_page_loaded(self):
        """
        Valida que la página de vender se haya cargado correctamente.
        """
        try:
            self.wait.until(EC.presence_of_element_located(self.SELECCIONE_FONDO))
            return True
        except TimeoutException:
            return False

    def validate_confirmation_page_loaded(self):
        """
        Valida que la página de confirmación se haya cargado correctamente.
        """
        try:
            self.wait.until(
                EC.presence_of_element_located(self.CONFIRMAR_OPERACION_BTN)
            )
            return True
        except TimeoutException:
            return False

    def validate_detalle_de_operacion_page_loaded(self):
        """
        Valida que la página de detalle de operación se haya cargado correctamente.
        """
        try:
            self.wait.until(
                EC.presence_of_element_located(self.DETALLE_DE_OPERACION_LABEL)
            )
            return True
        except TimeoutException:
            return False

    def select_fund_by_name(self, fund_name):
        """
        Selecciona un fondo por su nombre exacto o parcial.

        Args:
            fund_name (str): Nombre del fondo a buscar (ej: "VALMXES", "VXGUBCP")

        Returns:
            bool: True si la selección fue exitosa, False en caso contrario.
        """
        try:
            # Abrir el selector de fondos
            if not self._open_fund_selector():
                return False

            # Buscar el fondo por nombre
            fund_element = self._find_fund_by_criteria(name=fund_name)

            if fund_element:
                fund_element.click()
                print(f"✅ Fondo '{fund_name}' seleccionado exitosamente")
                return True
            else:
                print(f"❌ No se encontró el fondo '{fund_name}'")
                return False

        except Exception as e:
            print(f"❌ Error al seleccionar fondo por nombre: {e}")
            return False

    def select_fund_by_criteria(
        self, name=None, value_min=None, value_max=None, liquidity_days=None
    ):
        """
        Selecciona un fondo basado en múltiples criterios.

        Args:
            name (str, optional): Nombre parcial o completo del fondo
            value_min (float, optional): Valor mínimo del fondo
            value_max (float, optional): Valor máximo del fondo
            liquidity_days (int, optional): Días de liquidez (0 = hoy, 1 = mañana, etc.)

        Returns:
            bool: True si la selección fue exitosa, False en caso contrario.
        """
        try:
            # Abrir el selector de fondos
            if not self._open_fund_selector():
                return False

            # Buscar el fondo por criterios
            fund_element = self._find_fund_by_criteria(
                name=name,
                value_min=value_min,
                value_max=value_max,
                liquidity_days=liquidity_days,
            )

            if fund_element:
                fund_desc = fund_element.get_attribute("content-desc")
                fund_element.click()
                print(f"✅ Fondo seleccionado exitosamente: {fund_desc}")
                return True
            else:
                print(
                    "❌ No se encontró ningún fondo que cumpla con los criterios especificados"
                )
                return False

        except Exception as e:
            print(f"❌ Error al seleccionar fondo por criterios: {e}")
            return False

    def select_fund_by_visible_position(self, position):
        """
        Selecciona un fondo por su posición en la vista actual (sin scroll).

        Args:
            position (int): Posición del fondo en la vista actual (0 = primero visible)

        Returns:
            bool: True si la selección fue exitosa, False en caso contrario.
        """
        try:
            # Abrir el selector de fondos
            if not self._open_fund_selector():
                return False

            # Obtener fondos visibles actuales
            visible_funds = self._get_visible_funds()

            if position >= len(visible_funds):
                print(
                    f"❌ Posición {position} fuera de rango (fondos visibles: 0-{len(visible_funds)-1})"
                )
                return False

            fund_element = visible_funds[position]
            fund_desc = fund_element.get_attribute("content-desc")
            fund_element.click()
            print(f"✅ Fondo en posición {position} seleccionado: {fund_desc}")
            return True

        except Exception as e:
            print(f"❌ Error al seleccionar fondo por posición: {e}")
            return False

    def _open_fund_selector(self):
        """
        Abre el selector de fondos.

        Returns:
            bool: True si se abrió exitosamente, False en caso contrario.
        """
        try:
            select_fund_btn = self.wait.until(
                EC.element_to_be_clickable(self.SELECCIONE_FONDO)
            )
            select_fund_btn.click()
            sleep(2)  # Esperar a que se abra el selector
            return True
        except TimeoutException:
            print("❌ No se pudo abrir el selector de fondos")
            return False

    def _get_visible_funds(self):
        """
        Obtiene todos los fondos visibles en la pantalla actual.

        Returns:
            list: Lista de elementos de fondos visibles.
        """
        try:
            funds_locator = (
                AppiumBy.XPATH,
                "//android.widget.Button[contains(@content-desc, 'V')]",
            )
            return self.driver.find_elements(*funds_locator)
        except Exception:
            return []

    def _find_fund_by_criteria(
        self, name=None, value_min=None, value_max=None, liquidity_days=None
    ):
        """
        Busca un fondo que cumpla con los criterios especificados, usando scroll si es necesario.

        Args:
            name (str, optional): Nombre parcial o completo del fondo
            value_min (float, optional): Valor mínimo del fondo
            value_max (float, optional): Valor máximo del fondo
            liquidity_days (int, optional): Días de liquidez

        Returns:
            WebElement: Elemento del fondo encontrado o None si no se encuentra.
        """
        max_scrolls = 10  # Límite de scrolls para evitar bucle infinito
        scroll_count = 0
        previous_funds = set()

        while scroll_count < max_scrolls:
            # Obtener fondos visibles actuales
            visible_funds = self._get_visible_funds()

            if not visible_funds:
                break

            # Crear identificadores únicos para los fondos actuales
            current_funds = set()

            for fund_element in visible_funds:
                try:
                    fund_desc = fund_element.get_attribute("content-desc")
                    if not fund_desc:
                        continue

                    current_funds.add(fund_desc)

                    # Parsear la información del fondo
                    fund_info = self._parse_fund_description(fund_desc)

                    # Verificar si cumple con los criterios
                    if self._matches_criteria(
                        fund_info, name, value_min, value_max, liquidity_days
                    ):
                        return fund_element

                except Exception as e:
                    print(f"⚠️ Error procesando fondo: {e}")
                    continue

            # Si ya vimos estos fondos, hemos llegado al final
            if current_funds.issubset(previous_funds):
                break

            previous_funds.update(current_funds)

            # Hacer scroll hacia abajo
            self._scroll_fund_list_down()
            scroll_count += 1
            sleep(1)  # Breve pausa después del scroll

        return None

    def _parse_fund_description(self, description):
        """
        Parsea la descripción de un fondo para extraer su información.

        Args:
            description (str): Descripción completa del fondo

        Returns:
            dict: Diccionario con la información parseada del fondo
        """
        try:
            # Ejemplo: "VXGUBCP - $38.561459 (Liquida hoy)"
            # Ejemplo: "VLMXTEC - $6.700650 (Liquida en 1 dias)"

            fund_info = {
                "name": "",
                "value": 0.0,
                "liquidity_days": 0,
                "full_description": description,
            }

            # Extraer nombre del fondo (antes del primer " - ")
            if " - " in description:
                fund_info["name"] = description.split(" - ")[0].strip()

            # Extraer valor (buscar patrón $X.XXXXXX)
            import re

            value_match = re.search(r"\$(\d+\.?\d*)", description)
            if value_match:
                fund_info["value"] = float(value_match.group(1))

            # Extraer días de liquidez
            if "Liquida hoy" in description:
                fund_info["liquidity_days"] = 0
            elif "Liquida en" in description:
                days_match = re.search(r"Liquida en (\d+) dias?", description)
                if days_match:
                    fund_info["liquidity_days"] = int(days_match.group(1))

            return fund_info

        except Exception as e:
            print(f"⚠️ Error parseando descripción del fondo: {e}")
            return {
                "name": "",
                "value": 0.0,
                "liquidity_days": 0,
                "full_description": description,
            }

    def _matches_criteria(
        self, fund_info, name=None, value_min=None, value_max=None, liquidity_days=None
    ):
        """
        Verifica si un fondo cumple con los criterios especificados.

        Args:
            fund_info (dict): Información del fondo
            name, value_min, value_max, liquidity_days: Criterios de búsqueda

        Returns:
            bool: True si cumple con todos los criterios especificados
        """
        try:
            # Verificar nombre (búsqueda parcial, case-insensitive)
            if name and name.upper() not in fund_info["name"].upper():
                return False

            # Verificar valor mínimo
            if value_min is not None and fund_info["value"] < value_min:
                return False

            # Verificar valor máximo
            if value_max is not None and fund_info["value"] > value_max:
                return False

            # Verificar días de liquidez
            if (
                liquidity_days is not None
                and fund_info["liquidity_days"] != liquidity_days
            ):
                return False

            return True

        except Exception:
            return False

    def _scroll_fund_list_down(self):
        """
        Hace scroll hacia abajo en la lista de fondos.
        """
        try:
            # Obtener dimensiones de la pantalla
            size = self.driver.get_window_size()

            # Coordenadas para el scroll (desde 80% hacia 20% de la altura)
            start_y = int(size["height"] * 0.8)
            end_y = int(size["height"] * 0.2)
            x = int(size["width"] * 0.5)

            # Realizar scroll
            self.driver.swipe(x, start_y, x, end_y, duration=1000)

        except Exception as e:
            print(f"⚠️ Error al hacer scroll: {e}")

    def _get_selected_fund_value(self):
        """
        Extrae el valor del fondo seleccionado actual.

        Returns:
            float: Valor del fondo o None si no se puede obtener
        """
        try:
            print("🔍 Buscando información del fondo seleccionado...")

            # Localizadores más generales para capturar cualquier tipo de fondo
            fund_locators = [
                # Buscar cualquier elemento que contenga patrón de fondo con valor
                (
                    AppiumBy.XPATH,
                    "//android.widget.Button[contains(@content-desc, ' - $') and contains(@content-desc, 'Liquida')]",
                ),
                # Buscar fondos que empiecen con V (VALMX, VXGUBCP, etc.)
                (
                    AppiumBy.XPATH,
                    "//android.widget.Button[starts-with(@content-desc, 'V') and contains(@content-desc, '$')]",
                ),
                # Buscar cualquier elemento con formato de fondo
                (
                    AppiumBy.XPATH,
                    "//android.widget.Button[contains(@content-desc, '$') and contains(@content-desc, 'Liquida')]",
                ),
                # Buscar elementos que contengan nombres de fondos específicos conocidos
                (
                    AppiumBy.XPATH,
                    "//android.widget.Button[contains(@content-desc, 'VALMX') or contains(@content-desc, 'VXGUB') or contains(@content-desc, 'VXREP') or contains(@content-desc, 'VXDEU') or contains(@content-desc, 'VLMX')]",
                ),
                # Buscar cualquier elemento que tenga el patrón completo
                (
                    AppiumBy.XPATH,
                    "//android.widget.Button[contains(@content-desc, ' - $') and (contains(@content-desc, 'hoy') or contains(@content-desc, 'dias'))]",
                ),
                # Buscar elementos que empiecen por el nombre de Fondo
                (
                    AppiumBy.XPATH,
                    "//android.widget.Button[starts-with(@content-desc, 'Fondo')]",
                ),
            ]

            fund_element = None
            fund_description = None

            # Probar diferentes localizadores
            for i, locator in enumerate(fund_locators):
                try:
                    print(f"🔎 Probando localizador {i+1}: {locator[1]}")
                    elements = self.driver.find_elements(*locator)

                    if elements:
                        print(
                            f"✅ Encontrados {len(elements)} elementos con localizador {i+1}"
                        )

                        # Revisar cada elemento encontrado
                        for j, element in enumerate(elements):
                            try:
                                desc = element.get_attribute("content-desc")
                                if desc:
                                    fund_element = element
                                    fund_description = desc
                                    print(
                                        f"✅ Fondo válido encontrado en elemento {j+1}: {desc}"
                                    )
                                    break
                            except Exception as e:
                                print(f"⚠️ Error procesando elemento {j+1}: {e}")
                                continue

                        if fund_element:
                            break

                except Exception as e:
                    print(f"⚠️ Error con localizador {i+1}: {e}")
                    continue

            if fund_element is None or fund_description is None:
                print("❌ No se encontró información válida del fondo seleccionado")
                return None

            print(f"📋 Descripción del fondo encontrada: {fund_description}")

            # Extraer el valor usando expresión regular más robusta
            fund_value = self._extract_fund_value_from_description(fund_description)

            if fund_value is not None:
                print(f"💰 Valor del fondo extraído: ${fund_value}")
                return fund_value
            else:
                print("❌ No se pudo extraer el valor del fondo de la descripción")
                return None

        except Exception as e:
            print(f"❌ Error extrayendo valor del fondo: {e}")
            return None

    def _extract_fund_value_from_description(self, description):
        """
        Extrae el valor numérico del fondo de su descripción.

        Args:
            description (str): Descripción completa del fondo

        Returns:
            float: Valor del fondo o None si no se puede extraer
        """
        try:
            import re

            # Patrones más robustos para extraer el valor
            value_patterns = [
                r" - \$(\d+\.?\d*)",  # " - $38.561459"
                r"\$(\d+\.\d+)",  # "$38.561459"
                r"\$(\d+)",  # "$38" (sin decimales)
            ]

            for pattern in value_patterns:
                value_match = re.search(pattern, description)
                if value_match:
                    try:
                        fund_value = float(value_match.group(1))
                        print(
                            f"💰 Valor extraído con patrón '{pattern}': ${fund_value}"
                        )
                        return fund_value
                    except ValueError as e:
                        print(
                            f"⚠️ Error convirtiendo valor '{value_match.group(1)}' a float: {e}"
                        )
                        continue

            print(f"❌ No se pudo extraer valor de: {description}")
            return None

        except Exception as e:
            print(f"❌ Error extrayendo valor de la descripción: {e}")
            return None

    def get_all_available_funds(self):
        """
        Obtiene información de todos los fondos disponibles (incluyendo scroll).

        Returns:
            list: Lista con información de todos los fondos disponibles.
        """
        try:
            # Abrir el selector de fondos
            if not self._open_fund_selector():
                return []

            all_funds = []
            max_scrolls = 10
            scroll_count = 0
            seen_funds = set()

            while scroll_count < max_scrolls:
                visible_funds = self._get_visible_funds()

                if not visible_funds:
                    break

                new_funds_found = False

                for fund_element in visible_funds:
                    try:
                        fund_desc = fund_element.get_attribute("content-desc")
                        if fund_desc and fund_desc not in seen_funds:
                            fund_info = self._parse_fund_description(fund_desc)
                            all_funds.append(fund_info)
                            seen_funds.add(fund_desc)
                            new_funds_found = True

                    except Exception as e:
                        print(f"⚠️ Error procesando fondo: {e}")

                if not new_funds_found:
                    break

                self._scroll_fund_list_down()
                scroll_count += 1
                sleep(1)

            print(f"✅ Se encontraron {len(all_funds)} fondos en total")
            return all_funds

        except Exception as e:
            print(f"❌ Error obteniendo todos los fondos: {e}")
            return []

    def set_sell_amount(self, amount):
        """
        Establece la cantidad a vender.

        Args:
            amount (str): La cantidad a vender como cadena (ejemplo: "1000")

        Returns:
            bool: True si la cantidad fue establecida correctamente, False en caso contrario.
        """
        try:
            # Localizador del campo de importe
            amount_input_locator = self.IMPORTE_FIELD
            amount_input = self.wait.until(
                EC.element_to_be_clickable(amount_input_locator)
            )
            amount_input.click()
            amount_input.clear()
            amount_input.send_keys(amount)
            return True

        except TimeoutException:
            print("❌ No se encontró el campo de entrada de cantidad")
            return False
        except Exception as e:
            print(f"❌ Error al establecer la cantidad: {e}")
            return False

    def set_sell_amount_by_titles(self, number_of_titles):
        """
        Calcula y establece el importe de venta basado en el número de títulos deseados.

        Args:
            number_of_titles (int): Número de títulos que se desean vender

        Returns:
            bool: True si la operación fue exitosa, False en caso contrario.
        """
        try:
            print(f"🔢 Calculando importe para {number_of_titles} títulos...")

            # 1. Obtener el valor del fondo seleccionado
            fund_value = self._get_selected_fund_value()

            if fund_value is None:
                print("❌ No se pudo obtener el valor del fondo seleccionado")
                return False

            print(f"💰 Valor del fondo: ${fund_value}")

            # 2. Calcular el importe (número de títulos × valor del fondo)
            calculated_amount = number_of_titles * fund_value

            print(
                f"📊 Importe calculado: {number_of_titles} títulos × ${fund_value} = ${calculated_amount:.6f}"
            )

            # 3. Formatear el importe (redondear a 2 decimales para el input)
            formatted_amount = f"{calculated_amount:.2f}"

            print(f"💸 Importe formateado: ${formatted_amount}")

            # 4. Establecer el importe en el campo correspondiente
            success = self.set_sell_amount(formatted_amount)

            if success:
                print(
                    f"✅ Importe ${formatted_amount} establecido exitosamente para {number_of_titles} títulos"
                )
                return True
            else:
                print("❌ No se pudo establecer el importe calculado")
                return False

        except Exception as e:
            print(f"❌ Error al calcular importe por títulos: {e}")
            return False

    def get_liquidation_calculation_info(self):
        """
        Obtiene la información del cálculo estimado de liquidación después de ingresar un importe.

        Returns:
            dict: Diccionario con información de la liquidación o None si no se encuentra
        """
        try:
            print("📊 Obteniendo información del cálculo de liquidación...")

            # Buscar elementos que contengan información de liquidación
            liquidation_elements = self.driver.find_elements(
                AppiumBy.XPATH,
                "//android.view.View[contains(@content-desc, 'Títulos') or contains(@content-desc, 'Importe') or contains(@content-desc, 'Comisión')]",
            )

            liquidation_info = {
                "titles": None,
                "amount": None,
                "commission": None,
                "iva": None,
                "net_amount": None,
            }

            for element in liquidation_elements:
                content_desc = element.get_attribute("content-desc")
                if not content_desc:
                    continue

                print(f"📋 Analizando: {content_desc}")

                # Parsear información según el contenido
                if "Títulos" in content_desc:
                    # Extraer número de títulos
                    import re

                    titles_match = re.search(r"Títulos\n(\d+)", content_desc)
                    if titles_match:
                        liquidation_info["titles"] = int(titles_match.group(1))

                elif "Importe" in content_desc and "$" in content_desc:
                    # Extraer importe
                    amount_match = re.search(r"Importe\n\$(\d+\.?\d*)", content_desc)
                    if amount_match:
                        liquidation_info["amount"] = float(amount_match.group(1))

                elif "Comisión" in content_desc:
                    # Extraer comisión
                    commission_match = re.search(
                        r"Comisión\n\$(\d+\.?\d*)", content_desc
                    )
                    if commission_match:
                        liquidation_info["commission"] = float(
                            commission_match.group(1)
                        )

                elif "Neto a liquidar" in content_desc:
                    # Extraer neto a liquidar
                    net_match = re.search(
                        r"Neto a liquidar\n\$(\d+\.?\d*)", content_desc
                    )
                    if net_match:
                        liquidation_info["net_amount"] = float(net_match.group(1))

            print(f"✅ Información de liquidación obtenida: {liquidation_info}")
            return liquidation_info if any(liquidation_info.values()) else None

        except Exception as e:
            print(f"❌ Error obteniendo información de liquidación: {e}")
            return None

    def validate_calculated_titles(self, expected_titles):
        """
        Valida que el número de títulos calculado por la aplicación coincida con lo esperado.

        Args:
            expected_titles (int): Número esperado de títulos

        Returns:
            bool: True si coincide, False en caso contrario
        """
        try:
            print(f"🔍 Validando que se calcularon {expected_titles} títulos...")

            liquidation_info = self.get_liquidation_calculation_info()

            if liquidation_info is None:
                print("❌ No se pudo obtener información de liquidación")
                return False

            calculated_titles = liquidation_info.get("titles")

            if calculated_titles is None:
                print("❌ No se encontró información de títulos en el cálculo")
                return False

            if calculated_titles == expected_titles:
                print(f"✅ Títulos calculados correctamente: {calculated_titles}")
                return True
            else:
                print(
                    f"❌ Títulos no coinciden - Esperado: {expected_titles}, Calculado: {calculated_titles}"
                )
                return False

        except Exception as e:
            print(f"❌ Error validando títulos calculados: {e}")
            return False

    def select_contract_by_number(self, contract_number):
        """
        Selecciona un contrato específico por su número.

        Args:
            contract_number (str): Número del contrato (ej: "244231")

        Returns:
            bool: True si la selección fue exitosa, False en caso contrario.
        """
        try:
            contract_locator = (
                AppiumBy.XPATH,
                f'//android.view.View[contains(@content-desc, "Contrato - {contract_number}")]',
            )

            contract_element = self.wait.until(
                EC.element_to_be_clickable(contract_locator)
            )

            # Get contract info before clicking
            contract_info = contract_element.get_attribute("content-desc")
            print(f"✅ Seleccionando contrato: {contract_info}")

            contract_element.click()
            return True

        except TimeoutException:
            print(f"❌ No se encontró el contrato {contract_number}")
            return False
        except Exception as e:
            print(f"❌ Error al seleccionar contrato: {e}")
            return False

    def select_first_contract(self):
        """
        Selecciona el primer contrato disponible.

        Returns:
            bool: True si la selección fue exitosa, False en caso contrario.
        """
        try:
            contract_element = self.wait.until(
                EC.element_to_be_clickable(self.CONTRACT_ITEM)
            )

            # Get contract info before clicking
            contract_info = contract_element.get_attribute("content-desc")
            print(f"✅ Seleccionando primer contrato: {contract_info}")

            contract_element.click()
            return True

        except TimeoutException:
            print("❌ No se encontró ningún contrato")
            return False
        except Exception as e:
            print(f"❌ Error al seleccionar contrato: {e}")
            return False

    def get_all_contracts(self):
        """
        Obtiene todos los contratos disponibles.

        Returns:
            list: Lista de diccionarios con información de cada contrato
        """
        try:
            contracts_locator = (
                AppiumBy.XPATH,
                '//android.view.View[contains(@content-desc, "Contrato")]',
            )

            contract_elements = self.driver.find_elements(*contracts_locator)

            contracts = []
            for i, element in enumerate(contract_elements):
                content_desc = element.get_attribute("content-desc")

                # Parse contract number and amount from content-desc
                if content_desc:
                    parts = content_desc.split("\\n")
                    contract_line = parts[0] if parts else content_desc
                    amount = parts[1] if len(parts) > 1 else "N/A"

                    # Extract contract number
                    contract_number = (
                        contract_line.replace("Contrato - ", "")
                        if "Contrato - " in contract_line
                        else "Unknown"
                    )

                    contracts.append(
                        {
                            "index": i,
                            "contract_number": contract_number,
                            "amount": amount,
                            "full_description": content_desc,
                            "bounds": element.get_attribute("bounds"),
                        }
                    )

            return contracts

        except Exception as e:
            print(f"❌ Error al obtener contratos: {e}")
            return []

    def select_contract_by_index(self, index):
        """
        Selecciona un contrato por su índice en la lista.

        Args:
            index (int): Índice del contrato (0 = primero, 1 = segundo, etc.)

        Returns:
            bool: True si la selección fue exitosa, False en caso contrario.
        """
        try:
            contracts = self.get_all_contracts()

            if not contracts:
                print("❌ No se encontraron contratos disponibles")
                return False

            if index >= len(contracts):
                print(
                    f"❌ Índice {index} fuera de rango (disponibles: 0-{len(contracts)-1})"
                )
                return False

            contract_info = contracts[index]
            print(
                f"✅ Seleccionando contrato por índice {index}: {contract_info['full_description']}"
            )

            return self.select_contract_by_number(contract_info["contract_number"])

        except Exception as e:
            print(f"❌ Error al seleccionar contrato por índice: {e}")
            return False

    def get_contract_amount(self, contract_number):
        """
        Obtiene el monto de un contrato específico.

        Args:
            contract_number (str): Número del contrato

        Returns:
            str: Monto del contrato o None si no se encuentra
        """
        try:
            contracts = self.get_all_contracts()

            for contract in contracts:
                if contract["contract_number"] == contract_number:
                    return contract["amount"]

            print(f"❌ No se encontró el contrato {contract_number}")
            return None

        except Exception as e:
            print(f"❌ Error al obtener monto del contrato: {e}")
            return None

    def click_vender_button(self):
        """
        Hace clic en el botón Vender para ejecutar la venta.

        Returns:
            bool: True si el clic fue exitoso, False en caso contrario.
        """
        try:
            # Wait for the button to be enabled and clickable
            vender_button = self.wait.until(
                EC.element_to_be_clickable(self.VENDER_BUTTON)
            )

            # Verify button is enabled before clicking
            is_enabled = vender_button.get_attribute("enabled")
            is_clickable = vender_button.get_attribute("clickable")

            if is_enabled == "true" and is_clickable == "true":
                vender_button.click()
                return True
            else:
                print("❌ Botón Vender no está habilitado")
                return False

        except TimeoutException:
            print("❌ No se encontró el botón Vender o no está habilitado")
            return False
        except Exception as e:
            print(f"❌ Error al hacer clic en Vender: {e}")
            return False

    def click_confirmar_operacion(self):
        """
        Hace clic en el botón 'Confirmar operación' para confirmar la venta.

        Returns:
            bool: True si el clic fue exitoso, False en caso contrario.
        """
        try:
            print("🔍 Buscando botón 'Confirmar operación'...")

            # Wait for the confirmation button to be clickable
            confirmar_button = self.wait.until(
                EC.element_to_be_clickable(self.CONFIRMAR_OPERACION_BTN)
            )

            print("✅ Botón 'Confirmar operación' encontrado, haciendo clic...")
            confirmar_button.click()

            print("✅ Operación confirmada exitosamente")
            return True

        except TimeoutException:
            print("❌ No se encontró el botón 'Confirmar operación'")
            return False
        except Exception as e:
            print(f"❌ Error al confirmar operación: {e}")
            return False

    def validate_text_exists_on_page(
        self, text_to_find, partial_match=True, max_scrolls=10
    ):
        """
        Valida si un texto existe en cualquier parte de la página, usando scroll si es necesario.

        Args:
            text_to_find (str): Texto a buscar en la página
            partial_match (bool): Si True, busca coincidencia parcial. Si False, coincidencia exacta
            max_scrolls (int): Número máximo de scrolls a realizar

        Returns:
            bool: True si el texto se encuentra, False en caso contrario
        """
        try:
            print(f"🔍 Buscando texto: '{text_to_find}'")

            scroll_count = 0
            seen_content = set()

            while scroll_count < max_scrolls:
                # Obtener todo el contenido visible actual
                current_content = self._get_all_visible_text()

                # Verificar si el texto existe en el contenido actual
                if self._text_found_in_content(
                    text_to_find, current_content, partial_match
                ):
                    print(f"✅ Texto '{text_to_find}' encontrado en la página")
                    return True

                # Crear un identificador único del contenido actual
                content_signature = hash(str(sorted(current_content)))

                # Si ya vimos este contenido, hemos llegado al final
                if content_signature in seen_content:
                    print(
                        "🔄 Se detectó contenido repetido, se alcanzó el final de la página"
                    )
                    break

                seen_content.add(content_signature)

                # Hacer scroll hacia abajo
                print(f"📜 Haciendo scroll {scroll_count + 1}/{max_scrolls}")
                self._scroll_page_down()
                scroll_count += 1
                sleep(1)  # Pausa para que cargue el contenido

            print(
                f"❌ Texto '{text_to_find}' no encontrado después de {scroll_count} scrolls"
            )
            return False

        except Exception as e:
            print(f"❌ Error al buscar texto en la página: {e}")
            return False

    def _get_all_visible_text(self):
        """
        Obtiene todo el texto visible en la pantalla actual.

        Returns:
            list: Lista con todos los textos visibles
        """
        try:
            # Buscar todos los elementos que contengan texto
            text_elements = self.driver.find_elements(
                AppiumBy.XPATH,
                "//*[@content-desc and string-length(@content-desc) > 0]",
            )

            visible_texts = []

            for element in text_elements:
                try:
                    content_desc = element.get_attribute("content-desc")
                    if content_desc and content_desc.strip():
                        visible_texts.append(content_desc.strip())
                except Exception:
                    continue

            # También buscar elementos con texto (para casos donde no hay content-desc)
            try:
                text_nodes = self.driver.find_elements(
                    AppiumBy.XPATH, "//*[@text and string-length(@text) > 0]"
                )

                for element in text_nodes:
                    try:
                        text_content = element.get_attribute("text")
                        if text_content and text_content.strip():
                            visible_texts.append(text_content.strip())
                    except Exception:
                        continue
            except Exception:
                pass

            return visible_texts

        except Exception as e:
            print(f"⚠️ Error obteniendo texto visible: {e}")
            return []

    def _text_found_in_content(self, text_to_find, content_list, partial_match=True):
        """
        Verifica si el texto buscado existe en la lista de contenido.

        Args:
            text_to_find (str): Texto a buscar
            content_list (list): Lista de textos donde buscar
            partial_match (bool): Si True, busca coincidencia parcial

        Returns:
            bool: True si el texto se encuentra
        """
        try:
            text_to_find_clean = text_to_find.strip().lower()

            for content in content_list:
                content_clean = content.lower()

                if partial_match:
                    if text_to_find_clean in content_clean:
                        print(f"✅ Coincidencia parcial encontrada en: '{content}'")
                        return True
                else:
                    if text_to_find_clean == content_clean:
                        print(f"✅ Coincidencia exacta encontrada: '{content}'")
                        return True

            return False

        except Exception as e:
            print(f"⚠️ Error comparando texto: {e}")
            return False

    def _scroll_page_down(self):
        """
        Hace scroll hacia abajo en toda la página.
        """
        try:
            # Obtener dimensiones de la pantalla
            size = self.driver.get_window_size()

            # Coordenadas para el scroll (desde 80% hacia 20% de la altura)
            start_y = int(size["height"] * 0.8)
            end_y = int(size["height"] * 0.2)
            x = int(size["width"] * 0.5)

            # Realizar scroll
            self.driver.swipe(x, start_y, x, end_y, duration=1000)

        except Exception as e:
            print(f"⚠️ Error al hacer scroll en la página: {e}")

    def _scroll_page_up(self):
        """
        Hace scroll hacia arriba en toda la página.
        """
        try:
            # Obtener dimensiones de la pantalla
            size = self.driver.get_window_size()

            # Coordenadas para el scroll (desde 20% hacia 80% de la altura)
            start_y = int(size["height"] * 0.2)
            end_y = int(size["height"] * 0.8)
            x = int(size["width"] * 0.5)

            # Realizar scroll
            self.driver.swipe(x, start_y, x, end_y, duration=1000)

        except Exception as e:
            print(f"⚠️ Error al hacer scroll hacia arriba: {e}")

    def validate_error_message_exists(self, error_message):
        """
        Valida si un mensaje de error específico existe en la página.
        Función especializada para mensajes de error comunes.

        Args:
            error_message (str): Mensaje de error a buscar

        Returns:
            bool: True si el mensaje de error se encuentra
        """
        try:
            print(f"🚨 Validando mensaje de error: '{error_message}'")

            # Buscar el mensaje de error en la página
            error_found = self.validate_text_exists_on_page(
                error_message, partial_match=True
            )

            if error_found:
                print(f"⚠️ Mensaje de error confirmado: '{error_message}'")
            else:
                print(f"✅ No se encontró el mensaje de error: '{error_message}'")

            return error_found

        except Exception as e:
            print(f"❌ Error al validar mensaje de error: {e}")
            return False

    def get_all_page_content(self, max_scrolls=10):
        """
        Obtiene todo el contenido de texto de la página completa.
        Útil para debugging o análisis completo del contenido.

        Args:
            max_scrolls (int): Número máximo de scrolls a realizar

        Returns:
            list: Lista con todo el contenido de texto encontrado
        """
        try:
            print("📋 Obteniendo todo el contenido de la página...")

            all_content = []
            scroll_count = 0
            seen_content = set()

            while scroll_count < max_scrolls:
                current_content = self._get_all_visible_text()

                # Agregar contenido nuevo
                for content in current_content:
                    if content not in seen_content:
                        all_content.append(content)
                        seen_content.add(content)

                # Verificar si hay contenido nuevo
                content_signature = hash(str(sorted(current_content)))
                if content_signature in seen_content and scroll_count > 0:
                    break

                self._scroll_page_down()
                scroll_count += 1
                sleep(1)

            print(f"✅ Se obtuvo contenido de {len(all_content)} elementos de texto")
            return all_content

        except Exception as e:
            print(f"❌ Error obteniendo contenido de la página: {e}")
            return []
