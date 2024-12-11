def day01_1():
    with open("2024/day01/input_1.txt", "r") as file1:
        lines = file1.readlines()

    left, right = zip(*[[int(ll) for ll in li.strip().split()] for li in lines])
    left, right = sorted(left), sorted(right)
    print(
        "Solution for day01.1:",
        sum([abs(left - right) for left, right in zip(left, right)]),
    )


def day01_2():
    with open("2024/day01/input_1.txt", "r") as file1:
        lines = file1.readlines()
    left, right = zip(*[[int(ll) for ll in li.strip().split()] for li in lines])
    print(
        "Solution for day01.2:", sum([le * (ri == le) for ri in right for le in left])
    )


if __name__ == "__main__":
    day01_1()
    day01_2()
