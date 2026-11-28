import click

from ..__version__ import __version__
from ..commands import add, solve


@click.group(name="Pydoku")
@click.version_option(__version__)
def cli() -> None:
    """

    \b
     _____  __   __ ______   _____  _     _ _     _
    |_____]   \_/   |     \ |     | |____/  |     |
    |          |    |_____/ |_____| |    \_ |_____|
    """  # noqa: W605


cli.add_command(solve)
cli.add_command(add)
