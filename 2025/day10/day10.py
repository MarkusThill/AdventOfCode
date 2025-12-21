from __future__ import annotations

from itertools import combinations
import re
from collections import Counter
from itertools import chain

from functools import reduce
from operator import xor
import z3


_LINE_RE = re.compile(r"\[(.*?)\]\s*(.*?)\s*\{(.*?)\}\s*$")
_TUPLE_RE = re.compile(r"\(([^)]*)\)")


def _pattern_to_int(pattern: str) -> int:
    """Convert '.#' pattern to an int (LSB corresponds to the leftmost char after reversing)."""
    # Reverse to align character positions with bit indices.
    return int(pattern.replace(".", "0").replace("#", "1")[::-1], 2)


def _bits_to_mask(bits: set[int]) -> int:
    """Convert a set of bit indices to an integer bitmask."""
    return sum(1 << b for b in bits)


def day10_1(path: str = "2025/day10/input_1.txt") -> int:
    """Solve Day 10, Part 1 by brute-forcing the minimum number of button presses per row.

    Each input line is expected to have the form:

        [LIGHTS] (button) (button,button) ... {v1,v2,...}

    - `LIGHTS` is a string of '.' and '#', interpreted as a binary bitmask.
    - Each `( ... )` block describes one button as a set of bit indices it toggles.
    - The `{...}` list (voltages/joltages) is parsed but not used for Part 1.

    For each row, this function searches combinations of buttons of size 1, then 2, etc.,
    and returns the first `n` for which the XOR of the selected button masks equals the
    target lights mask. The result is the sum of these minimal press counts across rows.

    Note:
        This is intentionally a simple brute-force approach and may be slow if the number
        of buttons is large.
    """
    rows: list[tuple[int, list[int]]] = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            m = _LINE_RE.fullmatch(line.strip())
            if not m:
                raise ValueError(f"Line does not match expected format: {line!r}")

            lights_str, buttons_str, _joltages_str = m.groups()
            _joltages = [int(j) for j in _joltages_str.split(",")]

            target_mask = _pattern_to_int(lights_str)

            # Extract each "(...)" and convert to a bitmask directly
            button_masks: list[int] = []
            for raw in _TUPLE_RE.findall(buttons_str):
                # "(3)" or "(1,3)" → {3} or {1,3}
                bits = {int(x) for x in raw.split(",") if x}
                button_masks.append(_bits_to_mask(bits))

            rows.append((target_mask, button_masks))

    total_presses = 0

    for target_mask, button_masks in rows:
        best = 0

        # Try increasing combination sizes; include len(buttons) as well.
        for n in range(1, len(button_masks) + 1):
            for comb in combinations(button_masks, n):
                # Pressing buttons combines toggles mod 2 => XOR of masks.
                combined = reduce(xor, comb, 0)
                if combined == target_mask:
                    best = n
                    break
            if best:
                break

        if best == 0:
            raise ValueError(
                f"No solution found for target mask {target_mask} with {len(button_masks)} buttons"
            )

        total_presses += best

    return total_presses


def day10_2_solve_line(line):
    """
    Notes:
    - An combined approach, first solving the system of equations, using Gauss elimination etc.
    is also possible and then solving for the remaining free variables considering the constraints.
    (see combi_sympy_z3.ipynb)
    However, it requires some more work, especially on some edge cases. So we refrain from that and
    simply let the z3 solver solve the overall big problem.
    """
    m = re.match(r"\[(.*?)\]\s*(.*?)\s*\{(.*?)\}", line)
    if not m:
        raise ValueError("Input string does not match expected format")

    lights, buttons, joltages = m.groups()
    lights = int(
        lights.replace(".", "0").replace("#", "1")[::-1], 2
    )  # bitmap, invert for the bit indexes to match
    buttons = re.findall(r"\(([^)]*)\)", buttons)
    buttons = [{int(bb) for bb in b.strip().split(",")} for b in buttons]
    joltages = [int(j) for j in joltages.split(",")]
    row = (lights, buttons, joltages)

    # We are solving Ax=b for x
    # constraints x >= 0
    b = joltages

    n_rows = max(max(s) for s in buttons) + 1
    n_cols = len(buttons)
    A = [[0] * n_cols for _ in range(n_rows)]
    assert len(A) == n_rows
    assert len(A[0]) == n_cols
    assert len(b) == n_rows

    for col, rows in enumerate(buttons):
        for row in rows:
            A[row][col] = 1

    x = [z3.Int(f"x_{i}") for i in range(n_cols)]  # we have n_cols unknowns

    system_of_equations = []
    for i in range(n_rows):
        equation_lhs = []
        for j in range(n_cols):
            equation_lhs.append(x[j] * A[i][j])
        equation = sum(equation_lhs) == b[i]
        system_of_equations.append(equation)

    optim = z3.Optimize()
    optim.minimize(sum(x))

    # Add equations:
    for eq in system_of_equations:
        optim.add(eq)

    # Add constraints
    for x_i in x:
        optim.add(x_i >= 0)

    assert optim.check()
    solution = optim.model()

    x_solved = [solution[d].as_long() for d in x]
    size_x = sum(x_solved)
    return size_x


def day10_2(
    path: str = "2025/day10/input_1.txt",
) -> int:
    """ """
    total_sum = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            total_sum += day10_2_solve_line(line)

    return total_sum


if __name__ == "__main__":
    result_1 = day10_1()  # "2025/day10/example_1.txt"
    assert result_1 == 452, f"Real: {result_1} vs. Expected: {452}"
    print("Solution for day10.1:", result_1)

    result_2 = day10_2()  # "2025/day10/example_1.txt"
    assert result_2 == 17424, f"Real: {result_2} vs. Expected: {17424}"
    print("Solution for day09.2:", result_2)


def day10_1_prototype(
    path: str = "2025/day10/input_1.txt",
) -> int:
    """ " """
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\[(.*?)\]\s*(.*?)\s*\{(.*?)\}", line)
            if not m:
                raise ValueError("Input string does not match expected format")

            lights, buttons, joltages = m.groups()
            lights = int(
                lights.replace(".", "0").replace("#", "1")[::-1], 2
            )  # bitmap, invert for the bit indexes to match
            buttons = re.findall(r"\(([^)]*)\)", buttons)
            buttons = [{int(bb) for bb in b.strip().split(",")} for b in buttons]
            joltages = [int(j) for j in joltages.split(",")]
            row = (lights, buttons, joltages)
            rows.append(row)

    num_button_presses = []
    for target_light, buttons, _ in rows:
        best = 0
        for n in range(1, len(buttons)):
            if best > 0:
                break
            for button_comb in combinations(buttons, n):
                counts = Counter(chain.from_iterable(button_comb))
                bits = [bit_idx for bit_idx, c in counts.items() if c % 2 != 0]
                value = sum(1 << b for b in bits)
                if value == target_light:
                    best = n
                    break
        assert best > 0
        num_button_presses.append(best)

    return sum(num_button_presses)
