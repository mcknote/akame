import logging
from difflib import Match, SequenceMatcher
from typing import Dict, List, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StringDelta:
    """Class that compares two strings and formats the delta

    Args:
        a (str): String a to compare
        b (str): String b to compare
    """

    def __init__(self, a: str, b: str) -> None:
        self.a = a
        self.b = b

        self.load_matches()
        self.load_content_positions()
        self.load_all_delta_parts()

    def load_matches(self) -> None:
        """Function that initiates SequenceMatcher and matches"""
        self.matcher = SequenceMatcher(None, self.a, self.b)
        self.matches = self.matcher.get_matching_blocks()

    def get_content_positions_for_x(
        self, x: str
    ) -> Dict[str, List[Tuple[int, int]]]:
        """Function that gets the string postions from the matches

        Args:
            x (str): String to access, 'a' or 'b'

        Returns:
            Dict[str, List[Tuple[int, int]]]: Positions in under two parts,
                `matched` and `changed`
        """
        matched_start = [getattr(match, x) for match in self.matches]
        matched_end = [
            (getattr(match, x) + match.size) for match in self.matches
        ]

        matched_positions = [
            (start, end) for start, end in zip(matched_start, matched_end)
        ]
        changed_positions = [
            (end, start)
            for end, start in zip(matched_end[:-1], matched_start[1:])
        ]

        return {"matched": matched_positions, "changed": changed_positions}

    def load_content_positions(self) -> None:
        self.content_positions = {
            x: self.get_content_positions_for_x(x) for x in ("a", "b")
        }

    def load_all_delta_parts(self) -> None:
        self.load_parts_matched()
        self.load_parts_changed_a()
        self.load_parts_changed_b()

    def load_parts_matched(self) -> None:
        a_matched = self.content_positions["a"]["matched"]
        self.parts_matched = [self.a[pos[0] : pos[1]] for pos in a_matched]

    def load_parts_changed_a(self) -> None:
        a_changed = self.content_positions["a"]["changed"]
        self.parts_changed_a = [self.a[pos[0] : pos[1]] for pos in a_changed]

    def load_parts_changed_b(self) -> None:
        b_changed = self.content_positions["b"]["changed"]
        self.parts_changed_b = [self.b[pos[0] : pos[1]] for pos in b_changed]

    def get_delta_parts(self) -> Tuple[List[str], List[str], List[str]]:
        logger.info("Returning all delta parts in lists")
        return (self.parts_matched, self.parts_changed_a, self.parts_changed_b)

    def get_delta_in_html(self) -> str:
        logger.info("Formatting delta in HTML")
        template_matched = "<font>{part_matched}</font>"
        template_all = (
            template_matched + '<font color="green">{part_changed_a}</font>'
            '<font color="grey"><strike>{part_changed_b}</strike></font>'
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

        return "".join(formatted_strings)
