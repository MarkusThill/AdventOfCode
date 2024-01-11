from collections import deque


def _diff(x):
    return [x[i] - x[i - 1] for i in range(1, len(x))]


def day21():
    n_steps_part_1, n_steps_part_2 = 64, 26501365

    file1 = open("2023/day21/input.txt", "r")
    lines = [l.strip() for l in file1.readlines()]
    G = [list(l) for l in lines]
    X, Y = len(G), len(G[0])

    start = [(x, y) for x, l in enumerate(lines) for y, e in enumerate(l) if e == "S"]
    assert len(start) == 1

    x_start, y_start = start[0]
    part_1(G, X, Y, x_start, y_start)

    G[x_start][y_start] = "."
    budget = X * 2  # 3->10 for the example_1.txt input
    state = (x_start, y_start, budget)

    q = deque()
    q.appendleft(state)
    visited, final_set = set(), dict()
    while q:
        x, y, b = state = q.pop()
        if state in visited:
            continue
        visited.add(state)
        if b not in final_set:
            final_set[b] = 0
        final_set[b] += 1
        if b == 0:
            continue

        # Compute after states
        for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny, nb = new_state = (x + i, y + j, b - 1)
            # if nx >= 0 and nx < X and ny >= 0 and ny < Y and nb >= 0:
            if G[nx % X][ny % Y] == "." and new_state not in visited:
                q.appendleft(new_state)

    # sols = []
    # for b in range(len(final_set)):
    #    # print(b, final_set[b])
    #    sols.append(final_set[b])
    # sols = list(reversed(sols))
    sols = list(reversed([final_set[b] for b in range(len(final_set))]))

    # print("Solution X:", sols[64])
    print(f"Solution Day 21.1: {sols[n_steps_part_1]}")

    xx = [x - y for x, y in zip(_diff(sols)[X:], _diff(sols)[:-X])]
    delta = xx[-X:]
    diff = [x - y for x, y in zip(sols[X:], sols[:-X])]

    b = n_steps_part_2 % X
    n_diff = (n_steps_part_2 - X * 0) // X
    n_delta = n_diff * (n_diff - 1) // 2  # 1 + 2 + 3 + ... + (n_diff - 1)
    solution_2 = sols[X * 0 + b] + n_diff * diff[X * 0 + b] + n_delta * sum(delta)
    print(f"Solution Day 21.2: {solution_2}")


def part_1(G, X, Y, x_start, y_start):
    G[x_start][y_start] = "."
    budget = 64
    state = (x_start, y_start, budget)

    q = deque()
    q.appendleft(state)
    visited, final_set = set(), set()
    while q:
        x, y, b = state = q.pop()
        if state in visited:
            continue
        if b == 0:
            final_set.add((x, y))
            continue
        visited.add(state)
        # Compute after states
        for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny, nb = new_state = (x + i, y + j, b - 1)
            if nx >= 0 and nx < X and ny >= 0 and ny < Y and nb >= 0:
                if G[nx][ny] == "." and new_state not in visited:
                    q.appendleft(new_state)

    print(f"Solution Day 21.1: {len(final_set)}")


if __name__ == "__main__":
    day21()
