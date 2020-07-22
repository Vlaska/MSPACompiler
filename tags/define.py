from __future__ import annotations

from typing import Dict, Type

from .utils import fixSquareBrackets
from .baseTag import BaseTag
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
    def parse(cls, data: Dict):
        args = data['args']

        if len(args) != 3:
            return

        tagName = list(args[0].keys())[0].lower()
        tagArguments = {k.lower(): v for k, v in args[1].items()}
        options = {k.lower(): v for k, v in args[2].items()}

        content = data['content']

        if 'extends' in options:
            parentTag = BaseTag.tags.get(options['extends'].lower())
            if not parentTag:
                parentTag = BaseTag
        else:
            parentTag = BaseTag

        isSafe = None
        if 'unsafe' in options:
            isSafe = False
        if 'safe' in options:
            isSafe = True
        if isSafe is None:
            isSafe = parentTag.isSafe
        splitLines = 'splitlines' in options

        arguments = {**parentTag.arguments, **tagArguments}
        codes = parentTag.codes.copy()
        luaScope = parentTag.lua.cloneScope(parentTag.luaScope)
        textBlocks = parentTag.textBlocks.copy()

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
                BaseTag.lua.compileRegex(luaScope, regexName, t)

            for i in innerTags['defcode']:
                if not (
                        i['content'] and
                        (t := i['content'][0]) and
                        type(t) is str
                ):
                    continue
                func = BaseTag.lua.compileCode(t, luaScope)
                # func = BaseTag.lua.compileCode(fixSquareBrackets(t), luaScope)
                if func:
                    codes.append(func)

            if innerTags['text']:
                newTextBlock = Block(isSafe, splitLines)

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
        })
        tagClass.textBlocks.setParent(tagClass)

        BaseTag.tags.update({tagName: tagClass})

        return tagClass

    # def createTag(self, data: Dict) -> Type[BaseTag]:
    #     args = data['args']
    #     if len(args) < 3:
    #         raise ValueError('Not enought arguments')

    #     name = args['0'][0].lower()
    #     if name in BaseTag.tags:
    #         raise Exception('Tag already exists.')

    #     arguments = {k.lower(): v for k, v in args['1']}
    #     settings = {k.lower(): v for k, v in args['2']}

    #     extendsName = settings.get('extends', None)
    #     if extendsName and extendsName in BaseTag.tags:
    #         extends = BaseTag.tags[extendsName]
    #     else:
    #         extends = BaseTag

    #     arguments = {**extends.arguments, **arguments}
    #     isSafe = ('safe' in settings) and ('not-safe' not in settings)
    #     luaScope = self.lua.createScope()

    #     tags = {
    #         '__seq': [],
    #         'regex': [],
    #         'args': [],
    #         'defcode': [],
    #     }
    #     text = data['text']
    #     if text == '':
    #         return
    #     if type(text) is dict:
    #         for i in text['text']:
    #             if type(i) is not str and i['name'] in tags:
    #                 tags[i['name']].append(i)
    #             else:
    #                 tags['__seq'].append(i)
    #     elif type(text) is list:
    #         for i in text:
    #             if type(i) is not str and i['name'] in tags:
    #                 tags[i['name']].append(i)
    #             else:
    #                 tags['__seq'].append(i)
    #     else:
    #         tags['__seq'].append(text)

    #     textMethod = (
    #         '@classproperty\n'
    #         'def text(\n'
    #             '    cls,\n'
    #             '    text: str,\n'
    #             '    isTop: bool = False,\n'
    #             '    isSafe: bool = True,\n'
    #             '    **arguments\n'
    #         '):\n'
    #         '    out = ""\n'
    #         '    arguments = {**self.arguments, **arguments}\n'
    #         '    text = cls.textCleanup(text, isTop, isSafe)\n\n')

    #     regexTag = self.defineTags.get('regex')()
    #     for i in tags['regex']:
    #         self.lua.compileRegex(luaScope, *regexTag.createTag(i))
    #     argsTag = self.defineTags.get('args')()
    #     for i in tags['args']:
    #         textMethod += argsTag.createTag(i)
    #     defcodeTag = self.defineTags.get('defcode')()
    #     codes = []
    #     for i in tags['defcode']:
    #         codes.append(defcodeTag.createTag(i))

    #     for i in tags['__seq']:
    #         if type(i) is str:
    #             textMethod += f'    out += {quote(i)}\\n'
    #         else:
    #             print(i)
    #             # for j in i['text']:
    #             #     if type(j) is str:
    #             #         textMethod += f'    out += {quote(j)}\n'
    #             #     else:
    #             #         name = j['name']
    #             #         if name in self.defineTags:
    #             #             textMethod += self.defineTags.get(name)().createTag(j)
    #             #         elif name in self.tags:
    #             #             textMethod += f'    self.tags.get({quote(name)})()({j}, arguments)\n'
    #             textMethod += self.functionTextBuilder([i])

    #     return textMethod
    #     # return type(
    #     #     name,
    #     #     (extends, ),
    #     #     {
    #     #         'arguments': arguments,
    #     #         'codes': [*extends.codes, *codes]
    #     #     }
    #     # )
