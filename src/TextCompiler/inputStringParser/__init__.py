from arpeggio import ParserPython, visit_parse_tree

from .parseRules import mspaText
from .treeVisitor import Visitor
import re


NEW_LINE_FIX = re.compile('\r\n|\r')


def parse(text: str):
    parser = ParserPython(
        mspaText,
        debug=False,
        skipws=False,
        ws=r'\t ',
    )
    if '\r' in text:
        text = NEW_LINE_FIX.sub('\n', text)
    return visit_parse_tree(parser.parse(text), Visitor())
