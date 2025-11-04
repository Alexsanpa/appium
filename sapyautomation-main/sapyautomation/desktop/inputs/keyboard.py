"""
Keyboard methods using pyautogui.
"""
from pyautogui import typewrite
import pyautogui


def press_key(key=None):
    """
     Press and release an entered key valid in KEYBOARD_kEYS list.
    """
    if pyautogui.isValidKey(key):
        return pyautogui.press(key)

    raise KeyError("Key not found")


def press_hot_key(first_key, second_key, third_key=None):
    """home_key
    Press a combination of two or three keys simultaneously.
    """
    if pyautogui.isValidKey(first_key) and pyautogui.isValidKey(second_key):
        if not third_key:
            return pyautogui.hotkey(first_key, second_key)
        if pyautogui.isValidKey(third_key):
            return pyautogui.hotkey(first_key, second_key, third_key)

        raise KeyError("Key not found")
    raise KeyError("Key not found")


def type_text(text=None, interval_seconds=0.001):
    """
    Type text in the current active field. The first argument represent the
    text and is entered as a string. The second variable is the time between
    two keystrokes. Pay attention that you can only press single character
    keys. Keys like ":", "F1",... can not be part of the text argument.
    """

    for letter in text:
        if not pyautogui.isValidKey(letter):
            raise KeyError("Character in text not found")

    return typewrite(text, interval=interval_seconds)


def caps_lock():
    """
    Press the Caps Lock key.
    """
    return pyautogui.press('capslock')


def num_lock():
    """
    Press the Num Lock key.
    """
    return pyautogui.press('numlock')


def enter():
    """
    Press the enter key.
    """
    return pyautogui.press('enter')


def space_bar():
    """
    Press the space bar key.
    """
    return pyautogui.press('space')


def backspace():
    """
    Press the Backspace key.
    """
    return pyautogui.press('backspace')


def delete():
    """
    Press the Delete key.
    """
    return pyautogui.press('delete')


def end_key():
    """
    Press the End key.
    """
    return pyautogui.press('end')


def home_key():
    """
    Press the End key.
    """
    return pyautogui.press('home')


def tab():
    """
    Press the Tab key.
    """
    return pyautogui.press('tab')
