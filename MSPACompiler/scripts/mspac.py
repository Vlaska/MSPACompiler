from __future__ import annotations

import logging
import sys
from pathlib import Path
from pkgutil import get_data
from typing import Tuple

import click
from MSPACompiler.textCompiler import TextCompiler
from loguru import logger


@click.command()
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
def mspac(
    src: str,
    out: str,
    verbose: bool,
    load_default: bool,
    definitions: Tuple[str]
):
    if verbose:
        verbosity_level = 'INFO'
    else:
        verbosity_level = 'ERROR'
    logger.remove()
    logger.add(
        sys.stderr,
        level=verbosity_level,
        format='<level>{level}</level>: {message}'
    )

    src_file = Path(src)
    if src_file.stat().st_size == 0:
        exit(0)

    compiler = TextCompiler()
    try:
        if load_default:
            default_definitions = get_data(
                'MSPACompiler', 'default/tags.mspa'
            ).decode('utf-8')
            compiler.load_tags(default_definitions)

        for i in definitions:
            data = Path(i).read_text('utf-8')
            compiler.load_tags(data)

        out_text = compiler.compile(src_file.read_text('utf-8'))
    except Exception:
        # logger.exception('t')
        exit(1)

    if out == '-':
        print(out_text)
    else:
        Path(out).write_text(out_text, 'utf-8')


if __name__ == "__main__":
    mspac()
