from __future__ import annotations

from typing import Dict, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from TextCompiler.tags.baseTag import BaseTag


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
        function = baseTag.lua.compileCode(text, baseTag.lua.baseScope)
        baseTag.lua.addToScope(
            baseTag.luaScope,
            name,
            function,
            tempTags is not None
        )
