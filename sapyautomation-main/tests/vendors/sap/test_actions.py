import os
import unittest
from time import sleep

try:
    from sapyautomation.core.com import ComObject
    from sapyautomation.vendors.sap import actions, find_modal, \
        start_transaction
    from sapyautomation.vendors.sap.connection import SAP
    from sapyautomation.vendors.sap.login import Login
except ImportError:
    pass


class TestActions(unittest.TestCase):
    def setUp(self) -> None:
        skip = os.environ.get('IGNORE_TESTS', False)
        if skip:
            self.skipTest('Ignore tests variable enable')

        sap = SAP("AMCO DEV")
        sap.start()

    def test_find_element_by_id(self):
        session = SAP.get_current_connection(0)
        element = actions.find_element_by_id(id_locator="wnd[0]/mbar/menu[0]",
                                             session=session)
        self.assertEqual(element != '', True)

    def test_find_element_by_id_fail(self):
        session = SAP.get_current_connection(0)
        self.assertRaises(ModuleNotFoundError, actions.find_element_by_id,
                          id_locator="wnd[1]", session=session)

    def test_find_element_by_name(self):
        session = SAP.get_current_connection(0)
        element = actions.find_element_by_name("tbar[1]", session=session,
                                               type_element="GuiToolbar")
        self.assertEqual(element != '', True)

    def test_find_element_by_name_fail(self):
        session = SAP.get_current_connection(0)
        self.assertRaises(ModuleNotFoundError, actions.find_element_by_name,
                          "RSYST-MANDT", session=session,
                          type_element="GuiMenu")

    def test_find_element_by_text(self):
        session = SAP.get_current_connection(0)
        element = actions.find_element_by_name("RSYST-MANDT", session=session,
                                               type_element="GuiLabel")
        self.assertEqual(element != '', True)

    def test_send_keys_number(self):
        session = SAP.get_current_connection(0)
        session.findById("wnd[0]").maximize()
        session.findById("wnd[0]/usr/txtRSYST-MANDT").text = 110
        session.findById("wnd[0]/usr/txtRSYST-BNAME").text = os.environ \
            .get('SDC_USER')
        session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = os.environ \
            .get('SDC_PASSWORD')
        session.findById("wnd[0]/usr/txtRSYST-LANGU").text = "ES"
        element = actions.find_element_by_id(id_locator="wnd[0]",
                                             session=session)
        actions.send_keys(element=element, keys=0)

        list_elements = find_modal.identify_modal(session)
        if len(list_elements) != 0:
            find_modal.actions_modal(list_elements, session)

        title_element = actions.find_element_by_id(id_locator="wnd[0]/titl",
                                                   session=session)

        self.assertEqual(title_element.text == "SAP Easy Access", True)

    def test_sends_keys_number_fail(self):
        session = SAP.get_current_connection(0)
        session.findById("wnd[0]").maximize()
        session.findById("wnd[0]/usr/txtRSYST-MANDT").text = 110
        session.findById("wnd[0]/usr/txtRSYST-BNAME").text = os.environ \
            .get('SDC_USER')
        session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = os.environ \
            .get('SDC_PASSWORD')
        session.findById("wnd[0]/usr/txtRSYST-LANGU").text = "ES"
        element = actions.find_element_by_id(id_locator="wnd[0]",
                                             session=session)
        self.assertRaises(ValueError, actions.send_keys, element=element,
                          keys=100)

    def test_send_keys_command(self):
        session = SAP.get_current_connection(0)
        session.findById("wnd[0]").maximize()
        session.findById("wnd[0]/usr/txtRSYST-MANDT").text = 110
        session.findById("wnd[0]/usr/txtRSYST-BNAME").text = os.environ \
            .get('SDC_USER')
        session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = os.environ \
            .get('SDC_PASSWORD')
        session.findById("wnd[0]/usr/txtRSYST-LANGU").text = "ES"
        element = actions.find_element_by_id(id_locator="wnd[0]",
                                             session=session)
        actions.send_keys(element=element, keys="Enter")

        list_elements = find_modal.identify_modal(session)
        if len(list_elements) != 0:
            find_modal.actions_modal(list_elements, session)

        title_element = actions.find_element_by_id(id_locator="wnd[0]/titl",
                                                   session=session)

        self.assertEqual(title_element.text == "SAP Easy Access", True)

    def test_send_keys_command_fail(self):
        session = SAP.get_current_connection(0)
        session.findById("wnd[0]").maximize()
        session.findById("wnd[0]/usr/txtRSYST-MANDT").text = 110
        session.findById("wnd[0]/usr/txtRSYST-BNAME").text = os.environ \
            .get('SDC_USER')
        session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = os.environ \
            .get('SDC_PASSWORD')
        session.findById("wnd[0]/usr/txtRSYST-LANGU").text = "ES"
        element = actions.find_element_by_id(id_locator="wnd[0]",
                                             session=session)
        self.assertRaises(KeyError, actions.send_keys, element=element,
                          keys="Tab")

    def test_event_press(self):
        session = SAP.get_current_connection(0)
        login = Login()
        login.identify_system(0)
        login.login(client=110, user=os.environ.get('SDC_USER'),
                    password=os.environ.get('SDC_PASSWORD'), language="ES")
        element = actions.find_element_by_id(id_locator="wnd[0]/tbar[0]/btn["
                                                        "15]",
                                             session=session)
        actions.press(element=element)
        list_elements = find_modal.identify_modal(session=session)
        self.assertEqual(list_elements != '', True)

    def test_event_press_fail(self):
        session = SAP.get_current_connection(0)
        session.findById("wnd[0]").maximize()
        element = actions.find_element_by_id(id_locator="wnd[0]/usr/txtRSYST"
                                                        "-MANDT",
                                             session=session)
        self.assertRaises(AttributeError, actions.press, element=element)

    def test_event_select(self):
        login = Login()
        login.identify_system(0)
        login.login(client=110, user=os.environ.get('SDC_USER'),
                    password=os.environ.get('SDC_PASSWORD'), language="ES")

        sap = SAP("AMCO DEV")
        sap.start()
        new_session = SAP.get_current_connection(1)

        new_session.findById("wnd[0]").maximize()
        new_session.findById("wnd[0]/usr/txtRSYST-MANDT").text = 110
        new_session.findById("wnd[0]/usr/txtRSYST-BNAME").text = os.environ \
            .get('SDC_USER')
        new_session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = os.environ \
            .get('SDC_PASSWORD')
        new_session.findById("wnd[0]/usr/txtRSYST-LANGU").text = "ES"

        new_session.findById("wnd[0]").sendVKey(0)

        list_elements = find_modal.identify_modal(new_session)
        id_radiobutton_keep_sessions = list_elements["GuiModalWindow"][0][
            "child_elements GuiUserArea"]["GuiRadioButton"][1]["id"]
        element = actions.find_element_by_id(
            id_locator=id_radiobutton_keep_sessions,
            session=new_session)
        self.assertEqual(actions.select(element), True)

    def test_event_select_fail(self):
        session = SAP.get_current_connection(0)
        session.findById("wnd[0]").maximize()
        element = actions.find_element_by_id(id_locator="wnd[0]/usr/txtRSYST"
                                                        "-MANDT",
                                             session=session)
        self.assertRaises(AttributeError, actions.select, element=element)

    def test_event_close(self):
        sap_gui = ComObject("SAPGUI").get().GetScriptingEngine
        connection = sap_gui.Connections.Count
        session = SAP.get_current_connection(0)
        windows = actions.find_element_by_id(id_locator="wnd[0]",
                                             session=session)
        actions.close(windows=windows)
        new_connections = ''
        for _ in range(4):
            new_connections = sap_gui.Connections.Count
            if new_connections != connection:
                break
            sleep(1)

        self.assertEqual(new_connections == 0, True)

    def test_event_close_fail(self):
        session = SAP.get_current_connection(0)
        windows = actions.find_element_by_id(
            id_locator="wnd[0]/usr/txtRSYST-MANDT",
            session=session)
        self.assertRaises(AttributeError, actions.close, windows=windows)

    def test_input_text(self):
        session = SAP.get_current_connection(0)
        element = actions.find_element_by_id(id_locator="wnd[0]/usr/txtRSYST"
                                                        "-MANDT",
                                             session=session)

        self.assertEqual(actions.input_text(element=element,
                                            input_texts="110"), True)

    def test_input_text_fail(self):
        session = SAP.get_current_connection(0)
        element = actions.find_element_by_id(id_locator="wnd[0]/usr/lblRSYST"
                                                        "-MANDT",
                                             session=session)

        self.assertRaises(AttributeError, actions.input_text, element=element,
                          input_texts="110")

    def test_scroll(self):
        session = SAP.get_current_connection(0)
        login = Login()
        login.identify_system(0)
        login.login(client=110, user=os.environ.get('SDC_USER'),
                    password=os.environ.get('SDC_PASSWORD'), language="ES")
        start_transaction.start_transaction(num_connection=0,
                                            name_transaction="SE11",
                                            keep_session="/n")

        # elements
        txt_name_table = actions \
            .find_element_by_id("wnd[0]/usr/ctxtRSRD1-TBMA_VAL",
                                session=session)

        button_visualize = actions \
            .find_element_by_id("wnd[0]/usr/btnPUSHSHOW", session=session)

        # methods
        actions.input_text(txt_name_table, "MARA")
        actions.press(button_visualize)

        # elements
        button_content = actions \
            .find_element_by_id("wnd[0]/tbar[1]/btn[46]", session=session)

        # methods
        actions.press(button_content)

        # elements
        txt_value_low = actions.find_element_by_id("wnd[0]/usr/ctxtI1-LOW",
                                                   session=session)

        txt_value_high = actions.find_element_by_id("wnd[0]/usr/ctxtI1-HIGH",
                                                    session=session)
        button_execute = actions.find_element_by_id("wnd[0]/tbar[1]/btn[8]",
                                                    session=session)

        # methods
        actions.input_text(txt_value_low, "10")
        actions.input_text(txt_value_high, "1000000")
        actions.press(button_execute)

        # elements
        first_value_table = actions \
            .find_element_by_id("wnd[0]/usr/sub/1[0,0]/sub/1/3[0,"
                                "2]/sub/1/3/4[0,5]/lbl[9,5]", session=session)

        # methods
        text_firs_value = first_value_table.text

        # elements
        windows = actions.find_element_by_id("wnd[0]/usr", session=session)

        # methods
        actions.scroll_vertical(windows, 50)

        # elements
        first_value_table = actions \
            .find_element_by_id("wnd[0]/usr/sub/1[0,0]/sub/1/3[0,"
                                "2]/sub/1/3/4[0,5]/lbl[9,5]", session=session)

        # methods
        new_text_first_value = first_value_table.text

        # validate
        self.assertEqual(text_firs_value != new_text_first_value, True)

    def test_scroll_vertical_fail(self):
        session = SAP.get_current_connection(0)
        element = actions.find_element_by_id(id_locator="wnd[0]/usr/lblRSYST"
                                                        "-MANDT",
                                             session=session)
        self.assertRaises(AttributeError, actions.scroll_vertical,
                          element=element, pix=30)

    def test_wait_implicit(self):
        session = SAP.get_current_connection(0)
        login = Login()
        login.identify_system(0)
        login.login(client=110, user=os.environ.get('SDC_USER'),
                    password=os.environ.get('SDC_PASSWORD'), language="ES")
        actions.wait_element_exists(id_locator="wnd[0]/tbar[0]/okcd",
                                    session=session)

    def test_wait_implicit_fail(self):
        session = SAP.get_current_connection(0)
        login = Login()
        login.identify_system(0)
        login.login(client=110, user=os.environ.get('SDC_USER'),
                    password=os.environ.get('SDC_PASSWORD'), language="ES")
        self.assertRaises(ModuleNotFoundError, actions.wait_element_exists,
                          id_locator="wnd[0]/usr/txtRSYST-MANDT",
                          session=session)

    def test_select_value_combo(self):
        SAP.close()
        sap = SAP("S4 INICIATIVA")
        sap.start()
        session = SAP.get_current_connection(0)
        login = Login()
        login.identify_system(0)
        login.login(client=100, user=os.environ.get('S4M_USER'),
                    password=os.environ.get('S4M_PASSWORD'), language="ES")

        start_transaction.start_transaction(0, "ME21N", "/n")
        cmb_box = actions.find_element_by_name("MEPO_TOPLINE-BSART",
                                               session, "GuiComboBox")

        actions.select_value_combo(cmb_box, "Pedido estándar MEX")

        cmb_box = actions.find_element_by_name("MEPO_TOPLINE-BSART",
                                               session, "GuiComboBox")
        self.assertEqual(cmb_box.text.strip() == "Pedido estándar MEX",
                         True)

    def test_select_value_combo_fail(self):
        SAP.close()
        sap = SAP("S4 INICIATIVA")
        sap.start()
        session = SAP.get_current_connection(0)
        login = Login()
        login.identify_system(0)
        login.login(client=100, user=os.environ.get('S4M_USER'),
                    password=os.environ.get('S4M_PASSWORD'), language="ES")

        start_transaction.start_transaction(0, "ME21N", "/n")
        cmb_box = actions.find_element_by_name("MEPO_TOPLINE-BSART",
                                               session, "GuiComboBox")

        self.assertRaises(KeyError, actions.select_value_combo, cmb_box,
                          "Pedido", 2)

    def test_select_value_combo_fail_AttributeError(self):
        SAP.close()
        sap = SAP("S4 INICIATIVA")
        sap.start()
        session = SAP.get_current_connection(0)
        login = Login()
        login.identify_system(0)
        login.login(client=100, user=os.environ.get('S4M_USER'),
                    password=os.environ.get('S4M_PASSWORD'), language="ES")

        start_transaction.start_transaction(0, "ME21N", "/n")
        txt_org_pur = actions.find_element_by_name("MEPO1222-EKORG",
                                                   session,
                                                   "GuiCTextField")
        self.assertRaises(AttributeError, actions.select_value_combo,
                          txt_org_pur, "Pedido estándar", 2)

    def tearDown(self) -> None:
        sap = SAP("AMCO DEV")
        sap.close()
