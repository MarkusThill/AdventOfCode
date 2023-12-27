from itertools import cycle
import math


def day08():
    file1 = open("2023/day08/input_1.txt", "r")
    lines = [l.strip() for l in file1.readlines()]
    seq, _ = list(lines.pop(0)), lines.pop(0)
    lines = [l.split(" = ") for l in lines]
    graph = {l[0]: dict(zip(["L", "R"], l[1][1:-1].split(", "))) for l in lines}

    part_1(seq, graph)
    part_2(seq, graph)


def part_1(seq, graph):
    seq_iterator = cycle(seq)
    counter, node = 0, "AAA"
    while node != "ZZZ":
        node, counter = graph[node][next(seq_iterator)], counter + 1
    print(f"Solution Day 8.1: {counter}")


def part_2(seq, graph):
    node_list = [k for k in graph.keys() if k[-1] == "A"]
    cycle_length = [find_cycle_len(seq, graph, node) for node in node_list]
    print(f"Solution Day 8.2: {math.lcm(*cycle_length)}")


def find_cycle_len(seq, graph, node):
    counter, budget = 0, len(seq) * len(graph)
    seq_iterator = cycle(seq)
    while counter < budget:
        node, counter = graph[node][next(seq_iterator)], counter + 1
        if node[-1] == "Z":
            # The instructions suggest that we reach a terminal node
            # after repeating the WHOLE sequence n times. Hence, the counter
            # must be a multiple of the sequence length. If not, things get
            # slightly more complicated and we have to adapt the solution
            assert counter % len(seq) == 0
            return counter

    assert (
        counter < budget
    ), f"Something went wrong! Did not find any cycle with the given budget: {budget}"


if __name__ == "__main__":
    day08()
