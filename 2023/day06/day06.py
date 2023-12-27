import re
from functools import reduce
import math


def extract_line(line):
    return [int(i) for i in re.sub(" +", " ", line.split(":")[-1]).strip().split(" ")]


def day06():
    file1 = open("2023/day06/input_1.txt", "r")
    lines = [l.strip() for l in file1.readlines()]

    T_list, D_list = extract_line(lines[0]), extract_line(lines[1])

    # Part 1:
    n_beat = [
        sum([t * (T - t) > D for t in range(1, T + 1)]) for T, D in zip(T_list, D_list)
    ]
    print(f"Solution Day 6.1: {reduce(lambda x, y: x * y, n_beat)}")

    # Part 2:
    T = int("".join(map(str, T_list)))
    D = int("".join(map(str, D_list)))
    d = math.sqrt((T / 2) ** 2 - D)
    t1, t2 = int(T / 2 - d), int(T / 2 + d)
    print(f"Solution Day 6.2: {t2 - t1}")


if __name__ == "__main__":
    day06()
