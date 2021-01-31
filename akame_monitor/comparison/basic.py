import logging
from difflib import SequenceMatcher, Match
from os import stat

from .core import ComparerBase

from typing import List, Dict, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BasicComparer(ComparerBase):
    def __init__(self) -> None:
        super().__init__()
        self.content_changes: str = ""

    def get_matches(self) -> List[Match]:
        matcher = SequenceMatcher(None, self.content_0, self.content_1)
        return matcher.get_matching_blocks()

    @staticmethod
    def get_content_positions_for_x(
        matches: List[Match], x: str
    ) -> Dict[str, List[Tuple[int, int]]]:
        matched_start = [getattr(match, x) for match in matches]
        matched_end = [(getattr(match, x) + match.size) for match in matches]

        matched_positions = [
            (start, end) for start, end in zip(matched_start, matched_end)
        ]

        changed_positions = [
            (end + 1, start - 1)
            for end, start in zip(matched_end[:-1], matched_start[1:])
        ]

        return {"matched": matched_positions, "changed": changed_positions}

    def get_content_positions(
        self, matches: List[Match]
    ) -> Dict[str, Dict[str, List[Tuple[int, int]]]]:
        return {
            x: self.get_content_positions_for_x(matches=matches, x=x)
            for x in ("a", "b")
        }

    def get_parts_unchanged(self, a_matched: List[Tuple[int, int]]) -> List[str]:
        return [self.content_0[pos[0] : pos[1]] for pos in a_matched]

    def get_parts_changed_in_content_0(
        self, a_changed: List[Tuple[int, int]]
    ) -> List[str]:
        return [self.content_0[pos[0] : pos[1]] for pos in a_changed]

    def get_parts_changed_in_content_1(
        self, b_changed: List[Tuple[int, int]]
    ) -> List[str]:
        return [self.content_1[pos[0] : pos[1]] for pos in b_changed]

    def get_diff_parts(self) -> Tuple[List[str], List[str], List[str]]:
        matches = self.get_matches()
        content_positions = self.get_content_positions(matches)
        parts_unchanged = self.get_parts_unchanged(
            a_matched=content_positions["a"]["matched"]
        )
        parts_changed_0 = self.get_parts_changed_in_content_0(
            a_changed=content_positions["a"]["changed"]
        )
        parts_changed_1 = self.get_parts_changed_in_content_1(
            b_changed=content_positions["b"]["changed"]
        )
        return (parts_unchanged, parts_changed_0, parts_changed_1)

    @staticmethod
    def convert_diff_parts_to_html(
        parts_unchanged: List[str],
        parts_changed_0: List[str],
        parts_changed_1: List[str],
    ) -> str:
        format_unchanged = "<font>{part_unchanged}</font>"
        format_template = (
            format_unchanged + '<font color="green">{part_changed_1}</font>'
            '<font color="grey"><strike>{part_changed_0}</strike></font>'
        )

        formatted_strings = [
            format_template.format(
                part_unchanged=pu, part_changed_0=pc0, part_changed_1=pc1
            )
            for pu, pc0, pc1 in zip(
                parts_unchanged[:-1], parts_changed_0, parts_changed_1
            )
        ] + [format_unchanged.format(part_unchanged=parts_unchanged[-1])]

        return "".join(formatted_strings)

    def load_content_changes(self) -> None:
        if self.comparison_status == 1:
            parts_unchanged, parts_changed_0, parts_changed_1 = self.get_diff_parts()
            self.content_changes = self.convert_diff_parts_to_html(
                parts_unchanged, parts_changed_0, parts_changed_1
            )

    def express_comparison_results(self) -> None:
        self.load_content_changes()

        if self.comparison_status is None:
            self.status_code = -1
            self.message = "INITIATED"
        elif not self.comparison_status:
            self.status_code = 0
            self.message = "UNCHANGED"
        else:
            self.status_code = 1
            message_header = "<b>CHANGES DETECTED</b>"
            message_changes = self.content_changes
            self.message = f"{message_header}\n\n{message_changes}"
