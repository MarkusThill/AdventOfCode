import re


def day01_1():
    file1 = open("2023/day01/input_1.txt", "r")
    lines = file1.readlines()
    lines = [re.sub(r"\D", "", l) for l in lines]
    lines = [int(l[0] + l[-1]) for l in lines]
    print(
        f"Solution Day 1.1: {sum(lines)}",
    )


def day01_2():
    digs = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    with open("2023/day01/input_2.txt", "r") as file1:
        lines = file1.readlines()

    vals = []
    for l in lines:
        first, last = None, None
        for i in range(len(l)):
            if l[i].isdigit():
                first = l[i]
            for k, v in digs.items():
                if k in l[:i]:
                    first = v
            if first is not None:
                break

        for i in range(1, len(l) + 1):
            if l[-i].isdigit():
                last = l[-i]
            for k, v in digs.items():
                if k in l[-i:]:
                    last = v
            if last is not None:
                break
        vals.append(first + last)

    print(
        f"Solution Day 1.2: {sum([int(v) for v in vals])}",
    )


if __name__ == "__main__":
    day01_1()
    day01_2()
