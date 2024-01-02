def find_mirror(puzzle, ignore=-1, fix_smudge=False):
    N = len(puzzle)
    for x in range(0, N - 1):
        if x == ignore:
            continue  # allow to ignore mirror of part 1, since we need a new one
        i, j = x, x + 1
        fs = fix_smudge
        while i >= 0 and j < N:
            d = sum(c1 != c2 for c1, c2 in zip(puzzle[i], puzzle[j]))
            if not fs and d > 0 or d > 1:
                break
            fs &= not (d == 1 and fs)  # allow to fix smudge exactly once
            i, j = i - 1, j + 1
        else:
            return x + 1  # found the mirror...

    return 0


def day13():
    file1 = open("2023/day13/input.txt", "r")
    lines = [l.strip() for l in file1.readlines()]
    puzzles = [[]]
    for l in lines:
        if l == "":
            puzzles.append([])
            continue
        puzzles[-1].append(l)

    T = lambda p: ["".join(column) for column in zip(*p)]  # Tranpose puzzle

    #
    # Part 1:
    #
    rows_1, cols_1 = zip(*[(find_mirror(x) for x in [p, T(p)]) for p in puzzles])
    print(f"Solution Day 13.1: {100 * sum(rows_1) + sum(cols_1)}")

    # ========
    # Part 2:
    #
    rows_2, cols_2 = zip(
        *[
            (find_mirror(*x, fix_smudge=True) for x in [(p, r - 1), (T(p), c - 1)])
            for p, r, c in zip(puzzles, rows_1, cols_1)
        ]
    )
    print(f"Solution Day 13.2: {100 * sum(rows_2) + sum(cols_2)}")


if __name__ == "__main__":
    day13()
