from __future__ import annotations

from typing import Dict, Type

from .define import Define
from .macro import Macro
from .defcode import Defcode


class Defines:
    allowedTags = {
        'define': Define,
        'macro': Macro,
        'defcode': Defcode
    }

    @classmethod
    def parse(
            cls,
            data: Dict[str, str],
            baseTag: Type[BaseTag],
            tempTags: Dict[str, Type[BaseTag]] = None
    ):
        for i in data['content']:
            if type(i) is str:
                continue
            t = cls.allowedTags.get(i['name'].lower())
            if t:
                t.parse(i, baseTag, tempTags)
