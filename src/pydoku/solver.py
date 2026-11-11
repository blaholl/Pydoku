from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .commands.solve.solve import Level
    from .objects import Board


class Solver:
    def __init__(self, board: Board) -> None:
        self.board: Board = board

    @classmethod
    def open(cls, puzzle_path: Path, level: Level, puzzle: int) -> Board:
        from .objects import Board

        board: Board = Board.from_puzzle(
            puzzle_path=puzzle_path, level=level, num=puzzle
        )
        board.populate()

        return cls(board)

    def solve(self) -> None:
        self.board.check_naked_single()
        self.board.check_hidden_single()
        self.board.check_naked_single()
        self.board.check_naked_double()
        self.board.check_naked_single()
