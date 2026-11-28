import logging
from pathlib import Path
from typing import TYPE_CHECKING

from .utils.logger import set_log

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

    def cleanup(self) -> bool:
        if self.board.check_naked_single():
            self.cleanup()

        if self.board.check_hidden_single():
            self.cleanup()

        return self.board.verify()

    def solve(self, rounds: int = 3) -> None:
        solved: bool = False
        round: int = 1
        while solved is False or round <= rounds:
            set_log(msg=f"Round {round}/{rounds}", level=logging.INFO, fn="solve")
            if self.board.verify():
                solved = True
                set_log(msg="Puzzle solved", level=logging.INFO, fn="solve")
                break

            set_log(msg="Executing puzzle solver", level=logging.INFO, fn="solve")
            res = self.run()
            if res is True:
                solved = True
                set_log(msg="Puzzle solved", level=logging.INFO, fn="solve")
                break

            set_log(msg="Executing mid game techniques", level=logging.INFO, fn="solve")
            res = self.mid_1()
            if res is True:
                solved = True
                set_log(msg="Puzzle solved", level=logging.INFO, fn="solve")
                break

            if round >= rounds:
                set_log(
                    msg=f"Max rounds ({rounds}) exceeded",
                    level=logging.INFO,
                    fn="solve",
                )
                break
            round += 1

        return self.board.verify()

    def run(self) -> None:
        if self.cleanup():
            return True

        if self.board.check_naked_double():
            if self.cleanup():
                return True
            else:
                pass

        if self.board.check_hidden_double():
            self.board.check_naked_double()
            if self.cleanup():
                return True
            else:
                pass

        if self.board.check_locked_candidate():
            self.board.check_hidden_double()
            self.board.check_naked_double()
            if self.cleanup():
                return True
            else:
                pass

        if self.board.check_pointing_tuple():
            self.board.check_hidden_double()
            self.board.check_naked_double()
            if self.cleanup():
                return True
            else:
                pass

        if self.board.check_naked_triple():
            if self.cleanup():
                return True
            else:
                pass

        if self.board.check_hidden_triple():
            if self.cleanup():
                return True
            else:
                pass

        if self.board.check_x_wing():
            if self.cleanup():
                return True
            else:
                pass

        if self.board.check_y_wing():
            if self.cleanup():
                return True
            else:
                pass

        return False

    def mid_1(self) -> bool:
        if self.board.check_hidden_triple():
            if self.cleanup():
                return True
            else:
                pass

        return False
