# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def day3_1():
    # Using readlines()
    file1 = open('input3_1.txt', 'r')
    lines = file1.readlines()
    lines = [l.strip() for l in lines]

    total_prio = 0
    for l in lines:
        #print(l, len(l))
        left, right = l[:len(l)//2], l[len(l)//2:]
        assert len(left) == len(right)
        left, right = set(left), set(right)
        i = left.intersection(right)
        assert len(i) == 1
        elem = [j for j in i][0]
        ordi = ord(elem)
        prio = 0
        if ordi >= ord('a') and ordi <= ord('z'):
            prio = ordi - ord('a') + 1
        else:
            prio = ordi - ord('A') + 27

        total_prio += prio
        print(prio)

    print("Solution day 3.1:", total_prio)

def day3_2():
    # Using readlines()
    file1 = open('input3_1.txt', 'r')
    lines = file1.readlines()
    lines = [l.strip() for l in lines]

    assert len(lines) % 3 == 0
    total_prio = 0
    idx = 0
    for _ in range(len(lines)//3):
        for i in range(3):
            l = set(lines[idx])
            if i == 0:
                my_set = l
            else:
                my_set = my_set.intersection(l)
            idx += 1
        assert len(my_set) == 1

        elem = [j for j in my_set][0]
        ordi = ord(elem)
        if ordi >= ord('a') and ordi <= ord('z'):
            prio = ordi - ord('a') + 1
        else:
            prio = ordi - ord('A') + 27

        total_prio += prio

        print(prio)

    print("Solution day 3.2:", total_prio)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    day3_2()

    #print(ord('a'), ord('z'))
    #print(ord('A'), ord('Z'))
