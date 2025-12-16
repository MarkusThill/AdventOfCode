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


def day02_2(
    path: str = "2025/day02/input_1.txt",
    allowed_pattern_reps: set[int] | None = None,
) -> int:
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    list_id = [line.strip().split(",") for line in lines][0]
    list_id = [tuple(int(i) for i in entry.strip().split("-")) for entry in list_id]
    invalid_ids = set()
    for start, end in list_id:
        # TODO: extract function
        str_start, str_end = str(start), str(end)

        for pattern_len in range(1, 10):
            # It should always be possible to generate a sequence with twice the pattern:
            if pattern_len > len(str_end) // 2:
                break

            if len(str_start) % pattern_len == 0:
                str_start_chunks = [
                    str_start[i : i + pattern_len]
                    for i in range(0, len(str_start), pattern_len)
                ]
                min_pattern_value = int(str_start_chunks[0])
                if len(str_start_chunks) > 1 and any(
                    min_pattern_value < int(c) for c in str_start_chunks[1:2]
                ):
                    # print(f"{start}-{end}: {min_pattern_value}-? for pattern_len {pattern_len}")
                    min_pattern_value += 1
            else:
                # Anyhow the generated pattern will be larger than start (having more digits)
                min_pattern_value = int("1" + "0" * (pattern_len - 1))

            if len(str_end) % pattern_len == 0:
                str_end_chunks = [
                    str_end[i : i + pattern_len]
                    for i in range(0, len(str_end), pattern_len)
                ]
                max_pattern_value = int(str_end_chunks[0])
                if len(str_end_chunks) > 1 and any(
                    max_pattern_value > int(c) for c in str_end_chunks[1:2]
                ):
                    max_pattern_value -= 1
            else:
                # Anyhow the generated pattern will be smaller than end
                max_pattern_value = int("9" * pattern_len)

            if len(str_end) > len(str_start) and max_pattern_value < min_pattern_value:
                # A bit tricky in some cases: Just cover the whole range (brute-force)
                min_pattern_value = int("1" + "0" * (pattern_len - 1))
                max_pattern_value = int("9" * pattern_len)

            # print(f"{start}-{end}: {min_pattern_value}-{max_pattern_value} for pattern_len {pattern_len}")

            for pattern in range(min_pattern_value, max_pattern_value + 1):
                pattern_reps = 1
                while True:
                    pattern_reps += 1  # minimum value is 2 repetitions
                    str_pattern_sequence = str(pattern) * pattern_reps
                    int_pattern_sequence = int(str_pattern_sequence)
                    if int_pattern_sequence < start:
                        continue
                    if int_pattern_sequence > end:
                        break

                    # Can be used to replicate part 1
                    # with allowed_pattern_reps = {2}
                    if (
                        allowed_pattern_reps is not None
                        and pattern_reps not in allowed_pattern_reps
                    ):
                        continue

                    invalid_ids.add(int_pattern_sequence)

    print("Solution for day02.2:", sum(invalid_ids))
    return sum(invalid_ids)


if __name__ == "__main__":
    start = time.perf_counter()

    start = time.perf_counter()
    result = day02_1()  # "2025/day02/example_1.txt"
    assert result == 38310256125  # -> correct
    end = time.perf_counter()
    print(f"Time for day02_1: {end - start: .3f} seconds")

    start = time.perf_counter()
    result = day02_2()  # "2025/day02/example_1.txt"
    assert result == 58961152806  # -> correct
    end = time.perf_counter()
    print(f"Time for day02_2: {end - start: .3f} seconds")

    # Compute solution for part 1 with this function as well:
    start = time.perf_counter()
    result = day02_2(allowed_pattern_reps={2})  # "2025/day02/example_1.txt"
    assert result == 38310256125  # -> correct
    end = time.perf_counter()
    print(f"Time for day02_2: {end - start: .3f} seconds")
