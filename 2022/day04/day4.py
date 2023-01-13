def day4_1():
    # Using readlines()
    file1 = open('input4_1.txt', 'r')
    lines = file1.readlines()
    lines = [l.strip() for l in lines]

    sections = [ [ [int(w) for w in q.split('-')] for q in l.split(',')] for l in lines]
    print(sections[0])

    counter = 0
    for s in sections:
        l, r = s[0], s[1]
        if l[0] >= r[0] and l[1] <= r[1]:
            counter += 1
        elif l[0] <= r[0] and l[1] >= r[1]:
            counter += 1

    print("Solution day 4.1:", counter)



def day4_2():
    file1 = open('input4_1.txt', 'r')
    lines = file1.readlines()
    lines = [l.strip() for l in lines]

    sections = [ [ [int(w) for w in q.split('-')] for q in l.split(',')] for l in lines]
    print(sections[0])

    counter = 0
    for s in sections:
        l, r = s[0], s[1]
        if l[0] >= r[0] and l[1] <= r[1]:
            counter += 1
        elif l[0] <= r[0] and l[1] >= r[1]:
            counter += 1
        elif l[0] <= r[1] and l[1] >= r[1]:
            counter += 1
        elif r[0] <= l[1] and r[1] >= l[1]:
            counter += 1

    print("Solution day 4.2:", counter)


if __name__ == '__main__':
    day4_2()
