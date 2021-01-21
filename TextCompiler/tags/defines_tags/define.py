from __future__ import annotations

from typing import Callable, Dict, List, Type, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from TextCompiler.tags.blocks.innerBlock import InnerBlock
    from TextCompiler.tags.baseTag import BaseTag
    from TextCompiler.lua import Lua, LuaTable

from TextCompiler.tags.blocks.block import Block
from TextCompiler.tags.blocks.codeBlock import CodeBlock
from TextCompiler.tags.blocks.ifBlocks import IfBlock, IfNotBlock


class Define:
    """Create new tag
    """
    tag_name = 'define'
    allowed_blocks = {
        'if': IfBlock,
        'ifnot': IfNotBlock,
        'code': CodeBlock,
    }

    @classmethod
    def process(
            cls,
            data: Dict,
            base_tag: Type[BaseTag],
            temp_tags: Dict[str, Type[BaseTag]] = None
    ) -> Type[BaseTag]:
        """Create new tag

        Parameters
        ----------
        data : `Dict`
            Arguments and content passed to `define` tag

        base_tag : `Type[BaseTag]`
            Base tag stored in `TextCompiler`

        temp_tags : `Dict[str, Type[BaseTag]]`, optional
            If new tag is temporary, place it inside of `temp_tags`,
            by default `None`

        Returns
        -------
        `Type[BaseTag]`
            New tag
        """
        args = data['args']

        if len(args) < 1:
            return
        elif len(args) < 3:
            missing_args = 3 - len(args)
            for _ in range(missing_args):
                args.append({})

        tag_name = list(args[0].keys())[0].lower()
        tag_arguments = {k.lower(): v for k, v in args[1].items()}
        options = {k.lower(): v for k, v in args[2].items()}

        content = data['content']

        parent_tag = cls.__determin_base_class(options, base_tag)

        is_safe = cls.__determin_if_safe(options, parent_tag)
        strip_whitespaces = 'strip_whitespaces' in options
        split_lines = 'splitlines' in options

        arguments = {**parent_tag.arguments, **tag_arguments}
        codes = parent_tag.codes.copy()
        lua_scope = None
        text_blocks = parent_tag.compiler.copy()
        css = {}

        if content and content[0]:
            inner_tags = cls.__sort_inner_tags(content)

            if len(inner_tags['defcode']) or len(inner_tags['regex']):
                lua_scope = parent_tag.lua.cloneScope(parent_tag.lua_scope)

            cls.__compile_regex(base_tag.lua, lua_scope, inner_tags['regex'])

            cls.__compile_code(base_tag.lua, lua_scope,
                               inner_tags['defcode'], codes)

            css = cls.__process_css(inner_tags['css'])

            if_no_text = cls.__process_before_text(inner_tags)

            if inner_tags['text']:
                cls.__process_text(
                    text_blocks,
                    inner_tags['text'],
                    inner_tags['replace'],
                    is_safe,
                    split_lines,
                    strip_whitespaces,
                    if_no_text
                )

        tag_class: Type[BaseTag] = type(tag_name, (parent_tag,), {
            'tag_name': tag_name,
            'arguments': arguments,
            'codes': codes,
            'lua_scope': lua_scope,
            'source': data,
            'is_safe': is_safe,
            'compiler': text_blocks,
            'css': css,
        })
        tag_class.compiler.set_parent(tag_class)

        (base_tag.tags if temp_tags is None else temp_tags).update(
            {tag_name: tag_class}
        )

        return tag_class

    @staticmethod
    def __determin_if_safe(
        options: Dict[str, str],
        parent_tag: Type[BaseTag]
    ) -> bool:
        """Determin if the tag will be safe for HTML

        Parameters
        ----------
        options : `Dict[str, str]`
            Tag configuration options
        parent_tag : `Type[BaseTag]`
            `BaseTag` from which new tag will inherit

        Returns
        -------
        `bool`
        """
        is_safe = None
        if 'unsafe' in options:
            is_safe = False
        if 'safe' in options:
            is_safe = True
        if is_safe is None:
            is_safe = parent_tag.is_safe
        return is_safe

    @staticmethod
    def __determin_base_class(
        options: Dict[str, str],
        base_tag: Type[BaseTag]
    ):
        """Find base `BaseTag` from whom new tag will inherit

        Parameters
        ----------
        options : `Dict[str, str]`
            Tag configuration options

        base_tag : `Type[BaseTag]`
            Base tag stored in `TextCompiler`

        Returns
        -------
        `Type[BaseTag]`
        """
        parent_tag = None
        if 'extends' in options:
            parent_tag = base_tag.tags.get(options['extends'].lower())
        if not parent_tag:
            parent_tag = base_tag
        return parent_tag

    @staticmethod
    def __sort_inner_tags(content: Dict) -> Dict[str, List[Dict]]:
        """Sort inner tags contained inside of `define` tag

        Parameters
        ----------
        content : Dict
            Content of the `define` tag

        Returns
        -------
        `Dict[str, List[Dict]]`
            Sorted content
        """
        inner_tags = {
            'text': [],
            'defcode': [],
            'css': [],
            'regex': [],
            'replace': [],
            'ifnotext': [],
        }

        for i in content:
            if type(i) is str:
                continue
            elif (t := i['name'].lower()) in inner_tags:
                inner_tags[t].append(i)
        return inner_tags

    @staticmethod
    def __compile_regex(lua, lua_scope, regex):
        """Compile regex which will be accessible inside of the lua functions

        Parameters
        ----------
        lua : `Lua`
            Instance of `Lua` interface

        lua_scope : `LuaTable`
            Scope, to which the function will belong

        regex : `str`
            Regex expression
        """
        for i in regex:
            if not (
                    i['args'] and
                    i['args'][0] and
                    i['content'] and
                    (t := i['content'][0]) and
                    type(t) is str
            ):
                continue
            regex_name = list(i['args'][0])[0]
            lua.compile_regex(lua_scope, regex_name, t)

    @staticmethod
    def __compile_code(
        lua: Lua,
        lua_scope: LuaTable,
        code_srcs: str,
        codes: List[Callable]
    ):
        """Compile codes present in the `define` tag

        Parameters
        ----------
        lua : `Lua`
            Instance of `Lua` interface

        lua_scope : `LuaTable`
            Scope, to which the function will belong

        code_srcs : `str`
            Source code of the function

        codes : `List[Callable]`
            List of functions beloning to the new tag
        """
        for i in code_srcs:
            if not (
                    i['content'] and
                    (t := i['content'][0]) and
                    type(t) is str
            ):
                continue
            func = lua.compileCode(t, lua_scope)
            if func:
                codes.append(func)

    @staticmethod
    def __process_css(css) -> Dict[str, str]:
        """Process CSS present in 'define' tag

        Parameters
        ----------
        css : `List[Dict[str, str]]`
            Definitions of CSS classes

        Returns
        -------
        `Dict[str, str]`
            CSS classes
        """
        out = {}
        for i in css:
            name = list(i['args'][0])[0] if i['args'] else ''
            css_content = ''
            for j in i['content']:
                if type(j) is str:
                    css_content += j
            out[name] = css_content
        return out

    @staticmethod
    def __process_before_text(inner_tags: Dict) -> str:
        """Process `ifNoText` and `replace` tags in `define` tag. If no `text`
        tag is pressent inside `define` and `ifNoText` or `replace` contains
        some values, `text` will have default value of `'{text}'`

        Parameters
        ----------
        inner_tags : Dict
            Sorted tags present inside of `define` tag

        Returns
        -------
        `str`
            Value of `ifNoText` tag
        """
        if_no_tags = ''
        if inner_tags['ifnotext'] and \
                (t := inner_tags['ifnotext'][0]['content']) and \
                type(t[0]) is str:
            if_no_tags = t[0]
            if not inner_tags['text']:
                inner_tags['text'].append({'content': ['{text}']})

        if inner_tags['replace'] and not inner_tags['text']:
            inner_tags['text'].append({'content': ['{text}']})

        return if_no_tags

    @classmethod
    def __process_text(
        cls,
        text_blocks: List[Block],
        text: List[Dict[str, Union[str, Type[InnerBlock]]]],
        replace: List[Dict[str, str]],
        is_safe: bool,
        split_lines: bool,
        strip_whitespaces: bool,
        if_no_text: str
    ):
        """Create new text `Block`

        Parameters
        ----------
        text_blocks : `List[Block]`
            List of `Block`s to which new `Block` will be added

        text : `List[Dict[str, Union[str, Type[InnerBlock]]]]`
            Content of the `text` tag inside of `define`

        replace : `List[Dict[str, str]]`
            Arguments of the `replace` tag inside `define`

        is_safe : `bool`
            Whether to convert unescaped '<' and '>' to their '&gt;' and '&lt;'

        split_lines : `bool`
            Process each line separately

        strip_whitespaces : `bool`
            Remove trailing whitespaces

        if_no_text : `str`
            Text to be used if tag contains no text
        """
        new_text_block = Block(
            is_safe,
            split_lines,
            strip_whitespaces,
            ifNoText=if_no_text
        )

        text = text[0]['content']
        for i in text:
            if type(i) is str:
                new_text_block.add(i)
            else:
                inner_tag_name = i['name'].lower()
                if not (
                        inner_tag_name in cls.allowed_blocks and
                        i['args'][0] and
                        (key := list(i['args'][0])[0]) and
                        i['content'] and
                        type(i['content'][0]) is str
                ):
                    continue
                constructor = cls.allowed_blocks[inner_tag_name]
                val = i['content'][0] or ''
                new_text_block.add(constructor(key, val))

        for i in replace:
            if not (i['args'] and (t := i['args'][0])):
                continue
            to_replace = list(t.items())
            new_text_block.add_replacements(to_replace)

        text_blocks.append(new_text_block)
