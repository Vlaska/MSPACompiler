from __future__ import annotations

import logging
import sys
from pathlib import Path
from pkgutil import get_data
from typing import Tuple

import click
from MSPACompiler.textCompiler import TextCompiler
from loguru import logger
from fcache.cache import FileCache
from .mspac import mspac
import inspect


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
@click.option(
    '--verbose',
    '-v',
    is_flag=True,
    help='Enable verbose mode.'
)
def css(src, verbose, out, load_default):
    """Compile css present in tags"""
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

    compiler = TextCompiler()
    try:
        if load_default:
            default_definitions = get_data(
                'MSPACompiler', 'default/tags.mspa'
            ).decode('utf-8')
            compiler.load_tags(default_definitions)

        for i in src:
            data = Path(i).read_text('utf-8')
            compiler.load_tags(data)

        out_text = compiler.compile_css()
    except Exception:
        # logger.exception('t')
        exit(1)

    if out == '-':
        print(out_text)
    else:
        Path(out).write_text(out_text, 'utf-8')


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
def compile(
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
    import MSPACompiler
    import shutil
    src = Path(inspect.getfile(MSPACompiler)).parent / 'examples'
    shutil.copytree(src, Path().resolve() / 'examples', dirs_exist_ok=True)


@cli.command()
def default():
    """Copy default tags definitions to current folder"""
    default_definitions = get_data(
        'MSPACompiler', 'default/tags.mspa'
    )
    Path('./tags.mspa').write_bytes(default_definitions)
    click.echo('Written to "tags.mspa"')


@cli.command()
def clear():
    """Clear parsers cache"""
    c = FileCache(__name__)
    c.clear()
    c.close()
    click.echo("Cache cleared")


if __name__ == "__main__":
    cli()
