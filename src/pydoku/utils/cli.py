import click

from ..__version__ import __version__
from ..commands import solve


@click.group()
@click.version_option(__version__)
def cli() -> None:
    pass


cli.add_command(solve)
