from functools import reduce


def less_eq(dict_1, dict_2):
    return all([v <= dict_2[k] for k, v in dict_1.items()])


def dict_max(dict_1, dict_2):
    return {k: max(v, dict_2[k] if k in dict_2 else 0) for k, v in dict_1.items()}


def parse_input():
    file1 = open("2023/day02/input_1.txt", "r")
    lines = file1.readlines()

    lines = [l.split("Game ")[-1] for l in lines]
    lines = [l.split(":") for l in lines]
    my_games = {key: value for key, value in lines}
    my_games = {
        int(k): [vv.strip() for vv in v.split(";")] for k, v in my_games.items()
    }
    my_games = {
        k: [
            {kk: int(vv) for vv, kk in [s.strip().split(" ") for s in ms.split(",")]}
            for ms in v
        ]
        for k, v in my_games.items()
    }
    return my_games


def day02_1():
    require = {"red": 12, "green": 13, "blue": 14}
    my_games = parse_input()
    possible = {
        k: all([less_eq(my_set, require) for my_set in g]) for k, g in my_games.items()
    }
    solution = sum([id if v else 0 for id, v in possible.items()])

    print(f"Solution Day 2.1: {solution}")


def day02_2():
    my_games = parse_input()
    solution = 0
    for g in my_games.values():
        required_min = {"red": 0, "green": 0, "blue": 0}
        for my_set in g:
            required_min = dict_max(required_min, my_set)

        power = reduce(lambda x, y: x * y, required_min.values())
        solution += power

    print(f"Solution Day 2.2: {solution}")


if __name__ == "__main__":
    day02_1()
    day02_2()
