
from sapyautomation.core.management.base import BaseCommand
from sapyautomation.core.management.conf import LazySettings
try:
    from sapyautomation.vendors.sap.connection import SAP
    from sapyautomation.vendors.sap.login import Login
except ImportError:
    pass


class Command(BaseCommand):
    """ This command allows the user to run SAP

    Allows to open Sap and login with the credentials in secrets.ini

    """
    help = "Run n test cases."

    def add_arguments(self, parser):
        parser.add_argument('connection', nargs=1, help='Connection name')
        parser.add_argument('--credentials', nargs='?', help='foo help')

    def handle(self, **options):
        conn = options['connection']
        cred = options['credentials'] if options['credentials'] else 'SAP'

        sap = SAP(conn[0])
        sap.start()

        try:
            self.login_obj = Login()
        except NameError:
            pass
        data = LazySettings().CREDENTIALS(cred)
        login_obj = Login()
        login_obj.login(client=data['CLIENT'],
                        user=data['USER'],
                        password=data['PASSWORD'],
                        language=data['LANGUAGE'])

        print("Process finished")
