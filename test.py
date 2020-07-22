import json
from pathlib import Path

from tags.baseTag import BaseTag
from tags import parse
from parse import parse as parseText


# t = json.loads(Path('./out.json').read_text())
# parse(t)
parse(parseText(Path('./tags.mspa').read_text()))

p = parseText('[gamzee[quirk=1]: test test :o)]')
# print(p)
print(parse(p))
