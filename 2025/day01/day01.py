from __future__ import annotations


def day01_1(
    path: str = "2025/day01/input_1.txt", *, modulus: int = 100, start: int = 50
) -> int:
    """Solve day 01 part 1.

    The input contains lines like 'R12' or 'L3'. Starting from `start`, we move
    right/left by the given value on a ring of size `modulus`. Each time the
    position becomes 0, we increment the password counter.

    Args:
        path: Path to the input file.
        modulus: Ring size for wrap-around (modulus arithmetic).
        start: Initial position.

    Returns:
        The computed password count.
    """
    delta_for_dir: dict[str, int] = {"R": 1, "L": -1}

    position = start % modulus
    password = 0

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            s = raw.strip()
            if not s:
                continue

            direction = s[0]
            try:
                sign = delta_for_dir[direction]
            except KeyError as exc:
                raise ValueError(
                    f"Unknown direction: {direction!r} in line {s!r}"
                ) from exc

            try:
                value = int(s[1:])
            except ValueError as exc:
                raise ValueError(f"Invalid value in line {s!r}") from exc

            position = (position + sign * value) % modulus
            password += int(position == 0)

    print("Solution for day01.1:", password)
    return password


def day01_2(
    path: str = "2025/day01/input_1.txt",
    *,
    modulus: int = 100,
    start: int = 50,
) -> int:
    """Solve day 01 part 2.

    The input consists of movement instructions such as ``R12`` or ``L3``.
    Starting from an initial position on a ring of size ``modulus``, each
    instruction moves the position left or right by the given value.

    The password counter is incremented for every *new* crossing of position
    zero while moving in the negative direction. Special care is taken to
    correctly count crossings when movements span multiple full wraps or
    start/end exactly at zero.

    Args:
        path: Path to the input file.
        modulus: Size of the circular track (used for wrap-around).
        start: Initial position before processing any instructions.

    Returns:
        The computed password value.
    """
    delta_for_dir: dict[str, int] = {"R": 1, "L": -1}

    position = start % modulus
    password = 0

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue

            direction = line[0]
            try:
                sign = delta_for_dir[direction]
            except KeyError as exc:
                raise ValueError(
                    f"Unknown direction: {direction!r} in line {line!r}"
                ) from exc

            try:
                value = int(line[1:])
            except ValueError as exc:
                raise ValueError(f"Invalid value in line {line!r}") from exc

            # We count only *new* zero crossings.
            # Moving from 0 to a negative position would otherwise be counted
            # twice, so we apply a corrective offset here.
            increment = -(position == 0 and sign < 0)

            position = position + sign * value

            # Each full wrap across the modulus corresponds to a zero crossing.
            # Note: for negative values, Python's floor division applies
            # (e.g., -1 // 100 == -1).
            increment += abs(position // modulus)

            position %= modulus

            # If we land exactly on zero while moving negatively, count it.
            # Positive moves ending at multiples of the modulus are already
            # accounted for above.
            increment += int(position == 0 and sign < 0)

            password += increment

    print("Solution for day01.2:", password)
    return password


if __name__ == "__main__":
    day01_1()
    day01_2()
