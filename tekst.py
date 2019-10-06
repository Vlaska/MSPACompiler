import json
import main

tekst = [
    {
        "command": 'John: Weź ciasto z kanapy.'
    },
    {
        "text": "Captchalogujesz CIASTO z kanapy, wyrzucając TACKĘ z dolnej karty.",
        "command": "John: Połącz ciasta, aby zrobić ciasto dwuwarstwowe."
    },
    {
        'text': '''Następnie scalasz oba CIASTA poprzez wszystkie pięć kart.

Wszystko w twoim SYLADEKSIE wciśnięte pomiędzy CIASTA. Może byś najpierw pomyślał zanim coś zrobisz?''',
        "command": 'John: Wycofaj się na górę!'
    },
    {
        'text': '''Zatrzymujesz się na moment na korytarzu i po chwili idziesz dalej. Będziesz potrzebował czegoś, czym posprzątasz bałagan, którego zaraz narobisz, rozczłonkowując to CIASTO.

Na lewo jest ŁAZIENKA. Na prawo POKÓJ TATY. Jest zamknięty, a ty masz dożywotni zakaz wchodzenia do niego. Ten człowiek ma swoje sekrety.''',

        "command": 'John: Idź do łazienki i weź ręcznik.'

    },
    {
        'text': '''Wchodzisz do ŁAZIENKI. Przez okno widać twoje PODWÓRKO. Jego wisienką na torcie jest HUŚTAWKA, która zapewniła ci lata radości. Jest tam także SPRĘŻYNOWY POGO-SKOCZEK, który odpowiadał za niejedną bolesną ranę oraz zapewnił ci lata cierpień.

Na zlewie leży BRZYTWA TATY. Z boku na wieszaku wisi ŚWIEŻY RĘCZNIK.''',
        "command": 'John: Wydobądź z ciasta palmtop, kopertę i paczkę.'

    },
    {
        'text': '''Bierzesz BRZYTWĘ i za jej pomocą dokonujesz operacji chirurgicznej na CIEŚCIE.

Bierzesz RĘCZNIK i oczyszczasz wydobyte dobra.''',

        "command": 'John: Zbierz swoje przedmioty.'
    },
    {

        'text': '''Przedmioty wypychają ZMALTRETOWANE CIASTO do TOALETY.

I w ten oto sposób twój SYLADEKS znów jest pełen. Boże, jakie to dziadostwo jest irytujące.''',


        "command": 'John: Idź do sypialni.'
    },
    {
        "command": 'John: Podziwiaj plakat „Miłości na zamówienie.”'
    },
    {

        'text': '''Zwykle nie przepadasz za filmami dla lasek, ale luzacka charyzma Matthew McConaugheya jest w stanie odratować jakąkolwiek kupę zardzewiałego złomu.

To twoja „Ściana McConaugheya,” skromny ołtarzyk dla wspaniałego aktora. Uważasz, że film powyżej jest dużo lepszy.

CZY WIDZICIE JĄ? CHCĘ, BYŚCIE SOBIE WYOBRAZILI TĘ MAŁĄ DZIEWCZYNKĘ. [dławi się] A TERAZ WYOBRAŹCIE SOBIE, ŻE JEST BIAŁA.

Masz nas, Matthew! Twoja gładka gadka wyciągnęła na światło dzienne nasz głęboko skrywany rasizm! Cholera, dobry jesteś!''',


        "command": '[S] John: Sprawdź PESTERCHUM.'
    },
    {
        'text': '''-- gardenGnostic <jade, id<[GG]>:> zaczęła gnębić ectoBiologist <john, id<[EB]>:> o 16:34 --

<jade: cześć wszystkiego najlepszego john!!!!! \<3
haloooooo??
ok pogadamy później!!! :D>

-- gardenGnostic <jade, id<[GG]>:> zaprzestała gnębienia ectoBiologist <john, id<[EB]>:> o 16:56 --


-- turntechGodhead <dave, id<[TG]>:> zaczął gnębić ectoBiologist <john, id<[EB]>:> o 16:40 --

<dave: ej GG cię szuka dlaczego jesteś w ogóle nagle taki popularny
dzisiaj jest jakaś specjalna okazja czy co
czy zrobiłeś coś żeby się przypodobać dziewczynom
złamałeś sobie noge o szczeniaczka albo jakieś inne gówno
typie co ty robisz>
-- turntechGodhead <dave, id<[TG]>:> jest teraz koleżką z dala od komputera! --
<john: odkryłem kometę, która zniszczy ziemię, została nazwana moim imieniem.
teraz jestem sławny i wszyscy bardzo chcą ze mną rozmawiać.>
<dave: nie przestań
po prostu nie
nie gadaj o swoich okropnych głupich filmach ani nie rób do nich nawiązań
twoja obleśna męsko-platoniczna mięta do matta macconahaya jest przykrym widokiem>
<john: mcconaugheya.>
<dave: brzmi jak odgłos który mógłby wydać koń
tzn debilnie
tak samo debilne są wszystkie grafiki tego pajaca które wiszą u ciebie>
<john: to mojego taty.>
<dave: mowiłem o nicku cageu>
<john: że co?! nie typie, cage jest świetny. tak bardzo świetny.>
<dave: ha ha ale żenada
nawet nie lubisz go ironicznie ani nic to jest na serio co nie
hahaha>
<john: czasem robię rzeczy ironicznie.
a co z tym co wysłałem ci na urodziny?>
<dave: nie one są zajebiste>
<john: co? nie, są głupie, na tym polegał żart. IRONICZNY żart. łapiesz?
chwila...
serio masz je teraz na sobie, co nie?>
<dave: mam je na sobie ironicznie
bo są zajebiste
to że są ironiczne sprawia że są zajebiste
i vice versa
robisz notatki z tego jak być fajnym? jezu ogarnij sobie jebany długopis>
<john: zdajesz sobie sprawę z tego, że w którymś momencie dotykały dziwnej, trochę jakby wychudzonej twarzy stillera.>
<dave: fuj ta
no cóż
w każdym razie skoro przy tym jesteśmy
dostaleś pocztę
ta.
czy była tam może paczka>
<john: ta, jest taka jedna wielka czerwona.>
<dave: prawdopodobnie powinieneś ją otworzyć>
<john: tak bym zrobił, ale utknęła pod betą sburba, więc pewnie otworzę ją po tym, jak zainstaluję betę.>
<dave: o stary przyszła beta>
<john: no! chcesz w nią zagrać?>
<dave: haha nie ma mowy>
<john: dlaczego nie!>
<dave: brzmi tak CHOLERNIE nudno weź po prostu namów TT żeby zagrała ją kręcą takie rzeczy>
<john: gdzie ona poszła.>
<dave: internet jej pada co chwilę tak myslę
pewnie zaraz będzie online
o i chryste w dostawczej przyczepie czy ty ciągle używasz trybu stosu???
serio typie
musisz OGARNĄĆ swoje struktury danych bo to gówno jest po prostu żalosne>
<john: ok, tak zrobię.>''',
        "command": 'John: Otwórz przeglądarkę i wejdź na mspaintadventures.com'
    },
    {

        'text': '''Postanawiasz pozamulać chwilę przy komputerze zanim weźmiesz się za cokolwiek ważnego.

Otwierasz przeglądarkę TYPHEUS i kierujesz ją na to, co jest niewątpliwie najwspanialszą stroną internetową, jaka kiedykolwiek powstała.''',
        "command": '==>'
    },
    {
        'text': 'Nowa przygoda jest spoko, ale nie jesteś pewien, czy podoba Ci się tak samo jak poprzednia.',

        "command": 'John: Zainstaluj betę Sburba.'
    },
    {
        'text': '''Postanawiasz, że pora na mniej meta, a więcej beta.

Wkładasz CD i instalujesz BETĘ SBURBA.''',
        "command": '==>'
    },
    {
        'text': 'Co to kurwa jest.',
        "command": 'John: Ogarnij struktury danych.'
    },
    {
        'text': 'Idziesz do swojej SZAFY, w której trzymasz swoje ubrania oraz szereg przydatnych PORADNIKÓW PROGRAMOWANIA KOMPUTEROWEGO.',

        "command": 'John: Czytaj książkę Struktury Danych.'
    },
    {

        'text': '''Nie jesteś pewien, czy naprawdę chcesz się wciągać w to ogromne tomiszcze. Wygląda na naprawdę nudne. Oraz trochę jakby prostackie.

Może zamiast tego po prostu wypróbujesz ten darmowy moduł podawczy.''',

        "command": 'John: Zdobądź darmowy Moduł Podawczy.'
    },
    {

        'text': '''Otwierasz książkę na ostatniej stronie, gdzie w foliowej kieszonce dołączony jest darmowy MODUŁ PODAWCZY.

Ten konkretny kieruje się logiką KOLEJKOWANEJ STRUKTURY DANYCH, opierając się na metodzie „wchodzi pierwszy, wychodzi pierwszy”, inaczej niż w metodzie „wchodzi pierwszy, wychodzi ostatni”, praktykowanej przez STOS.''',
        "command": 'John: Dodaj Moduł Podawczy do Syladeksu.'
    },
    {

        'text': '''Przedmioty captchalogowane w twoim SYLADEKSIE nie są już natychmiastowo dostępne. Możesz użyć tylko przedmiotu na dolnej karcie, a na przedmioty na wyższych kartach poczekać, aż zostaną do niej zepchnięte.

Na przykład, CZERWONA PACZKA nie jest teraz dostępna. Możesz na chwilę obecną użyć jedynie BRZYTWY.

Ten tryb nie robi na tobie wrażenia szczególnego postępu względem poprzedniego. W istocie, wydaje się być nawet mniej poręcznym. Mimo to, dochodzisz do wniosku, że równie dobrze możesz dać mu szansę.''',

        "command": 'John: Przełącz z powrotem na Moduł Stosu.'
    },
    {

        'text': '''Nagle zastanawiasz się, czy jest to w ogóle wykonalne. Nie pamiętasz nawet, czy miałeś kiedykolwiek faktyczną kartę MODUŁU STOSU.

Uważasz to za odrobinę zbyt abstrakcyjne i wolałbyś za bardzo o tym nie myśleć.''',

        "command": 'John: Odłóż brzytwę.'
    },
    {

        'text': '''Od...

...łóż?

...

Chyba nie do końca rozumiesz.''',

        "command": 'John: Podnieś dwa przedmioty.'

    },
    {
        'text': '''Captchalogujesz jedno z CIAST.

W końcu znalazłeś zastosowanie dla tych wszystkich walających się wypieków: ZAPCHAJDZIURY.''',

        "command": 'John: Weź drugie ciasto.'

    },
    {
        'text': '''Drugie CIASTO sprawia, że BRZYTWA wystrzeliwuje z przodu twojego SYLADEKSU.

Boże święty.

TA PIĘKNA TWARZ.

Żałujesz, że BRZYTWA zdołała wystrzelić.''',

        "command": 'John: Weź więcej rzeczy.'
    },
    {

        'text': '''Otwierasz swoją MAGICZNĄ SKRZYNIĘ i captchalogujesz jedną ze swoich ulubionych książek wszechczasów, MĄDRY CZŁOWIEK MIKE'A CAVENEY.

No i mamy ŚWIEŻY RĘCZNIK.''',

        "command": 'John: Równie dobrze możesz wziąć te kajdanki.'
    },
    {

        'text': 'Bierzesz KAJDANKI DO SZTUCZEK, wystrzeliwując PALMTOP niczym pocisk.',

        "command": '==>'
    },
    {

        'text': 'A niech to szlag.',

        "command": 'John: Otwórz tę paczkę!'
    },
    {

        'text': '''Przyglądasz się paczce. Jest od jednego z twoich internetowych koleżków.

Niestety, jest zawinięta w taśmę klejącą. Będzie ci potrzebne coś ostrego, żeby ją otworzyć.

Ach, oczywiście! BRZYTWA! To wszystko takie proste, zastanawiasz się, dlaczego po prostu nie...''',

        "command": 'John: Weź brzytwę.'
    },
    {
        "command": 'John: Ponownie podnieś paczkę.',
    },
    {
        'text': 'Zajmijmy się tym od razu.',

        "command": 'John: Captchaloguj odłamki szkła.'

    },
    {
        'text': '''Szybkim ruchem łapiesz po kolei trzy ODŁAMKI SZKŁA i kulisz się dla własnego bezpieczeństwa.

Twój SYLADEKS sieje spustoszenie w twoim pokoju.

A teraz, skoro twoje karty są pełne szkła, raczej nie zamierzasz tego w najbliższym czasie powtarzać.''',

        "command": '==>'

    },
    {
        'text': 'Powinieneś chyba pójść po te rzeczy, zanim zapomnisz.',
        "command": 'John: Użyj brzytwy na czerwonej paczce.'
    }
]

parser = main.MSPA_Parser('./')
t = []
with open('out.txt', 'w', encoding='utf-8') as f:
    for i in tekst:
        # t.append({"command": i['command'], 'text': parser.generateHTML()})
        f.write(f'Komenda: {i["command"]}')
        if 'text' in i:
            parser.parse(i['text'])
            f.write(f'\n\n{parser.generateHTML()}\n\n\n------\n')
        else:
            f.write(f'\n\n\n------\n')

# with open('style.css', 'w', encoding='utf-8') as f:
#     f.write(parser.generateCSS())
