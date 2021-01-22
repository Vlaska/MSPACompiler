from __future__ import annotations
import logging

from typing import TYPE_CHECKING, Dict, List, Type

from MSPACompiler.lua import Lua
from MSPACompiler.tags.blocks.block import Block
from MSPACompiler.tags.compiler import Compiler

from loguru import logger

if TYPE_CHECKING:
    from MSPACompiler.textCompiler import TextCompiler


class BaseTag:
    """Base class from which all user defined tags inherit from.

    Raises
    ------
    e
        Exception raised, when:

            - user defined code throws an error
            - placeholder defined in text contains Python keyword
    """

    compiler: Compiler = Compiler([Block(
        is_safe=True,
        split_lines=False,
        strip_whitespaces=False,
        initial_data=['{text}']
    )])
    tag_name: str = ''
    arguments: Dict[str, str] = {}
    is_safe: bool = True

    tags: Dict[str, Type[BaseTag]] = {}
    css: Dict[str, str] = {}
    codes = [lambda x: x.decode('utf-8'), ]
    lua = Lua()
    lua_scope = lua.create_scope()

    @classmethod
    def compile(cls, data: Dict[str, str]) -> List[str]:
        """Compile content of a user defined tag

        Parameters
        ----------
        data : `Dict[str, str]`
            Data contained inside the tag

        Returns
        -------
        `List[str]`
            List of strings compiled from the content of tag

        Raises
        ------
        e
            Exception raised, when user defined code throws an error
        """
        text = data['content']
        args = cls.processArgs(data['args'])
        try:
            return [cls.compiler(i or '', args) for i in text]
        except Exception as e:
            logger.error(
                'There was an error while compiling content of '
                f'"{cls.tag_name}" tag'
            )
            raise e

    @classmethod
    def processArgs(cls, args: Dict[str, str]) -> Dict[str, str]:
        """Combine arguments (with their default values) passed on the creation
        of tag, with arguments passed on when tag was used.

        Parameters
        ----------
        args : `Dict[str, str]`
            Arguments passed when tag was called

        Returns
        -------
        `Dict[str, str]`
            Processed arguments
        """
        out = cls.arguments.copy()
        for i in args:
            out.update(i)
        out['tag_name'] = cls.tag_name
        return out

    @classmethod
    def new_instance(cls, parser: TextCompiler) -> Type[BaseTag]:
        """Create new instance of base tag. When creating new tags, it will be
        used as their base.

        Parameters
        ----------
        parser : `TextCompiler`
            Text compiler to which `BaseTag` instance belongs.

        Returns
        -------
        `Type[BaseTag]`
            New instance of `BaseTag`
        """
        t: Type[BaseTag] = type('BaseTag', (BaseTag, ), {
            'compiler': cls.compiler.copy(),
            'arguments': {},
            'tags': {},
            'codes': [lambda x: x.decode('utf-8'), ],
            'parser': parser,
            'css': {}
        })
        t.compiler.set_parent(t)
        return t

    @classmethod
    def compile_css(cls) -> str:
        """Method to compile css contained in tag

        Returns
        -------
        `str`
            Compiled css
        """
        out = []
        for k, v in cls.css.items():
            out.append(f'.{cls.tag_name}{k} {{{v}}}')
        return '\n'.join(out)


if not BaseTag.compiler.parent:
    BaseTag.compiler.parent = BaseTag
