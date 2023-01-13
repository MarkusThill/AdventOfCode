import numpy as np
import re
import ast
import math
import functools
#from interval import interval, inf, imath
import portion as P


def manhatten(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def distance_from_row(p, row):
    return abs(p[1] - row)


def day15_1():
    # Using readlines()
    file1 = open('input15_1.txt', 'r')
    lines = file1.readlines()
    lines = [l.strip() for l in lines]
    lines = [l.split(":") for l in lines]
    lines = [[e.split("at ") for e in l] for l in lines]
    lines = [[e[1] for e in l] for l in lines]
    lines = [[e.split(", ") for e in l] for l in lines]
    lines = [[[q.split("=") for q in e] for e in l] for l in lines]
    lines = [[[q[1] for q in e] for e in l] for l in lines]
    lines = [[(int(e[0]), int(e[1])) for e in l] for l in lines]

    row = 2000000

    row_intervals = P.empty()
    for l in lines:
        print(l)
        S, B = l[0], l[1]
        m = manhatten(p1=S, p2=B)
        print("m", m)
        dist_row = distance_from_row(S, row)
        print("dist_row", dist_row)
        freedom_in_row = m - dist_row
        print("freedom_in_row", freedom_in_row)
        if freedom_in_row < 0:  # how many '#' can we put in this row?
            continue
        i = P.closed(S[0] - freedom_in_row, S[0] + freedom_in_row)
        row_intervals |= i

        # check, if S or B are in this row
        if S[1] == row:
            i = P.closed(S[0],S[0])
            row_intervals -= i
        if B[1] == row:
            i = P.closed(B[0], B[0])
            row_intervals -= i

    total_length = 0
    for i in row_intervals:
        length = i.upper - i.lower
        if i.left == P.CLOSED and i.right == P.CLOSED:
            length += 1
        elif i.left == P.OPEN and i.right == P.OPEN:
            length -=1
        total_length += length


    print("Solution day 15.1:", total_length)

# Needs some optimizations using map() etc.
def day15_2():
    # Using readlines()
    file1 = open('input15_1.txt', 'r')
    lines = file1.readlines()
    lines = [l.strip() for l in lines]
    lines = [l.split(":") for l in lines]
    lines = [[e.split("at ") for e in l] for l in lines]
    lines = [[e[1] for e in l] for l in lines]
    lines = [[e.split(", ") for e in l] for l in lines]
    lines = [[[q.split("=") for q in e] for e in l] for l in lines]
    lines = [[[q[1] for q in e] for e in l] for l in lines]
    lines = [[(int(e[0]), int(e[1])) for e in l] for l in lines]

    N = 4000000
    range_interval = P.closed(0, N)

    for row in reversed(range(N)): # Solution for row 2703981
        if row % 1000 == 0:
            print(row)

        row_intervals = P.empty()
        for l in lines:
            S, B = l[0], l[1]
            m = manhatten(p1=S, p2=B)
            dist_row = distance_from_row(S, row)
            freedom_in_row = m - dist_row
            if freedom_in_row < 0:  # how many '#' can we put in this row?
                continue
            i = P.closed(S[0] - freedom_in_row, S[0] + freedom_in_row)
            row_intervals |= i

        # Intersection of where beacon CAN be and the given range
        row_solution = ~row_intervals & range_interval

        if row_solution.empty:
            continue

        for i in row_solution:
            length = i.upper - i.lower
            if i.left == P.CLOSED and i.right == P.CLOSED:
                length += 1
            elif i.left == P.OPEN and i.right == P.OPEN:
                length -= 1
            if length > 0:
                print(row, i)
                print()
                print("Solution day 15.2:", (i.lower+1)*N + row)
                print()
                return

    print("No Solution was found! Seems like the program is wrong!")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    day15_2()
