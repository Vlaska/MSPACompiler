from __future__ import annotations

from typing import TYPE_CHECKING, Union, Type, List, Tuple, Dict
import re

from TextCompiler.tags.blocks.innerBlock import InnerBlock
from TextCompiler.tags.blocks.ifBlocks import IfBlock

if TYPE_CHECKING:
    from TextCompiler.tags import BaseTag


class Block:
    def __init__(
            self,
            is_safe: bool,
            split_lines: bool,
            strip_whitespaces: bool,
            initial_data: List[Union[str, Type[InnerBlock]]] = None,
            ifNoText: str = ''
    ):
        self.is_safe = is_safe
        self.split_lines = split_lines
        self.strip_whitespaces = strip_whitespaces
        self.blocks = []
        self.replace: List[Tuple[str, str]] = []
        self.if_no_text = ifNoText
        if initial_data:
            self.blocks.extend(initial_data)

    def add(self, element: Union[str, Type[InnerBlock]]):
        self.blocks.append(element)

    def add_replacements(self, data: List[Tuple[str, str]]):
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
    def __compile(input_text, template, arguments, parent):
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

    def __compile_template(self, arguments):
        template = []
        template_string = ''

        for i in self.blocks:
            if type(i) is str:
                template_string += i
            elif isinstance(i, IfBlock):
                template_string += i(arguments)
            else:
                # if templateString:
                #     template.append(templateString)
                #     templateString = ''
                template.append(i)

        if template_string:
            template.append(template_string)

        return template

    @staticmethod
    def __strip_whitespaces(result):
        result = re.sub(r' +', ' ', result)
        result = re.sub(r'\n+', '\n', result)
        result = re.sub(r'\t+', '\t', result)
        result = re.sub(r'\r+', '\r', result)
        result = re.sub(r'\f+', '\f', result)
        result = re.sub(r'\v+', '\v', result)
        return result
