from main import MSPA_Parser

t = '''-- turntechGodhead <dave, id<[TG] >:> began pestering ectoBiologist <john, id<[EB] >:> at 16:13 -- 

<dave: hey so what sort of insane loot did you rake in today>
<john: i got a little monsters poster, it's so awesome. i'm going to watch it again today, the applejuice scene was so funny.>
<dave: oh hell that is such a coincidence i just found an unopened container of apple juice in my closet it is like fucking christmas up in here>
<john: ok thats fine, but i just have one question and then a word of caution. have you ever seen a movie called little monsters starring howie mandel and fred savage?>
<dave: but 
the seal on the bottle is unbroken 
are you suggesting someone put piss in my apple juice at the factory>
<john: all im saying is don't you think monster howie mandel has the power to do something as simple as reseal a bottle? 
try using your brain numbnuts.>
<dave: why did the fat kid or whoever drank it know what piss tasted like 
i mean his reaction was nigh instantaneous>
<john: it was the 15th day in a row howie mandel peed in his juice.>
<dave: ok i can accept that 
monster B-list celebrity douchebags are cunning and persistent pranksters 
also fred savage has a really punchable face 
but who cares about this lets stop talking about it 
did you get the beta yet>
<john: no. 
did you?> 
<dave: man i got two copies already 
but i dont care im not going to play it or anything the game sounds boring 
did you see how it got slammed in game bro????>
<john: game bro is a joke and we both know it.>
<dave: yeah
why dont you go check your mail maybe its there now>
<john: alright.>'''

p = MSPA_Parser('./')
p.parse(t)
with open('przykład.html', 'w', encoding='utf-8') as f:
    f.write('<link rel="stylesheet" href="style.css">\n\n')
    f.write(p.generateHTML())