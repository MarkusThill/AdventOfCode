from __future__ import annotations
import time


def day02_1(
    path: str = "2025/day02/input_1.txt",
) -> int:
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    list_id = [line.strip().split(",") for line in lines][0]
    list_id = [tuple(int(i) for i in entry.strip().split("-")) for entry in list_id]
    summ = 0
    for start, end in list_id:
        # TODO: extract function
        str_start = str(start)
        str_end = str(end)
        max_pattern_len = len(str_end) // 2
        min_pattern_len = len(str_start) // 2 + len(str_start) % 2

        # Should always be both odd to be true:
        if max_pattern_len < min_pattern_len:
            continue

        min_pattern_value = int(str_start[:min_pattern_len])
        if (
            min_pattern_value < int(str_start[min_pattern_len:])
            if len(str_start) > 1
            else start
        ):
            min_pattern_value += 1

        max_pattern_value = int(str_end[:max_pattern_len])
        if max_pattern_value > int(str_end[max_pattern_len:]):
            max_pattern_value -= 1

        if len(str_end) % 2 == 1:
            max_pattern_value = int("9" * max_pattern_len)
        if len(str_start) % 2 == 1:
            min_pattern_value = int("1" + "0" * (min_pattern_len - 1))

        if min_pattern_value > max_pattern_value:
            continue

        # Naive loop first:
        for idx in range(min_pattern_value, max_pattern_value + 1):
            pattern = int(2 * str(idx))
            if pattern > end:
                break

            summ += pattern

    print("Solution for day02.1:", summ)
    return summ


def _add_repeated_pattern_ids_in_range(
    out: set[int],
    *,
    start: int,
    end: int,
    pattern: int,
    pow10k: int,
    allowed_pattern_reps: set[int] | None,
) -> None:
    """Add repeated-pattern IDs for one base pattern within a numeric range.

    Builds the number formed by repeating `pattern` (as digits) 2, 3, 4, ... times,
    using numeric concatenation:

        seq_{r+1} = seq_r * pow10k + pattern

    and adds every `seq` that lies within [start, end] to `out`. If
    `allowed_pattern_reps` is provided, only repetition counts in that set
    are accepted.

    Args:
        out: Set to add valid IDs into (mutated in-place).
        start: Inclusive lower bound of the allowed range.
        end: Inclusive upper bound of the allowed range.
        pattern: The base pattern value to repeat (interpreted as `k` digits).
        pow10k: Precomputed 10**k where k is the pattern length in digits.
        allowed_pattern_reps: If provided, only accept sequences whose repetition
            count is contained in this set.

    Returns:
        None. Results are added to `out`.
    """
    reps = 1
    seq = pattern  # 1 repetition

    while True:
        reps += 1  # minimum value is 2 repetitions
        seq = seq * pow10k + pattern  # append pattern digits

        if seq < start:
            continue
        if seq > end:
            break

        if allowed_pattern_reps is not None and reps not in allowed_pattern_reps:
            continue

        out.add(seq)


def day02_2(
    path: str = "2025/day02/input_1.txt",
    allowed_pattern_reps: set[int] | None = None,
) -> int:
    """Solve day 02 part 2 by summing all invalid IDs in given ranges.

    The input file is expected to contain a single line with comma-separated
    ranges in the form "start-end,start-end,...". For each range, this function
    generates numbers formed by repeating a decimal pattern (with a configurable
    number of repetitions) and collects those that fall within the range. The
    final answer is the sum of all unique generated IDs across all ranges.

    Notes:
        - Pattern lengths are tried from 1 to 9.
        - Repetitions always start at 2 (minimum two pattern repetitions).
        - If `allowed_pattern_reps` is given, only those repetition counts are kept.

    Args:
        path: Path to the input file.
        allowed_pattern_reps: If provided, only accept sequences whose repetition
            count is contained in this set (e.g., `{2}` to replicate part 1).

    Returns:
        The sum of all unique invalid IDs found.
    """
    with open(path, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()

    ranges = [
        tuple(int(x) for x in entry.strip().split("-"))
        for entry in first_line.split(",")
        if entry.strip()
    ]

    invalid_ids: set[int] = set()

    for start, end in ranges:
        str_start = str(start)
        str_end = str(end)

        len_start = len(str_start)
        len_end = len(str_end)

        for pattern_len in range(1, 10):
            # It should always be possible to generate a sequence with twice the pattern:
            if pattern_len > len_end // 2:
                break

            # Compute min_pattern_value
            if len_start % pattern_len == 0:
                str_start_chunks = [
                    str_start[i : i + pattern_len]
                    for i in range(0, len_start, pattern_len)
                ]
                min_pattern_value = int(str_start_chunks[0])

                # Original code only checks chunk index 1 (slice [1:2]) and uses < comparison.
                if len(str_start_chunks) > 1 and any(
                    min_pattern_value < int(c) for c in str_start_chunks[1:2]
                ):
                    min_pattern_value += 1
            else:
                # Anyhow the generated pattern will be larger than start (having more digits)
                min_pattern_value = int("1" + "0" * (pattern_len - 1))

            # Compute max_pattern_value
            if len_end % pattern_len == 0:
                str_end_chunks = [
                    str_end[i : i + pattern_len] for i in range(0, len_end, pattern_len)
                ]
                max_pattern_value = int(str_end_chunks[0])

                # Original code only checks chunk index 1 (slice [1:2]) and uses > comparison.
                if len(str_end_chunks) > 1 and any(
                    max_pattern_value > int(c) for c in str_end_chunks[1:2]
                ):
                    max_pattern_value -= 1
            else:
                # Anyhow the generated pattern will be smaller than end
                max_pattern_value = int("9" * pattern_len)

            if len_end > len_start and max_pattern_value < min_pattern_value:
                # A bit tricky in some cases: Just cover the whole range (brute-force)
                min_pattern_value = int("1" + "0" * (pattern_len - 1))
                max_pattern_value = int("9" * pattern_len)

            pow10k = 10**pattern_len

            for pattern in range(min_pattern_value, max_pattern_value + 1):
                _add_repeated_pattern_ids_in_range(
                    invalid_ids,
                    start=start,
                    end=end,
                    pattern=pattern,
                    pow10k=pow10k,
                    allowed_pattern_reps=allowed_pattern_reps,
                )

    result = sum(invalid_ids)
    print("Solution for day02.2:", result)
    return result


if __name__ == "__main__":
    start = time.perf_counter()
    result = day02_1()  # "2025/day02/example_1.txt"
    assert result == 38310256125  # -> correct
    end = time.perf_counter()
    print(f"Time for day02_1: {end - start: .3f} seconds")

    start = time.perf_counter()
    result = day02_2()  # "2025/day02/example_1.txt"
    assert result == 58961152806, (
        f"Real: {result} vs. Expected: {58961152806}"
    )  # -> correct
    end = time.perf_counter()
    print(f"Time for day02_2: {end - start: .3f} seconds")

    # Compute solution for part 1 with this function as well:
    start = time.perf_counter()
    result = day02_2(allowed_pattern_reps={2})  # "2025/day02/example_1.txt"
    assert result == 38310256125, (
        f"Real: {result} vs. Expected: {38310256125}"
    )  # -> correct
    end = time.perf_counter()
    print(f"Time for day02_2: {end - start: .3f} seconds")
