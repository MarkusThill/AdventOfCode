def tilt_north(lines):
    grid = list(map(list, zip(*lines)))  # Transpose, is more comfortable, but slower...
    for col_idx in range(len(grid)):
        rock_idx = 0
        while True:
            col = grid[col_idx]
            try:
                rock_idx = col.index("O", rock_idx + 1)
            except ValueError:
                break  # No more round rock which could be moved in this column
            try:  # find closest #-rock, north from the current round O-rock
                southest_ns = "".join(col).rindex("#", 0, rock_idx)
            except ValueError:
                southest_ns = 0  # Did not find any rock in the north
            try:  # Find first empty space after the #-rock
                new_rock_idx = col.index(".", southest_ns, rock_idx)
            except ValueError:
                new_rock_idx = rock_idx  # no empty space in the north
            grid[col_idx][rock_idx] = "."
            grid[col_idx][new_rock_idx] = "O"

    return list(map(list, zip(*grid)))  # Transpose back...


def rotate_right(grid):
    return [list(row) for row in zip(*grid[::-1])]


def compute_load(grid):
    return sum([(len(grid) - i) for i, r in enumerate(grid) for c in r if c == "O"])


def cycle(grid):
    for _ in range(4):
        grid = tilt_north(grid)
        grid = rotate_right(grid)
    return grid


def naive_cycle_detector(sequence):
    """
    Fast enough cycle detector for this problem.
    Detects the start 'mu' of the cycle and the cycle length 'lambda'.
    """
    for mu in range(len(sequence)):
        for lam in range(1, len(sequence) // 2 - mu):
            for i in range(len(sequence) - mu - lam):
                if sequence[mu + i] != sequence[mu + lam + i]:
                    break
            else:
                return mu, lam
    return None, None


def day14():
    file1 = open("2023/day14/input.txt", "r")
    lines = [list(l.strip()) for l in file1.readlines()]

    # Part 1:
    grid = tilt_north(lines)
    print(f"Solution Day 14.1: {compute_load(grid)}")

    # Part 2:
    n_cycle = 1000000000
    grid, load_values = lines.copy(), list()
    for _ in range(10000):
        grid = cycle(grid)
        load_values.append(compute_load(grid))
        mu, lam = naive_cycle_detector(load_values)
        if None not in {mu, lam}:
            break

    print(f"Solution Day 14.2: {load_values[-1 + mu + ((n_cycle - mu) % lam)]}")


if __name__ == "__main__":
    day14()
