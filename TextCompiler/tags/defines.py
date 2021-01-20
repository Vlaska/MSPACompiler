from __future__ import annotations

from typing import Dict, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from TextCompiler.tags.baseTag import BaseTag

from TextCompiler.tags.defines_tags.define import Define
from TextCompiler.tags.defines_tags.macro import Macro
from TextCompiler.tags.defines_tags.defcode import Defcode


class Defines:
    allowed_tags = {
        'define': Define,
        'macro': Macro,
        'defcode': Defcode
    }

    @classmethod
    def parse(
            cls,
            data: Dict[str, str],
            base_tag: Type[BaseTag],
            temp_tags: Dict[str, Type[BaseTag]] = None
    ):
        for i in data['content']:
            if type(i) is str:
                continue
            t = cls.allowed_tags.get(i['name'].lower())
            if t:
                t.parse(i, base_tag, temp_tags)
