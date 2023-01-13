def day20_1():
    file1 = open('input20_1.txt', 'r')
    lines = file1.readlines()
    lines = [l.strip() for l in lines]

    mylist = [{"value": int(l), "visit_as": i} for i, l in enumerate(lines)]

    for v in range(len(mylist)):
        visit = [m["visit_as"] for m in mylist]
        idx = visit.index(v)
        value = mylist.pop(idx)
        val = value["value"]
        new_idx = (idx + val) % len(mylist)
        mylist.insert(new_idx, value)

    mylist = [q["value"] for q in mylist]
    idx_0 = mylist.index(0)
    sol = sum([mylist[(idx_0 + (i + 1) * 1000) % len(mylist)] for i in range(3)])
    print("Solution day 20.1:", sol)


def day20_2():
    file1 = open('input20_1.txt', 'r')
    lines = file1.readlines()
    lines = [l.strip() for l in lines]

    mylist = [{"value": int(l) * 811589153, "visit_as": i} for i, l in enumerate(lines)]

    for _ in range(10):
        for v in range(len(mylist)):
            visit = [m["visit_as"] for m in mylist]
            idx = visit.index(v)
            value = mylist.pop(idx)
            val = value["value"]
            new_idx = (idx + val) % len(mylist)
            mylist.insert(new_idx, value)

    mylist = [q["value"] for q in mylist]
    idx_0 = mylist.index(0)
    sol = sum([mylist[(idx_0 + (i + 1) * 1000) % len(mylist)] for i in range(3)])
    print("Solution day 20.2:", sol)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    day20_1()
    day20_2()
