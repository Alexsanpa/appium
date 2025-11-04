from pywinauto import findbestmatch
import time
'''Tomar como base el archivo actions.py de la carpeta vendors/sap y modificarlo para que funcione con JavaFX'''
from sapyautomation.vendors.sap.connection import SAP
from sapyautomation.vendors.sap.elements import ElementById, ElementByName,\
    ElementByLabel



def find_element_by_id(id_locator: str, session: object) -> object:
    """Identifies an element by id

    Identify an element by id locator on your active session

    Args:
        id_locator (str): id attribute of an element
        session (object): your active session

    Returns:
        element (object): element present on windows

    Raises:
        ModuleNotFoundError: if element is not present on windows
    """
    # to be developed



def find_element_by_text(
    text_locator: str, session: object, type_element: str
) -> object:

def find_element_by_name(name_locator: str, session: object,
                         type_element: str) -> object:
    """Identifies an element by name

    Identify an element by name locator

    Args:
        name_locator (str): name attribute of an element
        session (object): your active session
        type_element (str): type attribute of an element

    Returns:
        element (object): element present on windows

    Raises:
        ModuleNotFoundError: if element is not present on windows
    """
    element = ElementByName(element_name=name_locator, session=session,
                            type_element=type_element)

    return element.element()


def find_element_by_text(text_locator: str, session: object,
                         type_element: str) -> object:
    """Identifies an element by text

    Identify an element by text locator

    Args:
        text_locator (str): text attribute of an element
        session (object): your session active
        type_element (str): type attribute of an element

    Returns:
        element (object): element present on windows

    Raises:
        ModuleNotFoundError: if element is not present on windows
    """

    element = ElementByLabel(element_label=text_locator, session=session,
                             type_element=type_element)

    return element.element()


def press(element: object) -> None:
    """Simulates click event

    Simulate a click event on button, icon

    Args:
        element (object): element what you want to press

    Raises:
        AttributeError: If you want to press some element different like
        button or icon
    """
    try:
        element.press()
    except AttributeError:
        raise AttributeError


def press_by_id(element_id: str, connection: int = 0) -> None:
    """Simulates click event

    Simulate a click event on button, icon

    Args:
        element_id (object): element what you want to press
        connection (int): current connection number / session

    Raises:
        AttributeError: If you want to press some element different like
        button or icon
    """
    session = SAP.get_current_connection(connection)
    element = ElementById(element_id=element_id, session=session)
    element.press()

def select(element: object) -> bool:
    """Selects an option

    Select an option of menu or radiobutton

    Args:
        element (object): option what you want to select

    Return:
        bool: True if successful, False otherwise

    Raises:
        AttributeError: If you want to select some element different like
        menu or radiobutton
    """

    # to be developed


def select_value_combo(combo: object, text: str, position: int = 0):
    """Selects a item from a drop down list

    Select a specific value from a drop down list

    Args:
         combo (object): drop down list
         text (str): specific value from drop down list what you want to select
         position (int): position of specific value from drop down list
    Raises:
        KeyError: If your specific value is not into drop down list
        AttributeError: If you want to select a specific value on an element
        different like Combobox
    """

    # para el codigo de Marco


def find_element_by_control_identifier(
    window: object,
    control: str = None,
    control_type: str = None,
) -> list:
    """
    Get a list of similar controls based on the provided criteria.

    Args:
        window (object): The window object to search for controls.
        control (str, optional): The title of the control to search for. Defaults to None.
        control_type (str, optional): The type of the control to search for. Defaults to None.

    Returns:
        list: A list of control names in the order of the controls.

    """
    # flag if first search method fails
    search_fails = False
    # ----- DICT OF INDEX FOR ELEMENTS OF THE SAME TYPE -----
    if control is not None and control_type is not None:
        all_ctrls = window.descendants(control_type=control_type, title=control)
        if len(all_ctrls) == 0:
            all_ctrls = window.descendants()
            search_fails = True

    elif control is not None and control_type is None:
        all_ctrls = window.descendants(title=control)
        if len(all_ctrls) == 0:
            all_ctrls = window.descendants()
            search_fails = True

    elif control is None and control_type is not None:
        all_ctrls = window.descendants(control_type=control_type)
        if len(all_ctrls) == 0:
            all_ctrls = window.descendants()
            search_fails = True

    else:
        all_ctrls = window.descendants()

    # Create a list of all visible text controls
    txt_ctrls = [
        ctrl
        for ctrl in all_ctrls
        if ctrl.can_be_label and ctrl.is_visible() and ctrl.window_text()
    ]

    # Build a dictionary of disambiguated list of control names
    name_ctrl_id_map = findbestmatch.UniqueDict()
    for index, ctrl in enumerate(all_ctrls):
        ctrl_names = findbestmatch.get_control_names(ctrl, all_ctrls, txt_ctrls)
        for name in ctrl_names:
            name_ctrl_id_map[name] = index

    # create a list of control names in the order of the controls
    ctrl_id_name_map = []
    for name, index in name_ctrl_id_map.items():
        ctrl_id_name_map.append(name)

    if search_fails:
        matching_controls = [
            ctrl for ctrl in ctrl_id_name_map if control.lower() in ctrl.lower()
        ]
        ctrl_id_name_map = matching_controls

    return ctrl_id_name_map


def close_caja_warning(
    window: object,
    control: str = "AceptarButton",
    window_title: str = "¡Atención!",
    found_index: int = -1,
    control_type: str = None,
    timeout: int = 15,
) -> None:
    """
    Closes a warning dialog with the specified window title by clicking the specified control.

    Args:
    - window (object): The window object.
    - control (str): The name of the control to click. Defaults to "AceptarButton".
    - window_title (str): The title of the warning dialog to close. Defaults to "¡Atención!".
    - found_index (int): States the index to be found of the child window.
    - control_type (str): The type of the control to click. Defaults to None.

    Raises:
    - AttributeError: If there is an error finding the control or clicking on the control.
    """
    try:
        dlg = window.child_window(
            title=window_title,
            found_index=0,
        )

        dlg.wait("visible", timeout=timeout)
    except:
        return

    try:
        if found_index == 0:
            element = window.__getattribute__(control)

        else:
            ctlrs = find_element_by_control_identifier(
                window=window,
                control=control,
                control_type=control_type,
            )
            element = window.__getattribute__(ctlrs[found_index])
    except:
        raise AttributeError("Error finding the control")

    try:
        if is_element_visible(window=window, window_title=window_title):
            element.click()
    except:
        raise AttributeError("Error when clicking on the control")


def iniciate_transaction(
    window: object,
    transaction_code: str,
    control_clave_transaccion: str = "ClaveStatic",
    found_index: int = 0,
    control_type: str = None,
    window_title: str = None,
) -> None:
    """
    This function initiates a transaction by typing the transaction code followed by the 'ENTER' key.

    Args:
    - window (object): The window object representing the application window.
    - transaction_code (str): The code of the transaction to initiate.
    - control_clave_transaccion (str, optional): The name of the attribute that represents the transaction input field. Defaults to "ClaveStatic".
    - found_index (int, optional): The index of the control to use when multiple controls with the same name are found. Defaults to 0.
    - control_type (str, optional): The type of the control to search for when using window_title. Defaults to None.
    - window_title (str, optional): The title of the window to search for the control. Defaults to None.

    Returns:
    - None

    Raises:
    - AttributeError: If neither control_clave_transaccion nor window_title is specified.
    - ValueError: If window_title is specified but found_index is less than 0.

    """
    if control_clave_transaccion is None and window_title is None:
        raise AttributeError(
            "Debe especificar un atributo (control) o un especificar un atributo (window_title)"
        )
    if window_title is not None and found_index < 0:
        raise ValueError(
            "Cuando se utiliza 'window_title', el índice debe ser mayor o igual a 0. Intente utilizar 'control' en vez de 'window_title'."
        )
    transaction_code = transaction_code + "{ENTER}"
    try:
        if control_clave_transaccion is not None:
            if found_index == 0:
                control_clave = window.__getattribute__(control_clave_transaccion)

            else:
                ctlrs = find_element_by_control_identifier(
                    window=window,
                    control=control_clave_transaccion,
                    control_type=control_type,
                )
                control_clave = window.__getattribute__(ctlrs[found_index])

        elif window_title is not None:
            if control_type is None:
                control_clave = window.child_window(
                    title=window_title,
                    found_index=found_index,
                )
            else:
                control_clave = window.child_window(
                    title=window_title,
                    found_index=found_index,
                    control_type=control_type,
                )
    except AttributeError:
        print("Error al obtener el elemento")
        raise AttributeError

    try:
        control_clave.type_keys(transaction_code)
    except AttributeError:
        print("Error al ingresar la transaccion")


def click_coordinates(element_window: object) -> None:
    """
    Clicks on the center coordinates of the given element window.

    Args:
        element_window (object): The element window to click on.

    Raises:
        AttributeError: If there is an error obtaining or clicking on the element coordinates.
    """
    try:
        element_window.draw_outline()
        time.sleep(5)
        element_info = element_window.element_info
        width = element_info.rectangle.width()
        height = element_info.rectangle.height()
        x_center_of_element = width / 2
        y_center_of_element = height / 2

    except AttributeError:
        raise AttributeError("Error obtaining the element coordinates")

    try:
        element_window.click_input(
            coords=(int(x_center_of_element), int(y_center_of_element))
        )
    except AttributeError:
        raise AttributeError("Error clicking on the element coordinates")


def wait_element_exists(id_locator: str, session: object,
                        max_wait: int = 4) -> object:
    """Waits until element exists


def click_on_element_coordinates(
    window: object,
    control: str = None,
    found_index: int = 0,
    control_type: str = None,
    window_title: str = None,
) -> None:
    """
    Click on an element coordinates by name

    Args:
        window (object): The window object where the element is located.
        control (str, optional): The control of the element. Defaults to None.
        found_index (int, optional): The index of the found element. Defaults to 0.
        control_type (str, optional): The type of the control. Defaults to None.
        window_title (str, optional): The title of the window. Defaults to None.

    Raises:
        AttributeError: If there is an error obtaining the element or clicking on the element coordinates.

    This function clicks on an element within a window based on its coordinates. The element can be identified either by its control or window title.
    If both `control` and `window_title` are None, an AttributeError is raised.
    If `window_title` is used, the `found_index` must be greater than or equal to 0. Otherwise, a ValueError is raised.
    The function first obtains the element based on the provided parameters, then retrieves the element's coordinates.
    Finally, it clicks on the element using the calculated coordinates.

    """
    if control is None and window_title is None:
        raise AttributeError(
            "Debe especificar un atributo (control) o un especificar un atributo (window_title)"
        )
    if window_title is not None and found_index < 0:
        raise ValueError(
            "Cuando se utiliza 'window_title', el índice debe ser mayor o igual a 0. Intente utilizar 'control' en vez de 'window_title'."
        )
    try:
        if control is not None:
            if found_index == 0:
                element_window = window.__getattribute__(control)
            else:
                ctlrs = find_element_by_control_identifier(
                    window=window, control=control, control_type=control_type
                )
                element_window = window.__getattribute__(ctlrs[found_index])
            time.sleep(2)
        elif window_title is not None:
            if control_type is None:
                element_window = window.child_window(
                    title=window_title,
                    found_index=found_index,
                )
            else:
                element_window = window.child_window(
                    title=window_title,
                    found_index=found_index,
                    control_type=control_type,
                )

            time.sleep(2)
    except AttributeError:
        raise AttributeError("Error obtaining the element")

    click_coordinates(element_window)


def click_on_element(
    window: object,
    control: str = None,
    found_index: int = 0,
    control_type: str = None,
    window_title: str = None,
) -> None:
    """
    Click on an element specified by control.

    Args:
        window (object): The window where the element is located.
        control (str, optional): The control of the element. Defaults to None.
        found_index (int, optional): The index of the element if multiple elements with the same control exist. Defaults to 0.
        control_type (str, optional): The type of the control. Defaults to None.
        window_title (str, optional): The title of the window. Defaults to None.

    Raises:
        AttributeError: If there is an error obtaining the element or clicking on it.
        ValueError: If the index is invalid when using 'window_title' parameter.

    """
    if control is None and window_title is None:
        raise AttributeError(
            "Debe especificar un atributo (control) o un especificar un atributo (window_title)"
        )
    if window_title is not None and found_index < 0:
        raise ValueError(
            "Cuando se utiliza 'window_title', el índice debe ser mayor o igual a 0. Intente utilizar 'control' en vez de 'window_title'."
        )
    try:
        if control is not None:
            if found_index == 0:
                element = window.__getattribute__(control)
            else:
                ctlrs = find_element_by_control_identifier(
                    window=window, control=control, control_type=control_type
                )
                element = window.__getattribute__(ctlrs[found_index])

        elif window_title is not None:
            if control_type is None:
                element = window.child_window(
                    title=window_title,
                    found_index=found_index,
                )
            else:
                element = window.child_window(
                    title=window_title,
                    found_index=found_index,
                    control_type=control_type,
                )

    except AttributeError:
        raise AttributeError("Error obtaining the element")

    try:
        element.click()
    except AttributeError:
        raise AttributeError("Error clicking on the element")


def enter_keys(
    window: object,
    content: str,
    control: str = None,
    found_index: int = 0,
    control_type: str = None,
    window_title: str = None,
    enter: bool = True,
) -> None:
    """
    Enters the specified content in the input field and presses the Enter key.

    Args:
        window (object): The window object representing the application window.
        control (str): The name of the input field control.
        content (str): The content to be entered in the input field.
        found_index (int, optional): The index of the control if multiple controls with the same name are found. Defaults to 0.
        control_type (str, optional): The type of the control. Defaults to None.
        window_title (str, optional): The title of the window. Defaults to None.
        enter (bool, optional): Whether to press the Enter key after entering the content. Defaults to True.

    Raises:
        AttributeError: If neither control nor window_title is specified.
        ValueError: If the found_index is less than 0 when using window_title.
        AttributeError: If interaction with the element fails.
    """
    content = str(content)
    if enter:
        field = content.replace(" ", "{SPACE}") + "{ENTER}"

    else:
        field = content.replace(" ", "{SPACE}")

    if control is None and window_title is None:
        raise AttributeError(
            "Debe especificar un atributo (control) o un especificar un atributo (window_title)"
        )
    if window_title is not None and found_index < 0:
        raise ValueError(
            "Cuando se utiliza 'window_title', el índice debe ser mayor o igual a 0. Intente utilizar 'control' en vez de 'window_title'."
        )
    try:
        if control is not None:
            if found_index == 0:
                window.__getattribute__(control).type_keys(field)
            else:
                ctlrs = find_element_by_control_identifier(
                    window=window, control=control, control_type=control_type
                )
                window.__getattribute__(ctlrs[found_index]).type_keys(field)
        elif window_title is not None:
            if control_type is None:
                window.child_window(
                    title=window_title,
                    found_index=found_index,
                ).type_keys(field)
            else:
                window.child_window(
                    title=window_title,
                    found_index=found_index,
                    control_type=control_type,
                ).type_keys(field)
    except:
        raise AttributeError("Fallo al iteractuar con el elemento")


def wait_for_element(
    window: object,
    control: str = None,
    window_title: str = None,
    timeout: int = 45,
    found_index: int = 0,
    control_type: str = None,
) -> None:
    """
    Waits for an element to become visible on the specified window object.

    Args:
    - window (object): The window object.
    - control (str): The name of the control to wait for. Defaults to None.
    - window_title (str): The title of the window to wait for. Defaults to None.
    - timeout (int): The maximum time to wait for the element to become visible. Defaults to 45 seconds.
    - found_index (int): The index of the found element to wait for. Defaults to 0.
    - control_type (str): The type of control to wait for. Defaults to None.

    Raises:
    - AttributeError: If neither control nor window_title is specified.
    - ValueError: If window_title is specified and found_index is less than 0.
    - timeout: If the element is not found within the specified time.
def execute(connection: int = 0):
    """Execute SAP execute
    """
    session = SAP.get_current_connection(connection)
    windows = find_element_by_id("wnd[0]", session)
    send_keys(windows, "F8")

    Returns:
    - None
    """
    if control is None and window_title is None:
        raise AttributeError(
            "Debe especificar un atributo (control) o un especificar un atributo (window_title)"
        )
    if window_title is not None and found_index < 0:
        raise ValueError(
            "Cuando se utiliza 'window_title', el índice debe ser mayor o igual a 0. Intente utilizar 'control' en vez de 'window_title'."
        )
    try:
        if control is not None:
            if found_index == 0:
                window.__getattribute__(control).wait("visible", timeout=timeout)
            else:
                ctlrs = find_element_by_control_identifier(
                    window=window, control=control, control_type=control_type
                )
                window.__getattribute__(ctlrs[found_index]).wait(
                    "visible", timeout=timeout
                )
        elif window_title is not None:
            if control_type is None:
                window.child_window(
                    title=window_title,
                    found_index=found_index,
                ).wait("visible", timeout=timeout)
            else:
                window.child_window(
                    title=window_title,
                    found_index=found_index,
                    control_type=control_type,
                ).wait("visible", timeout=timeout)
    except:
        raise AttributeError("Fallo al iteractuar con el elemento")


def is_element_visible(
    window: object,
    control: str = None,
    window_title: str = None,
    timeout: int = 10,
    found_index: int = 0,
    control_type: str = None,
    condition: str = "visible",
) -> bool:
    """
    Looks for an element within a specified time.


    Args:
    - window (object): The window object.
    - control (str): The name of the control to wait for. Defaults to None.
    - window_title (str): The title of the window to wait for. Defaults to None.
    - timeout (int): The maximum time to wait for the element to become visible. Defaults to 10 seconds.
    - found_index (int): The index of the element to wait for. Defaults to 0.
    - control_type (str): The type of control to wait for. Defaults to None.
    - condition (str): The condition to wait for. Defaults to "visible".
        In pywinauto, the `wait` method is used to wait until a certain condition is met. The condition is specified as a string. Here are some conditions you can use with the `wait` method:

        - `'exists'`: Wait until the window is a valid handle.
        - `'visible'`: Wait until the window is not hidden.
        - `'enabled'`: Wait until the window is not disabled.
        - `'ready'`: Wait until the window is ready for user interaction.
        - `'active'`: Wait until the window is active.
def enter(connection: int = 0):
    """Execute SAP execute
    """
    session = SAP.get_current_connection(connection)
    windows = find_element_by_id("wnd[0]", session)
    send_keys(windows, "Enter")

    Raises:
    - AttributeError: If neither control nor window_title is specified.

    Returns:
    - bool: True if the element is visible within the specified time, False otherwise.
    """
    if control is None and window_title is None:
        raise AttributeError(
            "Debe especificar un atributo (control) o un especificar un atributo (window_title)"
        )
    if window_title is not None and found_index < 0:
        raise ValueError(
            "Cuando se utiliza 'window_title', el índice debe ser mayor o igual a 0. Intente utilizar 'control' en vez de 'window_title'."
        )
    if control is not None:
        try:
            if found_index == 0:
                window.__getattribute__(control).wait(condition, timeout=timeout)
            else:
                ctlrs = find_element_by_control_identifier(
                    window=window, control=control, control_type=control_type
                )
                window.__getattribute__(ctlrs[found_index]).wait(
                    condition, timeout=timeout
                )
            return True
        except:
            return False
    elif window_title is not None:
        try:
            if control_type is None:
                window.child_window(
                    title=window_title,
                    found_index=found_index,
                ).wait(condition, timeout=timeout)
            else:
                window.child_window(
                    title=window_title,
                    found_index=found_index,
                    control_type=control_type,
                ).wait(condition, timeout=timeout)
            return True
        except:
            return False


def get_text(
    window: object,
    control: str = None,
    found_index: int = 0,
    control_type: str = None,
    window_title: str = None,
) -> list:
    """
    Retrieves the text of a specified element within a window.

    Args:
        window (object): The window object containing the element.
        control (str, optional): The name of the control element. Defaults to None.
        found_index (int, optional): The index of the control element if there are multiple elements with the same name. Defaults to 0.
        control_type (str, optional): The type of the control element. Defaults to None.
        window_title (str, optional): The title of the window. Defaults to None.

    Returns:
        list: The text of the specified element.

    Raises:
        AttributeError: If neither control nor window_title is specified.
        ValueError: If window_title is specified but found_index is less than 0.
        AttributeError: If there is an error obtaining the element.
        AttributeError: If there is an error extracting the text of the element.
    """
    if control is None and window_title is None:
        raise AttributeError(
            "Debe especificar un atributo (control) o un especificar un atributo (window_title)"
        )
    if window_title is not None and found_index < 0:
        raise ValueError(
            "Cuando se utiliza 'window_title', el índice debe ser mayor o igual a 0. Intente utilizar 'control' en vez de 'window_title'."
        )
    try:
        if control is not None:
            if found_index == 0:
                element = window.__getattribute__(control)
            else:
                ctlrs = find_element_by_control_identifier(
                    window=window, control=control, control_type=control_type
                )
                element = window.__getattribute__(ctlrs[found_index])

        elif window_title is not None:
            if control_type is None:
                element = window.child_window(
                    title=window_title,
                    found_index=found_index,
                )
            else:
                element = window.child_window(
                    title=window_title,
                    found_index=found_index,
                    control_type=control_type,
                )

    except AttributeError:
        raise AttributeError("Error obtaining the element")

    try:
        return [desc.window_text() for desc in element.descendants()]

    except AttributeError:
        raise AttributeError("Error extracting the text of the element")
        
def save(connection: int = 0):
    """Execute SAP execute
    """
    session = SAP.get_current_connection(connection)
    windows = find_element_by_id("wnd[0]", session)
    send_keys(windows, "Ctrl+S")
