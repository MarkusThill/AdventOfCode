from itertools import pairwise


def is_safe(report: list[int]) -> bool:
    return all(-3 <= dd < 0 for dd in report) or all(0 < dd <= 3 for dd in report)


def sign(x: int) -> int:
    """
    Returns the sign of a number:
    - 1 if x is positive,
    - -1 if x is negative,
    - 0 if x is zero.

    Args:
        x (int): The number to evaluate.

    Returns:
        int: The sign of the number.
    """
    return (x > 0) - (x < 0)


def day02():
    with open("2024/day02/input_1.txt", "r") as file1:
        lines = file1.readlines()

    examples = [[int(ll) for ll in li.strip().split()] for li in lines]

    diffs = [[y - x for (x, y) in pairwise(row)] for row in examples]

    solution_1 = sum([is_safe(d) for d in diffs])
    solution_2 = sum(
        is_safe(d)
        or is_safe(d[1:])  # effectively removing first element
        or is_safe(d[:-1])  # effectively removing last element
        # Remove difference at index idx and add it to idx + 1:
        # (x1 - x0) (x2 - x1) (x3 - x2) (x4 - x3)
        #
        # Assume idx = 1:
        # (x1 - x0) (x2 - x1) + (x3 - x2) (x4 - x3)
        # --------------------------------------------
        # (x1 - x0) (x3 - x1) (x4 - x3) # effectively removed x2
        or any(
            is_safe(d[:idx] + [d[idx] + d[idx + 1]] + d[idx + 2 :])
            for idx in range(0, len(d) - 1)
            if sign(d[idx]) != sign(d[idx + 1])
        )
        for d in diffs
    )
    print("Solution Day 2.1:", solution_1)
    print("Solution Day 2.2:", solution_2)


if __name__ == "__main__":
    day02()
