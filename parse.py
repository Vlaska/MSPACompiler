from arpeggio import ParserPython, visit_parse_tree
from textParser.parseRules import mspaText
from textParser.treeVisitor import Visitor
from pathlib import Path
import json


def parse(text):
    parser = ParserPython(
        mspaText,
        debug=False,
        skipws=False,
        ws=r'\t ',
    )
    return visit_parse_tree(parser.parse(text), Visitor())


if __name__ == "__main__":
    text = Path('./tags.mspa').read_text()
    Path('./out.json').write_text(
        json.dumps(parse(text), indent=4),
        'utf-8'
    )

# kody z poprzednich rodziców nie są aktualizowane przy dziedziczeniu
