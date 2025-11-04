from datetime import datetime
from datetime import timedelta

from sapyautomation.vendors.sap.elements import ElementById, Window
from sapyautomation.vendors.sap.connection import SAP


class ModalWindow(Window):

    def __init__(self, index: int = 1, connection_index: int = 0,
                 session_index: int = 0):
        super().__init__(index, connection_index=connection_index,
                         session_index=session_index)

    @property
    def elements(self):
        """ Gets modal elements list
        """
        if not hasattr(self, '_elements'):
            self._elements = self._get_elements()

        return self._elements

    def _get_elements(self):
        """Identifies if your session has a GUIModal windows

        Identify a GUIModal windows on your active session

        Args:
           session (object): your active session

        Returns:
            list_elements (dict): elements of SAP GUIModal Windows

        Raises:
            TypeError: if your session is not a type of a CDispatch object
        """
        list_elements = {}
        list_children = {}
        list_children_toolbar = {}

        if self._session.Children.Count == 2:
            modal_window = ElementById("wnd[1]", self._session,
                                       window_index=self._index).element()
            modal_content = ElementById("wnd[1]/usr", self._session,
                                        window_index=self._index).element()
            modal_toolbar = ElementById("wnd[1]/tbar[0]", self._session,
                                        window_index=self._index).element()
            _type_element = str(modal_window.type)
            elements = list_elements.get(_type_element, [])
            elements.append({
                "id": modal_window.id,
                "text": modal_window.text,
                "child_elements GuiUserArea": list_children,
                "child_elements GuiToolbar": list_children_toolbar
            })
            list_elements[_type_element] = elements

            for x in range(modal_content.Children.Count):
                _type_element = str(modal_content.Children.ElementAt(x).type)
                elements_user_area = list_children.get(_type_element, [])
                elements_user_area.append({
                    "id": modal_content.Children.ElementAt(x).id,
                    "Text": modal_content.Children.ElementAt(x).text
                })
                list_children[_type_element] = elements_user_area

            for i in range(modal_toolbar.Children.Count):
                _type_element = str(modal_toolbar.Children.ElementAt(i).type)
                elements_toolbar = list_children_toolbar.get(_type_element, [])
                elements_toolbar.append({
                    "id": modal_toolbar.Children.ElementAt(i).id,
                    "Text": modal_toolbar.Children.ElementAt(i).text
                })
                list_children_toolbar[_type_element] = elements_toolbar

        return list_elements

    def get_title(self) -> str:
        """ Gets modal title
        """
        return self.element.text

    def info(self):
        """ Returns information about GuiModal Windows

        Args:
            elements (dict): elements of SAP GUIModal Windows
           session (object): your active session
        """
        return {'title': self.get_title(), }

    def click_ok(self):
        """Simulates a click on ok button

        Simulate a click on ok button

        Args:
            elements (dict): elements of SAP GUIModal Windows
            session (object): your active session
        """
        try:
            list_buttons = self.elements["GuiModalWindow"][0][
                "child_elements GuiUserArea"]["GuiButton"]
        except KeyError:
            list_buttons = self.elements["GuiModalWindow"][0][
                "child_elements GuiToolbar"]["GuiButton"]

        if list_buttons != '':
            id_button_ok = list_buttons[0]["id"]
            button_ok = ElementById(
                id_button_ok, self._session, self._index)
            button_ok.press()

    def click_cancel(self):
        """Simulates a click on cancel button

        Simulate a click on cancel button

        Args:
            elements (dict): elements of SAP GUIModal Windows
            session (object): your active session
        """
        try:
            list_buttons = self.elements["GuiModalWindow"][0][
                "child_elements GuiUserArea"]["GuiButton"]
        except KeyError:
            list_buttons = self.elements["GuiModalWindow"][0][
                "child_elements GuiToolbar"]["GuiButton"]

        if list_buttons != '' and len(list_buttons) == 2:
            id_button_cancel = list_buttons[1]["id"]

        elif list_buttons != '' and len(list_buttons) > 2:
            id_button_cancel = list_buttons[2]["id"]

        button_cancel = ElementById(id_button_cancel, self._session,
                                    window_index=self._index)
        button_cancel.press()


def modal_info(elements: dict = None):  # pylint: disable=unused-argument
    """ Returns information about GuiModal Windows

    Args:
        elements (dict): elements of SAP GUIModal Windows
       session (object): your active session
    """
    modal_window = ModalWindow(1)

    return modal_window.info()


def identify_modal(session: object = None):  # pylint: disable=unused-argument
    """Identifies if your session has a GUIModal windows

    Identify a GUIModal windows on your active session

    Args:
       session (object): your active session

    Returns:
        list_elements (dict): elements of SAP GUIModal Windows

    Raises:
        TypeError: if your session is not a type of a CDispatch object
    """
    list_elements = ModalWindow(1).elements

    return list_elements


def actions_modal(elements: dict, session: object):
    """Realizes actions on GuiModal Windows

    Perform an action depend on type of GuiModal Windows

    Args:
        elements (dict): elements of SAP GUIModal Windows
       session (object): your active session

    Returns:
        bool: True if successful, False otherwise.
    """
    modal_window = ModalWindow(1).info()
    connections = SAP.count_connections()

    if modal_window['title'] == 'Salir del sistema':
        # TODO dictionary object for text validation # pylint: disable=fixme
        click_ok_modal(elements, session)

        connection = connections
        while connection == connections:
            connection = SAP.count_connections()

        if connections - 1 == connection:
            return True

    if modal_window['title'] == 'License Information for Multiple Logons':
        id_radiobutton_keep_sessions = elements["GuiModalWindow"][0][
            "child_elements GuiUserArea"]["GuiRadioButton"][1]["id"]
        ElementById(id_radiobutton_keep_sessions, session).select()
        click_ok_modal(elements, session)

        connection = connections
        current_time = datetime.now()
        while connection == connections:
            now = datetime.now()
            connection = SAP.count_connections()
            if now >= (current_time + timedelta(seconds=3)):
                break

        if connection >= connections:
            return True

    if modal_window['title'] == 'Información':
        click_ok_modal(elements, session)

        connection = connections
        current_time = datetime.now()
        while connection == connections:
            now = datetime.now()
            connection = SAP.count_connections()
            if now >= (current_time + timedelta(seconds=3)):
                break

        if connection >= connections:
            return True

    return False


def click_ok_modal(elements: dict,  # pylint: disable=unused-argument
                   session: object):  # pylint: disable=unused-argument
    """Simulates a click on ok button

    Simulate a click on ok button

    Args:
        elements (dict): elements of SAP GUIModal Windows
        session (object): your active session
    """
    modal_window = ModalWindow(1)
    modal_window.click_ok()


def click_cancel_modal(elements: dict,  # pylint: disable=unused-argument
                       session: object):  # pylint: disable=unused-argument
    """Simulates a click on cancel button

    Simulate a click on cancel button

    Args:
        elements (dict): elements of SAP GUIModal Windows
        session (object): your active session
    """
    modal_window = ModalWindow(1)
    modal_window.click_cancel()
