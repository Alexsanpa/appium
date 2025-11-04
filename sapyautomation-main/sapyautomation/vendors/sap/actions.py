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
    element = ElementById(element_id=id_locator, session=session)

    return element.element()


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
    try:
        if not element.selected:
            element.select()

        return True
    except AttributeError:
        raise AttributeError


def close(windows: object) -> None:
    """Closes windows on SAP

    Close connection or session on SAP

    Args:
        windows (object): element what you want to close

    Raises:
        AttributeError: If you want to close some element different like
        connection or session
    """
    try:
        windows.close()
    except AttributeError:
        raise AttributeError


def send_keys(element: object, keys) -> None:
    """Sends keys in the Keyboard

    Send keys in the keyboard for do actions on screen

    Args:
        element (object): element what you want to send keys
        keys: Command or key
    """
    _element = ElementById(element.id)
    if not _element.exists():
        _element.element(5)
    _element.send_key(keys)


def scroll_vertical(element: object, index: int) -> None:
    """Does scroll vertical on screen

    Do scroll vertical on screen depends on position what you want

    Args:
        element (object): element what you want to scroll
        index (int): row index from table
    Raises:
        AttributeError: If you want to scroll some element different like
        windows
    """
    try:
        element.VerticalScrollbar.position = index
    except AttributeError:
        raise AttributeError


def scroll_horizontal(element: object, index: int) -> None:
    """Does scroll horizontal on screen

    Do scroll horizontal on screen depends column index what you want

    Args:
        element (object): element what you want to scroll
        index (int): column index from table
    Raises:
        AttributeError: If you want to scroll some element different like
        windows
    """
    try:
        element.HorizontalScrollbar.position = index
    except AttributeError:
        raise AttributeError


def input_text(element, input_texts) -> bool:
    """Inputs text on an element

    Input text on an element what you want

    Args:
        element (object): element what you want to input text
        input_texts (str): text what you want to input

    Returns:
         bool: True if successful, False otherwise

    Raises:
        AttributeError: If you want to input text on an element different like
        textField
    """
    try:
        element.text = input_texts

        value = element.text
        if value == input_texts:
            return True
    except AttributeError:
        raise AttributeError

    return False


def input_text_by_id(id_element: str, text: str, connection: int = 0) -> bool:
    """Inputs text on an element

    Input text on an element what you want

    Args:
        element (object): element what you want to input text
        input_texts (str): text what you want to input

    Returns:
         bool: True if successful, False otherwise

    Raises:
        AttributeError: If you want to input text on an element different like
        textField
    """
    session = SAP.get_current_connection(connection)
    element = ElementById(element_id=id_element, session=session)

    return element.input_text(text)


def wait_element_exists(id_locator: str, session: object,
                        max_wait: int = 4) -> object:
    """Waits until element exists

    Wait until an elements is present

    Args:
        id_locator (str): id attribute of an element
        session (object): your active session
        max_wait (int): max seconds to await the element to exist.

    Returns:
        element (object): element present on windows

    Raises:
        ModuleNotFoundError: if element is not present on windows
    """
    element = ElementById(element_id=id_locator, session=session)

    return element.element(max_wait)


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

    try:
        num_elements_list = combo.Entries.count

        elements = {}
        for x in range(num_elements_list):
            key = combo.Entries.ElementAt(x).value

            list_elements = elements.get(key, [])
            list_elements.append(combo.Entries.ElementAt(x).key)

            elements[key] = list_elements

        list_keys = elements[text]
        key = list_keys[position]
        combo.key = key
    except KeyError:
        raise KeyError
    except AttributeError:
        raise AttributeError


def click_on_tab_by_id(tab_id: str, connection: int = 0):
    """Selects a tab by id

    Click on tab by ID selector

    Args:
         tab_id (str): tab id selector
         connection (int): current connection number / session
    Raises:
        AttributeError: If an element has not attribute select or if not is
        a Tab object.
    """
    session = SAP.get_current_connection(connection)
    element = ElementById(element_id=tab_id, session=session)

    return element.select()


def execute(connection: int = 0):
    """Execute SAP execute
    """
    session = SAP.get_current_connection(connection)
    windows = find_element_by_id("wnd[0]", session)
    send_keys(windows, "F8")


def enter(connection: int = 0):
    """Execute SAP execute
    """
    session = SAP.get_current_connection(connection)
    windows = find_element_by_id("wnd[0]", session)
    send_keys(windows, "Enter")


def save(connection: int = 0):
    """Execute SAP execute
    """
    session = SAP.get_current_connection(connection)
    windows = find_element_by_id("wnd[0]", session)
    send_keys(windows, "Ctrl+S")
