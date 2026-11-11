import click

from ..commands import solve


@click.group()
def cli() -> None:
    pass


cli.add_command(solve)
