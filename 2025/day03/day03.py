from __future__ import annotations

def day03_1(path: str = "2025/day03/input_1.txt") -> int:
    """Solve the AoC riddle for day 03 part 1.

    Each line contains a sequence of digits. For each line, compute the maximum
    two-digit number that can be formed as `10*x + y` where `x` appears before
    `y` in the sequence (i.e., choose indices i < j). The final answer is the
    sum of these per-line maxima.

    Args:
        path: Path to the input file.

    Returns:
        Sum of the per-line maximum two-digit values.
    """
    total = 0

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            s = raw.strip()
            if not s:
                continue

            # Convert digits to ints once.
            digits = [ord(ch) - 48 for ch in s]

            # Track the largest digit seen to the right.
            max_suffix = digits[-1]
            best = 0

            # Iterate possible tens digits from right to left (excluding last).
            for x in reversed(digits[:-1]):
                cand = x * 10 + max_suffix
                if cand > best:
                    best = cand
                if x > max_suffix:
                    max_suffix = x

            total += best

    print("Solution for day01.1:", total)
    return total

def day03_2_old(path: str = "2025/day03/input_1.txt", n_digits: int = 12) -> int:
    """TODO: What is the runtime complexity of this solution?"""
    total = 0
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            s = raw.strip()
            if not s:
                continue

            # Convert digits to ints once.
            digits = [ord(ch) - 48 for ch in s]

            # Track the largest digit seen to the right.
            max_suffixes = digits[-n_digits+1:]
            best = 0

            for x in reversed(digits[:-n_digits+1]):
                seq = reversed([x] + max_suffixes)
                cand = sum(10**i * d for i, d in enumerate(seq))
                if cand > best:
                    best = cand
                idx = 0
                while idx < n_digits-1:
                    if x >= max_suffixes[idx]: # `>=` important here, to allow to pot. shift the equal digit further to the right...
                        max_suffixes[idx], x = x, max_suffixes[idx]
                    else:
                        break
                    idx += 1

            total += best
    return total


def day03_2(path: str = "2025/day03/input_1.txt", n_digits: int = 12) -> int:
    """Solve day 03 part 2 by summing per-line maximal n-digit sequences.

    For each non-empty input line consisting of decimal digits, this function
    computes the maximum integer that can be formed by selecting `n_digits`
    digits in order (left to right) using a greedy right-to-left scan.

    The algorithm maintains a list of the currently best `(n_digits - 1)` digits
    available to the right ("max suffixes"). For each new digit `x` scanned from
    right to left, it:
      1) forms a candidate number from `x` and the current suffix list,
      2) updates the suffix list by inserting `x` into it using a swap-based
         procedure (note: `>=` is required to allow shifting equal digits).

    Complexity:
        Let `m` be the number of digits in a line. For each of the ~`m` positions,
        we (a) build a candidate in O(n_digits) and (b) update the suffix list in
        O(n_digits). Therefore runtime is O(m * n_digits) per line and memory is
        O(n_digits). With `n_digits=12` this is effectively linear in practice.

    Args:
        path: Path to the input file.
        n_digits: Number of digits to select for the maximal sequence.

    Returns:
        The sum of the maximal `n_digits`-digit values for all non-empty lines.
    """
    if n_digits <= 0:
        raise ValueError("n_digits must be positive")

    total = 0
    k = n_digits - 1

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            s = raw.strip()
            if not s:
                continue

            digits = [ord(ch) - 48 for ch in s]
            if len(digits) < n_digits:
                # Not enough digits to form an n-digit number.
                # (Preserves your current behavior: contributes 0.)
                continue

            # Suffix list of length k (n_digits - 1).
            best = 0
            suffix = digits[-k:]

            for x in reversed(digits[:-k]):
                # Build candidate number from digits [x] + suffix using base-10 accumulation.
                # Equivalent to 
                # `seq = reversed([x] + max_suffixes); cand = sum(10**i * d for i, d in enumerate(seq))`, 
                # but faster.
                cand = x
                for d in suffix:
                    cand = cand * 10 + d
                if cand > best:
                    best = cand

                # Insert/update `x` into suffix list
                i = 0
                while i < k:
                    # `>=` important here, to allow to pot. shift the equal digit further to the right:
                    if x >= suffix[i]:  
                        suffix[i], x = x, suffix[i]
                        i += 1
                    else:
                        break

            total += best

    return total


if __name__ == "__main__":
    result = day03_1() # "2025/day03/example_1.txt"
    assert result == 17316, (
        f"Real: {result} vs. Expected: {17316}"
    ) 

    if True: # Verify that our solution works for part 1 as well
        result = day03_2(n_digits=2) # "2025/day03/example_1.txt"
        assert result == 17316, (
            f"Real: {result} vs. Expected: {17316}"
        ) 

    result = day03_2() # "2025/day03/example_1.txt"
    assert result == 171741365473332, (
        f"Real: {result} vs. Expected: {171741365473332}"
    ) 
    print("Solution for day03.2:", result)

    
