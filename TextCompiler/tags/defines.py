from __future__ import annotations

from typing import Dict, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from TextCompiler.tags.baseTag import BaseTag

from TextCompiler.tags.defines_tags.define import Define
from TextCompiler.tags.defines_tags.macro import Macro
from TextCompiler.tags.defines_tags.defcode import Defcode


class Defines:
    """Class responsible for analysing the content of "defines" tag.
    Defines can only recognize these three tags: "define", "macro" and
    "defcode".

    Using "define" you can define a new tag, which can use previously defined
    tag.

    Using "macro" you can add additional name for previously created tags.

    Using "defcode" you can create a lua function, which will be awailable for
    all tags and code blocks defined in the future.
    """
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
        """Iterate over "defines" content and process recognized tags.

        Parameters
        ----------
        data : Dict[str, str]
            Content of "defines" tag

        base_tag : Type[BaseTag]
            Base tag

        temp_tags : Dict[str, Type[BaseTag]], optional
            Temporary tags, by default None
        """
        for i in data['content']:
            if type(i) is str:
                continue
            t = cls.allowed_tags.get(i['name'].lower())
            if t:
                t.parse(i, base_tag, temp_tags)
