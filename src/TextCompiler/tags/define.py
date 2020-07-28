from __future__ import annotations

from typing import Dict, Type

# from .utils import fixSquareBrackets
# from .baseTag import BaseTag
from .block import Block
from .codeTag import CodeTag
from .ifTags import IfTag, IfNotTag


class Define:
    tag_name = 'define'
    allowedTags = {
        'if': IfTag,
        'ifnot': IfNotTag,
        'code': CodeTag,
    }

    @classmethod
    def parse(
            cls,
            data: Dict,
            baseTag: Type[BaseTag],
            tempTags: Dict[str, Type[BaseTag]] = None
    ):
        args = data['args']

        if len(args) != 3:
            return

        tagName = list(args[0].keys())[0].lower()
        tagArguments = {k.lower(): v for k, v in args[1].items()}
        options = {k.lower(): v for k, v in args[2].items()}

        content = data['content']

        if 'extends' in options:
            parentTag = baseTag.tags.get(options['extends'].lower())
            if not parentTag:
                parentTag = baseTag
        else:
            parentTag = baseTag

        isSafe = None
        if 'unsafe' in options:
            isSafe = False
        if 'safe' in options:
            isSafe = True
        if isSafe is None:
            isSafe = parentTag.isSafe
        stripWhitespaces = 'strip_whitespaces' in options
        splitLines = 'splitlines' in options
        ignoreWhitespaces = 'ignore_whitespaces' in options

        arguments = {**parentTag.arguments, **tagArguments}
        codes = parentTag.codes.copy()
        luaScope = parentTag.lua.cloneScope(parentTag.luaScope)
        textBlocks = parentTag.textBlocks.copy()
        css = {}

        if content and content[0]:
            innerTags = {
                'text': [],
                'defcode': [],
                'css': [],
                'regex': [],
                'replace': [],
            }

            for i in content:
                if type(i) is str:
                    continue
                elif (t := i['name'].lower()) in innerTags:
                    innerTags[t].append(i)

            for i in innerTags['regex']:
                if not (
                        i['args'] and
                        i['args'][0] and
                        i['content'] and
                        (t := i['content'][0]) and
                        type(t) is str
                ):
                    continue
                regexName = list(i['args'][0])[0]
                baseTag.lua.compileRegex(luaScope, regexName, t)

            for i in innerTags['defcode']:
                if not (
                        i['content'] and
                        (t := i['content'][0]) and
                        type(t) is str
                ):
                    continue
                func = baseTag.lua.compileCode(t, luaScope)
                # func = baseTag.lua.compileCode(fixSquareBrackets(t), luaScope)
                if func:
                    codes.append(func)

            for i in innerTags['css']:
                name = list(i['args'][0])[0] if i['args'] else ''
                # css[name] = i['content']
                cssContent = ''
                for j in i['content']:
                    if type(j) is str:
                        cssContent += j
                css[name] = cssContent

            if innerTags['text']:
                newTextBlock = Block(
                    isSafe,
                    splitLines,
                    stripWhitespaces,
                    # ignoreWhitespaces,
                )

                text = innerTags['text'][0]['content']
                for i in text:
                    if type(i) is str:
                        newTextBlock.add(i)
                    else:
                        innerTagName = i['name'].lower()
                        if not (
                                innerTagName in cls.allowedTags and
                                i['args'][0] and
                                (key := list(i['args'][0])[0]) and
                                i['content'] and
                                type(i['content'][0]) is str
                        ):
                            continue
                        constructor = cls.allowedTags[innerTagName]
                        val = i['content'][0] or ''
                        newTextBlock.add(constructor(key, val))

                for i in innerTags['replace']:
                    if not (i['args'] and (t := i['args'][0])):
                        continue
                    toReplace = list(t.items())
                    newTextBlock.addReplacements(toReplace)

                textBlocks.append(newTextBlock)

        tagClass: Type[BaseTag] = type(tagName, (parentTag,), {
            'tag_name': tagName,
            'arguments': arguments,
            'codes': codes,
            'luaScope': luaScope,
            'source': data,
            'wasBuild': True,
            'isSafe': isSafe,
            'textBlocks': textBlocks,
            'css': css,
        })
        tagClass.textBlocks.setParent(tagClass)

        (tempTags or baseTag.tags).update({tagName: tagClass})

        return tagClass
