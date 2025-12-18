from __future__ import annotations


from collections import deque


def day07_1(path: str = "2025/day07/input_1.txt") -> int:
    """Solve Day 07, Part 1.

    Simulates the downward propagation of a vertical beam through a 2D character
    grid. The grid contains a single beam source `'S'`, which emits a beam
    straight downward. As the beam propagates row by row, it may encounter
    splitter cells (`'^'`), which cause the beam to split horizontally.

    Grid semantics:
        - `'S'`: Beam source. Treated as an initial vertical beam.
        - `'^'`: Splitter. If a beam enters this cell from above, it splits into
          two new beams directed to the left and right on the next row.
        - Any other character: Empty or irrelevant; the beam continues straight
          downward.

    The simulation proceeds row by row until the bottom of the grid is reached
    or no active beams remain. Multiple beams may exist simultaneously, and all
    beam interactions are processed independently per row.

    Args:
        path: Path to the input text file containing the character grid.

    Returns:
        The number of splitter cells (`'^'`) that are hit from above by at least
        one beam during the simulation.

    Raises:
        ValueError: If the grid does not contain a beam source `'S'` in the first row.
    """
    with open(path, "r", encoding="utf-8") as f:
        grid = [line.rstrip("\n") for line in f]

    h = len(grid)
    w = len(grid[0]) if h else 0

    # Find the start position 'S' in the first row.
    si = 0
    sj = grid[0].find("S")
    if sj == -1:
        raise ValueError("No start 'S' found in the first row.")

    # Active beam positions are tracked as columns at the current row.
    active_cols: set[int] = {sj}

    n_splits = 0

    # Propagate from row si down to the last row.
    for i in range(si, h - 1):
        next_active: set[int] = set()

        for j in active_cols:
            ni = i + 1

            # Beam hits a splitter in the next row -> count + split left/right.
            if grid[ni][j] == "^":
                n_splits += 1
                if j - 1 >= 0:
                    next_active.add(j - 1)
                if j + 1 < w:
                    next_active.add(j + 1)
            else:
                # Otherwise it continues straight down.
                next_active.add(j)

        active_cols = next_active

        # Early exit: no beams left.
        if not active_cols:
            break

    return n_splits


def day07_2_infeasible(path: str = "2025/day07/input_1.txt") -> int:
    """Brute-force simulation for Day 07, Part 2 (infeasible for real input).

    This function performs an explicit breadth-first simulation of all beam
    paths through the grid. Starting from the beam source `'S'`, each beam
    position is enqueued and propagated row by row. When a beam encounters a
    splitter (`'^'`) in the next row, it branches into two new beams directed
    left and right; otherwise, it continues straight downward.

    Every distinct beam path is simulated independently until it reaches the
    bottom of the grid. The function counts how many beam paths reach the final
    row.

    This approach is computationally infeasible for the full puzzle input,
    because the number of active beam paths grows exponentially with grid
    height. The queue size quickly becomes enormous, making runtime and memory
    usage prohibitive. As a result, this implementation is only practical for
    very small grids and is intended primarily for:
        - validating results on the example input,
        - understanding the beam-splitting dynamics,
        - serving as a conceptual reference for a more efficient solution.

    Args:
        path: Path to the input text file containing the character grid.

    Returns:
        The total number of distinct beam paths that reach the bottom row
        of the grid.

    Raises:
        ValueError: If the grid does not contain a beam source `'S'`.

    Notes:
        - Time complexity is exponential in the number of splitter encounters.
        - A feasible solution requires reframing the problem as a counting or
          dynamic-programming problem rather than explicit path enumeration.
    """
    with open(path, "r", encoding="utf-8") as f:
        grid = [list(line.rstrip("\n")) for line in f]

    h = len(grid)
    w = len(grid[0]) if h else 0

    # Find the start position 'S'.
    start_pos = 0, grid[0].find("S")
    if start_pos[1] == -1:
        raise ValueError("No start 'S' found in the first row.")

    beam_queue: deque[tuple[int, int]] = deque([(start_pos)])

    time_line_counter = 0
    while beam_queue:
        si, sj = beam_queue.popleft()

        print("Current beam queue size:", len(beam_queue), "current index:", (si, sj))

        if si == h - 1:
            time_line_counter += 1
            # print("time_line_counter", time_line_counter)
            continue  # Reached bottom of grid

        # Beam hits a splitter in the next row -> count + split left/right.
        if grid[si + 1][sj] == "^":
            if sj - 1 >= 0:
                beam_queue.append((si + 1, sj - 1))
            if sj + 1 < w:
                beam_queue.append((si + 1, sj + 1))
        else:
            # Otherwise it continues straight down.
            beam_queue.append((si + 1, sj))

    return time_line_counter


def day07_2(path: str = "2025/day07/input_1.txt") -> int:
    """Solve Day 07, Part 2 via bottom-up dynamic programming.

    Assumes the beam source 'S' is located in the first row. The grid encodes
    whether a beam traveling downward will split when entering a cell on the
    next row:
      - If the cell below (i+1, j) is '^', paths from (i, j) branch to
        (i+1, j-1) and (i+1, j+1).
      - Otherwise, the path continues to (i+1, j).

    The DP is computed bottom-up. Let `dp_next[j]` be the number of ways to
    reach the bottom row starting from position (i+1, j). Then `dp_cur[j]` is
    derived from `dp_next` using the above transition. The answer is the number
    of ways starting at the column of 'S' in the top row.

    Args:
        path: Path to the input text file containing the character grid.

    Returns:
        The number of distinct beam paths from 'S' (top row) to the bottom row.

    Raises:
        ValueError: If 'S' is not found in the first row.
    """
    with open(path, "r", encoding="utf-8") as f:
        grid = [line.rstrip("\n") for line in f]  # keep as strings for fast indexing

    h = len(grid)
    w = len(grid[0]) if h else 0

    sj = grid[0].find("S")
    if sj == -1:
        raise ValueError("No start 'S' found in the first row.")

    # Base case: from any position on the bottom row, there is exactly one way
    # to "reach the bottom" (we are already there).
    dp_next = [1] * w

    # Build DP from row h-2 up to row 0.
    for i in range(h - 2, -1, -1):
        below = grid[i + 1]
        dp_cur = [0] * w

        # Interior columns (safe to access j-1 and j+1).
        for j in range(1, w - 1):
            dp_cur[j] = (
                dp_next[j - 1] + dp_next[j + 1] if below[j] == "^" else dp_next[j]
            )

        # Left boundary (j = 0).
        if w:
            dp_cur[0] = (dp_next[1] if w > 1 else 0) if below[0] == "^" else dp_next[0]

        # Right boundary (j = w-1).
        if w > 1:
            dp_cur[w - 1] = dp_next[w - 2] if below[w - 1] == "^" else dp_next[w - 1]

        dp_next = dp_cur

    # dp_next now corresponds to row 0.
    return dp_next[sj]


if __name__ == "__main__":
    result_1 = day07_1()  # "2025/day07/example_1.txt"
    assert result_1 == 1626, f"Real: {result_1} vs. Expected: {1626}"
    print("Solution for day07.1:", result_1)

    # Run the infeasible brute-force simulation on the example input only.
    if False:  # Turn off for benchmarking
        result_2 = day07_2("2025/day07/example_1.txt")
        print("Solution for day07.2 (example input):", result_2)
        assert result_2 == 40, f"Real: {result_2} vs. Expected: {40}"

    result_2 = day07_2()  # "2025/day07/example_1.txt"
    print("Solution for day07.2:", result_2)
    assert result_2 == 48989920237096, (
        f"Real: {result_2} vs. Expected: {48989920237096}"
    )
