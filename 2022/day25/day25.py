import numpy as np


def print_board(elves, shape):
    Q = np.full(shape, ".")
    for e in elves.values():
        Q[e] = "#"
    for l in Q:
        print("".join(l.tolist()))
    print()


def to_decimal(l):
    p = 1
    num = 0
    for i in reversed(l):
        if i == '0':
            num += 0
        elif i == '1':
            num += p
        elif i == '2':
            num += 2 * p
        elif i == '-':
            num -= p
        elif i == "=":
            num -= 2 * p
        p *= 5
    return num


def to_decimal2(l):
    p, num = 1, 0
    for i in reversed(l):
        num += p * i
        p *= 5
    return num


def day25_1():
    file1 = open('input25_1.txt', 'r')
    lines = file1.readlines()
    lines = [l.strip() for l in lines]
    lines = [list(l) for l in lines]

    deci = sum([to_decimal(l) for l in lines])

    p = int(np.log(deci) / np.log(5)) + 1

    snafu = [0] * p
    for i in range(len(snafu)):
        # which digit value -2..2 gets us the closest to deci?
        best, best_err = None, 10 ** 100
        for d in range(-2, 3):
            snafu[i] = d
            err = abs(to_decimal2(snafu) - deci)
            if err < best_err:
                best_err, best = err, d
        snafu[i] = best

    assert to_decimal2(snafu) == deci

    solution_p1 = [str(i) if i >= 0 else ["=", "-"][i] for i in snafu]
    print("Decimal Solution:", deci, ", SNAFU Representation:", "".join(solution_p1))


if __name__ == '__main__':
    day25_1()
