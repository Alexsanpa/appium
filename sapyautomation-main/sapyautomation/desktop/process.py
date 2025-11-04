"""
Process activities
"""
import os
import re
from subprocess import Popen
import psutil


def launch_process(process_executable: str = None):
    """Launch a process by executable

    First we try to launch the process with Popen library if it does not work
    then we try to open it with os.system lib and cmd command 'START' (only for
    'valid_programs').

    Args:
        process_executable (str): the name of the process to execute (default
        None)
    """

    valid_programs = ["saplogon",
                      "chrome",
                      "winword",
                      "firefox",
                      "microsoftedge"]

    try:
        return Popen(process_executable)
    except FileNotFoundError:
        if process_executable in valid_programs:
            if not process_executable[-4:] == ".exe":
                process_executable.replace(".exe", '')
            command = os.system("start " + process_executable + "> nul 2> nul")
            if command == 0:
                return True
        raise FileNotFoundError("Process not found")


def is_process_running(name: str) -> bool:
    """Checks if process is currently running

    Checks if given process name ('name') is currently running on the system
    by comparing each element of the psutil list with the given name.

    Args:
        name(str): the name of the process we want to check

    Returns:
        bool: True if the process 'name' is in the psutil list of psutil
        opened processes

    """

    if isinstance(name, Popen):
        if name.poll() is None:
            return True
    else:
        for p in psutil.process_iter():
            if name.lower() in p.name().lower():
                return True
    return False


def list_running_processes() -> set:
    """Returns currently running processes on the system.

    Returns:
        process_list(set(list)): with all names of unique processes currently
        running on the system.
    """

    process_list = []
    for p in psutil.process_iter():
        process_list.append(p.name())
    return set(process_list)


def open_program_by_name(name: str, main_drive: str = "C:\\"):
    """launch a custom program by its executable name and drive.

    Args:
        name(str): the name of the executable file
        main_drive(str): location for searching the executable file (default
        "C:\\" )
    """

    if not name[-4:] == ".exe":
        name += ".exe"
    for root, _, files in os.walk(main_drive):
        for file in files:
            if file == name and file.endswith(".exe"):
                return Popen(os.path.join(root, file))
    raise FileNotFoundError("Program not found")


def kill_process(name: str = None, process: Popen = None) -> None:
    """Kill a process by Popen process or by string name.

    Examples:
        kill_process("notepad") #  killing process by name (without .exe)
        kill_process("notepad.exe") #  killing process by name

        new_process = Popen("notepad")
        kill_process(new_process) #  killing process by process type Popen


    Args:
        name(str): the name of an executable name i.e. notepad.exe (default
        None)
        process(Popen) subprocess.Popen object (default None)
    """

    if process:
        try:
            return process.kill()
        except AttributeError:
            raise ValueError("(name) is not a process")
    elif isinstance(name, str):
        if not name[-4:] == ".exe":
            name += ".exe"
        command = os.system("taskkill /f /im " + name + " >nul 2>&1")
        if command == 0:
            return True
    raise FileNotFoundError("Process not found")


def is_chrome_running() -> bool:
    """Returns True if Google Chrome is running.

    Returns:
        bool: True if Google Chrome is running, False otherwise.
    """

    for p in psutil.process_iter():
        if "chrome.exe" in p.name():
            return True
    return False


def is_firefox_running() -> bool:
    """ Returns True if Mozilla Firefox is running.

     Returns:
        bool: True if Mozilla Firefox is running, False otherwise.
    """

    for p in psutil.process_iter():
        if "firefox.exe" in p.name().lower():
            return True
    return False


def is_edge_running() -> bool:
    """Returns True if Microsoft Edge is running.

     Returns:
        bool: True if Microsoft Edge is running, False otherwise.
    """

    for p in psutil.process_iter():
        if "microsoftedge.exe" in p.name().lower():
            return True
    return False


def is_word_running() -> bool:
    """Returns True if Microsoft Word is running.

     Returns:
        bool: True if Microsoft Word is running, False otherwise.
    """

    for p in psutil.process_iter():
        if "winword.exe" in p.name().lower():
            return True
    return False


def is_sap_running() -> bool:
    """Returns True if SAP is running.

     Returns:
        bool: True if SAP is running, False otherwise.
    """

    for p in psutil.process_iter():
        if "saplogon.exe" in p.name().lower():
            return True
    return False


def focus_on_window(wildcard: str):
    """Find a window whose title matches the wildcard regex
    Args:
        wildcard (str): window title to find, regex or raw string
    Exceptions:
        OSError: Window not found
    """
    import win32gui  # pylint: disable=import-error
    import pywintypes  # pylint: disable=import-error

    def window_enum_callback(hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            obj.append(hwnd)

    obj = []
    win32gui.EnumWindows(window_enum_callback, wildcard)

    try:
        win32gui.SetForegroundWindow(obj[0])
        win32gui.BringWindowToTop(obj[0])

        return obj[0]

    except IndexError:
        raise OSError('Window with title "{0}" not found'.format(wildcard))

    except pywintypes.error:
        pass
