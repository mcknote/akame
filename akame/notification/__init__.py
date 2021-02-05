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

    def notify_condition_met(self) -> None:
        message = self.get_formatted_message()
        logger.info(message)

    def notify_condition_notmet(self) -> None:
        message = self.comparer.message
        logger.info(message)

    def get_formatted_message(self) -> str:
        content_0 = self.comparer.content_0
        content_1 = self.comparer.content_1

        delta = StringDelta(a=content_0, b=content_1)
        try:
            message = FormatColoredTerminalText(delta).main()
        except ImportError as e:
            logger.info(
                f"Missing module '{e.name}'; printing plain text instead"
            )
            message = FormatPlainText(delta).main()

        return message
