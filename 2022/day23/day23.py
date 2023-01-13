import numpy as np
import time

from itertools import cycle

def print_board(elves, shape):
    Q = np.full(shape, ".")
    for e in elves.values():
        Q[e] = "#"
    for l in Q:
        print("".join(l.tolist()))
    print()


def day23_1():
    start_time = time.time()
    file1 = open('input23_1.txt', 'r')
    lines = file1.readlines()
    lines = [l.strip() for l in lines]

    lines = [list(l) for l in lines]
    X = np.array(lines)

    elves = list(zip(*np.where(X == "#")))
    elves = dict(zip(range(len(elves)), elves))
    step_cycle = cycle(range(4))

    for roundr in range(2000):  # outer loop for the rounds
        # print_board(elves, X.shape)
        elves_moved = 0
        start = next(step_cycle)

        # Step 1: for every elve, propose a new position
        new_elves = dict()
        c_pos = dict()
        e_set = set(elves.values())
        s2 = list(np.roll(range(4), -start))
        for e, v in elves.items():
            i, j = v
            new_pos_list = list()
            for direction in s2:
                if direction == 0:
                    if (i - 1, j) not in e_set and (i - 1, j - 1) not in e_set and (i - 1, j + 1) not in e_set:
                        new_pos_list.append((i - 1, j))
                elif direction == 1:
                    if (i + 1, j) not in e_set and (i + 1, j - 1) not in e_set and (i + 1, j + 1) not in e_set:
                        new_pos_list.append((i + 1, j))
                elif direction == 2:
                    if (i, j - 1) not in e_set and (i - 1, j - 1) not in e_set and (i + 1, j - 1) not in e_set:
                        new_pos_list.append((i, j - 1))
                elif direction == 3:
                    if (i, j + 1) not in e_set and (i - 1, j + 1) not in e_set and (i + 1, j + 1) not in e_set:
                        new_pos_list.append((i, j + 1))

            if 0 < len(new_pos_list) < len(s2):
                idx = new_pos_list[0]
                if idx not in c_pos: c_pos[idx] = 0
                c_pos[idx] += 1
                new_elves[e] = idx

        # Step 2: Move the elves only, if there are no collisions
        for e, v in elves.items():
            if e not in new_elves or c_pos[new_elves[e]] > 1:
                new_elves[e] = v
            else:
                elves_moved += 1

        assert len(new_elves) == len(elves)
        elves = new_elves

        if roundr == 9:  # after 10 rounds
            x, y = [e[0] for e in elves.values()], [e[1] for e in elves.values()]

            x_min, x_max, y_min, y_max = min(x), max(x), min(y), max(y)

            empty_tiles = (x_max - x_min + 1) * (y_max - y_min + 1) - len(elves)
            print("Solution Day 23.1:", empty_tiles)

        if elves_moved == 0:
            print("Solution Day 23.2: All elves stopped moving at round: ", roundr + 1)
            break
        if roundr % 100 == 0:
            print("Round: ", roundr)

    print("Time: ", round(time.time() - start_time, 2), "seconds!")


if __name__ == '__main__':
    day23_1()
