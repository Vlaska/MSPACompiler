from typing import Dict

from TextCompiler.tags.blocks.innerBlock import InnerBlock


class IfBlock(InnerBlock):
    """Block, that if an argument is present, returns it's value
    """

    def __init__(self, arg_name: str, ret_val: str = None):
        """Initialize the block

        Parameters
        ----------
        arg_name : `str`
            Name of the argument, for which to return it's value

        ret_val : `str`, optional
            Value to return, by default `None`
        """
        super().__init__()
        self.arg_name = arg_name
        self.ret_val = ret_val

    def __call__(self, arguments: Dict[str, str]) -> str:
        """Check if argument is present, and return stored value if it is

        Parameters
        ----------
        arguments : `Dict[str, str]`
            Tags arguments

        Returns
        -------
        `str`
            Stored value
        """
        return self.ret_val \
            if (self.arg_name in arguments and arguments[self.arg_name]) \
            else ''


class IfNotBlock(IfBlock):
    """Invers of the `IfBlock`, a.k.a. return it's value, if an argument is
    absent

    See also
    --------
    `IfBlock`
    """

    def __call__(self, arguments: Dict[str, str]):
        """Check if argument is present, and return stored value if it is not

        Parameters
        ----------
        arguments : `Dict[str, str]`
            Tags arguments

        Returns
        -------
        `str`
            Stored value
        """
        return self.ret_val \
            if not(self.arg_name in arguments and arguments[self.arg_name]) \
            else ''
