from selenium.webdriver import ActionChains


def click(element: object):
    """
    Click an element

    Args:
        element (object): your element what you want to click
    """
    element.click()


def change_windows(driver: object, windows: int):
    """
    switch between windows

    Args:
        driver (object): driver to interface with the browser
        windows (int): windows number

    """
    window_new = driver.window_handles[windows]
    driver.switch_to.window(window_new)


def switch_frame(driver: object, locator: str):
    """
    Switches between frames on DOM

    Args:
        driver (object): driver to interface with the browser
        locator (str): xpath attribute an element what you want to locate
    """
    driver.switch_to.default_content()
    num_frames = driver.find_elements_by_xpath("//iframe")

    driver.implicitly_wait(5)

    for x in range(len(num_frames)):
        driver.switch_to.frame(x)

        if driver.find_elements_by_xpath(locator) is not None:
            break
        driver.switch_to.default_content()

    driver.implicitly_wait(20)


def clear_text(element: object):
    """
    Clear text of an element

    Args:
        element (object): element what you want to clear
    """
    element.clear()


def click_actions(driver: object, element: object):
    """
    Simulates a click

    Args:
        driver (object): driver to interface with the browser
        element (object): your element what you want to click
    """
    actions = ActionChains(driver)
    actions.click(element)
    actions.perform()


def input_text_actions(driver: object, element: object, text: str):
    """
    Input text on an element

    Args:
        driver (object): driver to interface with the browser
        element (object): your element what you want to click
        text(str): text what yo want to input on a element
    """
    actions = ActionChains(driver)
    actions.send_keys_to_element(element, text)
    actions.perform()
