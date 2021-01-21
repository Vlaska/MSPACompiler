from __future__ import annotations

from typing import TYPE_CHECKING, Union, Type, List, Tuple, Dict
import re

from TextCompiler.tags.blocks.innerBlock import InnerBlock
from TextCompiler.tags.blocks.ifBlocks import IfBlock

if TYPE_CHECKING:
    from TextCompiler.tags import BaseTag
    from TextCompiler.tags.blocks.codeBlock import CodeBlock


class Block:
    def __init__(
            self,
            is_safe: bool,
            split_lines: bool,
            strip_whitespaces: bool,
            initial_data: List[Union[str, Type[InnerBlock]]] = None,
            ifNoText: str = ''
    ):
        """Initialize `Block`

        Parameters
        ----------
        is_safe : `bool`
            Whether to convert unescaped '<' and '>' to their '&gt;' and '&lt;'

        split_lines : `bool`
            Process each line separately

        strip_whitespaces : `bool`
            Remove trailing whitespaces

        initial_data : `List[Union[str, Type[InnerBlock]]]`, optional
            Initial segments, by default `None`

        ifNoText : `str`, optional
            Text to be used if tag contains no text, by default `''`
        """
        self.is_safe = is_safe
        self.split_lines = split_lines
        self.strip_whitespaces = strip_whitespaces
        self.segments = []
        self.replace: List[Tuple[str, str]] = []
        self.if_no_text = ifNoText
        if initial_data:
            self.segments.extend(initial_data)

    def add(self, element: Union[str, Type[InnerBlock]]):
        """Add new text segments to template processing

        Parameters
        ----------
        element : `Union[str, Type[InnerBlock]]`
            Segments to be added
        """
        self.segments.append(element)

    def add_replacements(self, data: List[Tuple[str, str]]):
        """Add text which has to be replaced e.g. "\\n" for "<br/>"

        Parameters
        ----------
        data : `List[Tuple[str, str]]`
            List of pairs containing old and new value
        """
        self.replace.extend(data)

    def __call__(
            self,
            text: str,
            arguments: Dict[str, str],
            parent: BaseTag
    ) -> str:
        if not text and self.if_no_text:
            text = self.if_no_text.format(**arguments)

        inputText = text.splitlines() if self.split_lines else [text]

        template = self.__compile_template(arguments)

        result = self.__compile(inputText, template, arguments, parent)

        for i in self.replace:
            result = result.replace(*i)

        if self.strip_whitespaces:
            result = self.__strip_whitespaces(result)

        return result

    @staticmethod
    def __compile(
        input_text: List[str],
        template: List[Union[str, CodeBlock]],
        arguments: Dict[str, str],
        parent: BaseTag
    ):
        """Insert each input string into initialy processed segments and join
        them

        Parameters
        ----------
        input_text : `List[str]`
            List of input string
        template : `List[Union[str, CodeBlock]]`
            Initialy processed segments
        arguments : `Dict[str, str]`
            Tags arguments
        parent : `BaseTag`
            `BaseTag` by which tag is processed

        Returns
        -------
        `str`
            Compiled string
        """
        out = []
        for i in input_text:
            result = ''
            for j in template:
                if type(j) is str:
                    result += j
                else:
                    result += j(i, arguments, parent.codes)

            if result:
                result = result.format(**arguments, text=i)
                out.append(result)
        return '\n'.join(out)

    def __compile_template(self, arguments) -> List[Union[str, CodeBlock]]:
        """Iterate over defined text segments and initially process them
        (concatinate strings, evaluate `if` blocks)

        Parameters
        ----------
        arguments : `Dict[str, str]`
            Tags arguments

        Returns
        -------
        `List[Union[str, CodeBlock]]`
            Initialy processed text segments
        """
        template = []
        template_string = ''

        for i in self.segments:
            if type(i) is str:
                template_string += i
            elif isinstance(i, IfBlock):
                template_string += i(arguments)
            else:
                if template_string:
                    template.append(template_string)
                    template_string = ''
                template.append(i)

        if template_string:
            template.append(template_string)

        return template

    @staticmethod
    def __strip_whitespaces(result: str) -> str:
        """Replace the series of whitespaces with single whitespace

        Parameters
        ----------
        result : `str`
            Input string

        Returns
        -------
        `str`
            String without repeating whitespaces
        """
        result = re.sub(r' +', ' ', result)
        result = re.sub(r'\n+', '\n', result)
        result = re.sub(r'\t+', '\t', result)
        result = re.sub(r'\r+', '\r', result)
        result = re.sub(r'\f+', '\f', result)
        result = re.sub(r'\v+', '\v', result)
        return result
