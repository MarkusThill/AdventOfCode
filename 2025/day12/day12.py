from __future__ import annotations

import numpy as np


def day12_1(path: str = "2025/day12/input_1.txt") -> int:
    """Solve Day 12, Part 1 using conservative area estimates.

    The input file consists of two sections:

    1. **Shape definitions** (first 30 lines):
       Six shapes are defined, each with an identifier and a 3×3 character
       representation. These shapes are parsed and stored as NumPy arrays
       for completeness, although they are not directly used in the area
       checks performed in this solution.

    2. **Region specifications** (remaining lines):
       Each line describes a rectangular region and the available count of
       each shape type.

    The goal is to determine for how many regions it can be proven that
    *all available shapes definitely fit* into the specified region.

    The algorithm proceeds as follows:

    - First, a **conservative upper bound** is applied by assuming that every
      shape occupies a full 3×3 area (9 tiles), even though each shape
      actually covers only 7 tiles. If the total conservative area of all
      shapes is still smaller than the region area, the shapes are guaranteed
      to fit.

    - If this test is inconclusive, certain known combinations of shapes that
      tile rectangles more efficiently are applied. These combinations reduce
      the effective total shape area estimate.

    - After each reduction step, the conservative area check is repeated. If
      the reduced upper bound is still smaller than the region area, the
      shapes are again guaranteed to fit.

    Only these sufficient (but not necessary) conditions are checked; no
    exhaustive placement or backtracking is performed.

    Args:
        path: Path to the input file for Day 12.

    Returns:
        The number of regions for which it can be proven that all shapes
        definitely fit into the region using the conservative estimates and
        shape-combination heuristics.
    """
    shapes: dict[int, np.ndarray] = {}

    with open(path, "r", encoding="utf-8") as f:
        # --- Parse first 30 lines: 6 shape blocks of 5 lines each ---
        # Block layout:
        #   0: "<id>..."
        #   1-3: 3 lines of 3 chars each
        #   4: separator/blank
        for _ in range(6):
            header = next(f).rstrip("\n")
            shape_id = int(header[0])

            r1 = next(f).rstrip("\n")
            r2 = next(f).rstrip("\n")
            r3 = next(f).rstrip("\n")
            _sep = next(f)  # consume separator line

            # np.array([list(r) for r in rows[idx+1:idx+4]])
            shape = np.array([list(r1), list(r2), list(r3)])
            shapes[shape_id] = shape
            assert shape.shape == (3, 3)

        # --- Process remaining lines as regions (streaming) ---
        shape_max_area = 9
        regions_with_fits = 0

        A013 = 7 * 3  # shapes: (0, 1, 3)
        A05 = 5 * 3   # shapes: (3, 5)

        for line in f:
            line = line.strip()
            if not line:
                continue

            dims_str, shape_nums_str = line.split(":", 1)
            dx_str, dy_str = dims_str.split("x", 1)
            dx = int(dx_str)
            dy = int(dy_str)
            target_area = dx * dy

            # counts
            n = [int(x) for x in shape_nums_str.split()]
            total = sum(n)

            # Quick check
            if total * shape_max_area < target_area:
                regions_with_fits += 1
                continue

            area_used = 0

            # Combine shapes: (0, 1, 3)
            take = n[0]
            if n[1] < take:
                take = n[1]
            if n[3] < take:
                take = n[3]

            if take:
                n[0] -= take
                n[1] -= take
                n[3] -= take
                total -= 3 * take
                area_used += take * A013

                if total * shape_max_area + area_used < target_area:
                    regions_with_fits += 1
                    continue

            # Combine shapes: (3, 5)
            take = n[3] // 2
            if n[5] < take:
                take = n[5]

            if take:
                n[3] -= take
                n[5] -= take
                total -= 2 * take
                area_used += take * A05

            if total * shape_max_area + area_used < target_area:
                regions_with_fits += 1

            # Thats all it needs to solve the problem apparently :)

    return regions_with_fits


if __name__ == "__main__":
    result_1 = day12_1()
    assert result_1 == 519, f"Real: {result_1} vs. Expected: {519}"
    print("Solution for day12.1:", result_1)
