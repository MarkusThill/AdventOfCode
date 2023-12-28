def diff(seq: list):
    return [seq[i] - seq[i - 1] for i in range(1, len(seq))]


def all_null(seq):
    return all([i == 0 for i in seq])


def predict(seq):
    seq_list = [seq]
    while not all_null(seq):
        seq = diff(seq)
        seq_list.append(seq)

    for idx in reversed(range(1, len(seq_list))):
        seq_list[idx - 1].append(seq_list[idx][-1] + seq_list[idx - 1][-1])
        seq_list[idx - 1].insert(0, seq_list[idx - 1][0] - seq_list[idx][0])

    return seq_list[0][-1], seq_list[0][0]


def day09():
    file1 = open("2023/day09/input_1.txt", "r")
    lines = [l.strip() for l in file1.readlines()]
    lines = [[int(i) for i in l.split(" ")] for l in lines]
    solution_1, solution_2 = zip(*list(map(predict, lines)))
    print(f"Solution Day 9.1: {sum(solution_1)}")
    print(f"Solution Day 9.2: {sum(solution_2)}")


if __name__ == "__main__":
    day09()
