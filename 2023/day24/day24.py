from collections import deque


def day24():
    boundary = (200000000000000, 400000000000000)
    file1 = open("2023/day24/input.txt", "r")
    lines = [l.strip() for l in file1.readlines()]
    lines = [(l.split(", "), r.split(", ")) for l, r in [l.split(" @ ") for l in lines]]
    lines = [tuple(map(int, l)) for l in [(x + y) for (x, y) in lines]]

    counter = 0
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            (a_1, b_1, _, x_1, y_1, _), (a_2, b_2, _, x_2, y_2, _) = lines[i], lines[j]
            den = x_1 * y_2 - x_2 * y_1
            if den == 0:  # parallel lines
                continue

            t_1 = ((a_2 - a_1) * y_2 + b_1 * x_2 - b_2 * x_2) / den
            t_2 = ((a_2 - a_1) * y_1 + b_1 * x_1 - b_2 * x_1) / den
            if t_1 < 0 or t_2 < 0:
                continue

            x = (-a_1 * x_2 * y_1 + x_1 * (-b_2 * x_2 + a_2 * y_2 + b_1 * x_2)) / den
            y = (-b_2 * x_2 * y_1 + y_2 * (-a_1 * y_1 + a_2 * y_1 + b_1 * x_1)) / den

            if boundary[0] <= x <= boundary[1] and boundary[0] <= y <= boundary[1]:
                counter += 1

    print(f"Solution Day 24.1: {counter}")


if __name__ == "__main__":
    day24()
