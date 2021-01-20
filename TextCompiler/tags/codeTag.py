from typing import Dict

from .innerBlock import InnerBlock


class CodeTag(InnerBlock):
    def __init__(self, argument_name: str, text_format: str):
        self.argument_name = argument_name
        self.text_format = text_format

    def __call__(self, text: str, arguments: Dict[str, str], codes) -> str:
        if not (
                self.argument_name in arguments and
                (t := arguments[self.argument_name]).isdecimal()
        ):
            return text

        idx = int(t)
        if not (0 < idx < len(codes)):
            idx = 0
        t = text.format(**arguments, text=text).encode('utf-8')
        return codes[idx](t)
