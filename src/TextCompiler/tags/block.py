from __future__ import annotations

from typing import Union, Type, List, Tuple, Dict
import re

from src.TextCompiler.tags import InnerBlock
from src.TextCompiler.tags.ifTags import IfTag


class Block:
    def __init__(
            self,
            isSafe: bool,
            splitLines: bool,
            stripWhitespaces: bool,
            # ignoreWhitespaces: bool,
            initialData: List[Union[str, Type[InnerBlock]]] = None
    ):
        self.isSafe = isSafe
        self.splitLines = splitLines
        self.stripWhitespaces = stripWhitespaces
        # self.ignoreWhitespaces = ignoreWhitespaces
        self.blocks = []
        self.replace: List[Tuple[str, str]] = []
        if initialData:
            self.blocks.extend(initialData)

    def add(self, element: Union[str, Type[InnerBlock]]):
        self.blocks.append(element)

    def addReplacements(self, data: List[Tuple[str, str]]):
        self.replace.extend(data)

    def __call__(
            self,
            text: str,
            arguments: Dict[str, str],
            parent: BaseTag
    ) -> str:
        # if self.ignoreWhitespaces and text.isspace():
        #     return ''

        out = []
        template = []
        templateString = ''
        inputText = text.splitlines() if self.splitLines else [text]

        for i in self.blocks:
            if type(i) is str:
                templateString += i
            elif isinstance(i, (IfTag)):
                templateString += i(arguments)
            else:
                if templateString:
                    template.append(templateString)
                    templateString = ''
                template.append(i)

        if templateString:
            template.append(templateString)

        for i in inputText:
            result = ''
            for j in template:
                if type(j) is str:
                    result += j
                else:
                    result += j(i, arguments, parent.codes)

            if result:
                result = result.format(**arguments, text=i)
                out.append(result)

        result = '\n'.join(out)
        for i in self.replace:
            result = result.replace(*i)

        if self.stripWhitespaces:
            result = re.sub(r' +', ' ', result)
            result = re.sub(r'\n+', '\n', result)
            result = re.sub(r'\t+', '\t', result)
            result = re.sub(r'\r+', '\r', result)
            result = re.sub(r'\f+', '\f', result)
            result = re.sub(r'\v+', '\v', result)

        return result
