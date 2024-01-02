def find_mirror(puzzle, ignore=-1):
    N = len(puzzle)
    n_matching_rows_max = 0
    ans = 0
    for x in range(N):
        if x == ignore - 1:
            continue
        i, j = x, x + 1
        n_matching_rows = 0
        while i >= 0 and j < N:
            if puzzle[i] != puzzle[j]:
                n_matching_rows = 0
                break
            i, j = i - 1, j + 1
            n_matching_rows += 1
        if n_matching_rows > n_matching_rows_max:
            ans = x + 1
            n_matching_rows_max = n_matching_rows

    return ans


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

    new_rows, new_cols = [], []
    for p, r, c in zip(puzzles, rows, cols):
        for i in range(len(p)):
            for j in range(len(p[0])):
                pp = list(p[i])
                pp[j] = "#" if pp[j] == "." else "."
                p[i] = "".join(pp)
                rr = find_mirror(p, ignore=r if r != 0 else -1)
                cc = find_mirror(
                    ["".join(column) for column in zip(*p)],
                    ignore=c if c != 0 else -1,
                )
                pp[j] = "#" if pp[j] == "." else "."
                p[i] = "".join(pp)

                if rr != 0 or cc != 0:
                    new_rows.append(rr)
                    new_cols.append(cc)
                    break
            if rr != 0 or cc != 0:
                break

    print(f"Solution Day 12.2: {100 * sum(new_rows) + sum(new_cols)}")


if __name__ == "__main__":
    day13()
