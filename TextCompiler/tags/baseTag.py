from __future__ import annotations

from typing import Dict, Type, TYPE_CHECKING

from .block import Block
from .textBlocks import TextBlocks
from .luaExec import Lua

if TYPE_CHECKING:
    from ..textParser import TextCompiler


class BaseTag:
    textBlocks = TextBlocks([Block(
        True,
        False,
        False,
        ['{text}']
    )])
    tag_name = ''
    arguments = {}
    wasBuild = True
    isSafe = True

    tags: Dict[str, Type[BaseTag]] = {}
    css: Dict[str, str] = {}
    codes = [lambda x: x.decode('utf-8'), ]
    lua = Lua()
    luaScope = lua.createScope()
    parser = None

    @classmethod
    def parse(cls, data: Dict[str, str]) -> str:
        text = data['content']
        args = cls.processArgs(data['args'])
        try:
            return [cls.textBlocks(i or '', args, cls.parser) for i in text]
        except Exception as e:
            print(cls.tag_name)
            raise e

    @classmethod
    def processArgs(cls, args):
        out = cls.arguments.copy()
        for i in args:
            out.update(i)
        out['tag_name'] = cls.tag_name
        return out

    @classmethod
    def newClassInstance(cls, parser: TextCompiler) -> Type[BaseTag]:
        t: Type[BaseTag] = type('BaseTag', (BaseTag, ), {
            'textBlocks': cls.textBlocks.copy(),
            'arguments': {},
            'tags': {},
            'codes': [lambda x: x.decode('utf-8'), ],
            'parser': parser,
            'css': {}
        })
        t.textBlocks.setParent(t)
        return t

    @classmethod
    def compileCSS(cls) -> str:
        out = []
        for k, v in cls.css.items():
            out.append(f'.{cls.tag_name}{k} {{{v}}}')
        return '\n'.join(out)


if not BaseTag.textBlocks.parent:
    BaseTag.textBlocks.parent = BaseTag
