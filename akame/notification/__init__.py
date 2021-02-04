import logging

from akame.comparison.core import ComparerType
from akame.comparison.delta import StringDelta

from .core import NotifierBase
from .formatters import FormatColoredTerminalText, FormatPlainText

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BasicNotifier(NotifierBase):
    """Class that handles notification through the console

    Args:
        task_name (str): Task name
    """

    def __init__(self, task_name: str) -> None:
        super().__init__(task_name)

    def send_notification(self, message: str) -> None:
        logger.info(message)

    def get_formatted_message(self, comparer: ComparerType) -> str:
        logger.info("Formatting delta for Pushover")

        delta = StringDelta(a=comparer.content_0, b=comparer.content_1)
        try:
            message = FormatColoredTerminalText(delta).main()
        except ImportError as e:
            logger.info(
                f"Missing module '{e.name}'; printing plain text instead"
            )
            message = FormatPlainText(delta).main()

        return message

    def main(self, comparer: ComparerType) -> None:
        if comparer.comparison_status == 1:
            message = self.get_formatted_message(comparer)
        else:
            message = comparer.message

        self.send_notification(message)
