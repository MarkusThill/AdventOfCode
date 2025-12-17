from __future__ import annotations
import numpy as np


def count_nonzero_neighbors(A: np.ndarray) -> np.ndarray:
    """Count the number of non-zero 8-connected neighbors for each cell in a 2D array.

    For every element in the input array, this function counts how many of its
    eight surrounding neighbors (horizontal, vertical, and diagonal) are
    non-zero. The array is treated as zero-padded at the boundaries, meaning
    neighbors outside the array bounds are assumed to be zero.

    The center cell itself is not included in the count.

    Args:
        A: A 2D NumPy array. Any non-zero value is treated as an occupied cell.

    Returns:
        A 2D NumPy array of the same shape as `A`, where each element contains
        the number of non-zero neighbors of the corresponding input cell.
        The returned values range from 0 to 8.
    """
    A = (A != 0).astype(np.int8)  # ensure binary
    P = np.pad(A, 1, mode="constant")

    return (
        P[:-2, :-2]
        + P[:-2, 1:-1]
        + P[:-2, 2:]
        + P[1:-1, :-2]
        + P[1:-1, 2:]
        + P[2:, :-2]
        + P[2:, 1:-1]
        + P[2:, 2:]
    )


def day04_1(path: str = "2025/day04/input_1.txt", neighbors_less_than: int = 4) -> int:
    """Solve Day 04, Part 1.

    Reads a grid-based puzzle input from a text file and interprets `'@'` as an
    occupied cell and any other character as empty. For each occupied cell, the
    number of occupied 8-connected neighbors (including diagonals) is computed
    using zero-padded boundaries. The function counts how many occupied cells
    have a neighbor count strictly less than the given threshold.

    Args:
        path: Path to the input text file containing the grid.
        neighbors_less_than: Upper bound (exclusive) on the number of occupied
            neighbors for a cell to be counted.

    Returns:
        The number of occupied cells (`'@'`) whose number of occupied neighbors
        is strictly less than `neighbors_less_than`.
    """
    with open(path, "r", encoding="utf-8") as f:
        rows = [line.rstrip("\n") for line in f]

    # '@' -> 1, everything else -> 0
    grid = (np.array([list(r) for r in rows], dtype="U1") == "@").astype(np.uint8)

    neighbors = count_nonzero_neighbors(grid)
    return int(((neighbors < neighbors_less_than) & (grid != 0)).sum())


def day04_2(path: str = "2025/day04/input_1.txt", neighbors_less_than: int = 4) -> int:
    """Solve Day 04, Part 2 by iteratively removing sparse occupied cells.

    The input file is interpreted as a grid where `'@'` denotes an occupied
    cell and any other character denotes empty. In each iteration, all occupied
    cells with fewer than `neighbors_less_than` occupied 8-connected neighbors
    are removed simultaneously. The function returns the total number of cells
    removed across all iterations.

    Args:
        path: Path to the input text file containing the grid.
        neighbors_less_than: Upper bound (exclusive) on the number of occupied
            neighbors for a cell to be removed.

    Returns:
        Total number of removed occupied cells over all iterations.

    Raises:
        ValueError: If `neighbors_less_than` is negative.
    """
    if neighbors_less_than < 0:
        raise ValueError("neighbors_less_than must be >= 0")

    with open(path, "r", encoding="utf-8") as f:
        rows = [line.rstrip("\n") for line in f]

    # Parse to boolean grid (faster for logical ops)
    grid = (np.array([list(r) for r in rows], dtype="U1") == "@").astype(np.uint8)

    total_removed = 0
    while True:
        neighbors = count_nonzero_neighbors(grid)  # assumes 8-connected, zero-padded
        removable = (grid != 0) & (neighbors < neighbors_less_than)

        removed_this_round = int(removable.sum())
        if removed_this_round == 0:
            break

        total_removed += removed_this_round
        grid[removable] = 0  # remove simultaneously

    return total_removed


if __name__ == "__main__":
    result = day04_1()  # "2025/day04/example_1.txt"
    assert result == 1441, f"Real: {result} vs. Expected: {1441}"
    print("Solution for day04.1:", result)

    result = day04_2()  # "2025/day04/example_1.txt"
    assert result == 9050, f"Real: {result} vs. Expected: {9050}"
    print("Solution for day04.2:", result)
