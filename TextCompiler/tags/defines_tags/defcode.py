from __future__ import annotations

from typing import Dict, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from TextCompiler.tags.baseTag import BaseTag


class Defcode:
    tag_name = 'defcode'

    @staticmethod
    def parse(
            data: Dict,
            base_tag: Type[BaseTag],
            temp_tags: Dict[str, Type[BaseTag]] = None
    ):
        if not (
                data['args'] and
                data['args'][0] and
                type(name := list(data['args'][0])[0]) is str and
                data['content'] and
                type(text := data['content'][0]) is str
        ):
            return
        function = base_tag.lua.compileCode(text, base_tag.lua.baseScope)
        base_tag.lua.addToScope(
            base_tag.lua_scope,
            name,
            function,
            temp_tags is not None
        )
