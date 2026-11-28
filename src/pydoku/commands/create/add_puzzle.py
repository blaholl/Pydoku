import sys


def input_row(row_num: int) -> list[int]:
    row = input(f"Row {row_num} > ")

    match row.lower():
        case "q":
            sys.exit(0)
        case "help":
            print("help")
            sys.exit(0)
        case _:
            if not row.isnumeric():
                print("Invalid input, please try again.")
                input_row(row_num)

            valid_row = validate_row(row)
            if confirm_row(valid_row):
                return valid_row
            else:
                input_row(row_num)


def validate_row(row_str: str) -> list[int]:
    row = [i for i in row_str]

    if len(row) != 9:
        while len(row) < 9:
            row.append(0)

    row = [int(i) for i in row]
    return row


def confirm_row(valid_row: list[int]) -> bool:
    print(valid_row)
    confirmation: str = input("Confirm row? [y/n] > ")

    match confirmation.lower():
        case "y":
            return True
        case "n":
            return False
        case "q":
            sys.exit(0)
        case _:
            return True
