from __future__ import annotations

from typing import Dict, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from MSPACompiler.tags.baseTag import BaseTag


class Defcode:
    """Create lua function available globaly
    """
    tag_name = 'defcode'

    @staticmethod
    def process(
            data: Dict,
            base_tag: Type[BaseTag],
            temp_tags: Dict[str, Type[BaseTag]] = None
    ):
        """Create lua function available globaly

        Parameters
        ----------
        data : Dict
            Dictionary containing the name of the function

        base_tag : Type[BaseTag]
            BaseTag to which the function will belong

        temp_tags : Dict[str, Type[BaseTag]], optional
            If specified, function will be awailable temporarily,
            by default None
        """
        if not (
                data['args'] and
                data['args'][0] and
                type(name := list(data['args'][0])[0]) is str and
                data['content'] and
                type(text := data['content'][0]) is str
        ):
            return
        function = base_tag.lua.compileCode(text, base_tag.lua.base_scope)
        base_tag.lua.add_to_scope(
            base_tag.lua_scope,
            name,
            function,
            temp_tags is not None
        )
