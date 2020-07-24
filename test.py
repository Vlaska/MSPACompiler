import json
from pathlib import Path
from pprint import pprint

from tags.baseTag import BaseTag
from tags import parse
from parse import parse as parseText


# t = json.loads(Path('./out.json').read_text())
# parse(t)
parse(parseText(Path('./tags.mspa').read_text('utf-8')))

p = parseText('''[gamzee: test test :o)
Test na
kilka
lini
tekstu blablabla]
[karkat: test]
[[kanaya: to jest test, czy kod jest dobrze napisany
[[tavros: to jest test, czy kod jest dobrze napisany
[[dirk: teraz po drobnych poprawkach wygląda, że tak
[[eridan: test połskich znaków
[[aa: wygląda na to, że kod eridana działa źle x//
[[gc: also, z jakiegoś powodu nie chce domyślnie uruchamiać kodów formatujących
[[ag: ale to powinno być łatwe do naprawienia
[[rose: muszę też dodać usuwanie powielających się białych znaków
test''')
# p = parseText('''also, są też skróty do wstępów wiadomości:

# [EBc]
# [GTc]
# [TTc]
# [TGc]
# [GCc]

# [GCc]
# [GTc]
# [TGc]
# [TTc]

# [AAc]
# [ATc]
# [TAc]
# [CGc]
# [ACc]
# [GAc]
# [GCc]
# [AGc]
# [CTc]
# [TCc]
# [CAc]
# [CCc]

# ugh, wygląda na to, że część z nich się pokrywa...''')
# pprint(p)
print(parse(p))
