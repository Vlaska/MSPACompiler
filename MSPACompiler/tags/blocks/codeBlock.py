from typing import Dict

from MSPACompiler.tags.blocks.innerBlock import InnerBlock


class CodeBlock(InnerBlock):
    """Block containing the code of the user defined tag
    """

    def __init__(self, argument_name: str, text_format: str):
        """Initialize code block

        Parameters
        ----------
        argument_name : `str`
            Name of the argument, by which the block deciedes, which function
            to run

        text_format : `str`
            String containing the placeholder for the text inside the tag, e.g.
            >>> {text}
            >>> begin {text} end
        """
        self.argument_name = argument_name
        self.text_format = text_format

    def __call__(self, text: str, arguments: Dict[str, str], codes) -> str:
        """Call a user defined function on the text provided in the tag

        Parameters
        ----------
        text : `str`
            Text, which is to be passed to the function

        arguments : `Dict[str, str]`
            Tags arguments

        codes : `List[Callable]`
            List of functions the tag has access to

        Returns
        -------
        `str`
            Text returned by function
        """
        if not (
                self.argument_name in arguments and
                (t := arguments[self.argument_name]).isdecimal()
        ):
            return text

        idx = int(t)
        if not (0 < idx < len(codes)):
            idx = 0
        t = self.text_format.format(
            text=text.format(
                **arguments,
                text=text
            )
        ).encode('utf-8')

        return codes[idx](t)
