import json
import re
from typing import Collection, Dict, List

from arpeggio import NoMatch, ParserPython, visit_parse_tree
from fcache.cache import FileCache
from loguru import logger

from .parseRules import entrypoint
from .treeVisitor import Visitor

NEW_LINE_FIX = re.compile('\r\n|\r')
CACHE = FileCache(__name__)

AST = List[Dict[str, Collection[Collection[str]]]]


class ParserError(Exception):
    pass


rules = {
    'ws': ['spaces'],
    r'\t| ': ['spaces'],
    'escapedText': ['text'],
    'escapedTextUntilNewLine': ['text untill new line'],
    'plainText': ['text'],
    'plainTextUntilNewLine': ['text'],
    'name': ['name'],
    'singleQuotedString': ['single quoted string'],
    'doubleQuotedString': ['double quoted string'],
    'codeString': ['string with ticks instead of quotes'],
    'string': ['single quoted string', 'double qouted string'],
    'beginTag': ['['],
    'beginOneLineTag': ['[['],
    'endTag': [']'],
    'separator': ',',
    ',': ',',
    '=': '=',
    ':': ':',
    'argument': ['name', 'quoted string', '='],
    'arguments': ['argument', 'list of arguments'],
    'args': ['[', 'argument', 'list of arguments', ']'],
    'tag': 'normal tag',
    'oneLineTag': 'one line tag',
    'text': ['one line tag', 'normal tag', 'code string', 'normal text'],
    'textUntilNewLine': ['one line tag', 'normal tag', 'code string', 'normal text'],
    'entrypoint': ['normal text', 'tags'],
    'EOF': ['end of text'],
}


def parse(text: str) -> List:
    parser = ParserPython(
        entrypoint,
        debug=False,
        skipws=False,
        ws=r'\t ',
    )
    if '\r' in text:
        text = NEW_LINE_FIX.sub('\n', text)
    try:
        return visit_parse_tree(parser.parse(text), Visitor())
    except NoMatch as e:
        t: List[str] = []
        for i in e.rules:
            key = i.rule_name or i.to_match
            p = rules.get(key, None)
            if p:
                t.extend(f'"{j}"' for j in p)
            else:
                t.append(f'"{e.to_match}"')
        message = f'Line: {e.line}, col: {e.col}. Expecting: ' + ', '.join(t)
        logger.critical(message)
        raise ParserError(message)


def caching_parser(text: str) -> List:
    name = str(hash(text))
    try:
        return json.loads(CACHE[name])
    except KeyError:
        out = parse(text)
        CACHE[name] = json.dumps(out)
        return out
