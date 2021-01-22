from __future__ import annotations

import logging
import sys
from pathlib import Path
from pkgutil import get_data
from typing import Tuple

import click
from MSPACompiler.textCompiler import TextCompiler
from loguru import logger
from .mspac import mspac


@click.group()
def cli():
    pass


@cli.command()
@click.argument(
    'src',
    type=click.Path(exists=True, file_okay=True, dir_okay=False,
                    readable=True, resolve_path=True, allow_dash=False),
    nargs=-1,
)
@click.option(
    '--out',
    '-o',
    nargs=1,
    type=click.Path(writable=True, resolve_path=True, allow_dash=True),
    default='-',
    help='Name of the output file. STDOUT by default.'
)
@click.option(
    '--load-default',
    '-l',
    is_flag=True,
    help='Load default tag definitions.'
)
def css(src):
    """Compile css present in tags"""
    pass


@cli.command()
@click.argument(
    'src',
    type=click.Path(exists=True, file_okay=True, dir_okay=False,
                    readable=True, resolve_path=True, allow_dash=False),
    nargs=1,
)
@click.option(
    '--out',
    '-o',
    nargs=1,
    type=click.Path(writable=True, resolve_path=True, allow_dash=True),
    default='-',
    help='Name of the output file. STDOUT by default.'
)
@click.option(
    '--verbose',
    '-v',
    is_flag=True,
    help='Enable verbose mode.'
)
@click.option(
    '--load-default',
    '-l',
    is_flag=True,
    help='Load default tag definitions.'
)
@click.option(
    '--definitions',
    '-d',
    multiple=True,
    type=click.Path(writable=True, resolve_path=True, allow_dash=False)
)
@click.pass_context
def compiler(
    ctx,
    src: str,
    out: str,
    verbose: bool,
    load_default: bool,
    definitions: Tuple[str]
):
    """Compile tags to text"""
    ctx.invoke(
        mspac,
        src=src,
        out=out,
        verbose=verbose,
        load_default=load_default,
        definitions=definitions,
    )


@cli.command()
def examples():
    """Copy examples to current folder"""
    pass


@cli.command()
def default():
    """Copy default tags definitions ("tags.mspa" file) to current folder"""
    pass


@cli.command()
def clear():
    """Clear parsers cache"""
    pass


if __name__ == "__main__":
    cli()
