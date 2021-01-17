from __future__ import annotations

from typing import List, Type, Dict, Union

from .tags import BaseTag, Defines
from .tags.textBlocks import TextBlocks
from .inputStringParser import parse as inputStrToAst
from sys import stderr


class TextCompiler:
    '''This class is an entrypoint to the compiler'''

    def __init__(self, tag_definitions: str = ''):
        """Initialize compiler

        Parameters
        ----------
        tag_definitions : str, optional
            Initial language tags. They will be present in all text blocks
            created after loading then in, by default ''
        """
        self.baseTag = BaseTag.newClassInstance(self)
        if tag_definitions:
            self.load_tags(tag_definitions)

    def load_tags(self, tag_definitions: str):
        """Load new tag definitions.

        After loaded, they will be available in all newly created blocks.

        Parameters
        ----------
        tag_definitions : str
            String containing tag definitions.
        """
        self.process_text(tag_definitions, False)

    def process_text(
            self,
            text: Union[str, list],
            use_tmp_tags: bool | Dict[str, Type[BaseTag]] = True
    ) -> str:
        tmp_tags = {} if use_tmp_tags else None
        ast: list = inputStrToAst(text)
        return self.__process_ast(ast, tmp_tags)

    def __process_ast(
            self,
            ast: List,
            tmp_tags: Dict[str, Type[BaseTag]]
    ) -> str:
        out = []

        for i in ast:
            if type(i) is dict:
                name = i['name']
                nameLower = name.lower()
                if nameLower == 'defines':
                    Defines.parse(i, self.baseTag, tmp_tags)
                else:
                    if tmp_tags is not None and nameLower in tmp_tags:
                        tag = tmp_tags.get(nameLower)
                    else:
                        tag = self.baseTag.tags.get(nameLower)

                    if tag is None:
                        print(f'Unknown tag: {name}', file=stderr)  # ERROR LOG
                        continue

                    i['content'] = [
                        self.__process_ast(i['content'], tmp_tags)
                    ]

                    t = tag.parse(i)
                    if t:
                        out.extend(t)
            elif i:
                out.append(i)

        return ''.join(out)

    def compile(self, text: str) -> str:
        """Compile input text

        Parameters
        ----------
        text : str
            Text to be compiled

        Returns
        -------
        str
            Resulting text
        """
        text = self.process_text(text).strip()
        return TextBlocks.ltGtEscapedRegex.sub(
            TextBlocks.replaceEscapedLtGt,
            text
        )

    def compile_css(self) -> str:
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

        compile(self.baseTag.tags)

        return '\n'.join(out)
