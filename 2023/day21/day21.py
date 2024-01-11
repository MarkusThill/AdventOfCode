from collections import deque


def diff(x):
    return [x[i] - x[i - 1] for i in range(1, len(x))]


def day21():
    n_steps_part_1, n_steps_part_2 = 64, 26501365
    n_grid_cycles = 2  # minimum 2, 10 for the example_1.txt input

    file1 = open("2023/day21/input.txt", "r")
    lines = [l.strip() for l in file1.readlines()]
    G = [list(l) for l in lines]
    X, Y = len(G), len(G[0])
    assert X == Y  # necessary for part 2 of the problem
    W = X

    start = [(x, y) for x, l in enumerate(lines) for y, e in enumerate(l) if e == "S"]
    assert len(start) == 1  # Should be only one starting point...
    x_start, y_start = start[0]
    budget = W * n_grid_cycles

    G[x_start][y_start] = "."
    state = (x_start, y_start, budget)

    q = deque()
    q.appendleft(state)
    visited, final_set = set(), [0] * (budget + 1)
    while q:
        x, y, cycle_offset = state = q.pop()
        if state in visited:
            continue
        visited.add(state)
        final_set[cycle_offset] += 1
        if cycle_offset == 0:
            continue

        # Compute after states, also works for part 1, since we never reach the edge
        for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny, nb = new_state = (x + i, y + j, cycle_offset - 1)
            if G[nx % X][ny % Y] == "." and new_state not in visited:
                q.appendleft(new_state)

    s = list(reversed([final_set[b] for b in range(len(final_set))]))  # solutions s[n]
    print(f"Solution Day 21.1: {s[n_steps_part_1]}")

    # Part 2:
    # An interesting oberservation is that after some time (certain number of steps)
    # we can observe a dependency between s[n] & s[n + W].
    # s[n + W] = s[n] + Δs_W[n]
    # TBC ...

    Δs_W = [x - y for x, y in zip(s[W:], s[:-W])]
    delta_ds = [x - y for x, y in zip(diff(s)[W:], diff(s)[:-W])][-W:]

    cycle_idx, cycle_offset = n_grid_cycles - 2, n_steps_part_2 % W
    s_start_idx = W * cycle_idx + cycle_offset
    n_diff = (n_steps_part_2 - W * cycle_idx) // W
    n_delta = n_diff * (n_diff - 1) // 2  # 1 + 2 + 3 + ... + (n_diff - 1)
    solution_2 = (
        s[s_start_idx]  # start with this pre-computed solution
        + n_diff * Δs_W[s_start_idx]  # add the difference
        + n_delta * sum(delta_ds)
    )
    print(f"Solution Day 21.2: {solution_2}")


if __name__ == "__main__":
    day21()
