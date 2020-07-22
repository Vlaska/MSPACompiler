from __future__ import annotations

from typing import Dict

from .baseTag import BaseTag
from .utils import fixSquareBrackets


class Defcode:
    tag_name = 'defcode'

    @staticmethod
    def parse(data: Dict):
        if not (
            data['args'] and
            data['args'][0] and
            type(name := list(data['args'][0])[0]) is str and
            data['content'] and
            type(text := data['content'][0]) is str
        ):
            return
        # codeText = fixSquareBrackets(text)
        # function = BaseTag.lua.compileCode(codeText, BaseTag.lua.baseScope)
        function = BaseTag.lua.compileCode(text, BaseTag.lua.baseScope)
        BaseTag.lua.addToGlobalScope(name, function)
