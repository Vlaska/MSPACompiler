from __future__ import annotations

from typing import Type, Dict, Union

from .tags import BaseTag, Defines
from .inputStringParser import parse as inputStrToAst
from sys import stderr


class TextParser:
    def __init__(self, initConfig: str):
        self.baseTag = BaseTag.newClassInstance(self)
        self.innerParse(initConfig, self.baseTag)
        self.tempTags = {}

    @staticmethod
    def innerParse(
            text: Union[str, list],
            baseTag: Type[BaseTag],
            tempTags: Dict[str, Type[BaseTag]] = None
    ) -> str:
        out = []
        if type(text) is str:
            text: list = inputStrToAst(text)
        useTempTags = tempTags is not None
        for i in text:
            if type(i) is dict:
                name = i['name']
                nameLower = name.lower()
                if nameLower == 'defines':
                    Defines.parse(i, baseTag, tempTags)
                else:
                    if useTempTags and nameLower in tempTags:
                        tag = tempTags.get(nameLower)
                    else:
                        tag = baseTag.tags.get(nameLower)

                    if tag is None:
                        print(f'Unknown tag: {name}', file=stderr)  # ERROR LOG
                        continue

                    i['content'] = [
                        TextParser.innerParse(i['content'], baseTag)
                    ]

                    t = tag.parse(i)
                    if t:
                        out.extend(t)
            elif i:
                out.append(i)
        return ''.join(out)

    def parse(self, text: str) -> str:
        return self.innerParse(text, self.baseTag, self.tempTags).strip()
    
    def resetTempTags(self):
        self.tempTags = {}

    def compileCSS(self) -> str:
        out = []
        used = set()
        
        def compile(t: dict):
            for i in t.values():
                if i in used:
                    continue
                used.add(i)
                v = i.compileCSS()
                if v:
                    out.append(v)

        compile(self.tempTags)
        compile(self.baseTag.tags)

        return '\n'.join(out)
