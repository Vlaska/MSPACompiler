from __future__ import annotations

from typing import Dict

from .baseTag import BaseTag


class Macro:
    @staticmethod
    def parse(data: Dict[str, str]):
        if not (data['args']):
            return
        for i in data['args']:
            for new, old in i.items():
                if not (new or old or new in BaseTag.tags):
                    continue
                tag = BaseTag.tags.get(old)
                if tag:
                    BaseTag.tags[new] = tag
