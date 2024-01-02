def find_mirror(puzzle, ignore=-1):
    N = len(puzzle)
    for x in range(0, N - 1):
        if x == ignore - 1:
            continue
        i, j = x, x + 1
        while i >= 0 and j < N:
            if puzzle[i] != puzzle[j]:
                break
            i, j = i - 1, j + 1
        if i < 0 or j >= N:
            return x + 1

    return 0


def find_mirror(puzzle, ignore=-1, fix_smudge=False):
    N = len(puzzle)
    for x in range(0, N - 1):
        if x == ignore - 1:
            continue
        i, j = x, x + 1
        fs = fix_smudge
        while i >= 0 and j < N:
            d = sum(c1 != c2 for c1, c2 in zip(puzzle[i], puzzle[j]))
            if not fs and d > 0 or d > 1:
                break
            if d == 1 and fs:
                fs = False

            i, j = i - 1, j + 1
        if i < 0 or j >= N:
            return x + 1

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

    rows = [find_mirror(p) for p in puzzles]
    cols = [find_mirror(["".join(column) for column in zip(*p)]) for p in puzzles]

    print(f"Solution Day 12.1: {100 * sum(rows) + sum(cols)}")

    # new_rows, new_cols = [], []
    # for p, r, c in zip(puzzles, rows, cols):
    #     for i in range(len(p)):
    #         for j in range(len(p[0])):
    #             pp = list(p[i])
    #             pp[j] = "#" if pp[j] == "." else "."
    #             p[i] = "".join(pp)
    #             rr = find_mirror(p, ignore=r if r != 0 else -1)
    #             cc = find_mirror(
    #                 ["".join(column) for column in zip(*p)],
    #                 ignore=c if c != 0 else -1,
    #             )
    #             pp[j] = "#" if pp[j] == "." else "."
    #             p[i] = "".join(pp)

    #             if rr != 0 or cc != 0:
    #                 new_rows.append(rr)
    #                 new_cols.append(cc)
    #                 break
    #         if rr != 0 or cc != 0:
    #             break

    # print(f"Solution Day 12.2: {100 * sum(new_rows) + sum(new_cols)}")

    new_rows, new_cols = [], []
    for p, r, c in zip(puzzles, rows, cols):
        rr = find_mirror(p, ignore=r if r != 0 else -1, fix_smudge=True)
        cc = find_mirror(
            ["".join(column) for column in zip(*p)],
            ignore=c if c != 0 else -1,
            fix_smudge=True,
        )
        if rr != 0 or cc != 0:
            new_rows.append(rr)
            new_cols.append(cc)

    print(f"Solution Day 12.2: {100 * sum(new_rows) + sum(new_cols)}")


if __name__ == "__main__":
    day13()
