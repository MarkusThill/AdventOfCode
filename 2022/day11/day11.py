import numpy as np
import re


def map_op(op_list):
    assert len(op_list) == 3
    assert op_list[0] == 'old'
    assert op_list[1] in ['+', '*']
    assert op_list[2] == 'old' or op_list[2].isdigit()

    lamb = None
    if op_list[1] == '+':
        lamb = lambda x: x + int(op_list[2])
    elif op_list[1] == '*':
        if op_list[2] == 'old':
            lamb = lambda x: x * x
        else:
            lamb = lambda x: x * int(op_list[2])
    else:
        raise NotImplementedError

    return lamb


def day11_1():
    file1 = open('input11_1.txt', 'r')
    lines = file1.readlines()
    lines = [l.strip() for l in lines]

    monkey_idx = 0
    n_lines_monkey = 7
    i = 0
    monkeys = []
    while i < len(lines):
        assert "Monkey" in lines[i], "Line does not contain Monkey"
        assert int(lines[i].split(" ")[1][:-1]) == monkey_idx  # Monkey id

        assert "Starting items:" in lines[i + 1]
        items = [int(item) for item in lines[i + 1].split("Starting items: ")[1].split(", ")]

        assert "Operation:" in lines[i + 2]
        operation = re.split(" +", lines[i + 2].split("Operation: ")[1].split("=")[1])[1:]
        assert len(operation) == 3

        assert 'Test: divisible by ' in lines[i + 3]
        test_div = int(lines[i + 3].split('Test: divisible by ')[1])

        assert "If true: throw to monkey " in lines[i + 4]
        throw_true = int(lines[i + 4].split("If true: throw to monkey ")[1])

        assert "If false: throw to monkey " in lines[i + 5]
        throw_false = int(lines[i + 5].split("If false: throw to monkey ")[1])

        assert i + 6 == len(lines) or lines[i + 6].strip() == ""  # empty line

        monkey = {"idx": monkey_idx, "items": items, "op": operation, "div": test_div,
                  "throw": {False: throw_false, True: throw_true}}
        monkey["op_lambda"] = map_op(monkey["op"])
        monkey["counter"] = 0

        monkeys.append(monkey)

        i += n_lines_monkey
        monkey_idx += 1

    for round in range(20):
        for m in monkeys:
            print("Monkey", m["idx"], ":")
            for i in m["items"]:
                print("  Monkey inspects an item with a worry level of", i)
                new_i = m["op_lambda"](i)
                print("    Worry level is changed to", new_i)
                new_i //= 3
                print("    Monkey gets bored with item. Worry level is divided by 3 to", new_i)
                decision = (new_i % m["div"] == 0)
                print("    Current worry level is", "" if decision else "not", " divisible by", m["div"])
                new_monkey = m["throw"][decision]
                print("    Item with worry level", new_i, "is thrown to monkey", new_monkey)
                monkeys[new_monkey]["items"].append(new_i)
                m["counter"] += 1
            m["items"] = []

        print("Done with round", round + 1, ":")
        for m in monkeys:
            print("Monkey", m["idx"], ":", m["items"])

    inspections = []
    for m in monkeys:
        print("Monkey", m["idx"], "inspected items", m["counter"], "times")
        inspections.append(m["counter"])

    inspections = list(sorted(inspections))
    print("Solution day 11.1:", inspections[-1] * inspections[-2])


def day11_2():
    file1 = open('input11_1.txt', 'r')
    lines = file1.readlines()
    lines = [l.strip() for l in lines]

    monkey_idx = 0
    n_lines_monkey = 7
    i = 0
    monkeys = []
    while i < len(lines):
        assert "Monkey" in lines[i], "Line does not contain Monkey"
        assert int(lines[i].split(" ")[1][:-1]) == monkey_idx  # Monkey id

        assert "Starting items:" in lines[i + 1]
        items = [int(item) for item in lines[i + 1].split("Starting items: ")[1].split(", ")]

        assert "Operation:" in lines[i + 2]
        operation = re.split(" +", lines[i + 2].split("Operation: ")[1].split("=")[1])[1:]
        assert len(operation) == 3

        assert 'Test: divisible by ' in lines[i + 3]
        test_div = int(lines[i + 3].split('Test: divisible by ')[1])

        assert "If true: throw to monkey " in lines[i + 4]
        throw_true = int(lines[i + 4].split("If true: throw to monkey ")[1])

        assert "If false: throw to monkey " in lines[i + 5]
        throw_false = int(lines[i + 5].split("If false: throw to monkey ")[1])

        assert i + 6 == len(lines) or lines[i + 6].strip() == ""  # empty line

        monkey = {"idx": monkey_idx, "items": items, "op": operation, "div": test_div,
                  "throw": {False: throw_false, True: throw_true}}
        monkey["op_lambda"] = map_op(monkey["op"])
        monkey["counter"] = 0

        monkeys.append(monkey)

        i += n_lines_monkey
        monkey_idx += 1

    f = 1
    for m in monkeys:
        f *= m["div"]
    # print(monkeys)
    for round in range(10000):
        for m in monkeys:
            #print("Monkey", m["idx"], ":")
            for i in m["items"]:
                #print("  Monkey inspects an item with a worry level of", i)
                new_i = m["op_lambda"](i) % f
                #print("    Worry level is changed to", new_i)
                # new_i //= 3
                # print("    Monkey gets bored with item. Worry level is divided by 3 to", new_i)
                decision = (new_i % m["div"] == 0)
                #print("    Current worry level is", "" if decision else "not", " divisible by", m["div"])
                new_monkey = m["throw"][decision]
                #print("    Item with worry level", new_i, "is thrown to monkey", new_monkey)
                monkeys[new_monkey]["items"].append(new_i)
                m["counter"] += 1
            m["items"] = []

        if round+1 in [1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]:
            print("== After round", round + 1, "==")
            inspections = []
            for m in monkeys:
                print("Monkey", m["idx"], "inspected items", m["counter"], "times")
                inspections.append(m["counter"])
            print()

    inspections = list(sorted(inspections))
    print("Solution day 11.2:", inspections[-1] * inspections[-2])


if __name__ == '__main__':
    day11_2()
