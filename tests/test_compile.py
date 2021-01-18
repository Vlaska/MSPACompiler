import pytest
from TextCompiler.textParser import TextCompiler


def test_1(compiler: TextCompiler):
    text = compiler.compile(
        '[[NANNASPRITE: Ponad [under :Medium], za [under :Siedmioma Bramami]'
    )
    assert text == (
        '<span class="nannasprite">NANNASPRITE: Ponad <u>Medium</u>, za '
        '<u>Siedmioma Bramami</u></span>'
    )


def test_2(compiler: TextCompiler):
    compiler.load_tags('''[defines:
        [define[test, [], []]:
            [defcode :function (text)
                return text
            end]
        ]
        [define[test_inherit1, [c=1], [extends=test]]:
            [defcode :function (text)
                return string.reverse(text)
            end]
            [text :[code[c]:{text}]]
        ]
    ]''')
    assert 'test' in compiler.baseTag.tags
    codes_test = compiler.baseTag.tags['test'].codes
    assert len(codes_test) == 2
    text = compiler.compile('''[defines:
        [define[test_inherit, [code=2], [extends=test]]:
            [defcode :function (text)
                return string.reverse(text)
            end]
            [text :[code[code]:{text}]]
        ]
    ]
    [test_inherit :test_string]''')
    assert len(codes_test) == 2
    assert compiler.compile('[test_inherit1[c=2] :test_string]') == \
        'test_string'[::-1]
    assert text == 'test_string'[::-1]


texts = [
    (
        '''[chat:
[[NANNASPRITE: Ponad [under :Medium], za [under :Siedmioma Bramami], w samym rdzeniu [under :Zaczątkosfery] znajduje się miejsce zwane [under :Skaia].
[[NANNASPRITE: Legenda głosi, że [under :Skaia] istnieje jako zapomniany tygiel nieskończonego potencjału twórczego. Co to oznacza, zapytasz? Obawiam się, że moje usta milczą w tej kwestii, kochanie! Hu hu!
[[NANNASPRITE: Lecz rzecz jasna, gdy mowa o krainie o tak dogłębnym znaczeniu, siły światła bez końca będą czuwać na jej straży, podczas gdy siły ciemności równie zawzięcie będą pragnąć jej zniszczenia!
]''',
        '''<div class="chat"><br>
<span class="nannasprite">NANNASPRITE: Ponad <u>Medium</u>, za <u>Siedmioma Bramami</u>, w samym rdzeniu <u>Zaczątkosfery</u> znajduje się miejsce zwane <u>Skaia</u>.</span><br>
<span class="nannasprite">NANNASPRITE: Legenda głosi, że <u>Skaia</u> istnieje jako zapomniany tygiel nieskończonego potencjału twórczego. Co to oznacza, zapytasz? Obawiam się, że moje usta milczą w tej kwestii, kochanie! Hu hu!</span><br>
<span class="nannasprite">NANNASPRITE: Lecz rzecz jasna, gdy mowa o krainie o tak dogłębnym znaczeniu, siły światła bez końca będą czuwać na jej straży, podczas gdy siły ciemności równie zawzięcie będą pragnąć jej zniszczenia!</span><br>
</div>'''
    ),
    (
        '''[text:Te bity były tak soczyste, że ich miejsce jest w alejce z napojami, tak właśnie czujesz. Matki polki depczą soki z tego gówna jak z winogron. Kumacie czaczę?

# Po bitach tak soczystych nie ma bata, żeby sobie nie strzelić ceremonialnego [html:<span style="color: blue;">Ł<span style="color: red;">Y</span>K</span>]a.

# 2+1+2 %10 = 5.
# ]''',
        '''Te bity były tak soczyste, że ich miejsce jest w alejce z napojami, tak właśnie czujesz. Matki polki depczą soki z tego gówna jak z winogron. Kumacie czaczę?<br>
<br>
# Po bitach tak soczystych nie ma bata, żeby sobie nie strzelić ceremonialnego <span style="color: blue;">Ł<span style="color: red;">Y</span>K</span>a.<br>
<br>
# 2+1+2 %10 = 5.<br>
#'''
    ),
    (
        '''also, są też skróty do wstępów wiadomości:

[EBc]
[GTc]
[TTc]
[TGc]
[GGc]

[aGGc]
[aGTc]
[aTGc]
[aTTc]

[tAAc]
[tATc]
[tTAc]
[tCGc]
[tACc]
[tGAc]
[tGCc]
[tAGc]
[tCTc]
[tTCc]
[tCAc]
[tCCc]

ugh, wygląda na to, że część z nich się pokrywa...''',
        '''also, są też skróty do wstępów wiadomości:

ectoBiologist <span class="john">[EB]</span>
ghostyTrickster <span class="john">[GT]</span>
tentacleTherapist <span class="rose">[TT]</span>
turntechGodhead <span class="dave">[TG]</span>
gardenGnostic <span class="jade">[GC]</span>

gutsyGumshoe <span class="jane">[GC]</span>
golgothasTerror <span class="jake">[GT]</span>
tipsyGnostalgic <span class="roxy">[TG]</span>
timaeusTestified <span class="dirk">[TT]</span>

apocalypseArisen <span class="aradia">[AA]</span>
adiosToreador <span class="tavros">[AT]</span>
twinArmageddons <span class="sollux">[TA]</span>
carcinoGeneticist <span class="karkat">[CG]</span>
arsenicCatnip <span class="nepeta">[AC]</span>
grimAuxiliatrix <span class="kanaya">[GA]</span>
gallowsCalibrator <span class="terezi">[GC]</span>
arachnidsGrip <span class="vriska">[AG]</span>
centaursTesticle <span class="equius">[CT]</span>
terminallyCapricious <span class="gamzee">[TC]</span>
caligulasAquarium <span class="eridan">[CA]</span>
cuttlefishCuller <span class="feferi">[CC]</span>

ugh, wygląda na to, że część z nich się pokrywa...'''
    ),
    (
        r'[[gamzee: test \\< \\> ù😼',
        r'<span class="gamzee">Gamzee: tEsT \\&lt; \\&gt; ù😼</span>'
    ),
    (
        '[hash:ROZMAeeeeWIAĆ]',
        '<span style="color: blue;">R</span><span style="color: red;">O</span>'
        '<span style="color: blue;">ZM</span><span style="color: red;">Aeeee'
        '</span><span style="color: blue;">W</span><span style="color: red;">'
        'IA</span><span style="color: blue;">Ć</span>'
    ),
    (
        '''[chat:-- [tgc] zaczął dręczyć (przyp. tłum. z ang. to pester – dręczyć) [ebc] o 16:13 --

[[TG: hej więc jaki zajebisty łup dziś zgarnąłeś
[[EB: dostałem plakat z małych potworów, jest wspaniały. obejrzę dzisiaj ten film jeszcze raz, scena z sokiem jabłkowym była mega śmieszna.
[[TG: o cholera co za przypadek znalazłem nieotwartą butelkę soku jabłkowego w mojej szafie to jakby były jakieś jebane święta
[[EB: ok fajnie, ale mam jedno pytanie i jednocześnie ostrzeżenie. oglądałeś kiedyś film małe potwory z howie mandelem i fredem savage?
[[TG: ale
[[TG: nakrętka jest cała
[[TG: sugerujesz że ktoś naszczał do mojego soku jabłkowego w fabryce
[[EB: a czy uważasz że potworny howie mandel nie ma mocy zrobienia czegoś tak prostego jak ponowne uszczelnienie butelki?
[[EB: zacznij myśleć ptasi móżdżku.
[[TG: czemu gruby dzieciak czy ktokolwiek kto pił ten sok wiedział jak smakują szczyny
[[TG: jego reakcja była przecież prawie natychmiastowa
[[EB: to był piętnasty dzień z rzędu jak howie mandel nasikał mu do soku.
[[TG: ok przyjąłem
[[TG: potworni idiotyczni celebryci klasy b to wytrwali i przebiegli pranksterzy
[[TG: no i fred savage ma mordę która aż się prosi o wpierdol
[[TG: ale kogo to obchodzi przestańmy w ogóle o tym gadać
[[TG: przyszła ci już beta
[[EB: nie.
[[EB: a tobie?
[[TG: stary mam już dwie kopie
[[TG: ale mam to gdzieś nie będę w to grał ani nic brzmi nudno
[[TG: widziałeś jak ją zjechali w game bro????
[[EB: game bro to żart i obaj o tym wiemy.
[[TG: ta
[[TG: idź sprawdź skrzynkę może już przyszła
[[EB: jasne.]''',
        '''<div class="chat">-- turntechGodhead <span class="dave">[TG]</span> zaczął dręczyć (przyp. tłum. z ang. to pester – dręczyć) ectoBiologist <span class="john">[EB]</span> o 16:13 --<br>
<br>
<span class="dave">TG: hej więc jaki zajebisty łup dziś zgarnąłeś</span><br>
<span class="john">EB: dostałem plakat z małych potworów, jest wspaniały. obejrzę dzisiaj ten film jeszcze raz, scena z sokiem jabłkowym była mega śmieszna.</span><br>
<span class="dave">TG: o cholera co za przypadek znalazłem nieotwartą butelkę soku jabłkowego w mojej szafie to jakby były jakieś jebane święta</span><br>
<span class="john">EB: ok fajnie, ale mam jedno pytanie i jednocześnie ostrzeżenie. oglądałeś kiedyś film małe potwory z howie mandelem i fredem savage?</span><br>
<span class="dave">TG: ale</span><br>
<span class="dave">TG: nakrętka jest cała</span><br>
<span class="dave">TG: sugerujesz że ktoś naszczał do mojego soku jabłkowego w fabryce</span><br>
<span class="john">EB: a czy uważasz że potworny howie mandel nie ma mocy zrobienia czegoś tak prostego jak ponowne uszczelnienie butelki?</span><br>
<span class="john">EB: zacznij myśleć ptasi móżdżku.</span><br>
<span class="dave">TG: czemu gruby dzieciak czy ktokolwiek kto pił ten sok wiedział jak smakują szczyny</span><br>
<span class="dave">TG: jego reakcja była przecież prawie natychmiastowa</span><br>
<span class="john">EB: to był piętnasty dzień z rzędu jak howie mandel nasikał mu do soku.</span><br>
<span class="dave">TG: ok przyjąłem</span><br>
<span class="dave">TG: potworni idiotyczni celebryci klasy b to wytrwali i przebiegli pranksterzy</span><br>
<span class="dave">TG: no i fred savage ma mordę która aż się prosi o wpierdol</span><br>
<span class="dave">TG: ale kogo to obchodzi przestańmy w ogóle o tym gadać</span><br>
<span class="dave">TG: przyszła ci już beta</span><br>
<span class="john">EB: nie.</span><br>
<span class="john">EB: a tobie?</span><br>
<span class="dave">TG: stary mam już dwie kopie</span><br>
<span class="dave">TG: ale mam to gdzieś nie będę w to grał ani nic brzmi nudno</span><br>
<span class="dave">TG: widziałeś jak ją zjechali w game bro????</span><br>
<span class="john">EB: game bro to żart i obaj o tym wiemy.</span><br>
<span class="dave">TG: ta</span><br>
<span class="dave">TG: idź sprawdź skrzynkę może już przyszła</span><br>
<span class="john">EB: jasne.</span></div>'''
    ),
    (
        "[html :`(?P<nonvowels>[^aąeęioóuyAĄEĘIOÓUY\]+)|(?P<vowels>[aąeęioóuyAĄEĘIOÓUY\]+)`]",
        "(?P<nonvowels>[^aąeęioóuyAĄEĘIOÓUY\]+)|(?P<vowels>[aąeęioóuyAĄEĘIOÓUY\]+)"
    ),
    (
        '[eridan: ł w Ł W]',
        '<span class="eridan">Eridan: łł ww ŁŁ WW</span>'
    ),
    (
        '[[eridan:` ł w Ł W []`',
        '<span class="eridan">Eridan: łł ww ŁŁ WW []</span>'
    ),
    (
        '[[eridan: ł w \r\nŁ W ',
        '<span class="eridan">Eridan: łł ww </span>\nŁ W'
    ),
    (
        '[[eridan:` ł w \nŁ W `',
        '<span class="eridan">Eridan: łł ww </span>\n'
        '<span class="eridan">Eridan: ŁŁ WW </span>'
    ),
    (
        '[[eridan: ` ł w \nŁ W `',
        '<span class="eridan">Eridan: ` łł ww </span>\nŁ W `'
    ),
    (
        r'`this is a \` test /` string`',
        'this is a ` test ` string'
    ),
    (
        '[unknown]',
        ''
    ),
    (
        '''[defines:
    [define[test, [t], []]:
        [text:[if[t]:true][ifnot[t]:false]]
    ]
][test[t=1]] [test]''',
        'true false'
    ),
    (
        '', ''
    )
]


css_text = '''.john {color: #0715CD;}
.rose {color: #B536DA;}
.dave {color: #E00707;}
.jade {color: #4AC925;}
.jane {color: #00D5F2;}
.jake {color: #1F9400;}
.roxy {color: #FF6FF2;}
.dirk {color: #F2A402;}
.nannasprite {color: #00D5F2;}
.aradia {color: #A10000;}
.tavros {color: #A15000;}
.sollux {color: #A1A100;}
.karkat {color: #626262;}
.nepeta {color: #416600;}
.kanaya {color: #008141;}
.terezi {color: #008282;}
.vriska {color: #005682;}
.equius {color: #000056;}
.gamzee {color: #2B0057;}
.feferi {color: #77003C;}
.scratch {color: #FFFFFF;}
.scratch:hover {background-color: #000000;}'''


@pytest.mark.parametrize('text,result', texts)
def test_3(text, result, compiler: TextCompiler):
    t = compiler.compile(text)
    assert t == result


def test_4(compiler: TextCompiler):
    results = compiler.compile_css()
    for i in css_text.splitlines():
        assert i in results


def test_5(u_compiler: TextCompiler):
    text = '''[defines:
    [define[test, [], []]: [text:test]]
    [define[test1, [], []]]
    [macro[]]
    [macro[unknown]]
    [macro[unknown1=unknown]]
    [macro[test=test1]]
    [macro[l1=test, l2=test1]]
]'''
    u_compiler.load_tags(text)
    tags = u_compiler.baseTag.tags
    assert len(tags) == 4
    assert tags['test'] is not tags['test1']
    assert tags['l1'] is tags['test']
    assert tags['l2'] is tags['l2']

    t = u_compiler.compile('''[defines:
    [macro[l3=test, l4=l3]]
][l3] [l4]''')
    assert t == 'test test'
