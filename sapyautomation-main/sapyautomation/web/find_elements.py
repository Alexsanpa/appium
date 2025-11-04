from selenium.common.exceptions import NoSuchElementException
from sapyautomation.web.elements import ElementByLink, ElementByXPath,\
    ElementByTag, ElementByClass, ElementById, ElementByName


def find_element_by_id(driver: object, locator: str):
    """Identifies an element by id

    Identify an element by id

    Args:
        driver (object): driver to interface with the browser
        locator (str): id attribute of an element

    Returns:
        web_element (object): element present on windows

    Raises:
        NoSuchElementException: if element is not present on windows
    """
    element = ElementById(driver, locator)

    return element.element()


def find_element_by_name(driver: object, locator: str):
    """Identifies an element by name

    Identify an element by name

    Args:
        driver (object): driver to interface with the browser
        locator (str): name attribute of an element

    Returns:
        web_element (object): element present on windows

    Raises:
        NoSuchElementException: if element is not present on windows
    """
    element = ElementByName(driver, locator)

    return element.element()


def find_element_by_xpath(driver: object, locator: str):
    """Identifies an element by xpath

    Identify an element by xpath

    Args:
        driver (object): driver to interface with the browser
        locator (str): xpath attribute of an element

    Returns:
        web_element (object): element present on windows

    Raises:
        NoSuchElementException: if element is not present on windows
    """
    element = ElementByXPath(driver, locator)

    return element.element()


def find_element_by_tag_name(driver: object, locator: str):
    """Identifies an element by tag name

    Identify an element by tag name

    Args:
        driver (object): driver to interface with the browser
        locator (str): tag name attribute of an element

    Returns:
        web_element (object): element present on windows

    Raises:
        NoSuchElementException: if element is not present on windows
    """
    element = ElementByTag(driver, locator)

    return element.element()


def find_element_by_class_name(driver: object, locator: str):
    """Identifies an element by class name

    Identify an element by class name

    Args:
        driver (object): driver to interface with the browser
        locator (str): class name attribute of an element

    Returns:
        web_element (object): element present on windows

    Raises:
        NoSuchElementException: if element is not present on windows
    """
    element = ElementByClass(driver, locator)

    return element.element()


def find_element_by_link_text(driver: object, locator: str):
    """Identifies an element by link text

    Identify an element by link text

    Args:
        driver (object): driver to interface with the browser
        locator (str): link text attribute of an element

    Returns:
        web_element (object): element present on windows

    Raises:
        NoSuchElementException: if element is not present on windows
    """
    element = ElementByLink(driver, locator)

    return element.element()


def find_element_by_partial_link_text(driver, locator):
    """Identifies an element by partial link text

    Identify an element by partial link text

    Args:
        driver (object): driver to interface with the browser
        locator (str): partial link text attribute of an element

    Returns:
        web_element (object): element present on windows

    Raises:
        NoSuchElementException: if element is not present on windows
    """
    element = ElementByLink(driver, locator, False)

    return element.element()


def find_all_elements_by_id(driver: object, locator: str):
    """Identifies a group of elements by id

    Identify a group of elements by id

    Args:
        driver (object): driver to interface with the browser
        locator (str): id attribute of an element

    Returns:
        web_element (object): element present on windows

    Raises:
        NoSuchElementException: if element is not present on windows
    """
    try:
        elements = driver.find_elements_by_id(locator)
    except NoSuchElementException:
        raise NoSuchElementException

    return elements


def find_all_elements_by_xpath(driver, locator):
    """Identifies a group of elements by xpath

    Identify a group of elements by xpath

    Args:
        driver (object): driver to interface with the browser
        locator (str): xpath attribute of an element

    Returns:
        web_element (object): element present on windows

    Raises:
        NoSuchElementException: if element is not present on windows
    """
    try:
        elements = driver.find_elements_by_xpath(locator)
    except NoSuchElementException:
        raise NoSuchElementException

    return elements
