import logging

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from akame.comparison.core import ComparerType
from akame.comparison.delta import StringDelta

from .core import NotifierBase
from .formatters import FormatEmailHTML

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SendGridNotifier(NotifierBase):
    """Class that handles notification through SendGrid

    Args:
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

    def send_notification(self, subject: str, message: str) -> None:
        logger.info("Sending out notification through SendGrid")

        client = SendGridAPIClient(self.sendgrid_api_key)
        message = Mail(
            from_email=self.from_email,
            to_emails=self.to_email,
            subject=subject,
            html_content=message,
        )
        try:
            client.send(message)
        except Exception as e:
            logger.error(f"Failed to send the message: {e}")

    def get_formatted_message(self, comparer: ComparerType) -> str:
        delta = StringDelta(a=comparer.content_0, b=comparer.content_1)
        formatter = FormatEmailHTML(delta)

        return formatter.main(
            task_name=self.task_name,
            comparer_message=comparer.message,
            target_url=self.target_url,
        )

    def main(self, comparer: ComparerType) -> None:
        if comparer.status_code == 1:
            message = self.get_formatted_message(comparer)
            subject = f"[{comparer.message}] {self.task_name}"
            self.send_notification(subject, message)