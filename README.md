# Pydoku Sudoku Solver

[![CodeQL Advanced](https://github.com/blaholl/Pydoku/actions/workflows/codeql.yml/badge.svg)](https://github.com/blaholl/Pydoku/actions/workflows/codeql.yml)  [![Python application](https://github.com/blaholl/Pydoku/actions/workflows/python-app.yml/badge.svg)](https://github.com/blaholl/Pydoku/actions/workflows/python-app.yml)

A complex, automated Sudoku puzzle solver that uses programmatic implementations of known Sudoku techniques rather than brute force.

## Goal
To create a Sudoku solver that relies solely on logic, rather than any sort of probability. The program will seek to implement this logic using an iterative, recursive application of the logic depending on board state.

## Usage
Pydoku uses a JSON-file to store its puzzles as a list-of-lists. The file is organized with the `level` of the puzzle as the top-level key and numbered keys corresponding with puzzle.

### Solve
```python
Usage: pydoku solve [OPTIONS]

Options:
  -l, --level [beginner|advanced|expert|pro|impossible|extended]
                                  Level of the puzzle to retrieve.
  -p, --puzzle INTEGER            Number of the puzzle to retrieve under each
                                  top-level "level" key.
  -r, --rounds INTEGER            Number of rounds to run the parser.
  --help                          Show this message and exit.
```

## Test Status
Testing is based on running the application against puzzles taken from the `Good Sudoku` app.  In the `Good` section of the app, every tenth puzzle is a more difficult "skull" puzzle that still only uses the techniques appropriate to that puzzle's level.

The goal is to test against 100 games per category and then a further 100 "skull" games in each category.

Current results:
|  Complete | Level | Successful Solves | Total puzzles | % |
| --- | --- | --- | --- | --- |
| [x] | Beginner | 100 | 100 | 100% |
| [x] | Advanced | 100 | 100 | 100% |
| [ ] | Expert | 95 | 100 | 95% |
| [ ] | Pro | 4 | 100 | 4% |
| [ ] | Impossible 1 (Core) | - | 30 | - |
| [ ] | Impossible 2 (Extended) | - | - | - |
| [ ] | Total | 299 | 400 | 74.75% |

## Implemented Techniques

| 9 / 36 (25%) |
|-|

<details>
<summary>View</summary>

* BiValue Cells
* Naked Single
* Hidden Single
* Naked Pair
* Locked Candidate
* Pointing Tuple
* Hidden Pair
* Naked Triple
* Hidden Triple
</details>

## TODO
### Application
* [ ] Build remainder of techniques
* [ ] Logging
* [ ] CLI Options
* [ ] Add remaining Impossible 1 puzzles
* [ ] Add Impossible 2 puzzles

### Techniques

<details>
<summary>View</summary>

* [ ] Define Advanced Techniques (1)
  * [ ] X-Wing
* [ ] Define Expert Techniques (3)
  * [ ] Naked Quaruple
  * [ ] Y Wing
  * [ ] Avoidable Rectangle
* [ ] Define Pro techniques (2)
  * [ ] Avoidable Rectangle
  * [ ] XYZ Wing
* [ ] Define Impossible 1 (Core) techniques (13)
  * [ ] Hidden Quadruple
  * [ ] Unique Rectangle
      * [ ] Type 1
      * [ ] Type 2
        * [ ] Type 2B
        * [ ] Type 2C
      * [ ] Type 3
        * [ ] Type 3B
      * [ ] Type 4a
      * [ ] Type 4B
      * [ ] Type 5
  * [ ] Hidden Rectangle
  * [ ] Swordfish
  * [ ] Jellyfish
* [ ] Define Impossible 2 (Extended) techniques (7)
  * [ ] Skyscraper
  * [ ] 2-String Kite
  * [ ] Empty Rectangle
  * [ ] Color Chain
  * [ ] Finned X-Wing
  * [ ] Finned Swordfish
  * [ ] Finned Jellyfish
* [ ] Other techniques (10)
  * [ ] Crane
  * [ ] 3D-Medusa
  * [ ] XY-Chain
  * [ ] AIC
  * [ ] W-Wing
  * [ ] ALS
  * [ ] X-Cycle
  * [ ] Bi-Value Universal Grave (BUG+1)
  * [ ] Sue de Coq
  * [ ] Turbot Fish
</details>