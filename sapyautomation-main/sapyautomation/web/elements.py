from time import sleep
from selenium.common.exceptions import NoSuchElementException,\
    ElementNotInteractableException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from sapyautomation.web.models import WEB_VIRTUAL_KEYS
from sapyautomation.core.utils.exceptions import FioriElementNotFound


class _Element:
    """ Base element object

    Args:
        driver(object): Browser driver object
        element_id(str): id of the wanted element
        element_name(str): name of the wanted element
        element_xpath(str): xpath of the wanted element
        element_tag(str): tag of the wanted element
        element_class(str): class of the wanted element
        element_link(str): link text of the wanted element
        exact_match(bool): flag to indicate exact matches only
    """
    def __init__(self, driver: object, element_id: str = None,
                 element_name: str = None, element_xpath: str = None,
                 element_tag: str = None, element_class: str = None,
                 element_link: str = None, exact_match: bool = True):
        self._driver = driver
        self._element_id = element_id
        self._element_name = element_name
        self._element_xpath = element_xpath
        self._element_tag = element_tag
        self._element_class = element_class
        self._element_link = element_link

        self._element = self._find_element(exact_match)

    @property
    def _actions(self):
        if not hasattr(self, '__actions'):
            setattr(self, '__actions', ActionChains(self._driver))

        return getattr(self, '__actions')

    def _find_element(self, exact_match: bool = True):
        """ Find element depending on data received

        Args:
            element_id(str): element id to be searched internally
            exact_match(bool): flag to indicate exact matches only.
        """
        element = None
        try:
            if self._element_id is not None:
                element = self._driver.find_element_by_id(self._element_id)

            elif self._element_name is not None:
                element = self._driver.find_element_by_name(self._element_name)

            elif self._element_xpath is not None:
                element = self._driver.find_element_by_xpath(
                    self._element_xpath)

            elif self._element_tag is not None:
                element = self._driver.find_element_by_tag_name(
                    self._element_tag)

            elif self._element_class is not None:
                element = self._driver.find_element_by_class_name(
                    self._element_class)

            elif self._element_link is not None:
                if exact_match:
                    element = self._driver.find_element_by_link_text(
                        self._element_link)

                else:
                    element = self._driver.find_element_by_partial_link_text(
                        self._element_link)

        except NoSuchElementException:
            pass

        return element

    @property
    def value(self):
        value = self.element().get_attribute('value')

        return value

    def exists(self, check_visible: bool = False):
        """ Verifies if the element exists

        Args:
            check_visible(bool): checks if the element is also visible

        Returns:
            True or False if the element exists
        """

        if self._element is not None:
            check_visible = self._element.is_displayed() if check_visible \
                else True
            if check_visible:
                return True

        return False

    def children(self, by_class: str = None,
                 by_xpath: str = None):
        """ Returns element's children

        Args:
            by_class(str): search children by class
            by_xpath(str): search children by xpath
        """
        elements = []

        if by_class is not None:
            elements = self.element().find_elements_by_class_name(by_class)

        elif by_xpath is not None:
            elements = self.element().find_elements_by_xpath(by_xpath)

        return elements

    def element(self, max_wait: int = 1, force: bool = False) -> object:
        """ Retrieves the element object

        Args:
            max_wait (int): max seconds to await for the element
            force (bool): force element clean search
        Returns:
            element (object): element present on windows

        Raises:
            ModuleNotFoundError: if element is not present on windows
        """
        if force or not self.exists():
            for _ in range(max_wait):
                sleep(1)
                self._element = self._find_element()
                if self.exists(True):
                    return self._element

            raise FioriElementNotFound("The element has not been found")

        return self._element

    def press(self, retry: int = 1):
        """ Do press action on the elemnt
        Simulate a click event on button, icon

        Args:
            retry(int): time to re-try de press action

        Raises:
            AttributeError: If you want to press some element different like
            button or icon
        """
        for i in range(retry):
            try:
                self._actions.click(self._element)
                self._actions.perform()
                break

            except StaleElementReferenceException as e:
                sleep(2)
                if i >= retry-1:
                    raise e

    def send_key(self, key):
        """Sends keys in the Keyboard

        Send keys in the keyboard for do actions on screen

        Args:
            element (object): element what you want to send keys
            keys: Command or key

        Raises:
              ValueError: If you send a keys incorrect or not enabled
               KeyError: If you send a command incorrect or not enabled
        """
        if not key.startswith('\\'):
            keys = WEB_VIRTUAL_KEYS[key]

        else:
            keys = (key, )

        self.set_focus()
        for k in keys:
            self._actions.key_down(k)

        keys.reverse()
        for k in keys:
            self._actions.key_up(k)

    def set_focus(self):
        """ Sets gui focus on element
        """
        return self._element.location_once_scrolled_into_view

    def select(self):
        """ Do select action on element
        Select an option of menu or radiobutton

        Return:
            bool: True if successful, False otherwise

        Raises:
            AttributeError: If you want to select some element different like
            menu or radiobutton
        """
        self._actions.click(self._element)

    def select_combo_value(self, text: str, exact_match: bool = False):
        """ selects a value from combo element
        Select a specific value from a drop down list

        Args:
             text (str): specific value from drop down list what you want to
                 select
             position (int): position of specific value from drop down list

        Raises:
            KeyError: If your specific value is not into drop down list
            AttributeError: If you want to select a specific value on an
                element
            different like Combobox
        """
        for option in self._element.find_elements_by_tag_name("option"):
            if (not exact_match and option.text.startswith(text)) or \
                    (exact_match and option.text == text):
                option.click()
                break

    def input_text(self, text: str, clear: bool = True):
        """ Adds text to input element
        Input text on an element what you want

        Args:
            texts (str): text what you want to input

        Returns:
             bool: True if successful, False otherwise

        Raises:
            AttributeError: If you want to input text on an element different
                like textField
        """
        for _ in range(30):
            try:
                self.element()
                if clear:
                    self._element.clear()

                self._element.send_keys(text)
                break

            except (ElementNotInteractableException):
                pass

    def scroll_vertical(self, index: int):
        """ Do vertical scroll on element
        Do scroll vertical on screen depends on position what you want

        Args:
            index (int): row index from table

        Raises:
            AttributeError: If you want to scroll some element different like
            windows
        """
        for i in range(index):
            if i > 0:
                self.send_key(Keys.ARROW_DOWN)

            else:
                self.send_key(Keys.ARROW_UP)

            self._actions.perform()

    def scroll_horizontal(self, index: int):
        """ Do horizontal scroll on element
        Do scroll horizontal on screen depends column index what you want

        Args:
            index (int): column index from table

        Raises:
            AttributeError: If you want to scroll some element different like
            windows
        """
        for i in range(index):
            if i > 0:
                self.send_key(Keys.ARROW_RIGHT)

            else:
                self.send_key(Keys.ARROW_LEFT)

            self._actions.perform()

    def child(self, element_name: str):
        """ Searchs for child element

        Args:
            element_name(str): fragment id of the wanted child

        Returns:
            Framework's element object if exists.
        """


class ElementById(_Element):
    """ Manages element identifing it by id

    Args:
        element_id(str): id of the wanted element
        driver(object): Browser driver object
    """
    def __init__(self, driver: object, element_id: str = None):
        super().__init__(driver=driver, element_id=element_id)


class ElementByName(_Element):
    """ Manages element identifing it by name

    Args:
        element_name(str): name of the wanted element
        driver(object): Browser driver object
    """
    def __init__(self, driver: object, element_name: str = None):
        super().__init__(driver=driver, element_name=element_name)


class ElementByXPath(_Element):
    """ Manages element identifing it by xpath

    Args:
        element_xpath(str): xpath of the wanted element
        driver(object): Browser driver object
    """
    def __init__(self, driver: object, element_xpath: str = None):
        super().__init__(driver=driver, element_xpath=element_xpath)


class ElementByTag(_Element):
    """ Manages element identifing it by tag

    Args:
        element_tag(str): tag of the wanted element
        driver(object): Browser driver object
    """
    def __init__(self, driver: object, element_tag: str = None):
        super().__init__(driver=driver, element_tag=element_tag)


class ElementByClass(_Element):
    """ Manages element identifing it by class

    Args:
        element_class(str): class of the wanted element
        driver(object): Browser driver object
    """
    def __init__(self, driver: object, element_class: str = None):
        super().__init__(driver=driver, element_class=element_class)


class ElementByLink(_Element):
    """ Manages element identifing it by link

    Args:
        element_link(str): link of the wanted element
        driver(object): Browser driver object
    """
    def __init__(self, driver: object, element_link: str = None,
                 exact_match: bool = True):
        super().__init__(driver=driver, element_link=element_link,
                         exact_match=exact_match)
