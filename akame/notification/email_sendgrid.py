# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import logging
from typing import Any, Dict

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from akame.comparison.core import ComparerType

from .core import NotifierBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SendGridNotifier(NotifierBase):
    def __init__(self, task_name: str, notifier_creds: Dict[str, Any]) -> None:
        super().__init__(task_name, notifier_creds)
        self.sendgrid_api_key = notifier_creds["sendgrid_api_key"]
        self.from_email = notifier_creds["from_email"]
        self.to_email = notifier_creds["to_email"]

    def send_notification(self, message: str) -> None:
        client = SendGridAPIClient(self.sendgrid_api_key)
        message = Mail(
            from_email="from_email@heres.whatsnew.mba",
            to_emails="jimmy@lin.mba",
            subject="Sending with Twilio SendGrid is Fun",
            html_content="<strong>and easy to do anywhere, even with Python</strong>",
        )
        try:
            client.send(message)
        except Exception as e:
            logger.error(f"Failed to send the message: {e}")

    def main(self, comparer: ComparerType) -> None:
        if comparer.status_code == 1:
            self.send_notification(comparer.message)