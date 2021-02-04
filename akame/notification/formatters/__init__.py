import logging

from akame.comparison.delta.core import DeltaType

from .core import FormatterBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FormatPlainText(FormatterBase):
    def __init__(self, delta: DeltaType) -> None:
        super().__init__(delta)

    def format_delta_parts(self):
        from textwrap import dedent

        template_changes = """
        Change #{i}
        ---
        Added:   '{part_changed_b}'
        Removed: '{part_changed_a}'
        """

        formatted_strings = [
            dedent(template_changes).format(
                i=i, part_changed_a=pc[0], part_changed_b=pc[1]
            )
            for i, pc in enumerate(
                zip(
                    self.parts_changed_a,
                    self.parts_changed_b,
                ),
                start=1,
            )
        ]

        self.formatted_message = "\n".join(formatted_strings)

    def main(self) -> str:
        self.format_delta_parts()
        return self.formatted_message


class FormatPushoverHTML(FormatterBase):
    def __init__(self, delta: DeltaType) -> None:
        super().__init__(delta)

    def format_delta_parts(self):
        template_matched = "<font>{part_matched}</font>"
        template_all = (
            template_matched + '<font color="green">{part_changed_b}</font>'
            '<font color="grey"><strike>{part_changed_a}</strike></font>'
        )

        formatted_strings = [
            template_all.format(
                part_matched=pm, part_changed_a=pc_a, part_changed_b=pc_b
            )
            for pm, pc_a, pc_b in zip(
                self.parts_matched[:-1],
                self.parts_changed_a,
                self.parts_changed_b,
            )
        ] + [template_matched.format(part_matched=self.parts_matched[-1])]

        self.formatted_message = "".join(formatted_strings)

    def main(self) -> str:
        self.format_delta_parts()
        return self.formatted_message


class FormatColoredTerminalText(FormatterBase):
    def __init__(self, delta: DeltaType) -> None:
        super().__init__(delta)

    def format_delta_parts(self):

        from termcolor import colored

        template_matched = "{part_matched}"
        template_all = template_matched + "{part_changed_b}{part_changed_a}"

        formatted_strings = [
            template_all.format(
                part_matched=colored(pm, "white"),
                part_changed_a=colored(pc_a, "grey"),
                part_changed_b=colored(pc_b, "green"),
            )
            for pm, pc_a, pc_b in zip(
                self.parts_matched[:-1],
                self.parts_changed_a,
                self.parts_changed_b,
            )
        ] + [template_matched.format(part_matched=self.parts_matched[-1])]

        self.formatted_message = "".join(formatted_strings)

    def main(self) -> str:
        self.format_delta_parts()
        return self.formatted_message