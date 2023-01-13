import numpy as np
import re
import ast
import math
import functools

def print_board(X):
    for i,x in enumerate(X):
        print(i, "".join(x.tolist()))

def day14_1():
    # Using readlines()
    file1 = open('input14_1.txt', 'r')
    lines = file1.readlines()
    lines = [l.strip() for l in lines]
    lines = [l.split(' -> ') for l in lines]
    lines = [[e.split(",") for e in l] for l in lines]
    lines = [[tuple([int(ee) for ee in e]) for e in l] for l in lines]

    all_x = [e[0] for l in lines for e in l]
    all_y = [e[1] for l in lines for e in l]

    shape = (max(all_y)+1, max(all_x) - min(all_x)+1)

    X = np.full(shape, '.')

    # Fill rocks
    for l in lines:
        start = l[0]
        print("start:", start)
        for stroke in l[1:]:
            x_start = start[0] - min(all_x)
            x_end = stroke[0] - min(all_x)
            x_start, x_end = tuple(sorted([x_start, x_end]))
            y_start = start[1]
            y_end = stroke[1]
            y_start, y_end = tuple(sorted([y_start, y_end]))
            print(x_start, y_start, "|", x_end, y_end)
            X[y_start:y_end+1, x_start:x_end+1] = '#'
            start = stroke

    fell_out = False
    for i in range(1000):
        s_x, s_y = 500 - min(all_x), 0
        moving = True
        while moving and not fell_out:
            if X[s_y+1, s_x] == '.':
                s_y += 1
            elif s_x == 0:
                fell_out = True
            elif X[s_y+1, s_x-1] == '.': # diagonal left
                s_y, s_x = s_y+1, s_x-1
            elif s_x >= X.shape[1]-1:
                fell_out = True
            elif X[s_y + 1, s_x + 1] == '.':  # diagonal right
                s_y, s_x = s_y + 1, s_x + 1
            else:
                moving = False

            fell_out = fell_out or (s_y >= X.shape[0]-1)

        if not fell_out:
            X[s_y, s_x] = 'o'
            print_board(X)
            print()
        else:
            print("fell out at:",i)
            break
        print(fell_out)
    print("Solution day 14.1:", "")


def day14_2():
    file1 = open('input14_1.txt', 'r')
    lines = file1.readlines()
    lines = [l.strip() for l in lines]
    lines = [l.split(' -> ') for l in lines]
    lines = [[e.split(",") for e in l] for l in lines]
    lines = [[tuple([int(ee) for ee in e]) for e in l] for l in lines]

    all_x = [e[0] for l in lines for e in l]
    all_y = [e[1] for l in lines for e in l]

    # append bottom line
    lines.append([ (0,max(all_y)+2), (1000,max(all_y)+2) ])
    print(lines[-1])

    # recompute...
    all_x = [e[0] for l in lines for e in l]
    all_y = [e[1] for l in lines for e in l]

    shape = (max(all_y)+1, max(all_x) - min(all_x)+1)
    X = np.full(shape, '.')


    # Fill rocks
    for l in lines:
        start = l[0]
        print("start:", start)
        for stroke in l[1:]:
            x_start = start[0] - min(all_x)
            x_end = stroke[0] - min(all_x)
            x_start, x_end = tuple(sorted([x_start, x_end]))
            y_start = start[1]
            y_end = stroke[1]
            y_start, y_end = tuple(sorted([y_start, y_end]))
            print(x_start, y_start, "|", x_end, y_end)
            X[y_start:y_end+1, x_start:x_end+1] = '#'
            start = stroke

    fell_out = False
    for i in range(100000):
        s_x, s_y = 500 - min(all_x), 0
        moving = True
        while moving and not fell_out:
            if X[s_y+1, s_x] == '.':
                s_y += 1
            elif s_x == 0:
                fell_out = True
            elif X[s_y+1, s_x-1] == '.': # diagonal left
                s_y, s_x = s_y+1, s_x-1
            elif s_x >= X.shape[1]-1:
                fell_out = True
            elif X[s_y + 1, s_x + 1] == '.':  # diagonal right
                s_y, s_x = s_y + 1, s_x + 1
            else:
                moving = False

            fell_out = fell_out or (s_y >= X.shape[0]-1)

        if not fell_out:
            X[s_y, s_x] = 'o'
        else:
            print_board(X)
            print("fell out at:", i)
            break

        if 500 - min(all_x) == s_x and 0 == s_y:
            print_board(X)
            print("Board is full after", i+1, "moves!")
            break

        #print(fell_out)
    print("Solution day 14.2:", i+1)

if __name__ == '__main__':
    day14_2()
