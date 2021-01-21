import click


@click.group()
def cli(input, output):
    pass


@click.command()
@click.argument("input", type=click.File('r'), nargs=1)
def test(input):
    pass


if __name__ == "__main__":
    cli()
