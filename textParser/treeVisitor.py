import re

from arpeggio import PTNodeVisitor


class Visitor(PTNodeVisitor):
    squareBracketsRegex = re.compile(r'(?:\\|/)(?:\[|\])')

    @staticmethod
    def __squareBracketFix(matchobj: re.Match):
        return matchobj.group(0)[-1]

    @classmethod
    def fixSquareBrackets(cls, text: str) -> str:
        return cls.squareBracketsRegex.sub(cls.__squareBracketFix, text)

    def visit_beginTag(self, node, children):
        return None

    def visit_endTag(self, node, children):
        return None

    def visit_separator(self, node, children):
        return None

    def visit_space(self, node, children):
        return None

    def visit_beginOneLineTag(self, node, children):
        return None

    def visit_singleQuote(self, node, children):
        return None

    def visit_doubleQuote(self, node, children):
        return None
    
    def visit_plainText(self, node, children):
        return self.fixSquareBrackets(children[0])

    def visit_plainTextUntilNewLine(self, node, children):
        text = children[0]
        if text[-1] == '\n':
            text = text[:-1]
        if text:
            return self.fixSquareBrackets(text)
        return None

    def visit_argString(self, node, children):
        # print(children)
        if len(children) == 2:
            return {children[0].strip(): children[1].strip()}
        return {children[0].strip(): ''}

    def visit_listOfStrings(self, node, children):
        return children

    def visit_args(self, node, children: list):
        out = []
        for v in children:
            if type(v) is dict:
                t = v
            else:
                # print(v)
                if len(v):
                    t = {j: m for i in v for j, m in i.items()}
                else:
                    t = {}
            out.append(t)
        # return {
        #     k: v for k, v in enumerate(children)
        # }
        return out

    def visit_tag(self, node, children):
        if len(children) >= 2:
            return children[0].strip().lower(), children[1]
        return children[0].strip().lower(), {}

    def visit_tagSelected(self, node, children):
        text = None
        if len(children) >= 2:
            text = children[1]
        if not isinstance(text, (list, tuple)):
            text = [text]
        else:
            _text = []
            for i in text:
                if isinstance(i, (list, tuple)):
                    _text.extend(i)
                else:
                    _text.append(i)
            text = _text
        return {
            'name': children[0][0],
            'args': children[0][1],
            'content': text,
        }

    def visit_oneLineTag(self, node, children):
        text = None
        if len(children) >= 2:
            text = children[1]
        if not isinstance(text, (list, tuple)):
            if type(text) is str and text[-1] == '\n':
                children.append('\n')
                text = text[:-1]
            if not text:
                text = None
            text = [text]
        else:
            _text = []
            for i in text:
                if isinstance(i, (list, tuple)):
                    _text.extend(i)
                else:
                    _text.append(i)
            if type(_text[-1]) is str and _text[-1] == '\n':
                children.append(_text.pop())
            text = _text

        out = {
            'name': children[0][0],
            'args': children[0][1],
            'content': text,
        }
        if children[-1] == '\n':
            return out, '\n'
        return out

    def visit_listOfStrings(self, node, children):
        return [i for i in children if i != ' ']

    def visit_text(self, node, children):
        return children

    def visit_mspaText(self, node, children):
        return children[0]
