from MSPACompiler.textCompiler import TextCompiler
import pytest
from MSPACompiler import lua
from lupa import LuaError


def test_lua_load(monkeypatch):
    code = b';kjnbgdfropij12opj0239-dfg]poawfddszf'
    monkeypatch.setattr(lua, 'get_data', lambda *args, **kwargs: code)

    with pytest.raises(Exception, match='initializing lua interpreter'):
        lua.Lua()


def test_2(u_compiler: TextCompiler):
    text = '''[defines:
    [defcode:1]
    [defcode[]:1]
    [defcode[[]]:1]
    [defcode[a]]
    [defcode[b]:[test]]
    [defcode[c] :` function (text) return "1. " .. text end`]
    [defcode[d] :` function (text) return "2. " .. text end`]
    [defcode[c] :` function (text) return "3. " .. text end`]
]'''
    u_compiler.load_tags(text)
    result = u_compiler.compile('''[defines:
    [defcode[c] :` function (text) return "4. " .. text end`]
    [defcode[e] :` function (text) return "5. " .. text end`]
    [define[test, [q=0], []]:
        [defcode: c]
        [defcode: d]
        [defcode: _my.c]
        [defcode: _my.e]
        [text:[code[q]:{text}]]
    ]
    [define[test1, [], []]: [defcode: c] [text :[code[a]:{text}]]]
    [define[test2, [a], []]: [defcode: c] [text :[code[a]:{text}]]]
]
[test:test]
[test[q=1]:test]
[test[q=2]:test]
[test[q=3]:test]
[test[q=4]:test]
a: [test1:test]
b: [test2[a="test"]:test]
''')
    assert len(u_compiler.base_tag.lua_scope._my) == 0
    assert u_compiler.base_tag.lua_scope.c
    assert u_compiler.base_tag.lua_scope.d
    assert '3. test' in result
    assert '2. test' in result
    assert '4. test' in result
    assert '5. test' in result
    assert 'a: test' in result
    assert 'b: test' in result


def test_3(u_compiler: TextCompiler):
    with pytest.raises(Exception):
        u_compiler.compile(
            '''[defines:
        [define[test, [a=1], []]:
            [defcode :` function (text)
                1 + "a"
                return text
            end`]]
            [text :[code[a]]]
            ][test:text]'''
        )
    # with pytest.raises(LuaError):
    u_compiler.load_tags(
        '''[defines:
        [define[test, [a=1], []]:
            [defcode :` function (text)
                t = text / 0
                return text .. " test"
            end`]
            [text :[code[a]:{text}]]
        ]
    ]'''
    )
    with pytest.raises(LuaError, match="attempt to perform arithmetic"):
        u_compiler.compile('[test:text]')


def test_4(u_compiler: TextCompiler):
    u_compiler.load_tags('''[defines:
    [define[test, [q=1]]:
        [defcode :` function (text) return string.reverse(text) end`]
        [text :example [code[q] :{text} end]]
    ]
]''')
    assert u_compiler.compile('[test:begin]') == 'example dne nigeb'
