from .exceptions import (  # noqa: I001
    EmptyCellError as EmptyCellError,
    IllegalAnswerError as IllegalAnswerError,
    PuzzleNotFoundError as PuzzleNotFoundError,
)

from .result import (
    Result as Result,
    Solved as Solved,
    Excluded as Excluded,
    NoOp as NoOp,
)

from .cli import cli as cli

from .logger import set_log as set_log
from .logger import set_cells as set_cells
from .logger import set_excluded as set_excluded
