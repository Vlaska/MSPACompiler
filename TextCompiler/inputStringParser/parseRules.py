import re

import arpeggio as ar
from arpeggio import RegExMatch as _


def ws():
    return ar.ZeroOrMore(_(r'\t| '))


def escapedText():
    return _(r'(((?:\\|/)(?:\[|\]))|([^[\]]))+')


def plainText():
    return ar.Optional(escapedText)


def escapedTextUntilNewLine():
    return _(r'(((?:\\|/)(?:\[|\]))|([^[\]\n]))+')


def plainTextUntilNewLine():
    return ar.Optional(escapedTextUntilNewLine)


def name():
    return _(r'[><{}@_!#$%^&*./\\0-9a-zA-Z-]+')


def singleQuotedString():
    return _(r"'.*?(?<!\\|/)'", re_flags=re.MULTILINE | re.S)


def doubleQuotedString():
    return _(r'".*?(?<!\\|/)"', re_flags=re.MULTILINE | re.S)


def codeString():
    return _(r'`.*?(?<!\\|/)`', re_flags=re.MULTILINE | re.S)


def string():
    return [singleQuotedString, doubleQuotedString]


def beginTag():
    return '['


def endTag():
    return ']'


def separator():
    return ws, ',', ws


def argument():
    return (
        [name, string],
        ar.Optional(
            ws,
            '=',
            ws,
            [name, string]
        )
    )


def arguments():
    return [args, argument]


def args():
    return (
        beginTag,
        ar.ZeroOrMore(arguments, sep=separator),
        ar.Optional(separator),
        ws,
        endTag
    )


def tag():
    return (ws, name, ws, ar.Optional(args), ws)


def tagSelected():
    return (
        beginTag,
        ar.OneOrMore(tag, sep=separator),
        ar.Optional(':', text),
        endTag
    )


def beginOneLineTag():
    return '[['


def oneLineTag():
    return (
        beginOneLineTag,
        ar.OneOrMore(tag, sep=separator),
        ar.Optional(':', textUntilNewLine)
    )


def text():
    return ar.ZeroOrMore([oneLineTag, tagSelected, codeString, plainText])


def textUntilNewLine():
    return ar.ZeroOrMore([
        oneLineTag,
        tagSelected,
        codeString,
        plainTextUntilNewLine
    ])


def entrypoint():
    return text, ar.EOF
