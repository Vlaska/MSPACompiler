import lupa
import logging
import json
import re


class Quirk:
    def __init__(self):
        self.lua = lupa.LuaRuntime(
            unpack_returned_tuples=True,
            register_eval=False,
            register_builtins=False
        )

        try:
            self.lua.eval('require "quirkbase"')
        except lupa.LuaSyntaxError:
            raise Exception('Error while importing "quirkbase.lua"')

        # def __iter(x):
            # if type(x) != str:
            # raise Exception("Only string can be iterated!")

            # return self.lua.globals().python.iter(list(str(x)))

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
        self.lua.globals().def_scope.iter = lambda x: self.lua.globals().python.iter(list(str(x)))
        # self.lua.globals().def_scope.iter = __iter
        # self.lua.globals().def_scope.iter = lambda x: self.lua.globals().python.iter(list(x))

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
            for i in range(len(quirks)):
                execute(self.compileQuirk, quirks[i], self.quirks[name], i + 1)
        elif t == dict:
            for k, v in quirks.items():
                execute(self.compileQuirk, v, self.quirks[name], k)

    def addQuirks(self, quirks):
        assert type(quirks) == dict, 'Incorect value'
        # if type(quirks) != dict:
        #     raise Exception('Incorrect value')

        for k, v in quirks.items():
            self.addQuirk(k, v)

    def register(self, name, content):
        if name not in self.quirks:
            self.quirks[name] = self.getNewScope()

        t = type(content)
        if t == dict:
            self.compileRegex(name, content.pop('regex', None))

            for k, v in content.items():
                self.scopeReg(v, self.quirks[name], k)
        else:
            raise Exception(
                'Content to register must be provided as dictionary'
            )

    def compileRegex(self, name, regex):
        if regex == None:
            return
        elif type(regex) != dict:
            raise Exception('Regex must be a dictionary')

        for k, v in regex.items():
            if type(v) != str:
                raise Exception('Regex formula must be a string')
            self.quirks[name][k] = re.compile(v)

    def loadFromDict(self, _dict):
        if 'register' in _dict:
            self.register(_dict['name'], _dict['register'])
        self.addQuirk(_dict['name'], _dict['quirks'])

    def processText(self, text, name, quirk=None):
        if name not in self.quirks:
            raise Exception(f'There is no quirk named "{name}"')

        if quirk:
            if quirk not in self.quirks[name]['quirks']:
                raise Exception(f'There is no quirk function named "{quirk}"')
        else:
            quirk = next(iter(self.quirks[name]['quirks']))

        try:
            return self.sandbox(text, self.quirks[name], quirk)
        except lupa.LuaError as e:
            self.logger.exception('Error: ')
            raise e


with open('./quirks/gamzee.json', 'r', encoding='utf-8') as f:
    t = json.load(f)

# print(list(q.quirks['karkat'].quirks))
q = Quirk()
q.loadFromDict(t)

with open('./quirks/karkat.json', 'r', encoding='utf-8') as f:
    t = json.load(f)

q.loadFromDict(t)

# print(q.parseText("to jest testowy tekst :o)", 'gamzee'))
print(q.processText("To jest testowy tekst numer 1 :o)", 'gamzee'))
print(q.processText("to jest testowy tekst numer 2 :o)", 'gamzee'))
print(q.processText("mogę w locie zmienić styl pisania autora", 'gamzee', 3))
print(q.processText("oraz zapamiętać wartości z poprzednich lini", 'gamzee', 3))
print(q.processText("tak jak teraz", 'gamzee', 3))
# print(q.parseText("mogę też zmienić autora tekstu, a formatowanie dostosuje się do tego", 'karkat'))
