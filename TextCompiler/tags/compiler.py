from __future__ import annotations

import re
from typing import TYPE_CHECKING, Dict, List, Type

from TextCompiler.tags.blocks.block import Block

if TYPE_CHECKING:
    from TextCompiler.tags.baseTag import BaseTag
    from TextCompiler.textCompiler import TextCompiler


class Compiler:
    """Class compiling output text of user defined tags
    """
    lt_gt_unescaped_regex = re.compile(r'(?:(?:\\\\|//)|(?<!\\|/))(?:[<>])')
    lt_gt_escaped_regex = re.compile(r'(?:\\|/)(?:[<>])')
    fix_lt_gt_text_regex = re.compile(r'&(?:gt|lt);', re.IGNORECASE)
    lt_gt_replacements = {
        '<': '&lt;',
        '>': '&gt;',
    }

    def __init__(
        self,
        init_blocks: List[Block] = None,
        parent: BaseTag = None
    ):
        """Initialize compiler

        Parameters
        ----------
        init_blocks : `List[Block]`, optional
            Initial blocks, by default `None`

        parent : `BaseTag`, optional
            `BaseTag` to which compiler belongs, by default `None`
        """
        self.blocks: List[Block] = []
        self.parent = parent
        if init_blocks and isinstance(init_blocks, list):
            self.blocks.extend(init_blocks)

    def append(self, val: Block):
        """Add new `Block`

        Parameters
        ----------
        val : `Block`
            `Block` to be added
        """
        self.blocks.append(val)

    def __call__(
            self,
            text: str,
            arguments: Dict[str, str]
    ) -> str:
        """Compile the content of the tag

        Parameters
        ----------
        text : `str`
            Text contained inside the tag
        arguments : `Dict[str, str]`
            Arguments passed to the tag

        Returns
        -------
        `str`
            Compiled text
        """
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
        """Create a copy of the compiler

        Returns
        -------
        `Compiler`
            New copy
        """
        return Compiler(self.blocks.copy(), self.parent)

    def copy(self) -> Compiler:
        """Create a copy of the compiler

        Returns
        -------
        `Compiler`
            New copy
        """
        return self.__copy__()

    def set_parent(self, parent: Type[BaseTag]):
        """Set the parent of the compiler

        Parameters
        ----------
        parent : `Type[BaseTag]`
            Parent of the compiler
        """
        self.parent = parent

    @classmethod
    def escape_lt_gt(cls, text: str) -> str:
        """Escape '<' and '>'

        Parameters
        ----------
        text : `str`
            Text to process

        Returns
        -------
        `str`
            Processed text
        """
        return cls.lt_gt_unescaped_regex.sub(lambda x: f'/{x.group(0)}', text)

    @classmethod
    def replace_unescaped_lt_gt(cls, match: re.Match) -> str:
        """Replace unescaped '<' and '>' with '&gt;' and '&lt;'

        Parameters
        ----------
        match : `re.Match`

        Returns
        -------
        `str`
        """
        text = match.group(0)
        out_sign = cls.lt_gt_replacements[text[-1]]
        return text[:2] + out_sign

    @staticmethod
    def replace_escaped_lt_gt(match: re.Match) -> str:
        """Unescape escaped '<' and '>'

        Parameters
        ----------
        match : `re.Match`

        Returns
        -------
        `str`
        """
        return match.group(0)[-1]
