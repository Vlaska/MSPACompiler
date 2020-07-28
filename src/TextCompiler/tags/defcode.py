from __future__ import annotations

from typing import Dict, Type

# from .baseTag import BaseTag
from .utils import fixSquareBrackets


class Defcode:
    tag_name = 'defcode'

    @staticmethod
    def parse(
            data: Dict,
            baseTag: Type[BaseTag],
            tempTags: Dict[str, Type[BaseTag]] = None
    ):
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
        function = baseTag.lua.compileCode(text, baseTag.lua.baseScope)
        baseTag.lua.addToGlobalScope(name, function)
