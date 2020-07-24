from __future__ import annotations

from typing import Iterable, List
import re

from .utils import fixSquareBrackets
from .block import Block


class TextBlocks:
    ltGtNotEscapedRegex = re.compile(r'(?<!\\|/)(?:[<>])')
    ltGtEscapedRegex = re.compile(r'(?:\\|/)(?:[<>])')

    def __init__(self, initBlocks: List[Block] = None, parent = None):
        self.blocks: List[Block] = []
        self.parent = parent
        if initBlocks and isinstance(initBlocks, (list, tuple)):
            self.blocks.extend(initBlocks)
    
    def append(self, val: Block):
        self.blocks.append(val)
    
    def extend(self, vals: Iterable[Block]):
        self.blocks.extend(vals)

    def __call__(self, text: str, arguments: Dict[str, str]) -> str:
        for i in self.blocks[::-1]:
            if i.isSafe:
                text = self.escapeLtGt(text)
            else:
                text = self.ltGtNotEscapedRegex.sub(self.replaceEscapedLtGt, text)
            text = i(text, arguments, self.parent)

        text = self.ltGtNotEscapedRegex.sub(self.replaceEscapedLtGt, text)
        text = self.ltGtEscapedRegex.sub(self.replaceEscapedLtGt, text)

        # return fixSquareBrackets(text)
        return text

    def __copy__(self) -> TextBlocks:
        return TextBlocks(self.blocks.copy(), self.parent)
    
    def copy(self) -> TextBlocks:
        return self.__copy__()
    
    def setParent(self, parent):
        self.parent = parent

    @classmethod
    def escapeLtGt(cls, text: str):
        return cls.ltGtNotEscapedRegex.sub(lambda x: f'/{x.group(0)}', text)

    @staticmethod
    def replaceUnescapedLtGt(match: re.Match) -> str:
        if match.group(0) == '<':
            return '&lt;'
        return '&gt;'

    @staticmethod
    def replaceEscapedLtGt(match: re.Match) -> str:
        return match.group(0)[-1]
