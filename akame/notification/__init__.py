import logging

from akame.comparison.core import ComparerType
from akame.comparison.delta import StringDelta

from .core import NotifierBase
from .formatters import FormatColoredTerminalText, FormatPlainText

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BasicNotifier(NotifierBase):
    """Class that handles notification through the console"""

    def __init__(self) -> None:
        super().__init__()

    def load_task_info(self, task_name: str, target_url: str) -> None:
        self.task_name = task_name
        self.target_url = target_url

    def send_notification(self, message: str) -> None:
        logger.info(message)

    def get_formatted_message(self, comparer: ComparerType) -> str:

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
