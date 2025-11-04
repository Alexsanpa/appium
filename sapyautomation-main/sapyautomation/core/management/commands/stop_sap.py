from sapyautomation.core.management.base import BaseCommand
from sapyautomation.desktop.process import kill_process, is_sap_running


class Command(BaseCommand):
    """ This command forces SAP to stop
    """

    def handle(self, **options):
        if is_sap_running():
            kill_process('saplogon.exe')
