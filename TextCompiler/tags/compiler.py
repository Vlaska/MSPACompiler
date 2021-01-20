from __future__ import annotations

import re
from typing import TYPE_CHECKING, Dict, List

from TextCompiler.tags.blocks.block import Block

if TYPE_CHECKING:
    from ..textParser import TextCompiler


class Compiler:
    lt_gt_unescaped_regex = re.compile(r'(?:(?:\\\\|//)|(?<!\\|/))(?:[<>])')
    lt_gt_escaped_regex = re.compile(r'(?:\\|/)(?:[<>])')
    fix_lt_gt_text_regex = re.compile(r'&(?:gt|lt);', re.IGNORECASE)
    lt_gt_replacements = {
        '<': '&lt;',
        '>': '&gt;',
    }

    def __init__(self, init_blocks: List[Block] = None, parent=None):
        self.blocks: List[Block] = []
        self.parent = parent
        if init_blocks and isinstance(init_blocks, list):
            self.blocks.extend(init_blocks)

    def append(self, val: Block):
        self.blocks.append(val)

    def __call__(
            self,
            text: str,
            arguments: Dict[str, str],
            parser: TextCompiler
    ) -> str:
        for i in self.blocks[::-1]:
            if i.is_safe:
                text = self.escape_lt_gt(text)
            else:
                text = self.lt_gt_unescaped_regex.sub(
                    self.replace_unescaped_lt_gt,
                    text
                )
            text = i(text, arguments, self.parent)

        text = self.lt_gt_unescaped_regex.sub(
            self.replace_unescaped_lt_gt, text)
        text = self.fix_lt_gt_text_regex.sub(
            lambda x: x.group(0).lower(), text)

        return text

    def __copy__(self) -> Compiler:
        return Compiler(self.blocks.copy(), self.parent)

    def copy(self) -> Compiler:
        return self.__copy__()

    def set_parent(self, parent):
        self.parent = parent

    @classmethod
    def escape_lt_gt(cls, text: str):
        return cls.lt_gt_unescaped_regex.sub(lambda x: f'/{x.group(0)}', text)

    @classmethod
    def replace_unescaped_lt_gt(cls, match: re.Match) -> str:
        text = match.group(0)
        out_sign = cls.lt_gt_replacements[text[-1]]
        return text[:2] + out_sign

    @staticmethod
    def replace_escaped_lt_gt(match: re.Match) -> str:
        return match.group(0)[-1]
