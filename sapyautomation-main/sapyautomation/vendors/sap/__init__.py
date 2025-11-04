from .connection import SAP


def get_current_connection(num_connection: int):
    return SAP.get_current_connection(num_connection)


def get_sap_information(session: int = 0):
    return SAP.get_sap_information(session)
