# Pydoku Sudoku Solver

[![CodeQL Advanced](https://github.com/blaholl/Pydoku/actions/workflows/codeql.yml/badge.svg)](https://github.com/blaholl/Pydoku/actions/workflows/codeql.yml)  [![Python application](https://github.com/blaholl/Pydoku/actions/workflows/python-app.yml/badge.svg)](https://github.com/blaholl/Pydoku/actions/workflows/python-app.yml)

> [!Note]
> The docs are not up-to-date for this project.

A complex, automated Sudoku puzzle solver that uses programmatic implementations of known Sudoku techniques rather than brute force.

## Goal
To create a Sudoku solver that relies solely on logic, rather than any sort of probability. The program will seek to implement this logic using an iterative, recursive application of the logic depending on board state.

## Test Status
Testing is based on running the application against puzzles taken from the `Good Sudoku` app.  In the `Good` section of the app, every tenth puzzle is a more difficult "skull" puzzle that still only uses the techniques appropriate to that puzzle's level.

The goal is to test against 100 games per category and then a further 100 "skull" games in each category.

Current results:
| Level | Successful Solves | Total puzzles | % |
| --- | --- | --- | --- |
| Beginner | 100 | 100 | 100% |
| Advanced | 100 | 100 | 100% |
| Expert | 100 | 100 | 100% |
| Pro | 100 | 100 | 100% |
| Impossible 1 (Core) | 19 | 30 | 64% |
| Impossible 2 (Extended) | - | - | - |
| Total | 419 | 430 | 97.44% |

# Techniques
### Beginner
* BiValue Cells
* Naked Single
* Hidden Single
* Naked Pair
* Locked Candidate
* Pointing Tuple

### Advanced
* Hidden Pair
* Naked Triple
* X-Wing

### Pro
* Hidden Triple
* Y-Wing
* Naked Quadruple

### Impossible 1 (Core)
* XYZ Wing
* Unique Rectangles Type 1
* Unique Rectangles Type 4a

## TODO
### Applications
* [ ] Replace current techniques with optimized verions
* [ ] Build out below techniques
* [ ] Convert exclusion returns to generator pipelines
* [ ] Logging

### Interface - ?
* [ ] Build basic Textual interface

### Techniques
* [ ] Define Pro techniques
    * [ ] Avoidable Rectangle
* [ ] Define Impossible 1 (Core) techniques
    * [ ] Hidden Quadruple
    * [ ] Unique Rectangle
        * [ ] Type 2
          * [ ] Type 2B
          * [ ] Type 2C
        * [ ] Type 3
          * [ ] Type 3B
        * [ ] Type 4B
        * [ ] Type 5
    * [ ] Hidden Rectangle
    * [ ] Swordfish
    * [ ] Jellyfish
* [ ] Define Impossible 2 (Extended) techniques
    * [ ] Skyscraper
    * [ ] 2-String Kite
    * [ ] Empty Rectangle
    * [ ] Color Chain
    * [ ] Finned X-Wing
    * [ ] Finned Swordfish
    * [ ] Finned Jellyfish
* [ ] Other techniques
    * [ ] Crane
    * [ ] 3d-Medusa
    * [ ] XY-Chain
    * [ ] AIC
    * [ ] W-Wing