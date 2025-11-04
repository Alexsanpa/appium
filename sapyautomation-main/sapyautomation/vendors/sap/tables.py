import os

import numpy as np

from sapyautomation.vendors.sap.connection import SAP
from sapyautomation.vendors.sap.actions import find_element_by_id, \
    scroll_vertical, scroll_horizontal


def get_rows(start: str, session: object) -> list:
    """Get elements from columns in a list.

    This method takes an element as start point to find elements bellow,
    it reads the total visible rows to know how much to scroll and it
    validate each row searching for an element in the same column as the
    starting point. It scrolls when there is no more rows to read and then
    scrolls the parent element containter and searches again until there are
    no more rows.

    Args:
        start (str): starting element id.
        session (object): session object where the method is going to search.

    Returns:
        A list of the elements in the column.

    """
    actual = get_actual_name(start)
    parent = get_parent_name(start)
    parent_element = find_element_by_id(parent, session)
    scroll_vertical(parent_element, 0)
    col, row = actual.replace("lbl[", '').replace("]", '').split(',')

    visible_rows = get_visible_rows(start, row, session)

    found_text_elements = []
    row_counter = int(row) + 2
    scroll_counter = 1
    read_row = True

    while read_row:
        ele = parent + "/lbl[" + \
              str(col) + "," + str(row_counter) + "]"
        try:
            ele = find_element_by_id(ele, session)
            found_text_elements.append(str(ele.text))

        except ModuleNotFoundError:
            if row_counter > visible_rows:
                scrol = visible_rows * scroll_counter

                scroll_vertical(parent_element, scrol)
                scroll_counter += 1
                row_counter = int(row) + 1
            if get_visible_rows(start, row, session) < 1:
                read_row = False

        row_counter += 1

    return found_text_elements


def get_visible_rows(start: str, row: int, session: object) -> int:
    """Returns the number or visible rows in screen.

    It returns the visible rows in screen, this method is used to know how
    many rows we need to scroll to be able to see new elements on the screen
    and read them.

    Args:
        start (str): element id from the starting point.
        row (int): starting row to count (row number for the column labels).
        session (object): session object where the method is going to search.

    Returns:
        the x coordinate from the las visible object in the scripting tree.

    """
    parent = get_parent_name(start)
    parent_element = find_element_by_id(parent, session)
    children = parent_element.Children
    len_children = len(children)
    max_visible_rows = children[len_children - 1].Id.replace(
        parent + get_label_type(start) + "[",
        '').replace("]", '').split(',')[1]
    return int(max_visible_rows) - int(row) - 1


def get_cols(start: str, session: object) -> list:
    """Search for new columns and call get_visible_rows() for each.

    thid method search for new columns after the start element given and
    call the get_rows() method to find the elements in each column found.

    Args:
        start (str):
        session (int): session object where the method is going to search.

    Returns:
        A list of lists with the elements found for each column found from
        the start element.

    """
    parent = get_parent_name(start)
    actual = get_actual_name(start)

    parent_element = find_element_by_id(parent, session)
    label_type = get_label_type(start)
    col, row = actual.replace(label_type + "[", '').replace("]", '').split(',')

    scroll_horizontal(parent_element, col)

    found_text_elements = []
    found_id_elements = []
    scroll_index = 0
    read_columns = True
    tabla = []

    while read_columns:
        new = get_children_from_col(start, session, col)

        try:
            ele = parent + get_label_type(start) + "[" + \
                  str(new[scroll_index]) + "," + str(row) + "]"
            ele = find_element_by_id(ele, session)
            if ele.text != '':
                if ele.text in found_text_elements:
                    break
                found_text_elements.append(ele.text)
                found_id_elements.append(ele.Id)
                tabla.append(get_rows(ele.Id, session))

        except IndexError:
            read_columns = False

        if scroll_index == int(len(new)) - 1:
            last_scroll = int(new[scroll_index]) + int(col)
            scroll_vertical(parent_element, 0)
            scroll_horizontal(parent_element, last_scroll)
            scroll_index = 0
        else:
            scroll_index += 1

    tabla.insert(0, found_text_elements)

    return tabla


def get_children_from_col(full_path: str, session: object, column: int = 0):
    """Returns the x value for every column name coordinates

    The full path defines the starting point where we want to start the
    search, this method returns the x coordinate, normally this id is
    consecutive from the start point but there are tables that has
    inconsistent x coordinates i.e. lbl[3,3], lbl[9,3], lbl[21,3], lbl[35,3]).
    this method is used to get the id from the new elements in screen.

    Args:
        full_path (str): starting element id.
        session (object): session object where the method is going to search.
        column (int): column number where the column labels are.

    Returns:
        A list with the x value of every column on screen.

    """
    parent = get_parent_name(full_path)
    parent_element = find_element_by_id(parent, session)
    children = parent_element.Children
    new_children = []

    for child in children:
        if "," + str(column) in child.Id:
            new_children.append(get_actual_name(child.Id).replace(
                get_label_type(
                    full_path) + "[", '').replace("]", '').split(',')[0])
    return new_children


def get_actual_name(full_path: str):
    """Returns the element name from the full path.

    Example:
        path = "/app/con[0]/ses[0]/wnd[0]/usr/tbl_SAP_VIEWER/txt[0,0]"
        name = get_actual_name(path)

        name = "txt[0,0]"

    Args:
        full_path (str): element id.

    Returns:
        the label name from the given id.

    """
    return str(
        os.path.basename(os.path.normpath(full_path)))


def get_parent_name(full_path: str):
    """Returns the name from the parent element ot the given element.

    When we want to scroll a table from a table element we need first to get
    the parent element id and scroll it.

    Example:
        path = "/app/con[0]/ses[0]/wnd[0]/usr/tbl_SAP_VIEWER/txt[0,0]"
        parent = get_get_parent_name(path)

        parent = "/app/con[0]/ses[0]/wnd[0]/usr/tbl_SAP_VIEWER"

    Args:
        full_path (str): Complete id from element.

    Returns:
        the same id without the last element splitting by "/".


    """
    return full_path.replace(
        full_path.split('/')[len(full_path.split('/')) - 1], '')


def get_label_type(full_path: str) -> str:
    """Returns the type of element from an element id.

    Example:
        path = "/app/con[0]/ses[0]/wnd[0]/usr/tbl_SAP_VIEWER/txt[0,0]"
        typo = get_get_parent_name(path)

        typo = "txt"

    Args:
        full_path (str): element id to get the element type.

    Returns:
        the string of the id given element.

    """
    parent = get_parent_name(full_path)
    new = full_path.replace(parent, '')
    index = new.index('[')
    return new[:index]


def get_table(full_path: str, session: object = 0) -> list:
    """Returns the table information selecting the starting point.

    Returns all the data from a table, giving the first element (0,0) where the
    table starts.

    Args:
        full_path (str): Element id from the starting element.
        session (object): session object where the method is going to search.

    Returns:
        A list of lists with all the table data.

    """
    tabla = get_cols(full_path, session)

    numpy_array = np.array(tabla)
    transpose = numpy_array.T
    transpose_list = transpose.tolist()

    return transpose_list


def set_value(table_id, x: int, y: int, value: str) -> bool:
    """Writes a 'value' in the positions 'x','y' element from 'table_id'

    Set element text to 'value' giving the parent element id and the
    coordinates for the element.

    Args:
        table_id (str): Id of the element container of the textfield[x,y]
        x (int): column number
        y (int): row number
        value (str):

    Returns: true if the value was setted correctly, False otherwise.

    """
    session = SAP.get_current_connection(0)
    element = find_element_by_id(table_id,
                                 session)

    children = element.Children

    for child in children:
        if '[' + str(x) + ',' + str(y) + ']' in child.Id:
            child.text = value
            if child.text == value:
                return True
    return False
