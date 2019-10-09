import json
import logging
import re

import lupa

from .modules import strong, quirkbase


class QuirkSetter:
    def __init__(self):
        self.lua = lupa.LuaRuntime(
            unpack_returned_tuples=True,
            register_eval=False,
            register_builtins=False
        )

        try:
            self.lua.execute(strong)
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
        self.lua.globals().def_scope.iter =\
            lambda x: self.lua.globals().python.iter(list(str(x)))

        self.compileQuirk = self.lua.globals().compileQuirk
        self.sandbox = self.lua.globals().sandbox
        self.scopeReg = self.lua.globals().register
        self.getNewScope = self.lua.globals().cloneScope

        self.quirks = {}

        self.logger = logging.getLogger(__name__)

    def addQuirk(self, name, quirks):
        if name not in self.quirks:
            self.quirks[name] = self.getNewScope()

        def execute(func, *args):
            try:
                return func(*args)
            except lupa.LuaSyntaxError as e:
                self.logger.exception("Error: ")
                raise e

        t = type(quirks)
        if t == str:
            execute(self.compileQuirk, quirks, self.quirks[name])
        elif t == list:
            if len(quirks):
                for i in range(len(quirks)):
                    execute(self.compileQuirk, quirks[i], self.quirks[name], i + 1)
        elif t == dict:
            for k, v in quirks.items():
                execute(self.compileQuirk, v, self.quirks[name], k)

    def register(self, name, content):
        if name not in self.quirks:
            self.quirks[name] = self.getNewScope()

        assert type(content) is dict, 'Content to register must be provided '\
            'as dictionary'

        self.compileRegex(name, content.pop('regex', None))

        for k, v in content.items():
            self.scopeReg(v, self.quirks[name], k)

    def compileRegex(self, name, regex):
        if regex == None:
            return

        assert type(regex) is dict, 'Regex must be a dictionary'

        for k, v in regex.items():
            assert type(v) is str, 'Regex formula must be a string'
            self.quirks[name][k] = re.compile(v)

    def loadFromDict(self, _dict):
        assert type(_dict) is dict, 'Incorrect input'
        if 'quirks' in _dict:
            if 'register' in _dict:
                self.register(_dict['name'], _dict['register'])
            self.addQuirk(_dict['name'], _dict['quirks'])

    def loadFromList(self, _list):
        assert type(_list) is list, 'Incorrect input'

        for quirk in _list:
            self.loadFromDict(quirk)

    def processText(self, text, name, quirk=None):
        if name not in self.quirks:
            return text

        if quirk:
            assert quirk in self.quirks[name][
                'quirks'], f'There is no quirk function named "{quirk}"'
        else:
            quirk = next(iter(self.quirks[name]['quirks']))

        out = []
        try:
            for line in text.splitlines():
                out.append(self.sandbox(line, self.quirks[name], quirk))
            return '\n'.join(out)
        except lupa.LuaError as e:
            self.logger.exception('Error: ')
            raise e
