import numpy as np
import re
import ast
import math
import functools


def compare(left, right):
    for i in range(max(len(left), len(right))):
        if i == len(left):
            return True
        if i == len(right):
            return False

        l, r = left[i], right[i]
        if type(l) is type(r):
            if type(l) is int:
                if l == r: continue
                return l < r
            if type(l) is list:
                ret = compare(l, r)  # compare two lists
                if ret is None: continue
                return ret
            else:
                raise NotImplementedError()
        # One is a list, the other an integer
        if type(l) is not list: l = [l]
        if type(r) is not list: r = [r]
        ret = compare(l, r)
        if ret is None: continue
        return ret

    return None  # could not make a decision


def day13_1():
    # Using readlines()
    file1 = open('input13_1.txt', 'r')
    lines = file1.readlines()
    lines = [l.strip() for l in lines]

    i = 0
    idx = 1
    solution = 0
    while i < len(lines):
        left = ast.literal_eval(lines[i])
        right = ast.literal_eval(lines[i + 1])
        if compare(left, right):
            solution += idx
        i += 3
        idx += 1
    print("Solution day 13.1:", solution)


def cmp(x, y):
    return -(2 * compare(x, y) - 1)


def day13_2():
    file1 = open('input13_1.txt', 'r')
    lines = file1.readlines()
    lines = [l.strip() for l in lines]

    i = 0
    all_lists = []
    while i < len(lines):
        left = ast.literal_eval(lines[i])
        right = ast.literal_eval(lines[i + 1])
        all_lists += [left, right]
        i += 3

    sep1, sep2 = [[2]], [[6]]
    all_lists += [sep1, sep2]

    all_lists_sorted = sorted(all_lists, key=functools.cmp_to_key(cmp))

    for l in all_lists_sorted:
        print(l)

    index1 = all_lists_sorted.index(sep1) + 1
    index2 = all_lists_sorted.index(sep2) + 1
    print("Solution day 13.2:", index1 * index2)


if __name__ == '__main__':
    day13_2()
