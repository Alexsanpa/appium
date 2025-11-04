"""
Mouse methods using pyautogui.
"""

import pyautogui


def get_mouse_coordinates():
    """
    Return the absolute coordinates of the current
    position of the mouse.
    """
    coord = pyautogui.position()
    x_position = coord[0]
    y_position = coord[1]
    return x_position, y_position


def click_on_position(x_position=None, y_position=None, clicks=1):
    """
    Clicks N times on a pixel position on the visible screen determined by x
    and y
    coordinates.
    """
    move_to_position(x_position, y_position)

    return pyautogui.click(clicks=clicks)


def double_click_on_position(x_position=None, y_position=None):
    """
    Double clicks on a pixel position on the visible screen determined by x
    and y coordinates.
    """
    move_to_position(x_position, y_position)

    return pyautogui.doubleClick()


def right_click_on_position(x_position=None, y_position=None):
    """
    Right clicks on a pixel position on the visible screen determined by x
    and y coordinates.
    """
    move_to_position(x_position, y_position)
    return pyautogui.rightClick()


def move_to_position(x_position=None, y_position=None, seconds=0):
    """
    Moves pointer to a x-y position in N seconds.
    """
    max_x, max_y = pyautogui.size()
    if x_position < 0:
        x_position = max_x + x_position

    if y_position < 0:
        y_position = max_y + y_position

    return pyautogui.moveTo(x_position, y_position, duration=seconds)


def move_relative(x_position=None, y_position=None, seconds=0):
    """
    Moves the mouse an x- and y- distance relative to its current pixel
    position in N seconds.
    """
    return pyautogui.moveRel(x_position, y_position, duration=seconds)


def drag_to_position(x_position=None, y_position=None, duration=0.2,
                     button='left'):
    """
    Drag the mouse from its current position to a entered x-y position,
    while holding a specified button.
    """
    return pyautogui.dragTo(x_position, y_position, duration=duration,
                            button=button)
