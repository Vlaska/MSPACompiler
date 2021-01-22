import re

from arpeggio import PTNodeVisitor


class Visitor(PTNodeVisitor):
    squareBracketsRegex = re.compile(r'(?:\\|/)(?:\[|\])')
    tickRegex = re.compile(r'(?:\\|/)`')
    whitespaces = {
        '\\n': '\n',
        '\\t': '\t',
        '\\r': '\r',
        '\\f': '\f',
        '\\v': '\v',
    }

    # * helpers
    @staticmethod
    def __squareBracketFix(matchobj: re.Match):
        return matchobj.group(0)[-1]

    @classmethod
    def fixSquareBrackets(cls, text: str) -> str:
        return cls.squareBracketsRegex.sub(cls.__squareBracketFix, text)

    def fix_special_characters(self, text: str) -> str:
        return re.sub(
            r'\\[ntrfv]',
            lambda x: self.whitespaces[x.group(0)],
            text
        )

    # * discard tags
    def visit_beginTag(self, node, children):
        return None

    def visit_endTag(self, node, children):
        return None

    def visit_separator(self, node, children):
        return None

    def visit_ws(self, node, children):
        return None

    def visit_beginOneLineTag(self, node, children):
        return None

    # * process
    def visit_codeString(self, node, children):
        return self.tickRegex.sub('`', node.value[1:-1])

    def visit_plainText(self, node, children):
        return self.fixSquareBrackets(children[0])

    def visit_plainTextUntilNewLine(self, node, children):
        return self.fixSquareBrackets(children[0])

    def visit_argument(self, node, children):
        name = children[0] if len(children) else ""
        if node[0].rule_name != 'string':
            name = name.strip()
        if len(children) == 2:
            value = children[1]
            if node[-1].rule_name != 'string':
                value = value.strip()
            return {name: value}
        return {name: ''}

    def visit_string(self, node, children):
        return self.fix_special_characters(children[0][1:-1])

    def visit_name(self, node, children):
        return self.fix_special_characters(node.value)

    def visit_args(self, node, children: list):
        out = []
        for v in children:
            if type(v) is dict:
                t = v
            else:
                if len(v):
                    t = {j: m for i in v for j, m in i.items()}
                else:
                    t = {}
            out.append(t)
        return out

    def visit_tag(self, node, children):
        name = children[0].strip().lower()
        if len(children) > 1:
            return name, children[1]
        return name, {}

    def visit_tagSelected(self, node, children):
        text = None
        if len(children) > 1:
            text = children[1]
        if not isinstance(text, list):
            text = [text]
        name, args = children[0]
        return {
            'name': name,
            'args': args,
            'content': text,
        }

    def visit_oneLineTag(self, node, children):
        text = None
        if len(children) >= 2:
            text = children[1]
        if not isinstance(text, list):
            if not text:
                text = None
            text = [text]

        return {
            'name': children[0][0],
            'args': children[0][1],
            'content': text,
        }

    def visit_text(self, node, children):
        return children

    def visit_textUntilNewLine(self, node, children):
        return children

    def visit_entrypoint(self, node, children):
        try:
            return children[0]
        except IndexError:
            return ''
