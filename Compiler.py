import json
from pathlib import Path
import re

from quirkSetter import QuirkSetter
from Parser import generateDict


class TextCompiler:
    def __init__(self, quirks: list=None, macros: str=None):
        self.quirkSetter = QuirkSetter()
        self.quirks = {
            'default': {
                'color': '#000000',
            }
        }
        self.globalMacros = {}
        self.localMacros = {}

        if quirks:
            self.loadQuirksFromList(quirks)
        if macros:
            assert type(macros) is str, "Incorrect 'macros' type, "\
                "expected string"
            parsedMacros = [out
                            for out in generateDict(macros)
                            if type(out) is dict and out['type'] is 'def']
            for macro in parsedMacros:
                self.globalMacros[macro['name']] = macro['content']

    def loadQuirk(self, quirk):
        assert type(quirk) is dict, 'Incorrect argument'
        assert 'name' in quirk, 'Quirk data must contain name.'

        self.quirks[quirk['name']] = quirk
        self.quirkSetter.loadFromDict(quirk)

    def loadQuirksFromList(self, _list):
        assert type(_list) is list, "Incorrect 'quirks' type, "\
                "expected list"
        for quirk in _list:
            self.loadQuirk(quirk)

    def processColor(self, color):
        if not color:
            return None
        if type(color) is str:
            return color
        elif type(color) is list:
            if len(list) in [3, 4]:
                return '#{:02x}{:02x}{:02x}{:02x}'.format(
                    color[0],
                    color[1],
                    color[2],
                    color[3] if len(color) == 4 else 255
                )
        raise Exception('Incorrect color format')

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

            if 'style' in q:
                if type(q['style']) is list:
                    args.extend(q['style'])
                elif type(q['style']) is str:
                    args.append(q['style'])

            t = '\n\t'.join(args)

            if len(args):
                css.append(f'.{q} {{\n\t{t}\n}}')

            if h_bg:
                css.append(
                    f'.{q}[data-highlight="true"]'
                    f'{{\n\tbackground-color: {h_bg};\n}}'
                )

        return '\n\n'.join(css)

    def escapeText(self, text: str):
        return text.replace('<', '&lt;').replace('>', '&gt;')

    def compileMacro(self, name, content):
        self.localMacros[name] = content

    def compileTree(self, tree):
        out = []

        if not tree:
            return ''

        for node in tree:
            if type(node) is str:
                out.append(self.escapeText(node))
            else:
                out.append(self.compileTag(node))

        return ''.join(out).replace('\n', '<br>\n')

    def processText(self, text, quirk, quirkID):
        if quirk:
            quirkID = int(quirkID) if quirkID else quirkID
            text = self.quirkSetter.processText(text, quirk, quirkID)
        return self.escapeText(text)

    def getMacroContent(self, macro):
        if macro in self.localMacros:
            return self.localMacros[macro]
        if macro in self.globalMacros:
            return self.globalMacros[macro]
        return None

    def compileTagContent(self, settings, content):
        out = []

        classList = []
        classesFromMacros = []
        for _class in settings['classes']:
            if _class[0] is '#':
                macro = self.getMacroContent(_class[1:])
                if macro:
                    classesFromMacros.extend(macro['classes'])
                    settings['params'].update(macro['params'])
            else:
                classList.append(_class)

        classList = [*classesFromMacros, *classList]

        quirk = ''
        quirkToSet = None
        for c in classList:
            if c in self.quirks:
                quirk = c
                break

        for c in classList:
            if c in self.quirks and 'quirks' in self.quirks[c]:
                quirkToSet = c
                break

        for node in content:
            if type(node) is str:
                out.append(self.processText(node, quirkToSet,
                                            settings['params'].get('quirk', None)))
            else:
                out.append(self.compileTag(node))

        img = settings['params'].get('img', None)
        url = settings['params'].get('url', None)
        style = settings['params'].get('style', None)
        classes = ''.join(classList)
        _id = settings['params'].get(
            'id', self.quirks[quirk]['id'] if quirk in self.quirks else '')

        if style:
            style = f' style="{style}"'

        if url:
            begginTag = f'<a href="{url}"{style if style else ""}>'
            out = out if len(out) else [url]
            endTag = '</a>'
        elif img:
            begginTag = f'<img src="{img}"{style if style else ""}>'
            endTag = '</img>'

        out = ''.join(out)
        outText = []
        for line in out.splitlines():
            outText.append(f'<span class="{classes}">{_id}{line}</span>')
        if len(outText) is 0:
            outText.append(f'<span class="{classes}">{_id}</span>')
        if url or img:
            return begginTag + '\n'.join(outText) + endTag
        return '\n'.join(outText)

    def compileTag(self, node):
        if node['type'] == 'html':
            return node['content'][0]
        if node['type'] == 'def':
            self.compileMacro(node['name'], node['content'])
            return ''
        return self.compileTagContent(
            node['settings'],
            node['content']
        )

    def compile(self, text):
        assert type(text) is str, 'Incorrect type'
        output = re.sub(' +', ' ', self.compileTree(generateDict(text)))
        self.localMacros.clear()
        return output
