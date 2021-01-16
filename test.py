from pathlib import Path
from pprint import pprint

from TextCompiler.textParser import TextParser
from TextCompiler.inputStringParser import parse

t = TextParser(Path('./tags.mspa').read_text('utf-8'))

# src = '''[chat:
# [[NANNASPRITE: Ponad [under :Medium], za [under :Siedmioma Bramami], w samym rdzeniu [under :Zaczątkosfery] znajduje się miejsce zwane [under :Skaia].
# [[NANNASPRITE: Legenda głosi, że [under :Skaia] istnieje jako zapomniany tygiel nieskończonego potencjału twórczego. Co to oznacza, zapytasz? Obawiam się, że moje usta milczą w tej kwestii, kochanie! Hu hu!
# [[NANNASPRITE: Lecz rzecz jasna, gdy mowa o krainie o tak dogłębnym znaczeniu, siły światła bez końca będą czuwać na jej straży, podczas gdy siły ciemności równie zawzięcie będą pragnąć jej zniszczenia!
# ]
# '''
# src = '''[text:Te bity były tak soczyste, że ich miejsce jest w alejce z napojami, tak właśnie czujesz. Matki polki depczą soki z tego gówna jak z winogron. Kumacie czaczę?

# Po bitach tak soczystych nie ma bata, żeby sobie nie strzelić ceremonialnego [html:<span style="color: blue;">Ł<span style="color: red;">Y</span>K</span>]a.

# 2+1+2 %10 = 5.
# ]'''
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
# src = '''[t :ROZMAeeeeWIAĆ]'''
src = '[[NANNASPRITE: Ponad [under :Medium], za [under :Siedmioma Bramami], w samym rdzeniu [under :Zaczątkosfery] znajduje się miejsce zwane [under :Skaia].'
src = '[[NANNASPRITE: Ponad [under :Medium], za [under :Siedmioma Bramami]'
out = t.parse(src)
print(out)
# print('*' * 10)
# out = parse(src)
# pprint(out[0])
# Path('test.html').write_text(out, 'utf-8')
# print(t.compileCSS())
