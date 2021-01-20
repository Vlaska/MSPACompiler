from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Type, List

if TYPE_CHECKING:
    from TextCompiler.tags.baseTag import BaseTag


class Macro:
    @staticmethod
    def parse(
            data: Dict[str, List[Dict[str, str]]],
            base_tag: Type[BaseTag],
            temp_tags: Dict[str, Type[BaseTag]] = None
    ):
        if not (data['args']):
            return

        for i in data['args']:
            for new, old in i.items():
                new, old = new.lower(), old.lower()

                if temp_tags is not None:
                    dst = temp_tags
                    if old in temp_tags:
                        src = temp_tags
                    else:
                        src = base_tag.tags
                else:
                    dst = base_tag.tags
                    src = base_tag.tags

                if not (new and old) or new in dst:
                    continue

                tag = src.get(old)
                if tag:
                    dst[new] = tag
