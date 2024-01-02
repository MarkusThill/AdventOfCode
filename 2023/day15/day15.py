from collections import OrderedDict


def hash(l):
    ans = 0
    for c in l:
        ans += ord(c)
        ans *= 17
        ans &= 255  # bitwise AND instead of modulo
    return ans


def day15():
    file1 = open("2023/day15/input.txt", "r")
    lines = [l.strip() for l in file1.readlines()]
    assert len(lines) == 1
    items = lines[0].split(",")

    # Part 1:
    solutions = [hash(l) for l in items]
    print(f"Solution Day 15.1: {sum(solutions)}")

    # Part 2:
    box_list = [OrderedDict() for _ in range(256)]
    for l in items:
        assert "=" in l or "-" in l
        if "=" in l:  # add a lens
            label, focal_length = l.split("=")
            box_list[hash(label)][label] = int(focal_length)
            continue

        idx = hash(l[:-1])  # We have to remove a lens, if existant
        if l[:-1] in box_list[idx]:
            del box_list[idx][l[:-1]]

    solution_2 = [
        (i + 1) * (j + 1) * fl
        for i in range(256)
        for j, fl in enumerate(box_list[i].values())
    ]

    print(f"Solution Day 15.2: {sum(solution_2)}")


if __name__ == "__main__":
    day15()
