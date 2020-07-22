from __future__ import annotations

from .baseTag import BaseTag
from .defines import Defines


BaseTag.tags.update({
    'defines': Defines,
})


def parse(text: list) -> str:
    out = []
    for i in text:
        if type(i) is dict:
            name = i['name']
            tag = BaseTag.tags.get(name.lower())

            if tag is None:
                print(f'Unknown tag: {name}')  # ERROR LOG
                continue

            t = tag.parse(i)
            if t:
                out.extend(t)
        elif i:
            out.append(i)
    return ''.join(out)
