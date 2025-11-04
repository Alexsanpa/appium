"""Crear una clase que permita interactuar con pymetrybus"""
from pywinauto import Application
import time
import os
from pywinauto import Desktop
import xml.etree.ElementTree as ET
import json


class PymetryBus:
    def __init__(self, pymetry_path: str = "../pymetryBus/responses"):
        """
        Constructor for PymetryBus Class
        """
        self.archivo_employee = (
            "./resources/Pymetry/EmployeeNumbers/employee_numbers.txt"
        )
        self.archivo_client = "./resources/Pymetry/EmployeeNumbers/client_numbers.txt"
        self.archivo_cards = "./resources/Pymetry/Tarjetas/card_numbers.txt"
        self.archivo_checks = "./resources/Pymetry/Cheques/checks.txt"

        self.card_dict = self.get_dictionary_of_matching_files(
            pymetry_path, match="tarjeta"
        )

    def add_employee_number(self, employee_number: str):
        """
        Add employee number to the input field

        Args:
            employee_number (str): employee number to add
        """
        if not os.path.exists(self.archivo_employee):
            open(self.archivo_employee, "w").close()
        with open(self.archivo_employee, "w") as f:
            f.write(employee_number + "\n")

    def add_client_number(self, client_number: str):
        """
        Add client number to the input field

        Args:
            clients_number (str): employee number to add
        """

        if not os.path.exists(self.archivo_client):
            open(self.archivo_client, "w").close()
        with open(self.archivo_client, "w") as f:
            f.write(client_number + "\n")

    def get_dictionary_of_matching_files(
        self, current_path: str, match: str = "tarjeta"
    ) -> dict:
        """
        Get files from their respective directories.

        Args:
            current_path (str): The path of the directory to search in.
            match (str, optional): The string to match in the file content. Defaults to "tarjeta".

        Returns:
            dict: A dictionary containing the file names and their corresponding paths.

        Raises:
            ValueError: If the given path is not a directory or if there are no files with the given match.
        """
        path_dict = {}
        # If the current is a directory
        if os.path.isdir(current_path):
            # Get the list of files and directories in the current directory
            paths = os.listdir(current_path)
            # Recursively search for files in each subdirectory
            for path in paths:
                path = os.path.join(current_path, path)
                if os.path.isdir(path):
                    continue
                with open(path, "r") as file:
                    xml_data = file.read()

                    root = ET.fromstring(xml_data)
                    p_data = root.find(".//{http://developer.intuit.com/}p_data")
                    if p_data is not None:
                        p_data_text = p_data.text
                    else:
                        continue
                    p_data = json.loads(p_data_text)
                    card_number = p_data.get(match, None)

                    if card_number is not None:
                        # Add the card_number and its path to the dictionary
                        path_dict[card_number] = path

        else:
            raise ValueError("The given path is not a directory.")
        if path_dict == {}:
            raise ValueError("There are no files with the given match.")

        return path_dict

    def add_card(self, card_number: str):
        """
        Add employee number to the input field

        Args:
            card_number (str): The card number to add

        Raises:
            ValueError: If the card number does not exist in the card dictionary
        """
        card_number = str(card_number)
        card_number = card_number.strip()
        card_number = card_number.replace(" ", "")
        card_number = card_number.replace("'", "")
        card_number = card_number.replace("''", "")
        card_number = card_number.replace('"', "")
        card_number = card_number.replace(",", "")
        card_number = card_number.replace(".", "")
        if card_number in self.card_dict:
            source_file = self.card_dict[card_number]
            destination_file = "./resources/Pymetry/Tarjetas/SymLeeTarjeta.xml"

            # Check if the file exists. If the file exists, remove it
            if os.path.exists(destination_file):
                os.remove(destination_file)

            with open(source_file, "rb") as src, open(destination_file, "wb") as dst:
                # Read and write the file
                dst.write(src.read())

        else:
            raise ValueError("The card number does not exist")

    def add_check(self, check_number: str):
        """
        Add employee number to the input field

        Args:
            employee_number (str): employee number to add
        """
        if not os.path.exists(self.archivo_checks):
            open(self.archivo_checks, "w").close()
        with open(self.archivo_checks, "w") as f:
            f.write(check_number + "\n")
