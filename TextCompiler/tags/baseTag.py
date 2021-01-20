from __future__ import annotations

from typing import Dict, Type, TYPE_CHECKING

from .block import Block
from .textBlocks import TextBlocks
from .luaExec import Lua

if TYPE_CHECKING:
    from ..textParser import TextCompiler


class BaseTag:
    text_blocks = TextBlocks([Block(
        is_safe=True,
        split_lines=False,
        strip_whitespaces=False,
        initial_data=['{text}']
    )])
    tag_name = ''
    arguments = {}
    is_safe = True

    tags: Dict[str, Type[BaseTag]] = {}
    css: Dict[str, str] = {}
    codes = [lambda x: x.decode('utf-8'), ]
    lua = Lua()
    lua_scope = lua.createScope()
    parser = None

    @classmethod
    def parse(cls, data: Dict[str, str]) -> str:
        text = data['content']
        args = cls.processArgs(data['args'])
        try:
            return [cls.text_blocks(i or '', args, cls.parser) for i in text]
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
    def new_instance(cls, parser: TextCompiler) -> Type[BaseTag]:
        t: Type[BaseTag] = type('BaseTag', (BaseTag, ), {
            'textBlocks': cls.text_blocks.copy(),
            'arguments': {},
            'tags': {},
            'codes': [lambda x: x.decode('utf-8'), ],
            'parser': parser,
            'css': {}
        })
        t.text_blocks.set_parent(t)
        return t

    @classmethod
    def compile_css(cls) -> str:
        out = []
        for k, v in cls.css.items():
            out.append(f'.{cls.tag_name}{k} {{{v}}}')
        return '\n'.join(out)


if not BaseTag.text_blocks.parent:
    BaseTag.text_blocks.parent = BaseTag
