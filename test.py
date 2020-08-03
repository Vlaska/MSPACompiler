from pathlib import Path

from src.TextCompiler.textParser import TextParser

t = TextParser(Path('./tags.mspa').read_text('utf-8'))

src = '''[chat:[gamzee: test test :o)
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
test]

[defines:
[macro[test=gamzee]]
[define[test1, [], []]: [text :test] [css: color: #ff00ff;]]
]
]
'''
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
# src = '[[gamzee: test \\\\< \\\\> ù😼'
# print(src)
out = t.parse(src)
print(out)
Path('test.html').write_text(out, 'utf-8')
print(t.compileCSS())
