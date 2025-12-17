from __future__ import annotations

from bisect import bisect_right


def normalize(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Normalize a list of closed integer intervals.

    Sorts the input intervals by their start value and merges all overlapping
    or directly adjacent intervals (i.e., intervals where `next_lo <= prev_hi + 1`).

    Args:
        intervals: A list of closed integer intervals represented as
            `(lo, hi)` tuples, where `lo <= hi`.

    Returns:
        A list of non-overlapping, normalized closed intervals, sorted by
        ascending start value.
    """
    # Sort intervals lexicographically: first by `lo`, then by `hi`.
    intervals = sorted(intervals)

    # We build merged intervals incrementally from left to right.
    merged: list[list[int]] = []

    for lo, hi in intervals:
        # Start a new interval if this one is disjoint from the previous.
        if not merged or lo > merged[-1][1] + 1:
            merged.append([lo, hi])
        else:
            # Otherwise, extend the previous interval if necessary.
            if hi > merged[-1][1]:
                merged[-1][1] = hi

    # Convert back to immutable tuples for the public API.
    return [(lo, hi) for lo, hi in merged]


def contains(x: int, intervals: list[tuple[int, int]], starts: list[int]) -> bool:
    """Check whether a value lies within any normalized interval.

    Uses binary search over the interval start points to locate the candidate
    interval in O(log n) time.

    Args:
        x: The value to test.
        intervals: A list of normalized, non-overlapping closed intervals.
        starts: A list of interval start values (`lo`), extracted from
            `intervals` and sorted in the same order.

    Returns:
        True if `x` lies inside any interval in `intervals`, False otherwise.
    """
    # Find the index of the rightmost interval whose start <= x.
    i = bisect_right(starts, x) - 1

    # Check whether x is within the bounds of that interval.
    return i >= 0 and x <= intervals[i][1]


def day05(path: str = "2025/day05/input_1.txt") -> tuple[int, int]:
    """Solve Day 05, Parts 1 and 2.

    The input file consists of two sections separated by an empty line:
    - A list of closed integer intervals in the form "lo-hi"
    - A list of integer values ("ingredients")

    Part 1 counts how many ingredient values lie within at least one interval.
    Part 2 computes the total number of integer values covered by the union
    of all intervals.

    Args:
        path: Path to the puzzle input file.

    Returns:
        A tuple `(part1, part2)` where:
        - `part1` is the count of ingredient values contained in any interval.
        - `part2` is the total size of the normalized interval union.
    """
    # Read all lines, stripping trailing newlines only.
    with open(path, "r", encoding="utf-8") as f:
        rows = [line.rstrip("\n") for line in f]

    # Split input into interval definitions and ingredient values.
    sep = rows.index("")
    interval_lines, ingredient_lines = rows[:sep], rows[sep + 1 :]

    # Parse ingredient values.
    ingredients = [int(s) for s in ingredient_lines]

    # Parse interval definitions of the form "lo-hi".
    intervals = [tuple(map(int, s.split("-"))) for s in interval_lines]

    # Normalize intervals once; all queries assume this invariant.
    intervals = normalize(intervals)

    # Extract sorted start values for binary search.
    starts = [lo for lo, _ in intervals]

    # Part 1: count ingredient values that fall into any interval.
    result_part1 = sum(contains(x, intervals, starts) for x in ingredients)

    # Part 2: sum the sizes of all normalized closed intervals.
    result_part2 = sum(hi - lo + 1 for lo, hi in intervals)

    return result_part1, result_part2


if __name__ == "__main__":
    result_1, result_2 = day05()
    assert result_1 == 607, f"Real: {result_1} vs. Expected: {607}"
    print("Solution for day05.1:", result_1)

    assert result_2 == 342433357244012, (
        f"Real: {result_2} vs. Expected: {342433357244012}"
    )
    print("Solution for day05.2:", result_2)
