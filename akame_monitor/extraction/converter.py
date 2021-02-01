import json


def convert_json_to_dict(text: str):
    """Function that converts JSON to dictionary

    Args:
        text (str): text to be processed

    Returns:
        str: processed text
    """
    return json.loads(text)


class JSONString:
    """Class that handles conversion of JSON strings

    Args:
        text (str): text to be processed
    """

    def __init__(self, text: str) -> None:
        self.text = text

    def load_text_in_dict(self) -> None:
        self.text_in_dict = convert_json_to_dict(self.text)
