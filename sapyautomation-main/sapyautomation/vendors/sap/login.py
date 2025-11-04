from win32com.universal import com_error  # pylint: disable=import-error

from sapyautomation.core.utils.exceptions import SapError, SapSessionNotFound
from sapyautomation.vendors.sap.find_modal import ModalWindow
from sapyautomation.vendors.sap.elements import Window
from sapyautomation.vendors.sap.connection import SAP


class Login:
    """ Login object to manage login actions
    """
    def __init__(self):
        self._wnd = Window(0)

    def logout(self):
        """ Logs out the user session
        Goes back through screens until it can logout

        Raises:
            SapNotSavedChanges: When there is changes that requires saving
        """
        self._wnd.element.close()

        for _ in range(10):
            try:
                self.identify_modal()
            except (SapSessionNotFound, com_error, AttributeError):
                break

    @staticmethod
    def identify_modal():
        modal_window = ModalWindow(1)
        _modals = ('Exit Editing', 'Log Off', 'Copyright')

        if modal_window.exists():
            modal_title = modal_window.get_title()
            if any(res in modal_window.get_title() for res in _modals):
                modal_window.click_ok()

            elif 'License Information for Multiple Logons' in modal_title:
                id_radiobutton_keep_sessions = modal_window.elements[
                    "GuiModalWindow"][0]["child_elements GuiUserArea"][
                        "GuiRadioButton"][1]["id"]
                modal_window.child(id_radiobutton_keep_sessions).select()
                modal_window.click_ok()

            else:
                modal_window.send_key(0)

            return True

        return False

    @staticmethod
    def identify_system() -> str:
        """
        Identify name system and return it.

        Keyword arguments:
        num_connection -- number connection what you want to access
        """
        info = SAP.get_sap_information()
        return info.system_name

    def accept_on_login_modals(self):
        """ Loops until there is no more message modals

        Accepts any message modals that appears on login.
        """
        for _ in range(10):
            if self.identify_modal():
                continue

            break

    def login(self, client: int, user: str, password: str, language: str) -> \
            str:
        """
        Allow to log in to system

        Keyword arguments:
        client   -- client what you want to access
        user     -- user name to access to system
        password -- password to access to system
        language -- language to system
         """
        try:
            self._wnd.maximize()
            self._wnd.child("txtRSYST-MANDT").input_text(client)
            self._wnd.child("txtRSYST-BNAME").input_text(user)
            self._wnd.child("pwdRSYST-BCODE").input_text(password)
            self._wnd.child("txtRSYST-LANGU").input_text(language)
            self._wnd.send_key(0)
            # TODO: validate no error messages pylint: disable=fixme
            self.accept_on_login_modals()

            # TODO: window menu listing pylint: disable=fixme
            self._wnd.child("tbar[1]/btn[34]").set_focus()

            return self._wnd.get_title()

        except com_error as e:
            msg = self._wnd.get_message()['text']
            if msg is not None:
                raise SapError(msg)

            if e.excepinfo[2] == "The control could not be found by id.":
                raise SapSessionNotFound("Session has already started")
