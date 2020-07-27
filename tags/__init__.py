from __future__ import annotations

from .baseTag import BaseTag
from .defines import Defines


BaseTag.tags.update({
    'defines': Defines,
})


class TextParser:
    def __init__(self):
        self.baseTag = BaseTag.newClassInstance(self)

    @staticmethod
    def innerParse(text: list, baseTag: Type[BaseTaq]) -> str:
        out = []
        for i in text:
            if type(i) is dict:
                name = i['name']
                nameLower = name.lower()
                if nameLower == 'defines':
                    Defines.parse(i, baseTag)
                else:
                    tag = baseTag.tags.get(nameLower)

                    if tag is None:
                        print(f'Unknown tag: {name}')  # ERROR LOG
                        continue

                    i['content'] = [TextParser.innerParse(i['content'], baseTag)]

                    t = tag.parse(i)
                    if t:
                        out.extend(t)
            elif i:
                out.append(i)
        return ''.join(out)

    def parse(self, text: list) -> str:
        return self.innerParse(text, self.baseTag).strip()
