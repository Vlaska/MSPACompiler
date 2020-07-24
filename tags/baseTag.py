import re
from typing import Dict

from .utils import fixSquareBrackets
from .block import Block
from .textBlocks import TextBlocks
from .luaExec import Lua


class BaseTag:
    '''
        settings: 
            safe: < and > stay that way
            unsafe: < and > gets converted to &lt; and &gt;
            extends=<TAG>: defined tag extends previous tag
            splitlines: split text by '\\n'

        special tags:
            define[name, [args], [settings]]
            regex
            function
            text
            out-text
            defcode
            code
            if
            ifnot
            for
            args
            normal
    '''
    textBlocks = TextBlocks([Block(True, False, False, ['{text}'])])
    tag_name = ''
    arguments = {}
    wasBuild = True
    isSafe = True


    tags = {}
    codes = [lambda x: x.decode('utf-8'), ]
    lua = Lua()
    luaScope = None


    @staticmethod
    def safeText(text: str) -> str:
        return text

    @classmethod
    def notSafeText(cls, text: str) -> str:
        return cls.ltGtEscapedRegex.sub(
            cls.replaceSafeLtGt,
            cls.ltGtNotEscapedRegex.sub(
                cls.replaceUnsafeLtGt,
                text
            )
        )

    @classmethod
    def parse(cls, data: Dict[str, str]) -> str:
        text = data['content']
        args = cls.processArgs(data['args'])
        try:
            return [cls.textBlocks(i or '', args) for i in text]
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

    # @classmethod
    # def init(cls):
    #     cls.textBlocks = TextBlocks([Block(True, False, ['{text}'])], cls)

    # init()


if not BaseTag.textBlocks.parent:
    BaseTag.textBlocks.parent = BaseTag
