import logging
import re
from pathlib import Path

import lupa

LuaTable = lupa._lupa


class Lua:
    def __init__(self):
        self.lua = lupa.LuaRuntime(
            unpack_returned_tuples=True,
            register_eval=False,
            register_builtins=False,
            encoding='utf-8',
        )

        try:
            path = Path(__file__).with_name('libs')
            quirkbase = (path / 'quirkbase.lua').read_text()
            self.lua.execute(quirkbase)
        except lupa.LuaSyntaxError:
            raise Exception('Error while importing base functions.')

        self.lua.globals().def_scope.str = {
            'capitalize': str.capitalize,
            'casefold': str.casefold,
            'center': str.center,
            'count': str.count,
            'encode': str.encode,
            'endswith': str.endswith,
            'expandtabs': str.expandtabs,
            'find': str.find,
            'format': str.format,
            'isalnum': str.isalnum,
            'isalpha': str.isalpha,
            'isascii': str.isascii,
            'isdecimal': str.isdecimal,
            'isdigit': str.isdigit,
            'islower': str.islower,
            'isnumeric': str.isnumeric,
            'isprintable': str.isprintable,
            'isspaceisupper': str.isspace,
            'isupper': str.isupper,
            'ljust': str.ljust,
            'lower': str.lower,
            'lstrip': str.lstrip,
            'replace': str.replace,
            'rfind': str.rfind,
            'rindex': str.rindex,
            'rjust': str.rjust,
            'rsplit': str.rsplit,
            'rstrip': str.rstrip,
            'split': str.split,
            'splitlines': str.splitlines,
            'startswith': str.startswith,
            'strip': str.strip,
            'swapcase': str.swapcase,
            'title': str.title,
            'upper': str.upper
        }

        self.lua.globals().def_scope.re = re
        self.lua.globals().def_scope.getMatchGroup = lambda x, i: x.group(i)
        self.lua.globals().def_scope.iter = \
            lambda x: self.lua.globals().python.iter(list(str(x)))

        self.cloneScope = self.lua.globals().cloneScope
        self.compileCode = self.lua.globals().compileCode

        self.logger = logging.getLogger(__name__)

    def createScope(self):
        return self.cloneScope()

    @staticmethod
    def compileRegex(scope: LuaTable, name: str, regex: str):
        scope.regex[name] = re.compile(regex)

    def addToScope(self, base_scope, name: str, function, is_tmp: bool):
        if name:
            if is_tmp:
                base_scope._my[name] = function
            else:
                self.lua.globals().def_scope[name] = function
                base_scope[name] = function

    @staticmethod
    def reset_tmp_code(scope):
        scope._my = {}

    @property
    def baseScope(self):
        return self.lua.globals().def_scope
