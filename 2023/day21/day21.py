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
    # Δs_W[n] = s[n + W] - s[n] (ABCD)
    # ds[n] = s[n + 1] - s[n] # TODO: ds -> D
    #
    # Δds_W[n] = ds[n + W] - ds[n] = ds[n + kW] - ds[n + (k-1)W] = const.
    #
    # ds[n + kW] = ds[n + (k-1)W] + Δds_W[n]
    #            = ds[n + (k-2)W] + Δds_W[n] + Δds_W[n] = ds[n + (k-2)W] + 2*Δds_W[n]
    #            = ds[n + (k-3)W] + Δds_W[n] + Δds_W[n] + Δds_W[n] = ds[n + (k-3)W] + 3*Δds_W[n]
    #            = ...
    #            = ds[n + (0)W] + Δds_W[n] + ... + Δds_W[n]
    #            = ds[n] + kΔds_W[n]
    # ds[n] = ds[n - W] + Δds_W[n] # TODO: needed anywhere?
    #

    #
    # s[n + 1] = s[n] + ds[n]
    # s[n + 2] = s[n + 1] + ds[n + 1] = s[n] + ds[n] + ds[n + 1]
    # s[n + 3] = s[n + 2] + ds[n + 2] = s[n + 1] + ds[n + 1] + ds[n + 2] = s[n] + ds[n] + ds[n + 1] + ds[n + 2]
    # ...
    # s[n + W] = s[n] + ds[n] + ds[n + 1] + ds[n + 2] + ... + ds[n + W - 1]
    #          = s[n] + Σ_{w=0..W-1}{ ds[n + w] }
    #          = s[n] + Δs_W[n] (see above) # TODO: Coeffizientenvergleich mit erster Formel
    #
    # using rearanged eq. (ABCD):
    #         s[n + W] = s[n] + Δs_W[n] (QWERTZ)
    #
    # s[n + 2W] = s[n] + Σ_{w=0..2W-1}{ ds[n + w] }
    #           = s[n] + Σ_{w=0..W-1}{ ds[n + w] } + Σ_{w=0..W-1}{ ds[n + w + W] }
    #           = s[n] + R(n, 0) + R(n, 1) # TODO
    #           = s[n] + Σ_{w=0..W-1}{ ds[n + w] } + Σ_{w=0..W-1}{ ds[n + w] + Δds_W[n + w] }
    #           = s[n] + Σ_{w=0..W-1}{ ds[n + w] } + Σ_{w=0..W-1}{ ds[n + w] } + Σ_{w=0..W-1}{ Δds_W[n + w] }
    #           = s[n] +         Δs_W[n]           +         Δs_W[n]           + Σ_{w=0..W-1}{ Δds_W[n + w] }
    #
    # with:
    # R(n, k) = Σ_{w=0..W-1}{ ds[n + w + kW] }
    #         = Σ_{w=0..W-1}{ ds[n + w] + kΔds_W[n + w] }
    #         = Σ_{w=0..W-1}{ ds[n + w] } + Σ_{w=0..W-1}{ kΔds_W[n + w] }
    #         = Δs_W[n] + k*Σ_{w=0..W-1}{ Δds_W[n + w] }
    #
    # s[n + kW] = s[n] + Σ_{w=0..kW-1}{ ds[n + w] }
    #           = s[n] + Σ_{w=0..W-1}{ ds[n + w] } + Σ_{w=0..W-1}{ ds[n + w + W] } + Σ_{w=0..W-1}{ ds[n + w + 2W] } + ... + Σ_{w=0..W-1}{ ds[n + w + (k-1)W] }
    #           = s[n] +

    Δs_W = [x - y for x, y in zip(s[W:], s[:-W])]
    Δds_W = [x - y for x, y in zip(diff(s)[W:], diff(s)[:-W])][-W:]

    cycle_idx, cycle_offset = n_grid_cycles - 2, n_steps_part_2 % W
    s_start_idx = W * cycle_idx + cycle_offset
    n_diff = (n_steps_part_2 - W * cycle_idx) // W
    n_delta = n_diff * (n_diff - 1) // 2  # 1 + 2 + 3 + ... + (n_diff - 1)
    solution_2 = (
        s[s_start_idx]  # start with this pre-computed solution
        + n_diff * Δs_W[s_start_idx]  # add the difference
        + n_delta * sum(Δds_W)
    )
    print(f"Solution Day 21.2: {solution_2}")


if __name__ == "__main__":
    day21()

    # s[n + W] = s[n] + Δs_W[n]
    # s[n + 2W] = s[n+W] + Δs_W[n + W]
    #           = s[n] + Δs_W[n] + Δs_W[n + W]
    #
    # ds[n - 1] = s[n] - s[n - 1]
    # s[n] = s[n - 1] + ds[n - 1]
    # s[n - 1] = s[n - 2] + ds[n - 2]
    # s[n - k] = s[n - k - 1] + ds[n - k -1]
    # s[n] = s[n - 1] + ds[n - 1] =  s[n - 2] + ds[n - 2] + ds[n - 1] = s[n - W] + ds[n - W] + ... + ds[n - 2] + ds[n - 1]
    #      = s[n - W] + Σ_w{ds[n - w]}
    # ds[n + W] = ds[n] + Δds_W[n % W]
    # s[n + 1] = s[n] + ds[n]
    #
