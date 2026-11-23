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


def table(P, T) -> bool:
    nums = list(range(1, 10))
    can = [1, 2, 3, 4]
    sol = [5, 6, 7, 8, 9]
    return (P in nums and P != 1) or (T not in can) or (T in sol)


if __name__ == "__main__":
    truth_table(["P", "T"], table)
