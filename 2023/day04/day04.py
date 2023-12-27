import re


def day04():
    file1 = open("2023/day04/input_1.txt", "r")
    lines = [l.strip() for l in file1.readlines()]
    lines = [l.split(":") for l in lines]
    ids, cards = zip(
        *[(int(re.sub(" +", " ", l[0]).strip().split(" ")[1]), l[1]) for l in lines]
    )

    cards = [re.sub(" +", " ", c).strip() for c in cards]
    cards = [c.split(" | ") for c in cards]
    cards = [
        {
            "winning": {int(cc) for cc in c[0].split(" ")},
            "mine": {int(cc) for cc in c[1].split(" ")},
        }
        for c in cards
    ]
    cards = {cid: c for cid, c in zip(ids, cards)}

    points = {
        cid: len(c["winning"].intersection(c["mine"])) for cid, c, in cards.items()
    }

    solution_1 = sum([int(2 ** (-1 + p)) for p in points.values()])
    print(f"Solution Day 4.1: {solution_1}")

    # Part 2:
    new_points = {k: 0 for k in points.keys()}
    for i in range(1, len(points) + 1):
        for j in range(points[i]):
            new_points[i + j + 1] += 1 + new_points[i]

    print(f"Solution Day 4.2: {len(points) + sum(new_points.values())}")


if __name__ == "__main__":
    day04()
