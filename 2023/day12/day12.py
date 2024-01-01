from itertools import groupby


def brutus_dp(mem, seq, exp_ns, seq_idx, exp_ns_idx, ns_count):
    expected_ns_block_len = exp_ns[exp_ns_idx] if exp_ns_idx < len(exp_ns) else 0

    if seq_idx == len(seq):  # Termination criterion reached -> end of sequence
        # if all #-blocks are completed, the #-counter (ns_count) has to be 0:
        if exp_ns_idx == len(exp_ns) and ns_count == 0:
            return 1

        # if not #-blocks are completed, the last char has to complete the last block:
        if exp_ns_idx == len(exp_ns) - 1 and ns_count == expected_ns_block_len:
            return 1
        return 0

    # hash table access:
    hash_key = (seq_idx, exp_ns_idx, ns_count)
    if hash_key in mem:
        return mem[hash_key]

    counter = 0
    if seq[seq_idx] in {".", "?"}:
        # Only continue if also the last char was a '.' or the expected #-block-length was met
        if ns_count == 0 or ns_count == expected_ns_block_len:
            counter += brutus_dp(
                mem, seq, exp_ns, seq_idx + 1, exp_ns_idx + (ns_count > 0), 0
            )
    if seq[seq_idx] in {"#", "?"}:
        counter += brutus_dp(mem, seq, exp_ns, seq_idx + 1, exp_ns_idx, ns_count + 1)

    mem[hash_key] = counter
    return counter


def day12():
    file1 = open("2023/day12/input.txt", "r")
    lines = [l.strip() for l in file1.readlines()]

    springs = [
        {"s": list(sp), "rle": tuple(int(i) for i in rle.split(","))}
        for (sp, rle) in (l.split(" ") for l in lines)
    ]

    #
    # Part 1:
    #
    # Old:
    # combs = [brutus_naive(s["s"], s["rle"]) for s in springs]
    #
    f = lambda s: brutus_dp(dict(), s["s"], s["rle"], 0, 0, 0)
    combs_1 = [f(s) for s in springs]
    print(f"Solution Day 12.1: {sum(combs_1)}")

    #
    # Part 2:
    #
    reps = 5
    springs_2 = [
        {
            "s": list("?".join(["".join(s["s"]) for _ in range(reps)])),
            "rle": s["rle"] * reps,
        }
        for s in springs
    ]
    combs_2 = [f(s) for s in springs_2]
    print(f"Solution Day 12.2: {sum(combs_2)}")


def rle(inp):
    return tuple(len(list(group)) for key, group in groupby(inp) if key != ".")


def brutus_naive(seq, exp_rle):
    if "?" not in seq:
        return 1 * (rle(seq) == exp_rle)

    counter = 0
    idx = seq.index("?")
    new_seq = seq.copy()
    for c in ["#", "."]:
        new_seq[idx] = c
        counter += brutus_naive(new_seq, exp_rle)

    return counter


if __name__ == "__main__":
    day12()
