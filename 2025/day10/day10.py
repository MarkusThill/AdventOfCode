from __future__ import annotations

import re
from itertools import combinations
from functools import reduce
from operator import xor

from collections import Counter
from itertools import chain
import z3


# Matches a full input line of the form:
#
#   [LIGHTS] (button) (button,button) ... {v1,v2,...}
#
# Breakdown:
#   \[ (.*?) \]        -> Group 1: everything inside square brackets
#                        Example: "[.#.#]"  -> ".#.#"
#
#   \s*                -> Optional whitespace
#
#   (.*?)              -> Group 2: the entire button section
#                        Example: "(3) (1,3) (0,2,4)"
#
#   \s*                -> Optional whitespace
#
#   \{ (.*?) \}        -> Group 3: everything inside curly braces
#                        Example: "{5,12,7}" -> "5,12,7"
#
#   \s*$               -> Optional trailing whitespace until end of line
#
# Example full match:
#   "[.#.#] (3) (1,3) {5,12,7}"
#
_LINE_RE = re.compile(r"\[(.*?)\]\s*(.*?)\s*\{(.*?)\}\s*$")


# Matches a single parenthesized tuple inside the button section.
#
# Breakdown:
#   \(                 -> Literal opening parenthesis
#   ([^)]*)            -> Group 1: all characters until the next ')'
#                        (i.e., the comma-separated indices)
#   \)                 -> Literal closing parenthesis
#
# Example matches:
#   "(3)"       -> group(1) == "3"
#   "(1,3)"     -> group(1) == "1,3"
#   "(0,2,4)"   -> group(1) == "0,2,4"
#
# Used with `findall()` to extract *all* button definitions from the line.
#
_TUPLE_RE = re.compile(r"\(([^)]*)\)")



def _pattern_to_int(pattern: str) -> int:
    """Convert a '.#' pattern string into an integer bitmask.

    The pattern is interpreted as a binary number where:
    - '.' maps to 0
    - '#' maps to 1

    The string is reversed before conversion so that the *leftmost*
    character corresponds to the least-significant bit (LSB). This
    aligns character positions with bit indices used elsewhere.

    Args:
        pattern: String consisting of '.' and '#' characters.

    Returns:
        Integer representation of the pattern as a bitmask.
    """
    # Replace symbols with binary digits and reverse for LSB alignment.
    return int(pattern.replace(".", "0").replace("#", "1")[::-1], 2)


def _bits_to_mask(bits: set[int]) -> int:
    """Convert a set of bit indices to an integer bitmask.

    Each element `b` in `bits` sets the `b`-th bit in the resulting integer.

    Args:
        bits: Set of non-negative bit indices.

    Returns:
        Integer mask with the specified bits set.
    """
    # Sum of powers of two is equivalent to setting bits individually.
    return sum(1 << b for b in bits)


def day10_1(path: str = "2025/day10/input_1.txt") -> int:
    """Solve Day 10, Part 1 using a brute-force search.

    Each input line is expected to have the format::

        [LIGHTS] (button) (button,button) ... {v1,v2,...}

    where:
    - ``LIGHTS`` is a string of '.' and '#', interpreted as a target bitmask.
    - Each ``( ... )`` group describes a button as the set of bit positions
      that are toggled when the button is pressed.
    - The ``{...}`` section contains voltages/joltages, which are parsed but
      not used in Part 1.

    For each row, the function tries all combinations of buttons of size
    1, then 2, and so on, until it finds a combination whose XOR-combined
    mask equals the target lights mask. The smallest such number of button
    presses is accumulated into the final result.

    Note:
        This approach is intentionally brute-force and may be slow if
        many buttons are present per row.

    Args:
        path: Path to the input file.

    Returns:
        The sum of the minimum number of button presses required for
        each row.
    """
    # Parsed rows: (target_mask, list_of_button_masks)
    rows: list[tuple[int, list[int]]] = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            # Parse the full line using a strict regex.
            m = _LINE_RE.fullmatch(line.strip())
            if not m:
                raise ValueError(f"Line does not match expected format: {line!r}")

            lights_str, buttons_str, _joltages_str = m.groups()

            # Joltages are parsed for completeness but unused in Part 1.
            _joltages = [int(j) for j in _joltages_str.split(",")]

            # Convert the lights pattern into a target bitmask.
            target_mask = _pattern_to_int(lights_str)

            # Parse each "(...)" button specification into a bitmask.
            button_masks: list[int] = []
            for raw in _TUPLE_RE.findall(buttons_str):
                # Example: "(3)" -> {3}, "(1,3)" -> {1, 3}
                bits = {int(x) for x in raw.split(",") if x}
                button_masks.append(_bits_to_mask(bits))

            rows.append((target_mask, button_masks))

    total_presses = 0

    # Solve each row independently.
    for target_mask, button_masks in rows:
        best = 0

        # Try combinations of increasing size.
        for n in range(1, len(button_masks) + 1):
            for comb in combinations(button_masks, n):
                # Combining button effects corresponds to XOR:
                # toggling the same bit twice cancels out.
                combined = reduce(xor, comb, 0)
                if combined == target_mask:
                    best = n
                    break
            if best:
                break

        # If no combination matches, the puzzle constraints are violated.
        if best == 0:
            raise ValueError(
                f"No solution found for target mask {target_mask} "
                f"with {len(button_masks)} buttons"
            )

        total_presses += best

    return total_presses


def day10_2_solve_line(line: str) -> int:
    """Solve Day 10, Part 2 for a single input line using Z3 optimization.

    This parses one puzzle row and formulates it as an integer linear system:

        A x = b

    where:
      - `x[j]` is the (non-negative integer) number of times button `j` is pressed.
      - `A[i][j]` is 1 if button `j` affects row index `i`, otherwise 0.
      - `b[i]` is the required target value for row index `i` (the joltages).

    The objective is to minimize the total number of presses:

        minimize sum(x)

    Notes:
      - A combined (hybrid) approach is possible: first solve the linear system
        symbolically using elimination (Gauss, RREF, etc.), then optimize over
        the remaining free variables under additional constraints (see
        `combi_sympy_z3.ipynb`).
        This can substantially reduce the number of variables seen by the solver
        and may be faster for highly underdetermined systems.

      - However, the symbolic elimination step operates over the rationals.
        As a result, the parametric solution may contain *non-integer*
        coefficients (e.g. fractions) even when `A` and `b` are integer-valued.
        In such cases, extra care is required to:
          * eliminate denominators,
          * add explicit divisibility or integrality constraints on free variables,
          * or reject rational solution spaces that do not admit integer lifts.

      - Additional edge cases arise in the hybrid approach, including multiple
        free variables, missing bounds on free parameters, variables dropping
        out of the optimization model unless explicitly constrained, and
        inconsistent or degenerate systems. Handling these robustly requires
        significantly more bookkeeping.

      - For these reasons, this implementation deliberately lets Z3 solve the
        full constrained optimization problem directly, favoring robustness
        and clarity over maximal symbolic pre-reduction.

      - The `lights` mask is parsed for completeness (same as Part 1), but is not
        used in this Part 2 solver in the code shown here.

    Args:
        line: A single input line in the format:
            "[LIGHTS] (button) (button,button) ... {v1,v2,...}"

    Returns:
        The minimal total number of button presses satisfying all constraints.

    Raises:
        ValueError: If the input line does not match the expected format or is
            structurally inconsistent.
    """

    # Strict parsing: ensure the entire line matches the expected structure.
    m = _LINE_RE.fullmatch(line.strip())
    if not m:
        raise ValueError("Input string does not match expected format")

    lights_str, buttons_str, joltages_str = m.groups()

    # Convert the lights pattern into a bitmask.
    # NOTE: This is intentionally unused below (kept for parity with Part 1
    # and for potential debugging / extensions).
    _lights = int(
        lights_str.replace(".", "0").replace("#", "1")[::-1], 2
    )

    # Parse each "(...)" button specification into a set of row indices.
    # Example: "(1,3)" -> {1, 3}
    buttons = [
        {int(bb) for bb in raw.split(",") if bb}
        for raw in _TUPLE_RE.findall(buttons_str)
    ]

    # Parse the right-hand side vector b.
    # b[i] specifies the required sum of button presses affecting row i.
    b = [int(j) for j in joltages_str.split(",") if j]

    # Edge case: no buttons at all.
    # Then the only feasible solution is b == 0 everywhere.
    if not buttons:
        if any(v != 0 for v in b):
            raise ValueError("No buttons available, but non-zero targets found.")
        return 0

    # Number of variables: one integer press count per button.
    n_cols = len(buttons)

    # Number of equation rows is determined by the maximum referenced index.
    # Assumes row indices are 0-based and contiguous.
    n_rows = max(max(s) for s in buttons) + 1
    if len(b) != n_rows:
        raise ValueError(
            f"Expected {n_rows} joltages, but got {len(b)}."
        )

    # Build a sparse representation:
    # For each equation row i, store the list of buttons that affect it.
    #
    # This avoids constructing a dense A matrix of size (n_rows x n_cols),
    # which would be mostly zeros and slow to iterate over.
    row_to_cols: list[list[int]] = [[] for _ in range(n_rows)]
    for col, rows in enumerate(buttons):
        for r in rows:
            row_to_cols[r].append(col)

    # Z3 decision variables: x_0, x_1, ..., x_(n_cols-1)
    x = [z3.Int(f"x_{i}") for i in range(n_cols)]

    opt = z3.Optimize()

    # Non-negativity constraints: button presses cannot be negative.
    # These are essential both semantically and for guiding the optimizer.
    for x_i in x:
        opt.add(x_i >= 0)

    # Add one linear equation per row:
    #
    #   sum_{j in row_to_cols[i]} x[j] == b[i]
    #
    # This is equivalent to A x = b, but constructed sparsely.
    for i, cols in enumerate(row_to_cols):
        if not cols:
            # If no button affects this row, the only way to satisfy the
            # equation is b[i] == 0.
            opt.add(b[i] == 0)
        else:
            opt.add(z3.Sum([x[j] for j in cols]) == b[i])

    # Objective: minimize the total number of button presses.
    # If multiple optimal solutions exist, Z3 may return any one of them.
    opt.minimize(z3.Sum(x))

    # Solve the optimization problem.
    if opt.check() != z3.sat:
        raise ValueError("No feasible solution found for this line.")

    model = opt.model()

    # Extract concrete integer values from the model and sum them.
    return sum(model.evaluate(v).as_long() for v in x)




def day10_2(
    path: str = "2025/day10/input_1.txt",
) -> int:
    """Solve Day 10, Part 2 by summing the per-line Z3 optimum.

    For each input line, `day10_2_solve_line()` computes the minimal number of
    non-negative integer button presses needed to satisfy the linear system for
    that line. This function aggregates these minima across the entire file.

    Args:
        path: Path to the input file.

    Returns:
        Sum of the minimal total press counts across all lines.
    """
    total_sum = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            # Solve each line independently and accumulate.
            total_sum += day10_2_solve_line(line)

    return total_sum



if __name__ == "__main__":
    result_1 = day10_1()  # "2025/day10/example_1.txt"
    assert result_1 == 452, f"Real: {result_1} vs. Expected: {452}"
    print("Solution for day10.1:", result_1)

    result_2 = day10_2()  # "2025/day10/example_1.txt"
    assert result_2 == 17424, f"Real: {result_2} vs. Expected: {17424}"
    print("Solution for day10.2:", result_2)


def day10_1_prototype(
    path: str = "2025/day10/input_1.txt",
) -> int:
    """Solve Day 10, Part 1 (prototype / baseline implementation).

    This function intentionally reflects the *original prototyping approach*
    used early on: parse each row, then brute-force the smallest number of
    button presses whose combined toggles match the target light mask.

    The prototype models "pressing multiple buttons" by:
      1) collecting all toggled bit indices across the selected buttons,
      2) counting how often each bit index appears,
      3) keeping only indices with odd counts (since even toggles cancel),
      4) converting the remaining indices into an integer bitmask,
      5) comparing that mask to the target.

    Notes on optimizations (implemented later in the improved solution):
      - Precompile regex and use `fullmatch()` instead of `match()` for stricter parsing.
      - Convert each button's set of indices into an integer bitmask once during parsing.
        Then combining buttons becomes a simple XOR of integers (much faster than counting).
      - Replace `Counter(chain.from_iterable(...))` with bitwise operations.
      - Iterate `n` up to `len(buttons) + 1` (this prototype misses the full-size combination).
      - Avoid storing all `rows` if you can process each line on the fly.

    Args:
        path: Path to the input file.

    Returns:
        Sum of the minimal number of button presses required for each row.

    Raises:
        ValueError: If an input line does not match the expected format.
        AssertionError: If no solution is found for a row (prototype assumption).
    """
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            # Prototype parsing: uses a one-off regex per line.
            # Later optimized version precompiles the pattern and uses fullmatch().
            m = re.match(r"\[(.*?)\]\s*(.*?)\s*\{(.*?)\}", line)
            if not m:
                raise ValueError("Input string does not match expected format")

            lights, buttons, joltages = m.groups()

            # Convert ".#.." style pattern into an integer mask:
            # - '.' -> 0, '#' -> 1
            # - reverse string so character positions line up with bit indices
            lights = int(
                lights.replace(".", "0").replace("#", "1")[::-1], 2
            )  # bitmap, invert for the bit indexes to match

            # Extract all "(...)" button definitions as strings like "3" or "1,3".
            # Later optimized version also precompiles this regex.
            buttons = re.findall(r"\(([^)]*)\)", buttons)

            # Prototype representation: each button is stored as a *set of indices*.
            # Optimization later: immediately convert each set to an integer bitmask,
            # so combining buttons is just XOR.
            buttons = [{int(bb) for bb in b.strip().split(",")} for b in buttons]

            # Parsed but unused in Part 1; still kept for completeness.
            joltages = [int(j) for j in joltages.split(",")]

            row = (lights, buttons, joltages)
            rows.append(row)

    num_button_presses = []
    for target_light, buttons, _ in rows:
        best = 0

        # Brute-force increasing combination size:
        # NOTE: This prototype iterates only up to len(buttons) - 1 (range excludes endpoint),
        # so it never tries the full set of all buttons.
        for n in range(1, len(buttons)):
            if best > 0:
                break

            for button_comb in combinations(buttons, n):
                # Flatten all toggled indices across the selected buttons
                # and count how often each index appears.
                #
                # Optimization later:
                # - Counting + chaining allocates and does hashing work.
                # - Using integer masks and XOR avoids all of this.
                counts = Counter(chain.from_iterable(button_comb))

                # Keep only bits toggled an odd number of times (even cancels out).
                bits = [bit_idx for bit_idx, c in counts.items() if c % 2 != 0]

                # Convert list of bit indices into an integer mask.
                # Optimization later: this is avoided by precomputing each button as a mask.
                value = sum(1 << b for b in bits)

                # If the combined toggles equal the target lights, we found a solution.
                if value == target_light:
                    best = n
                    break

        # Prototype assumption: each row is guaranteed solvable.
        # Later version raises a clearer error rather than asserting.
        assert best > 0
        num_button_presses.append(best)

    return sum(num_button_presses)



def day10_2_solve_line_prototype(line):
    """Solve Day 10, Part 2 for a single input line using Z3 optimization.

    This parses one puzzle row and formulates it as an integer linear system:

        A x = b

    where:
      - `x[j]` is the (non-negative integer) number of times button `j` is pressed.
      - `A[i][j]` is 1 if button `j` affects (toggles / contributes to) row index `i`,
        otherwise 0.
      - `b[i]` is the required target value for row index `i` (here: the joltages).

    In addition to feasibility, we minimize the total number of presses:

        minimize sum(x)

    Notes:
      - A combined approach is possible: first solve the linear system using
        elimination (Gauss, rref, etc.), then search the remaining free variables
        under constraints (see `combi_sympy_z3.ipynb`).
        That can be faster, but it needs careful handling of edge cases, so this
        prototype directly lets Z3 solve the entire constrained optimization.

      - The `lights` mask is parsed for completeness (same as Part 1), but is not
        used in this Part 2 solver in the code shown here.

    Args:
        line: A single input line in the format:
            "[LIGHTS] (button) (button,button) ... {v1,v2,...}"

    Returns:
        The minimal total number of button presses (sum of all x[j]) that satisfies
        the system for this line.

    Raises:
        ValueError: If the input line does not match the expected format.
        z3.Z3Exception: If Z3 encounters an internal error while building/solving.
    """
    # Prototype parsing (same style as Part 1 prototype):
    # - Later optimized versions usually precompile regex patterns and use fullmatch().
    m = re.match(r"\[(.*?)\]\s*(.*?)\s*\{(.*?)\}", line)
    if not m:
        raise ValueError("Input string does not match expected format")

    lights, buttons, joltages = m.groups()

    # Convert lights pattern to an integer mask:
    # '.' -> 0, '#' -> 1, reverse so indices map to bit positions.
    # NOTE: Parsed but not used in the Part 2 constraints below.
    lights = int(
        lights.replace(".", "0").replace("#", "1")[::-1], 2
    )  # bitmap, invert for the bit indexes to match

    # Extract button definitions like "(3)" or "(1,3)".
    buttons = re.findall(r"\(([^)]*)\)", buttons)

    # Each button becomes a set of affected row indices.
    # Example: "(1,3)" -> {1, 3}.
    buttons = [{int(bb) for bb in b.strip().split(",")} for b in buttons]

    # Target vector b: required "joltages" per affected row index.
    # Assumption: its length matches the number of logical equation rows.
    joltages = [int(j) for j in joltages.split(",")]

    row = (lights, buttons, joltages)  # kept for debugging / inspection (unused later)

    # We are solving A x = b for integer x with constraints x >= 0.
    # Here b is the list of joltages.
    b = joltages

    # Number of equation rows is derived from the *maximum referenced index* in buttons.
    # If buttons reference indices up to K, then we need rows 0..K inclusive => K+1.
    #
    # Potential edge case: if `buttons` is empty, `max(...)` would fail.
    n_rows = max(max(s) for s in buttons) + 1

    # One variable per button (number of presses).
    n_cols = len(buttons)

    # Build dense 0/1 matrix A (n_rows x n_cols).
    # Optimization opportunity:
    #   - This is dense, but each column is sparse (only a few ones).
    A = [[0] * n_cols for _ in range(n_rows)]
    assert len(A) == n_rows
    assert len(A[0]) == n_cols
    assert len(b) == n_rows

    # Fill A: for each button/column, mark which equation rows it contributes to.
    for col, rows in enumerate(buttons):
        for row in rows:
            A[row][col] = 1

    # Z3 integer decision variables: x_0, x_1, ..., x_(n_cols-1).
    x = [z3.Int(f"x_{i}") for i in range(n_cols)]  # we have n_cols unknowns

    system_of_equations = []
    for i in range(n_rows):
        # Build the left-hand side sum_j x[j] * A[i][j].
        # Optimization opportunity:
        #   - `A[i][j]` is 0/1, so this can be built more sparsely by only summing over
        #     buttons that affect row i (instead of iterating all j).
        equation_lhs = []
        for j in range(n_cols):
            equation_lhs.append(x[j] * A[i][j])

        # Each row i enforces that the linear combination equals b[i].
        equation = sum(equation_lhs) == b[i]
        system_of_equations.append(equation)

    # Use Optimize() to minimize an objective under constraints.
    optim = z3.Optimize()

    # Objective: minimize total number of presses.
    # If multiple optimal solutions exist, Z3 may return any of them.
    optim.minimize(sum(x))

    # Add equations:
    for eq in system_of_equations:
        optim.add(eq)

    # Non-negativity constraints: button presses can't be negative.
    # Optimization opportunity:
    #   - If integrality is required (it is here), x_i are Int already.
    for x_i in x:
        optim.add(x_i >= 0)

    # Check satisfiable/optimal. `check()` returns sat/unsat/unknown.
    # Note: `assert optim.check()` is a bit brittle because:
    #   - sat is truthy, but "unknown" is also truthy-ish in Python contexts sometimes
    #     (and behavior is easy to misunderstand).
    # This is intentionally left as-is since it's prototype code.
    assert optim.check()

    solution = optim.model()

    # Read the model values back into Python ints.
    # Potential edge case:
    #   - If a variable is unconstrained, it may not appear in the model. Here, the
    #     equations + objective should pin everything down enough, but this depends
    #     on the structure of A and b.
    x_solved = [solution[d].as_long() for d in x]

    # Return the minimized sum(x).
    size_x = sum(x_solved)
    return size_x