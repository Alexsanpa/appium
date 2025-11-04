from sapyautomation.core.backends import MailBackend


def send_email(recipients: list, subject: str, content: str,
               extra_content: dict = None, attch_images: list = None):
    """ Sends email to recipients
    Args:
        recipients(list): List of recipients.
        subject(str): Subject of the email.
        content(str): Content of the email.
        extra_content(dict): Extra content for the email.
        attch_images(list): List of images to attach to the email.
    """
    backend = MailBackend()
    backend.create_msg(recipients, subject, content, extra_content)
    backend.attach_to_msg(images=attch_images)
    backend.send_email()
