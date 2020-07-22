from __future__ import annotations

import re


squareBracketsRegex = re.compile(r'(?:\\|/)(?:\[|\])')


def __squareBracketFix(matchobj: re.Match):
    return matchobj.group(0)[-1]


def fixSquareBrackets(text: str):
    return squareBracketsRegex.sub(__squareBracketFix, text)
