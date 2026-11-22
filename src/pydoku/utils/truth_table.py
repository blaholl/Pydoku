import itertools as it
from collections.abc import Callable


def truth_table(variables: list[str], expression: Callable) -> None:
    n = len(variables)
    print()
    header = " | ".join(str(i) for i in variables) + " | Result"
    print(header)
    print("-" * len(header))

    for v in it.product((True, False), repeat=n):
        env = dict(zip(variables, v))
        res = expression(**env)
        row = " | ".join(str(env[var])[0] for var in variables) + f" | {(str(res)[0])}"
        print(row)


def table(P, T, D) -> bool:
    return (P and D) or (T and not D)


if __name__ == "__main__":
    truth_table(["P", "T", "D"], table)
