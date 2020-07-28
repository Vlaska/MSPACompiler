from arpeggio import ParserPython, visit_parse_tree

from .parseRules import mspaText
from .treeVisitor import Visitor


def parse(text):
    parser = ParserPython(
        mspaText,
        debug=False,
        skipws=False,
        ws=r'\t ',
    )
    return visit_parse_tree(parser.parse(text), Visitor())
