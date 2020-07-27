from __future__ import annotations

from typing import Dict, Type

# from .baseTag import BaseTag


class Macro:
    @staticmethod
    def parse(data: Dict[str, str], baseTag: Type[BaseTag]):
        if not (data['args']):
            return
        for i in data['args']:
            for new, old in i.items():
                new, old = new.lower(), old.lower()
                if not (new or old or new in baseTag.tags):
                    continue
                tag = baseTag.tags.get(old)
                if tag:
                    baseTag.tags[new] = tag
