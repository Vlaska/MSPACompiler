from __future__ import annotations

from typing import Union, Type, List, Tuple, Dict

from tags.innerBlock import InnerBlock
from tags.ifTags import IfTag, IfNotTag


class Block:
    def __init__(
            self,
            isSafe: bool,
            splitLines: bool,
            initialData: List[Union[str, Type[InnerBlock]]] = None
    ):
        self.isSafe = isSafe
        self.splitLines = splitLines
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
                result = result.format(**arguments, text=text)
                out.append(result)

        result = '\n'.join(out)
        for i in self.replace:
            result = result.replace(*i)

        return result
