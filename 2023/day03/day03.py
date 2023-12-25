def search_left_right(line, j):
    if j < 0 or j >= len(line) or not line[j].isdigit():
        return 0
    jj = j
    while (jj > 0) and (line[jj - 1].isdigit()):
        jj -= 1

    kk = j
    while (kk < len(line) - 1) and (line[kk].isdigit()):
        kk += 1
    num = line[jj:kk]
    return int(num) if len(num) > 0 else 0


def day03():
    file1 = open("2023/day03/input_1.txt", "r")
    lines = file1.readlines()
    lines = [l.strip() for l in lines]
    sum_1, sum_2 = 0, 0
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            s = lines[i][j]
            if not s.isdigit() and s != ".":
                adj_list = [
                    search_left_right(lines[i], j - 1),
                    search_left_right(lines[i], j + 1),
                ]
                if i >= 1:
                    num = search_left_right(lines[i - 1], j)
                    adj_list += [num]
                    if num == 0:
                        adj_list += [
                            search_left_right(lines[i - 1], j - 1),
                            search_left_right(lines[i - 1], j + 1),
                        ]

                if i < len(lines) - 1:
                    num = search_left_right(lines[i + 1], j)
                    adj_list += [num]
                    if num == 0:
                        adj_list += [
                            search_left_right(lines[i + 1], j - 1),
                            search_left_right(lines[i + 1], j + 1),
                        ]

                adj_list = list(filter(lambda x: x != 0, adj_list))

                # Solution for part 1
                sum_1 += sum(adj_list)

                # Solution for part 2
                if len(adj_list) == 2 and s == "*":
                    sum_2 += adj_list[0] * adj_list[1]

    print(f"Solution Day 3.1: {sum_1}")
    print(f"Solution Day 3.2: {sum_2}")


if __name__ == "__main__":
    day03()
