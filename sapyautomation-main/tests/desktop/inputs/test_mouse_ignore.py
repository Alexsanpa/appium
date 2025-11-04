import os
import unittest


class TestMouseCases(unittest.TestCase):

    def setUp(self):
        skip = os.environ.get('IGNORE_TESTS', False)
        if skip:
            self.skipTest('Ignore tests variable enable')
        self.x = 660
        self.y = 533

    def test_get_mouse_coordinates(self):
        from sapyautomation.desktop.inputs.mouse import get_mouse_coordinates
        import pyautogui
        pyautogui.moveTo(self.x, self.y)
        new_x, new_y = get_mouse_coordinates()

        self.assertEqual(new_x, self.x, "X is not on coordinate")
        self.assertEqual(new_y, self.y, "X is not on coordinate")

    def test_click_position(self):
        from sapyautomation.desktop.inputs.mouse import \
            get_mouse_coordinates, click_on_position
        click_on_position(self.x, self.y)

        click_x, click_y = get_mouse_coordinates()
        self.assertEqual(click_x, self.x, "No valid click on position")
        self.assertEqual(click_y, self.y, "No valid click on position")

    def test_double_click_position(self):
        from sapyautomation.desktop.inputs.mouse import \
            get_mouse_coordinates, double_click_on_position
        double_click_on_position(self.x, self.y)

        click_x, click_y = get_mouse_coordinates()
        self.assertEqual(click_x, self.x, "No valid double click on position")
        self.assertEqual(click_y, self.y, "No valid double click on position")

    def test_right_click_position(self):
        from sapyautomation.desktop.inputs.mouse import \
            get_mouse_coordinates, right_click_on_position
        right_click_on_position(self.x, self.y)

        click_x, click_y = get_mouse_coordinates()
        self.assertEqual(click_x, self.x, "No valid right click on position")
        self.assertEqual(click_y, self.y, "No valid right click on position")

    def test_move_to_position(self):
        from sapyautomation.desktop.inputs.mouse import \
            get_mouse_coordinates, move_to_position
        move_to_position(self.x, self.y)
        new_x, new_y = get_mouse_coordinates()

        self.assertEqual(self.x, new_x, "No valid move to position")
        self.assertEqual(self.y, new_y, "No valid move to position")

    def test_move_to_relative_position(self):
        from sapyautomation.desktop.inputs.mouse import \
            get_mouse_coordinates, move_to_position, move_relative
        move_to_position(self.x, self.y)
        move_relative(10, 10)
        new_x, new_y = get_mouse_coordinates()

        self.assertEqual(self.x + 10,  new_x, "No valid move to relative "
                                              "position")
        self.assertEqual(self.y + 10,  new_y, "No valid move to relative "
                                              "position")

    def test_drag_to_position(self):
        from sapyautomation.desktop.inputs.mouse import \
            get_mouse_coordinates, drag_to_position
        drag_to_position(self.x, self.y)
        new_x, new_y = get_mouse_coordinates()

        self.assertEqual(self.x, new_x, "No valid drag to position")
        self.assertEqual(self.y, new_y, "No valid drag to position")
