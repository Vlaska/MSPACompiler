from arpeggio import RegExMatch as _
import arpeggio as ar


def space():
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


def singleQuote():
    return "'"


def doubleQuote():
    return '"'


def singleQuotedString():
    return singleQuote, _(r'(((?:\\|/)(?:\'))|([^\']))*'), singleQuote


def doubleQuotedString():
    return doubleQuote, _(r"(((?:\\|/)(?:\"))|([^\"]))*"), doubleQuote


def string():
    return [singleQuotedString, doubleQuotedString]


def beginTag():
    return _(r'(?<!\\|/)\[')


def endTag():
    return _(r'(?<!\\|/)\]')


def separator():
    return space, ',', space


def argument():
    return (
        [name, string],
        ar.Optional(
            space,
            '=',
            space,
            [name, string]
        )
    )


def arguments():
    return [argument, args]


def args():
    return (
        beginTag,
        ar.OneOrMore(arguments, sep=separator),
        ar.Optional(separator),
        space,
        endTag
    )


def tag():
    return (space, name, space, ar.Optional(args), space)


def tagSelected():
    return (
        beginTag,
        ar.OneOrMore(tag, sep=separator),
        ar.Optional(':', text),
        endTag
    )


def beginOneLineTag():
    return _(r'(?<!\\|/)\[\[')


def oneLineTag():
    return (
        beginOneLineTag,
        ar.OneOrMore(tag, sep=separator),
        ar.Optional(':', textUntilNewLine),
        ['\n', endTag, ar.EOF]
    )


def text():
    return ar.ZeroOrMore([oneLineTag, tagSelected, plainText])


def textUntilNewLine():
    return ar.ZeroOrMore([oneLineTag, tagSelected, plainTextUntilNewLine])


def entrypoint():
    return text, ar.EOF
