from __future__ import annotations

import math
from itertools import zip_longest


def day06_1(path: str = "2025/day06/input_1.txt") -> int:
    """Solve Day 06, Part 1.

    The input file consists of several rows of integers followed by a final
    row of operators (`'+'` or `'*'`). Each column represents an independent
    subproblem: the operator in the last row determines whether the values
    in that column are summed or multiplied. The function returns the sum
    of the results of all column-wise subproblems.

    Args:
        path: Path to the input text file.

    Returns:
        The sum of all column-wise results after applying the specified
        operators.

    Raises:
        ValueError: If an unsupported operator is encountered in the input.
    """
    # Read and split each line on whitespace; this handles arbitrary spacing.
    with open(path, "r", encoding="utf-8") as f:
        rows = [line.split() for line in f]

    # The last row defines the operator for each column.
    operands = rows[-1]

    # All preceding rows contain integer values.
    numbers = [[int(x) for x in row] for row in rows[:-1]]

    # Transpose rows into columns so each column can be processed independently.
    columns = zip(*numbers)

    # Map each supported operator to its corresponding reduction function.
    reducers = {
        "+": sum,
        "*": math.prod,
    }

    try:
        # Apply the appropriate reduction to each column and sum the results.
        return sum(reducers[op](col) for col, op in zip(columns, operands))
    except KeyError as exc:
        # An operator was encountered that is not supported.
        raise ValueError(f"Unsupported operator: {exc}") from None


def day06_2(path: str = "2025/day06/input_1.txt") -> int:
    """Solve Day 06, Part 2.

    The input file represents a fixed-width character grid followed by a final
    row of operators. This function:

    1. Reads the grid while preserving all whitespace.
    2. Transposes the grid at the character level (columns become rows),
       padding shorter rows with spaces.
    3. Strips each transposed column to obtain string tokens.
    4. Splits these tokens into groups separated by empty strings.
    5. Converts each group to integers and applies a column-wise reduction
       (`+` or `*`) as specified by the operator row.
    6. Returns the sum of all reduced group results.

    Args:
        path: Path to the input text file.

    Returns:
        The sum of all group-wise reduction results.

    Raises:
        ValueError: If an unsupported operator is encountered in the operator row.
        AssertionError: If the number of processed groups does not match the
            number of operators.
    """
    # Read all lines verbatim except for the trailing newline.
    # Whitespace inside the lines must be preserved for correct transposition.
    with open(path, "r", encoding="utf-8") as f:
        rows = [line.rstrip("\n") for line in f]

    # The final row contains whitespace-separated operators, one per group.
    operands = rows[-1].split()

    # Dispatch table mapping operators to their reduction functions.
    reducers = {
        "+": sum,
        "*": math.prod,
    }

    total = 0  # Accumulates the final result
    current_group: list[int] = []  # Values collected for the current group
    op_idx = 0  # Index into the operands list

    # Transpose all rows except the operator row.
    # `zip_longest` preserves column alignment by padding with spaces (probably not necessary, though).
    for chars in zip_longest(*rows[:-1], fillvalue=" "):
        # Convert a column of characters into a string and trim surrounding whitespace.
        token = "".join(chars).strip()

        if token == "":
            # An empty token marks the end of the current group.
            if current_group:
                try:
                    # Reduce the current group using the corresponding operator.
                    total += reducers[operands[op_idx]](current_group)
                except KeyError as exc:
                    raise ValueError(f"Unsupported operator: {exc}") from None

                # Advance to the next operator and reset the group.
                op_idx += 1
                current_group = []
            else:
                # Multiple empty separators in a row are ignored.
                continue
        else:
            # Non-empty token: convert to int and add to the current group.
            current_group.append(int(token))

    # Handle the final group (if the input does not end with a separator).
    if current_group:
        try:
            total += reducers[operands[op_idx]](current_group)
        except KeyError as exc:
            raise ValueError(f"Unsupported operator: {exc}") from None
        op_idx += 1

    # Sanity check: every operator must correspond to exactly one group.
    assert op_idx == len(operands), f"Used {op_idx} operators, expected {len(operands)}"

    return total


if __name__ == "__main__":
    result_1 = day06_1()  # "2025/day06/example_1.txt"
    assert result_1 == 6503327062445, f"Real: {result_1} vs. Expected: {6503327062445}"
    print("Solution for day06.1:", result_1)

    result_2 = day06_2()  # "2025/day06/example_1.txt"
    print("Solution for day06.2:", result_2)
    assert result_2 == 9640641878593, f"Real: {result_2} vs. Expected: {9640641878593}"
