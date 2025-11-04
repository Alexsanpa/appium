from time import sleep

try:
    from win32com.universal import com_error
except ImportError:
    pass

from sapyautomation.vendors.sap.connection import SAP
from sapyautomation.vendors.sap.models import (GUI_VIRTUAL_KEYS,
                                               GUI_ELEMENT_TYPES)


class _Element:
    """ Base element object

    Args:
        element_id(str): id of the wanted element
        element_name(str): name of the wanted element
        element_label(str): label of the wanted element
        session(object): SAP session object
        type_element(str): type of the element searched by name or label.
        window_index(int): index of window where element will be searched
    """
    def __init__(self, element_id: str = None, element_name: str = None,
                 element_label: str = None, session: object = None,
                 type_element: str = None, window_index: int = None,
                 connection_index: int = 0, session_index: int = 0):
        self.__connection_index = connection_index
        self.__session_index = session_index
        self.__session = session

        self.__element_id(element_id, window_index)
        self._element_name = element_name
        self._element_label = element_label
        self._type_element = type_element

        self._element = self._find_element()

    @property
    def _session(self):
        if self.__session is None:
            self.__session = SAP.get_current_connection(
                self.__connection_index, self.__session_index)

        return self.__session

    def __element_id(self, element_id: str, window_index: int):
        """ Gets windows id with window index

        Args:
            window_index(int): index id of the wanted window.

        """
        if element_id is not None:
            if 'wnd[' in element_id:
                _element_id = element_id.split('wnd[')[1][2:]

                if window_index is not None:
                    self._element_id = f"wnd[{window_index}]{_element_id}"
                else:
                    self._element_id = element_id

        else:
            self._element_id = None

    def _find_element(self, element_id: str = None):
        """ Find element depending on data received

        Args:
            element_id(str): element id to be searched internally

        """
        element = None
        element_id = self._element_id if element_id is None else element_id
        try:
            if self._element_id is not None:
                element = self._session.findById(element_id)
            elif self._element_name is not None:
                element = self._session.activewindow.FindByName(
                    self._element_name, self._type_element)
            elif self._element_label is not None:
                element = self._session.activewindow.FindByLabel(
                    self._element_label, self._type_element)

        except com_error:
            try:
                if self._element_name is not None:
                    element = self._session.activewindow.FindByName(
                        self._element_name, self._type_element)
                elif self._element_id is not None:
                    element = self._session.findById(element_id)
                elif self._element_label is not None:
                    element = self._session.activewindow.FindByLabel(
                        self._element_label, self._type_element)

            except com_error:
                pass

        return element

    def exists(self):
        """ Verifies if the element exists

        Returns:
            True or False if the element exists
        """
        return self._element is not None

    def element(self, max_wait: int = 1) -> object:
        """ Retrieves the element object

        Args:
            max_wait (int): max seconds to await for the element

        Returns:
            element (object): element present on windows

        Raises:
            ModuleNotFoundError: if element is not present on windows
        """
        if not self.exists():
            for _ in range(max_wait):
                self._element = self._find_element()

                if self.exists():
                    return self._element

                sleep(1)

            raise ModuleNotFoundError("The element has not been found")

        return self._element

    def press(self):
        """ Do press action on the elemnt
        Simulate a click event on button, icon

        Raises:
            AttributeError: If you want to press some element different like
            button or icon
        """
        try:
            self.element().press()
        except AttributeError:
            raise AttributeError("The element cannot be pressed, "
                                 "verify the object type.")

    def send_key(self, key):
        """Sends keys in the Keyboard

        Send keys in the keyboard for do actions on screen

        Args:
            element (object): element what you want to send keys
            keys: Command or key

        Raises:
              ValueError: If you send a keys incorrect or not enabled
               KeyError: If you send a command incorrect or not enabled
        """
        try:
            if not isinstance(key, int):
                key = GUI_VIRTUAL_KEYS[key]

            self.element().sendVKey(key)

        except com_error:
            raise ValueError("The virtual key is not enabled")

        except KeyError:
            raise KeyError("Command has not been enabled")

    def set_focus(self):
        """ Sets gui focus on element
        """
        try:
            self.element().setFocus()
        except AttributeError:
            raise AttributeError("The element cannot be on focus, "
                                 "verify the object type.")

    def select(self):
        """ Do select action on element
        Select an option of menu or radiobutton

        Return:
            bool: True if successful, False otherwise

        Raises:
            AttributeError: If you want to select some element different like
            menu or radiobutton
        """
        try:
            self.element().select()
        except AttributeError:
            raise AttributeError("The element cannot be selected, "
                                 "verify the object type.")

    def select_combo_value(self, text: str, position: int = 0):
        """ selects a value from combo element
        Select a specific value from a drop down list

        Args:
             text (str): specific value from drop down list what you want to
                 select
             position (int): position of specific value from drop down list

        Raises:
            KeyError: If your specific value is not into drop down list
            AttributeError: If you want to select a specific value on an
                element
            different like Combobox
        """
        try:
            num_elements_list = self.element().Entries.count

            elements = {}
            for x in range(num_elements_list):
                key = self.element().Entries.ElementAt(x).value

                list_elements = elements.get(key, [])
                list_elements.append(self.element().Entries.ElementAt(x).key)

                elements[key] = list_elements

            list_keys = elements[text]
            key = list_keys[position]
            self.element().key = key

        except KeyError:
            raise KeyError("The searched value doesn't exists.")

        except AttributeError:
            raise AttributeError("The element doesn't have values to "
                                 "be selected, verify the object type.")

    def input_text(self, text: str):
        """ Adds text to input element
        Input text on an element what you want

        Args:
            texts (str): text what you want to input

        Returns:
             bool: True if successful, False otherwise

        Raises:
            AttributeError: If you want to input text on an element different
                like textField
        """
        try:
            self.element().text = text

            value = self.element().text
            if value == text:
                return True

        except AttributeError:
            raise AttributeError("The element doesn't have text "
                                 "attribute, verify the object type.")

        return False

    def scroll_vertical(self, index: int):
        """ Do vertical scroll on element
        Do scroll vertical on screen depends on position what you want

        Args:
            index (int): row index from table

        Raises:
            AttributeError: If you want to scroll some element different like
            windows
        """
        try:
            self.element().VerticalScrollbar.position = index

        except AttributeError:
            raise AttributeError("The element doesn't have vertical scroll")

    def scroll_horizontal(self, index: int):
        """ Do horizontal scroll on element
        Do scroll horizontal on screen depends column index what you want

        Args:
            index (int): column index from table

        Raises:
            AttributeError: If you want to scroll some element different like
            windows
        """
        try:
            self.element().HorizontalScrollbar.position = index

        except AttributeError:
            raise AttributeError("The element doesn't have horizontal scroll")

    def child(self, element_name: str):
        """ Searchs for child element

        Args:
            element_name(str): fragment id of the wanted child

        Returns:
            Framework's element object if exists.
        """
        element_id = None

        for x in range(self.element().Children.Count):
            _id = self.element().Children.ElementAt(x).id
            if element_name not in _id:
                section = self._find_element(_id)
                for i in range(section.Children.Count):
                    _id = section.Children.ElementAt(i).id
                    if element_name in _id:
                        break

            if element_name in _id:
                element_id = _id
                break

        return ElementById(element_id, self._session)


class ElementById(_Element):
    """ Manages element identifing it by id

    Args:
        element_id(str): id of the wanted element
        session(object): SAP session object
        window_index(int): index of window where element will be searched

    """
    def __init__(self, element_id: str, session: object = None,
                 window_index: int = None, type_element: str = None,
                 connection_index: int = 0, session_index: int = 0):
        element_name, type_element = self.get_element_data_from_id(
            element_id, type_element)

        super().__init__(element_id=element_id,
                         element_name=element_name,
                         type_element=type_element,
                         session=session,
                         window_index=window_index,
                         connection_index=connection_index,
                         session_index=session_index)

    @staticmethod
    def get_element_data_from_id(element_id: str,
                                 type_element: str = None):

        element_name = element_id
        _type_element = None

        if element_id is not None and '/' in element_id:
            data = element_id.split('/')[-1]

            if len(data) < 5:
                element_name = data

            elif data[3].islower():
                element_name = data[4:]
                _type_element = data[:4]

            elif data[2].islower():
                element_name = data[3:]
                _type_element = data[:3]

        if type_element is None and _type_element in GUI_ELEMENT_TYPES.keys():
            type_element = GUI_ELEMENT_TYPES[_type_element]

        return element_name, type_element


class ElementByName(_Element):
    """ Manages element identifing it by name

    Args:
        element_name(str): name of the wanted element
        session(object): SAP session object
        type_element(str): type of the element searched by name or label.

    """
    def __init__(self, element_name: str, session: object, type_element: str,
                 window_index: int = None, connection_index: int = 0,
                 session_index: int = 0):
        super().__init__(element_name=element_name,
                         session=session,
                         type_element=type_element,
                         window_index=window_index,
                         connection_index=connection_index,
                         session_index=session_index)


class ElementByLabel(_Element):
    """ Manages element identifing it by label

    Args:
        element_label(str): label of the wanted element
        session(object): SAP session object
        type_element(str): type of the element searched by name or label.

    """
    def __init__(self, element_label: str, session: object, type_element: str,
                 window_index: int = None, connection_index: int = 0,
                 session_index: int = 0):
        super().__init__(element_label=element_label,
                         session=session,
                         type_element=type_element,
                         window_index=window_index,
                         connection_index=connection_index,
                         session_index=session_index)


class Window:
    """ Window object to manages actions
    """

    def __init__(self, index: int = 0, connection_index: int = 0,
                 session_index: int = 0):
        self._index = index
        self._session_index = session_index
        self._window = ElementById("wnd[0]",
                                   None,
                                   window_index=index,
                                   connection_index=connection_index,
                                   session_index=session_index)

    @property
    def _session(self):
        return self._window._session

    @property
    def element(self):
        """ Retrieves Sap element object
        """
        return self._window.element()

    def exists(self):
        """ Verifies if window exists
        """
        return self._window.exists()

    def maximize(self):
        """ Do maximize action on window
        """
        return self.element.maximize()

    def close(self):
        """ Simulate pressing close button on window
        """
        self._window.element().close()

    def send_key(self, key):
        """Sends keys in the Keyboard

        Send keys in the keyboard for do actions on screen

        Args:
            element (object): element what you want to send keys
            keys: Command or key
        """
        self._window.send_key(key)

    def child(self, element_name: str):
        """ Searchs for child element

        Args:
            element_name(str): fragment id of the wanted child
        """
        return self._window.child(element_name)

    def get_title(self) -> str:
        """ Gets window title

        Returns:
            Window's title
        """
        title_element = self.child("titl")

        return title_element.element().text

    def get_message_from_panel(self) -> str:
        """ Gets message form window panel

        Returns:
            Message from Window's bottom bar
        """
        panel = self.child("sbar/pane[0]")

        return panel.element(5).text

    def get_message(self) -> str:
        """ Gets message from window with message type

        Returns:
            Message and message type from Window's panel
        """
        panel = self.child("sbar").element(5)
        types = {"E": "Error",
                 "W": "Warning",
                 "S": "Success",
                 "A": "Abort",
                 "I": "Information"}

        return {'type': types[panel.element().MessageType],
                'text': panel.text}
