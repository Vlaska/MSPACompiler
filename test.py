from pathlib import Path
from pprint import pprint

from src.TextCompiler.textParser import TextParser
from src.TextCompiler.inputStringParser import parse

t = TextParser(Path('./tags.mspa').read_text('utf-8'))

# src = '''[chat:[gamzee: test test :o)
# Test na
# kilka
# lini
# tekstu blablabla]
# [karkat: test]
# [[kanaya: to jest test, czy kod jest dobrze napisany
# [[tavros: to jest test, czy kod jest dobrze napisany
# [[dirk: teraz po drobnych poprawkach wygląda, że tak
# [[eridan: test połskich znaków
# [[aa: wygląda na to, że kod eridana działa źle x// 
# [[gc: also, z jakiegoś powodu nie chce domyślnie uruchamiać kodów formatujących
# [[ag: ale to powinno być łatwe do naprawienia
# [[rose: muszę też dodać usuwanie powielających się białych znaków
# test]
# [url[href="/test"]]

# [defines:
# [macro[test=gamzee]]
# [define[test1, [], []]: [text :test] [css: color: #ff00ff;]]
# ]
# '''
src = '''[text:Te bity były tak soczyste, że ich miejsce jest w alejce z napojami, tak właśnie czujesz. Matki polki depczą soki z tego gówna jak z winogron. Kumacie czaczę?

Po bitach tak soczystych nie ma bata, żeby sobie nie strzelić ceremonialnego [html:<span style="color: blue;">Ł<span style="color: red;">Y</span>K</span>]a.

2+1+2 %10 = 5.
]'''
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
# print('*' * 10)
# out = parse(src)
# pprint(out[0])
# Path('test.html').write_text(out, 'utf-8')
# print(t.compileCSS())
