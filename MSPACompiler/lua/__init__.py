import re
from pkgutil import get_data
from loguru import logger

import lupa

LuaTable = lupa._lupa


class Lua:
    """Class for interacting with Lua interpreter
    """

    def __init__(self):
        """Initialize Lua interpretter.

        Raises
        ------
        Exception
            `quirkbase.lua` containes errors
        """
        self.lua = lupa.LuaRuntime(
            unpack_returned_tuples=True,
            register_eval=False,
            register_builtins=False,
            encoding='utf-8',
        )

        try:
            quirkbase = get_data(
                __name__, 'libs/quirkbase.lua'
            ).decode('utf-8')
            self.lua.execute(quirkbase)
        except Exception:
            logger.critical('Error while initializing lua interpreter.')
            raise Exception('Error while initializing lua interpreter.')

        # Allow lua access to the python string methods
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

        # Allow lua access to regex
        self.lua.globals().def_scope.re = re
        self.lua.globals().def_scope.getMatchGroup = lambda x, i: x.group(i)

        # Iterattor for texts with unicode characters
        self.lua.globals().def_scope.iter = \
            lambda x: self.lua.globals().python.iter(list(str(x)))

        # Lua function for creating new lua scope based on existing one
        self.cloneScope = self.lua.globals().cloneScope

        # Lua function to compile new function
        self.compileCode = self.lua.globals().compileCode

    def create_scope(self) -> LuaTable:
        """Create new lua scope

        Returns
        -------
        LuaTable
            New lua scope
        """
        return self.cloneScope()

    @staticmethod
    def compile_regex(scope: LuaTable, name: str, regex: str):
        """Compile regex for use inside of lua functions

        Parameters
        ----------
        scope : `LuaTable`
            Scope, in which compiled regex is to be used

        name : `str`
            Name of the regex

        regex : `str`
            Regex expression
        """
        scope.regex[name] = re.compile(regex)

    def add_to_scope(self, base_scope, name: str, function, is_tmp: bool):
        """Add function to the lua scope

        Parameters
        ----------
        base_scope : `LuaTable`
            BaseTag lua scope

        name : `str`
            Name under which the function will be available in the scope

        function : `Callable`
            Function to be added to the scope

        is_tmp : `bool`
            Does this function come from temporary tag? If yes, it can be
            accessed using `_my.[name]`
        """
        if name:
            if is_tmp:
                base_scope._my[name] = function
            else:
                self.lua.globals().def_scope[name] = function
                base_scope[name] = function

    @staticmethod
    def reset_tmp_code(scope):
        """Discard temporary functions

        Parameters
        ----------
        scope : `LuaTable`
        """
        scope._my = {}

    @property
    def base_scope(self):
        """Return the source base lua scope

        Returns
        -------
        `LuaTable`
            Source base lua scope
        """
        return self.lua.globals().def_scope
