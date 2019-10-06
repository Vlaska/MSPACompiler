import json
from pathlib import Path
import re

keywords = ['img', 'url', 'animate', '-animate',
            'def', 'quirk', '-quirk', 'html', 'id']
tagsWithArguments = {'url': {'argc': 1}, 'animate': {'argc': 1}, 'quirk': {
    'argc': 1}, 'def': {'argc': 1}, 'id': {'argc': 1}}


class ParsingError(Exception):
    pass


class MSPA_Parser:
    def __init__(self, projectPath, saveLocation=None):
        self.projectPath = projectPath
        self.quirks = self.loadQuirks()
        self.modQuriks = {}
        self.parsedText = []
        self.generatedHTML = ''
        self.removedTag = False

    def loadQuirks(self):
        t = Path(self.projectPath, 'quirks')
        quirks = {}

        if t.is_dir():
            quirkFolder = t

            files = [i for i in quirkFolder.iterdir() if i.is_file()
                     and i.suffix == '.json']

            for i in files:
                try:
                    te = json.loads(i.read_text())
                except json.JSONDecodeError:
                    pass
                else:
                    if self.isValidQuirk(te, i.stem):
                        quirks.update({te['name']: te})

        if 'default' not in quirks:
            quirks.update(
                {'default': {'color': {'r': 0, 'g': 0, 'b': 0, 'a': 255}}})

        return quirks

    def isValidQuirk(self, quirk, name):
        if 'name' in quirk and name == quirk['name'] and name not in keywords:
            return True
        return False

    def processColor(self, color):
        if color:
            if type(color) == str:
                return color
            elif type(color) == list:
                if len(list) in [3, 4]:
                    return '#{:02x}{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2], color[3] if len(color) == 4 else 255)
            elif type(color) == dict:
                return '#{:02x}{:02x}{:02x}{:02x}'.format(color.get("r", 0), color.get("g", 0), color.get("b", 0), color.get("a", 255))
            raise Exception('Nieprawidłowy kolor')
        else:
            return None

    def generateCSS(self):
        css = []
        for q in self.quirks:
            args = []
            c = self.processColor(self.quirks[q].get('color', None))
            bg_c = self.processColor(self.quirks[q].get('bg-color', None))
            h_bg = self.processColor(self.quirks[q].get('highlight-bg', None))

            if c:
                args.append(f'color: {c};')
            if bg_c:
                args.append(f'background-color: {bg_c};')

            t = '\n\t'.join(args)

            if len(args):
                css.append('.{} {{\n\t{}\n}}'.format(q, t))

            if h_bg:
                css.append(
                    '.{}[data-highlight="true"] {{\n\tbackground-color: {};\n}}'.format(q, h_bg))

        return '\n\n'.join(css)

    def __quote(self, s):
        t = type(s)
        if t == str:
            return f'"{s}"'
        if t == list:
            return [self.__quote(i) for i in s]

    def parseTags(self, text):
        tags = {'classes': {}}
        tag = []
        args = []
        arg = []
        string = False
        lastPos = 0

        for pos in range(len(text)):
            char = text[pos]
            lastPos = pos

            if char in ['\n', '\0']:
                raise ParsingError(f'Tagi nie zostały odpowiednio zamknięte.\n"{text[pos:pos+30]}"')

            if char == '>' and not string:
                raise ParsingError('Tekst przedwcześnie zamknięty')
            elif char == '>' and string:
                args.append(''.join(arg))
                arg.clear()
                string = False
                continue

            if char == '<' and not string:
                string = True
                continue

            if char == ' ' and not string:
                continue

            if char in [',', ':'] and not string:
                if len(tag) == 0:
                    raise ParsingError('Tag nieprawidłowy tag.')
                _tag = ''.join(tag)

                if _tag in keywords:
                    if _tag in tagsWithArguments and len(args) < tagsWithArguments[_tag]['argc']:
                        raise ParsingError(f'''Tag "{_tag}" otrzymał nieprawidłową ilość argumentów.
                                Wymagana ilość: {tagsWithArguments[_tag]["argc"]}
                                Podana ilość: {len(args)}''')
                    tags[_tag] = args.copy() if len(args) else None
                else:
                    tags['classes'][_tag] = args.copy() if len(args) else None

                args.clear()
                tag.clear()

                if char == ':':
                    break

                continue

            if string:
                arg.append(char)
            else:
                tag.append(char)

        t = [i for i in ['img', 'url', 'html', 'def'] if i in tags]
        if len(t) and len(tags['classes']) != 0:
            raise ParsingError(
                f'Tag{"" if len(t) == 1 else "i"} "{" ".join(self.__quote(t))}" nie mo{"że" if len(t) == 1 else "gą"} występować z innymi tagami.')

        return tags, lastPos + 1

    def _parse(self, text, first=False):
        t = self.parseTags(text)
        parsedText = {'tags': t[0], 'text': []}
        html = 'html' in t[0]
        currentText = []
        lastChar = ['', ''] if html else ''
        lastPos = 0
        continuePos = t[1]

        for pos in range(len(text)):
            if pos < continuePos:
                continue

            lastPos = pos
            char = text[pos]

            if html:
                if char == '>':
                    if lastChar[-1] in ['/', '\\'] and lastChar[0] not in ['/', '\\']:
                        currentText.pop()
                        break
                    elif lastChar in [['/', '/'], ['\\', '\\']]:
                        currentText.pop()

                currentText.append(char)
                lastChar.pop(0)
                lastChar.append(char)
            else:
                if char == '\n' and not first:
                    lastPos -= 1
                    break

                if char == '>':
                    if lastChar not in ['/', '\\']:
                        break
                    else:
                        currentText.pop()

                if char == '<':
                    if lastChar not in ['/', '\\']:
                        parsedText['text'].append(''.join(currentText))
                        lastChar = ''
                        currentText.clear()

                        t = self._parse(text[pos + 1:])
                        parsedText['text'].append(t[0])
                        continuePos = pos + t[1]
                        continue
                    else:
                        currentText.pop()

                currentText.append(char)
                lastChar = char

        if len(currentText):
            parsedText['text'].append(''.join(currentText))

        return parsedText, lastPos + 2

    def parse(self, text):
        self.parsedText.clear()
        self.generatedHTML = ''
        parsedText = []
        currentText = []
        lastChar = ''
        continuePos = 0
        for pos in range(len(text)):
            if pos < continuePos:
                continue

            char = text[pos]

            if char == '<':
                if lastChar not in ['/', '\\']:
                    parsedText.append(''.join(currentText))
                    lastChar = ''
                    currentText.clear()

                    t = self._parse(text[pos + 1:], True)
                    parsedText.append(t[0])
                    continuePos = pos + t[1]
                    continue
                else:
                    currentText.pop()

            currentText.append(char)
            lastChar = char

        if len(currentText):
            parsedText.append(''.join(currentText))

        self.parsedText = parsedText
        return self.parsedText

    def _generageHTML(self, parsedText):
        text = []

        for p in parsedText['text']:
            if type(p) == str:
                if len(p):
                    text.append(re.sub('^ ', '', p.replace(
                        '<', '&lt;').replace('>', '&gt;')))
            else:
                if 'def' in p['tags']:
                    self.removedTag = True
                elif 'html' in p['tags']:
                    for i in p['text']:
                        text.append(i)
                else:
                    text.append(self._generageHTML(p))

        text = ''.join(text).split('\n')
        classes = parsedText['tags']['classes'] or {}
        t = []
        for i in text:
            if 'url' in parsedText['tags']:
                link = parsedText['tags']['url'][0] if len(
                    parsedText['tags']['url']) else '#'
                text = i if len(i) else link
                args = ' '.join(parsedText['tags']['url'][1:])

                t.append(
                    f'''<a href="{link}"{" " if len(args) else ""}{args}>{text}</a>''')
            elif 'img' in parsedText['tags']:
                args = ' '.join(parsedText['tags']['img'] or [])
                t.append(
                    f'''<img src="{i}"{" " if len(args) else ""}{args}>''')
            elif 'html' in parsedText['tags']:
                t.append(i)
            else:
                args = []
                preText = ''
                if 'id' not in parsedText['tags']:
                    for j in reversed(sorted(classes.keys())):
                        if j in self.quirks and 'preText' in self.quirks[j]:
                            preText = self.quirks[j]['preText']
                            break
                else:
                    preText = parsedText['tags']['id'][0]

                for j in classes:
                    if 'highlight-bg' in self.quirks[j] and 'data-highlight' not in args:
                        args.append('data-highlight')

                    if classes[j]:
                        for k in classes[j]:
                            args.append(k)

                args = ' '.join(args)
                t.append(
                    f'<span class="{" ".join(classes)}"{" " if len(args) else ""}{args}>{preText}{i}</span>')
        return '\n<br>\n'.join(t)

    def generateHTML(self):
        text = []
        for p in self.parsedText:
            if type(p) == str:

                t = re.sub('^ ', '', p.replace(
                    '<', '&lt;').replace('>', '&gt;'))
                if self.removedTag:
                    self.removedTag = False
                    t = re.sub('^\n', '', t)

                text.append(t.replace('\n', '<br>\n'))
                # text.append(re.sub('(?:^ | $)', '', p.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '\n<br>\n')))
            else:
                if 'def' in p['tags']:
                    self.removedTag = True
                elif 'html' in p['tags']:
                    for i in p['text']:
                        text.append(i)
                else:
                    text.append(self._generageHTML(p))

        self.generatedHTML = re.sub(' +', ' ', ''.join(text))
        return self.generatedHTML


if __name__ == '__main__':
    test = '''testtesttse
<jade: test>
test <jade <style="color: #c4118e; font-size: 30px;">, id<Jade: >: test
<url<http://www.google.pl><style="color: #11c47f">:Google>
<url<http://www.google.pl>:>
<img<width="200"><height="100">:madrala.png>
<url<https://homestuckproject.pl>:<img:trollcool.gif>>>
<def<john>: to jeszcze w żaden sposób nie oddziałowuje na resztę>
<html:<h1>TEST</h1>//>/>
<dave: <john, id<>: f\<<rose: y u play baby game y yu no shcut>\>de

ts>>
<scratch: testtestets>'''

    parser = MSPA_Parser('./')

    with open('out.json', 'w', encoding='utf-8') as f:
        t = parser.parse(test)
        f.write(json.dumps([test, t], indent=4))

    with open('style.css', 'w', encoding='utf-8') as f:
        f.write(parser.generateCSS())

    with open('out.html', 'w', encoding='utf-8') as f:
        f.write('<link rel="stylesheet" href="style.css">\n\n')
        f.write(f'<p>\n{parser.generateHTML()}\n</p>')
        f.write(
            '<script>document.querySelectorAll(\'[data-highlight]\')[0].dataset.highlight="true"</script>')
    # generateHTML(parse(test))
