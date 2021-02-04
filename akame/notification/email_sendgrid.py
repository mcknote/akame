import logging
from typing import Any, Dict

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from akame.comparison.core import ComparerType

from .core import NotifierBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SendGridNotifier(NotifierBase):
    """Class that handles notification through SendGrid

    Args:
        task_name (str): Task name
        sendgrid_api_key (str): SendGrid API key
        from_email (str): Emails to be sent from
        to_email (str): Emails to be sent to
    """

    def __init__(
        self,
        sendgrid_api_key: str,
        from_email: str,
        to_email: str,
    ) -> None:
        super().__init__()
        self.sendgrid_api_key = sendgrid_api_key
        self.from_email = from_email
        self.to_email = to_email

    def send_notification(self, message: str) -> None:
        client = SendGridAPIClient(self.sendgrid_api_key)
        message = Mail(
            from_email=self.from_email,
            to_emails=self.to_email,
            subject=f"Monitoring Task: {self.task_name}",
            html_content=message,
        )
        try:
            client.send(message)
        except Exception as e:
            logger.error(f"Failed to send the message: {e}")

    def main(self, comparer: ComparerType) -> None:
        if comparer.status_code == 1:
            self.send_notification(comparer.message)