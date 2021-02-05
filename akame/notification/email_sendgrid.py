import logging

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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

    def notify_condition_met(self) -> None:
        logger.info("Sending out notification through SendGrid")

        message = self.get_formatted_message()
        subject = self.get_formatted_subject()

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

    def get_formatted_message(self) -> str:
        content_0 = self.comparer.content_0
        content_1 = self.comparer.content_1
        task_name = self.comparer.task_name
        target_url = self.comparer.target_url
        comparer_message = self.comparer.message

        delta = StringDelta(a=content_0, b=content_1)
        formatter = FormatEmailHTML(delta)

        return formatter.main(
            task_name=task_name,
            comparer_message=target_url,
            target_url=comparer_message,
        )

    def get_formatted_subject(self) -> str:
        task_name = self.comparer.task_name
        comparer_message = self.comparer.message
        return f"[{comparer_message}] {task_name}"
