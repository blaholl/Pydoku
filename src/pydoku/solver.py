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

    def cleanup(self) -> None:
        if self.board.check_naked_single():
            self.cleanup()

        if self.board.check_hidden_single():
            self.cleanup()

    def solve(self, rounds: int = 3) -> None:
        solved: bool = False
        round: int = 1
        while solved is False or round <= rounds:
            if self.board.verify():
                solved = True
                break

            res = self.run()
            if res is True:
                solved = True
                break

            if round >= rounds:
                break
            round += 1

        return self.board.verify()

    def run(self) -> None:
        self.cleanup()

        if self.board.check_naked_double():
            self.cleanup()

        if self.board.check_hidden_double():
            self.board.check_naked_double()
            self.cleanup()

        if self.board.check_locked_candidate():
            self.board.check_hidden_double()
            self.board.check_naked_double()
            self.cleanup()

        if self.board.check_pointing_tuple():
            self.board.check_hidden_double()
            self.board.check_naked_double()
            self.cleanup()

        if self.board.check_naked_triple():
            self.cleanup()

        if self.board.check_hidden_triple():
            self.cleanup()

        if self.board.check_x_wing():
            self.cleanup()

        if self.board.check_y_wing():
            self.cleanup()

        if self.board.verify():
            return True

    def mid_1(self) -> bool:
        techniques = [self.board.check_hidden_triple()]

        return any(techniques)
