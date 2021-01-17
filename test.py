from pathlib import Path
from pprint import pprint

from TextCompiler.textParser import TextCompiler
from TextCompiler.inputStringParser import parse

t = TextCompiler(Path('./tags.mspa').read_text('utf-8'))

# src = '''[chat:
# [[NANNASPRITE: Ponad [under :Medium], za [under :Siedmioma Bramami], w samym rdzeniu [under :Zaczątkosfery] znajduje się miejsce zwane [under :Skaia].
# [[NANNASPRITE: Legenda głosi, że [under :Skaia] istnieje jako zapomniany tygiel nieskończonego potencjału twórczego. Co to oznacza, zapytasz? Obawiam się, że moje usta milczą w tej kwestii, kochanie! Hu hu!
# [[NANNASPRITE: Lecz rzecz jasna, gdy mowa o krainie o tak dogłębnym znaczeniu, siły światła bez końca będą czuwać na jej straży, podczas gdy siły ciemności równie zawzięcie będą pragnąć jej zniszczenia!
# ]
# '''
src = '''[chat:
[[NANNASPRITE: Ponad [under :Medium], za [under :Siedmioma Bramami], w samym rdzeniu [under :Zaczątkosfery] znajduje się miejsce zwane [under :Skaia].
[[NANNASPRITE: Legenda głosi, że [under :Skaia] istnieje jako zapomniany tygiel nieskończonego potencjału twórczego. Co to oznacza, zapytasz? Obawiam się, że moje usta milczą w tej kwestii, kochanie! Hu hu!
[[NANNASPRITE: Lecz rzecz jasna, gdy mowa o krainie o tak dogłębnym znaczeniu, siły światła bez końca będą czuwać na jej straży, podczas gdy siły ciemności równie zawzięcie będą pragnąć jej zniszczenia!
]'''
# src = '''[text:Te bity były tak soczyste, że ich miejsce jest w alejce z napojami, tak właśnie czujesz. Matki polki depczą soki z tego gówna jak z winogron. Kumacie czaczę?

# # Po bitach tak soczystych nie ma bata, żeby sobie nie strzelić ceremonialnego [html:<span style="color: blue;">Ł<span style="color: red;">Y</span>K</span>]a.

# # 2+1+2 %10 = 5.
# # ]'''
# src = ('''also, są też skróty do wstępów wiadomości:

# [EBc]
# [GTc]
# [TTc]
# [TGc]
# [GGc]

# [aGGc]
# [aGTc]
# [aTGc]
# [aTTc]

# [tAAc]
# [tATc]
# [tTAc]
# [tCGc]
# [tACc]
# [tGAc]
# [tGCc]
# [tAGc]
# [tCTc]
# [tTCc]
# [tCAc]
# [tCCc]

# ugh, wygląda na to, że część z nich się pokrywa...''')
# pprint(p)
# src = '[[gamzee: test \\\\< \\\\> ù😼'
# print(src)
# src = '''[hash:ROZMAeeeeWIAĆ]'''
# src = '[[NANNASPRITE: Ponad [under :Medium], za [under :Siedmioma Bramami], w samym rdzeniu [under :Zaczątkosfery] znajduje się miejsce zwane [under :Skaia].'
# src = '[[NANNASPRITE: Ponad [under :Medium], za [under :Siedmioma Bramami]'
out = t.compile(src)
print(out)
# print('*' * 10)
# out = parse(src)
# pprint(out[0])
# Path('test.html').write_text(out, 'utf-8')
# print(t.compile_css())
