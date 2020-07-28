from __future__ import annotations

from typing import Iterable, List, Union
import re

from .block import Block


class TextBlocks:
    ltGtUnescapedRegex = re.compile(r'(?:(?:\\\\|//)|(?<!\\|/))(?:[<>])')
    ltGtEscapedRegex = re.compile(r'(?:\\|/)(?:[<>])')
    fixLtGtTextRegex = re.compile(r'&(?:gt|lt);', re.IGNORECASE)
    ltGtReplacements = {
        '<': '&lt;',
        '>': '&gt;',
    }

    def __init__(self, initBlocks: List[Block] = None, parent=None):
        self.blocks: List[Block] = []
        self.parent = parent
        if initBlocks and isinstance(initBlocks, (list, tuple)):
            self.blocks.extend(initBlocks)

    def append(self, val: Block):
        self.blocks.append(val)

    def extend(self, vals: Iterable[Block]):
        self.blocks.extend(vals)

    def __call__(
            self,
            text: str,
            arguments: Dict[str, str],
            parser: TextParser
    ) -> str:
        for i in self.blocks[::-1]:
            if i.isSafe:
                text = self.escapeLtGt(text)
            else:
                text = self.ltGtUnescapedRegex.sub(
                    self.replaceUnescapedLtGt, text)
            text = i(text, arguments, self.parent)

        text = self.ltGtUnescapedRegex.sub(self.replaceUnescapedLtGt, text)
        text = self.ltGtEscapedRegex.sub(self.replaceEscapedLtGt, text)
        text = self.fixLtGtTextRegex.sub(lambda x: x.group(0).lower(), text)

        return text

    def __copy__(self) -> TextBlocks:
        return TextBlocks(self.blocks.copy(), self.parent)

    def copy(self) -> TextBlocks:
        return self.__copy__()

    def setParent(self, parent):
        self.parent = parent

    @classmethod
    def escapeLtGt(cls, text: str):
        return cls.ltGtUnescapedRegex.sub(lambda x: f'/{x.group(0)}', text)

    @classmethod
    def replaceUnescapedLtGt(cls, match: re.Match) -> str:
        text = match.group(0)
        outSign = cls.ltGtReplacements[text[-1]]
        if len(text) == 3:
            return text[:2] + outSign
        return outSign

    @staticmethod
    def replaceEscapedLtGt(match: re.Match) -> str:
        return match.group(0)[-1]
