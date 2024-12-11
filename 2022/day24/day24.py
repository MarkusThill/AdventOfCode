import numpy as np
import time
from collections import deque


def day24_1():
    start_time = time.time()
    file1 = open("input24_1.txt", "r")
    lines = file1.readlines()
    lines = [l.strip() for l in lines]

    lines = [list(l) for l in lines]
    X = np.array(lines)

    assert X[0, 1] == "." and X[-1, -2] == "."
    X = X[1:-1, 1:-1]
    assert np.in1d(X[:, 0], [">", "<", "."]).all()
    assert np.in1d(X[:, -1], [">", "<", "."]).all()

    blizzards_dict = dict()
    blizzards_dict[0] = dict()
    dir_list = [">", "<", "^", "v"]
    for d in dir_list:
        br, bc = np.where(X == d)
        blizzards_dict[0][d] = list(zip(br.tolist(), bc.tolist()))

    # After T steps the board returns to its original state. It is not necessary to pre-compute
    # X * Y = 3000 time steps. The least common multiple (lcm) should be sufficient
    T = np.lcm(*X.shape)

    # Board state for t=0:
    blizzards = dict()
    blizzards[0] = set()
    for ss in [set(b) for b in blizzards_dict[0].values()]:
        blizzards[0] |= ss

    # Pre-generate all board positions fot t > 0:
    for t in range(1, T):
        for k, (di, dj) in zip(dir_list, [(0, 1), (0, -1), (-1, 0), (1, 0)]):
            b = blizzards_dict[t - 1][k]
            new_b = list()
            for i, j in b:
                bb = [i + di, j + dj]
                if bb[0] >= X.shape[0]:
                    bb[0] = 0
                elif bb[0] < 0:
                    bb[0] = X.shape[0] - 1
                if bb[1] >= X.shape[1]:
                    bb[1] = 0
                elif bb[1] < 0:
                    bb[1] = X.shape[1] - 1
                new_b.append((bb[0], bb[1]))

            if t not in blizzards_dict:
                blizzards_dict[t] = dict()
            if k not in blizzards_dict[t]:
                blizzards_dict[t][k] = dict()
            blizzards_dict[t][k] = new_b

            if t not in blizzards:
                blizzards[t] = set()
            blizzards[t] |= set(new_b)

    del blizzards_dict

    s = (0, -1, 0, False, False)
    dq = deque([s])
    visited = set()
    solution_p1, solution_p2 = None, None
    while True:
        s = dq.popleft()
        if s in visited:
            continue
        visited.add(s)

        s_t, s_i, s_j, s_end, s_start = s

        # get blizzards for time t+1
        b_t1 = blizzards[(s_t + 1) % T]

        if s_i == X.shape[0] - 1 and s_j == X.shape[1] and not s_end:
            s_end = True
            if solution_p1 is None:
                solution_p1 = s_t
        elif s_i == X.shape[0] - 1 and s_j == X.shape[1] and s_end and s_start:
            solution_p2 = s_t
            break
        elif s_i == -1 and s_j == 0 and s_end and not s_start:
            s_start = True

        # generate new states to visit
        for di, dj in [(0, 0), (1, 0), (0, 1), (0, -1), (-1, 0)]:
            s_new = (s_i + di, s_j + dj)
            s_s = (s_t + 1, s_i + di, s_j + dj, s_end, s_start)
            if 0 <= s_new[0] < X.shape[0] and 0 <= s_new[1] < X.shape[1]:
                if s_new not in b_t1 and s_s not in visited:
                    dq.append(s_s)
            elif s_new[0] == X.shape[0] - 1 and s_new[1] == X.shape[1]:  # goal
                dq.append(s_s)
            elif s_new[0] == -1 and s_new[1] == 0:  # start point
                dq.append(s_s)

    print("Time: ", round(time.time() - start_time, 2), "seconds!")
    print("Solution part 1:", solution_p1)
    print("Solution part 2:", solution_p2)


if __name__ == "__main__":
    day24_1()
