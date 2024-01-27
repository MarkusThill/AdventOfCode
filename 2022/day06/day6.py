def day6_1():
    file1 = open("2022/day06/input6_1.txt", "r")
    lines = file1.readlines()
    lines = [l.strip() for l in lines]

    solution = None

    n = 14  # 4/14
    for l in lines:
        for i in range(0, len(l)):
            sub = l[i : i + n]
            subset = set(list(sub))
            if len(subset) == n:
                solution = i + n
                break
        print("Solution day 6.1:", solution)


if __name__ == "__main__":
    day6_1()
