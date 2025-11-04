import os
import unittest

try:
    from sapyautomation.vendors.sap import find_modal, actions
    from sapyautomation.vendors.sap.connection import SAP
    from sapyautomation.vendors.sap.login import Login
    from sapyautomation.vendors.sap.messages import identify_message
    from sapyautomation.vendors.sap.start_transaction import start_transaction
    from sapyautomation.core.com import ComObject
except ImportError:
    pass


class TestModal(unittest.TestCase):
    def setUp(self) -> None:
        skip = os.environ.get('IGNORE_TESTS', False)
        if skip:
            self.skipTest('Ignore tests variable enable')

        sap = SAP("S4 INICIATIVA")
        sap.start()

    def test_identify_modal(self):
        session = SAP.get_current_connection(0)
        login = Login()
        login.identify_system(0)
        login.login(client=100, user="BI-user01",
                    password="Welcome1", language="ES")

        session.findById("wnd[0]/tbar[0]/btn[15]").press()
        list_elements = find_modal.identify_modal(session=session)
        self.assertNotEqual('', list_elements)

    def test_identify_modal_fail(self):
        session = SAP.get_current_connection(0)
        login = Login()
        login.identify_system(0)
        login.login(client=100, user="BI-user01",
                    password="Welcome1", language="ES")
        session.findById("wnd[0]/tbar[0]/btn[15]").press()
        self.assertRaises(TypeError, find_modal.identify_modal,
                          session='hi')

    def test_actions_modal_exit_SAP(self):
        session = SAP.get_current_connection(0)
        login = Login()
        login.identify_system(0)
        login.login(client=100, user="BI-user01",
                    password="Welcome1", language="ES")

        session.findById("wnd[0]/tbar[0]/btn[15]").press()
        json_object = find_modal.identify_modal(session)
        self.assertEqual(find_modal.actions_modal(json_object, session), True)

    def test_actions_modal_user(self):
        SAP.close()
        sap = SAP("AMCO DEV")
        sap.start()
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

        json_object = find_modal.identify_modal(new_session)
        self.assertEqual(find_modal.actions_modal(elements=json_object,
                                                  session=new_session),
                         True)

    def test_actions_modal_pwd_incorrect(self):
        login = Login()
        login.identify_system(0)
        self.assertRaises(ConnectionError, login.login, client=100,
                          user="BI-user01",
                          password="Deloitte", language="ES")

        sap = SAP("S4 INICIATIVA")
        sap.start()
        new_session = SAP.get_current_connection(1)
        new_session.findById("wnd[0]").maximize()
        new_session.findById("wnd[0]/usr/txtRSYST-MANDT").text = 100
        new_session.findById("wnd[0]/usr/txtRSYST-BNAME").text = "BI-user01"
        new_session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = "Welcome1"
        new_session.findById("wnd[0]/usr/txtRSYST-LANGU").text = "ES"

        new_session.findById("wnd[0]").sendVKey(0)

        json_object = find_modal.identify_modal(new_session)
        self.assertEqual(find_modal.actions_modal(elements=json_object,
                                                  session=new_session),
                         True)

    def test_click_button_ok_userArea(self):
        sap_gui = ComObject("SAPGUI").get().GetScriptingEngine
        session = SAP.get_current_connection(0)
        login = Login()
        login.identify_system(0)
        login.login(client=100, user="BI-user01",
                    password="Welcome1", language="ES")
        connections = sap_gui.Connections.Count

        session.findById("wnd[0]/tbar[0]/btn[15]").press()
        list_elements = find_modal.identify_modal(session=session)

        find_modal.click_ok_modal(list_elements, session)

        connection = connections
        while connection == connections:
            connection = sap_gui.Connections.Count

        self.assertEqual(connections - 1 == connection, True)

    def test_click_button_ok_toolbar(self):
        SAP.close()
        sap = SAP("AMCO DEV")
        sap.start()
        login = Login()
        login.identify_system(0)
        self.assertRaises(ConnectionError, login.login, client=110,
                          user=os.environ.get('SDC_USER'),
                          password="Deloitte", language="ES")

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

        find_modal.click_ok_modal(list_elements, new_session)

        title = actions.find_element_by_id("wnd[0]/titl", new_session).text
        self.assertEqual(title, "SAP Easy Access")

    def test_click_button_cancel_userArea(self):
        session = SAP.get_current_connection(0)
        login = Login()
        login.identify_system(0)
        login.login(client=100, user="BI-user01",
                    password="Welcome1", language="ES")

        session.findById("wnd[0]/tbar[0]/btn[15]").press()
        list_elements = find_modal.identify_modal(session=session)

        find_modal.click_cancel_modal(list_elements, session)

        title = actions.find_element_by_id("wnd[0]/titl", session).text
        self.assertEqual(title, "SAP Easy Access")

    def test_click_button_cancel_toolbar(self):
        SAP.close()
        sap = SAP("AMCO DEV")
        sap.start()
        sap_gui = ComObject("SAPGUI").get().GetScriptingEngine
        login = Login()
        login.identify_system(0)
        login.login(110, os.environ.get('SDC_USER'), os.environ
                    .get('SDC_PASSWORD'), "ES")

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

        connections = sap_gui.Connections.Count

        list_elements = find_modal.identify_modal(new_session)

        find_modal.click_cancel_modal(list_elements, new_session)

        connection = connections
        while connection == connections:
            connection = sap_gui.Connections.Count

        self.assertEqual(connection == 1, True)

    def test_click_button_ok_3_buttons(self):
        session = SAP.get_current_connection(0)
        login = Login()
        login.identify_system(0)
        login.login(client=100, user="BI-user01",
                    password="Welcome1", language="ES")

        start_transaction(0, "ME21N", "/n")
        txt_org_pur = actions.find_element_by_name("MEPO1222-EKORG",
                                                   session, "GuiCTextField")
        actions.input_text(txt_org_pur, "2000")

        txt_grp_pur = actions.find_element_by_name("MEPO1222-EKGRP",
                                                   session, "GuiCTextField")
        actions.input_text(txt_grp_pur, "120")

        windows = actions.find_element_by_id("wnd[0]", session)
        actions.send_keys(windows, "Enter")

        button_save = actions.find_element_by_name("btn[11]",
                                                   session,
                                                   "GuiButton")
        actions.press(button_save)

        list_elements = find_modal.identify_modal(session)
        find_modal.click_ok_modal(list_elements, session)
        elements = identify_message(session)
        text_message = elements["Message"][0]["text"]

        self.assertEqual(text_message != '', True)

    def test_click_button_cancel_3_buttons(self):
        session = SAP.get_current_connection(0)
        login = Login()
        login.identify_system(0)
        login.login(client=100, user="BI-user01",
                    password="Welcome1", language="ES")

        start_transaction(0, "ME21N", "/n")
        txt_org_pur = actions.find_element_by_name("MEPO1222-EKORG",
                                                   session, "GuiCTextField")
        actions.input_text(txt_org_pur, "2000")

        txt_grp_pur = actions.find_element_by_name("MEPO1222-EKGRP",
                                                   session, "GuiCTextField")
        actions.input_text(txt_grp_pur, "120")

        windows = actions.find_element_by_id("wnd[0]", session)
        actions.send_keys(windows, "Enter")

        button_save = actions.find_element_by_name("btn[11]",
                                                   session,
                                                   "GuiButton")
        actions.press(button_save)

        list_elements = find_modal.identify_modal(session)
        find_modal.click_cancel_modal(list_elements, session)

        title = actions.find_element_by_id("wnd[0]/titl", session)
        self.assertEqual(title.text, "Crear pedido")

    def tearDown(self) -> None:
        sap = SAP("AMCO DEV")
        sap.close()
