from time import sleep


def identify_message(session: object) -> dict:
    """Identifies a messages

    Identify a message on screen

    Args:
        session (object): your active windows

    Returns:
        list_elements (dict): a list of elements of message like type and text
    """
    list_elements = {}
    msg = ''
    for _ in range(4):
        msg = session.findById("wnd[0]/sbar").text
        if msg != '':
            break
        sleep(1)

    if msg != '':
        msg_type = session.findById("wnd[0]/sbar").MessageType
        types = {"E": "Error",
                 "W": "Warning",
                 "S": "Success",
                 "A": "Abort",
                 "I": "Information"}

        msg_complete = types[msg_type]
        elements = list_elements.get("Message", [])
        elements.append({
            "text": msg,
            "type": msg_complete
        })
        list_elements["Message"] = elements
    return list_elements
