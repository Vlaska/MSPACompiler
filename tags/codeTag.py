from typing import Dict

from tags.innerBlock import InnerBlock


class CodeTag(InnerBlock):
    def __init__(self, argumentName: str, textFormat: str):
        self.argumentName = argumentName
        self.textFormat = textFormat

    def __call__(self, text: str, arguments: Dict[str, str], codes) -> str:
        if not (
                self.argumentName in arguments and
                (t := arguments[self.argumentName]).isdecimal()
        ):
            return text

        idx = int(t)
        if not (0 < idx < len(codes)):
            idx = 0
        t = text.format(**arguments, text=text).encode('utf-8')
        return codes[idx](t)
