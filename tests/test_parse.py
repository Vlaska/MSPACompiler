from textwrap import dedent

import pytest
from arpeggio import NoMatch
from TextCompiler.inputStringParser import parse


def test_1():
    ast = parse('[defines]')
    assert ast == [{'name': 'defines', 'content': [None], 'args': {}}]
    ast = parse('[[defines:')
    assert ast == [{'name': 'defines', 'content': [None], 'args': {}}]
    ast = parse('[[defines')
    assert ast == [{'name': 'defines', 'content': [None], 'args': {}}]


def test_2():
    ast1 = parse(
        '[[t :[under :Medium][under :Siedmioma Bramami]'
    )[0]
    assert type(ast1) is not str
    assert ast1['name'] == 't'
    assert ast1['args'] == {}
    assert len(ast1['content']) == 2
    assert ast1['content'][0] == {
        'name': 'under',
        'args': {},
        'content': ['Medium']
    }
    ast2 = parse(
        '[t :[under :Medium][under :Siedmioma Bramami]]'
    )[0]
    assert ast1 == ast2


@pytest.mark.parametrize(
    'bracket,value',
    [
        (r'\[', '['), (r'\]', ']'),
        (r'/[', '['), (r'/]', ']'),
        (r'\\[', r'\['), (r'\\]', r'\]'),
        (r'//[', '/['), (r'//]', '/]')
    ]
)
def test_3(bracket, value):
    ast = parse(bracket)[0]
    assert type(ast) is str
    assert ast == value


@pytest.mark.parametrize(
    'text',
    [
        '[test: test if i have to have closing bracket',
        '[t["\']]',
        '''[test:

        ''',
        '[:test]',
        '[ :test]',
        '[test',
        '[tag name with spaces]',
        '[[]',
        '[]]',
        '[ [:]',
        '[]',
        '[',
        '[[',
        '[[test[',
        '[test[]',
        '[test[[]]',
        '[test[]]',
        ']',
    ]
)
def test_4(text):
    with pytest.raises(NoMatch):
        parse(text)


def test_5():
    ast = parse(
        '[ define [test, [id=1, param="with space and []"], [extends=test1]]]'
    )[0]
    args = ast['args']
    assert ast['name'] == 'define'
    assert len(args) == 3
    assert args[0] == {'test': ''}
    assert args[1] == {'id': '1', 'param': 'with space and []'}
    assert args[2] == {'extends': 'test1'}


# def test_6():
#     ast = parse(
#             '[[1 :this tag can span only one line\n'
#             '[[2 :unless it has selected tag within [3 :then it can span '
#             'several\n'
#             '\n'
#             '\n'
#             'lines]'
#             '[[4 :back to single line\n'
#     )
#     assert len(ast) == 5
#     assert ast == ''
    # ast1, ast2, p2, ast3, p4
    # assert ast1 == {'name': 1, 'args': {}, 'content': [
    #     'this tag can span only one line']}
