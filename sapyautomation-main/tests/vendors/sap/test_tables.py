import os
import unittest

try:
    from sapyautomation.vendors.sap.connection import SAP
    from sapyautomation.vendors.sap.login import Login
    from sapyautomation.vendors.sap.start_transaction import start_transaction
    from sapyautomation.vendors.sap.actions import find_element_by_id, press, \
        input_text, scroll_vertical
    from sapyautomation.vendors.sap.tables import get_table, set_value
    from sapyautomation.desktop.inputs.mouse import click_on_position
    from sapyautomation.desktop.inputs.keyboard import enter

except ImportError:
    pass


class TestGeneralMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.skip = os.environ.get('IGNORE_TESTS', False)
        if not cls.skip:
            cls.sap = SAP("S4 INICIATIVA")
            cls.sap.start()
            login = Login()
            login.identify_system(0)
            login.login(
                client=100,
                user=os.environ.get('S4M_USER'),
                password=os.environ.get('S4M_PASSWORD'),
                language="ES")

    def setUp(self) -> None:
        if self.skip:
            self.skipTest('Ignore tests variable enable')

    def test_get_data_from_table(self):
        from sapyautomation.desktop.inputs.keyboard import press_key
        session = SAP.get_current_connection(0)
        start_transaction(num_connection=0,
                          name_transaction="SE11",
                          keep_session="/n")

        txt_name_table = find_element_by_id("wnd[0]/usr/ctxtRSRD1-TBMA_VAL",
                                            session=session)

        button_visualize = \
            find_element_by_id("wnd[0]/usr/btnPUSHSHOW", session=session)

        input_text(txt_name_table, "MARA")
        press(button_visualize)

        button_content = \
            find_element_by_id("wnd[0]/tbar[1]/btn[46]", session=session)

        press(button_content)

        txt_value_low = find_element_by_id("wnd[0]/usr/ctxtI1-LOW",
                                           session=session)
        txt_value_high = find_element_by_id("wnd[0]/usr/ctxtI1-HIGH",
                                            session=session)

        input_text(txt_value_low, "10")
        input_text(txt_value_high, "1000000")

        textfield1 = find_element_by_id("/app/con[0]/ses[0]/wnd["
                                        "0]/usr/ctxtI3-LOW", session)

        x = textfield1.ScreenLeft + 3
        y = textfield1.ScreenTop + 3

        click_on_position(x, y)
        press_key("f4")
        table = get_table("/app/con[0]/ses[0]/wnd[1]/usr/lbl[1,1]", session)

        self.assertTrue(
            "ZHAL" in (item for sublist in table for item in sublist))
        self.assertTrue(
            "Servicios" in (item for sublist in table for item in sublist))

    def test_set_data_from(self):
        session = SAP.get_current_connection(0)
        start_transaction(num_connection=0,
                          name_transaction="VA01",
                          keep_session="/n")

        class_text = find_element_by_id(
            "/app/con[0]/ses[0]/wnd[0]/usr/ctxtVBAK-AUART",
            session=session)

        input_text(class_text, "OR1")
        enter()

        user_window = find_element_by_id("/app/con[0]/ses[0]/wnd[0]/usr",
                                         session)

        try:
            scroll_vertical(user_window, 60)
        except Exception:
            pass

        table = r"/app/con[0]/ses[0]/wnd[" \
                r"0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01" \
                r"/ssubSUBSCREEN_BODY:SAPMV45A:4400/subSUBSCREEN_TC:SAPMV45A" \
                r":4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG"

        set_value(table, 1, 0, "test1")
        cell = find_element_by_id(table + "/ctxtRV45A-MABNR[1,0]", session)

        self.assertEqual("test1", cell.text)

    @classmethod
    def tearDownClass(cls) -> None:
        if not cls.skip:
            cls.sap.close()
