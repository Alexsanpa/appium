import smtplib
from pathlib import Path

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from sapyautomation.core import LazySettings
from sapyautomation.core.utils.general import get_resource, wait
from sapyautomation.core.utils.exceptions import SMTPError


class MailBackend:
    """ Class to create and send emails

    Note:
        Available settings entries:
        MAIL_SERVER, MAIL_PORT, MAIL_SSL_PORT, MAIL_USE_SSL.
    """

    def __init__(self):
        self.connection = SMTPConnection()

    def create_msg(self, recipients: list, subject: str, content: str,
                   extra_content: dict = None):
        """ Creates email object to send.
        Args:
            email_to(list): list of recipients emails.
            subject(str): subject of the message.
        """
        msg = MIMEMultipart('related')
        if extra_content is None:
            extra_content = {}
        extra_content['subject'] = subject
        extra_content['content'] = content

        mail_content = self._load_template(extra_content)

        msg['Subject'] = subject
        msg['From'] = self.connection.user
        msg['To'] = ', '.join(recipients)

        msg.attach(MIMEText(mail_content, 'html'))

        self._msg = msg

    @staticmethod
    def _load_template(parameters: dict) -> str:
        """ loads email template and parses data to it
        Args:
        Returns:
            Str: parsed template as str

        """
        path = Path(get_resource('email_template.html'))
        parsed_template = []

        with path.open(mode='r') as file:
            for line in file.readlines():
                for key in parameters.keys():
                    line = line.replace('{{%s}}' % key, parameters[key])

                parsed_template.append(line)

        return ''.join(parsed_template)

    def attach_to_msg(self, images: list = None, documents: list = None):
        """ Add attachments to the email
        Args:
            images(list): list of images to attach.
        """
        if images is not None:
            for img in images:
                image = self._attachment(Path(img), 'img')

                self._msg.attach(image)

        if documents is not None:
            for doc in documents:
                document = self._attachment(Path(doc), 'doc')

                self._msg.attach(document)

    @staticmethod
    def _attachment(path: Path, attch_type: str):
        """ Generates sendable attachment format
        Args:
            path(Path): Path object of attachment file
            type(str): attachment type
        """
        file = path.open('rb')
        if attch_type == 'img':
            attch = MIMEImage(file.read())

        elif attch_type == 'doc':
            attch = MIMEBase('application', "octet-stream")
            attch.set_payload(file.read())
            encoders.encode_base64(attch)

        attch.add_header(
            'Content-Disposition', 'attachment',
            filename=path.parts[-1])
        attch.add_header('Content-ID',
                         '<%s>' % path.parts[-1].split('.')[0])

        return attch

    def send_email(self):
        """ Sends email if its been created

        Raises:
            SMTPError: if message cant be sended
        """

        if hasattr(self, '_msg'):
            self.connection.open()
            self.connection.send_email(self._msg)
            self.connection.close()

            return True

        raise SMTPError('No message to send.')


class SMTPConnection:
    """ This class manages smtp connection
    """

    def __init__(self):
        self._credentials = LazySettings().CREDENTIALS('MAIL')
        self.user = self._credentials['USER']

    def open(self):
        """ Opens the connection

        Gets credentials and parameters from LazySettings
        """
        if LazySettings().MAIL_USE_SSL:
            connection = smtplib.SMTP_SSL(LazySettings().MAIL_SERVER,
                                          LazySettings().MAIL_SSL_PORT)
            connection.connect(LazySettings().MAIL_SERVER,
                               LazySettings().MAIL_SSL_PORT)
        else:
            connection = smtplib.SMTP(LazySettings().MAIL_SERVER,
                                      LazySettings().MAIL_PORT)
            connection.connect(LazySettings().MAIL_SERVER,
                               LazySettings().MAIL_PORT)
        connection.ehlo()
        connection.login(self._credentials['USER'],
                         self._credentials['PASSWORD'])

        self._connection = connection

    def send_email(self, msg: MIMEMultipart):
        """ Sends email
        """
        self._connection.sendmail(msg['From'], msg['To'], msg.as_string())

    def close(self):
        """ Closes the connection """
        wait(1)
        self._connection.quit()
