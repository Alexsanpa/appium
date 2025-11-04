import re
import textwrap
from enum import Enum

TIMESTAMP_FORMAT = '%Y-%m-%d_%H-%M-%S'


class Convention(Enum):
    under_score = 0
    camel_case = 1
    title_camel_case = 2
    bad_under_score = 3
    bad_camel_case = 4


def string_to_pep_convention(string: str,
                             convention: Convention = Convention.under_score):
    """ Converts string to a pep8 naming convention

    Args:
        string(str): string to be converted
        convention(Convention): convention to be used for ther formatting

    """
    formatted_string = ''
    string = re.sub(r"[^a-zA-Z0-9 -]+", '', string)
    if convention == Convention.under_score:
        string = string.lower().strip()
        formatted_string = '_'.join(string.split(' '))

    elif convention == Convention.camel_case:
        string = string.lower().strip()
        first_part = True
        formatted_string = ""

        for part in re.split(' |_|-', string):
            if not first_part:
                formatted_string = formatted_string + part.strip().title()
                continue
            formatted_string = formatted_string + part.strip()

            first_part = False

    return formatted_string


def wrap_text(string: str, max_chars: int = 80) -> list:
    """ Wraps text to specific char count.

    Args:
        string(str): text to be wrapped.
        max_chars(int): max vhar count.

    Returns:
        list of wrapped lines.

    """
    wrapped_text = []
    string = textwrap.fill(string, max_chars)

    for line in string.split('\n'):
        wrapped_text.append(line)

    return wrapped_text


def convert_text_to_matrix(text: str) -> list:
    """ Converts text to a matrix.

    Args:
        text(str): text to be converted.

    Returns:
        list of lists.

    """
    expected_result_lang = {"ESP": "Resultado esperado:",
                            "ENG": "Expected result:",
                            "POR": "Resultado esperado:"}
    description_lang = {"ESP": "Descripción:",            
                        "ENG": "Description:",
                        "POR": "Descrição:"}

    clean_text = text.strip()
    first_word = clean_text.split()[0].strip()

    language = ""
    if first_word in "Descripción:":
        language = "ESP"
    elif first_word in "Descrição:":
        language = "POR"
    else:
        language = "ENG"

    index_desc = clean_text.find(expected_result_lang[language])

    description = clean_text[:index_desc].strip()
    expected_result = clean_text[index_desc:].strip()

    matrix = []
    description_list = [description_lang[language], description.replace(
        description_lang[language], "").strip()]
    expected_result_list = [expected_result_lang[language], expected_result.replace(
        expected_result_lang[language], "").strip()]

    matrix.append(description_list)
    matrix.append(expected_result_list)

    return matrix
