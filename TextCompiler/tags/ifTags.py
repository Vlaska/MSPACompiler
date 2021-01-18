from typing import Dict

from .innerBlock import InnerBlock


class IfTag(InnerBlock):
    def __init__(self, argName: str, retVal: str = None):
        super().__init__()
        self.argName = argName
        self.retVal = retVal

    def __call__(self, arguments: Dict[str, str]) -> str:
        return self.retVal \
            if (self.argName in arguments and arguments[self.argName]) else ''


class IfNotTag(IfTag):
    def __call__(self, arguments: Dict[str, str]):
        return self.retVal \
            if not(self.argName in arguments and arguments[self.argName]) \
            else ''
