def day2_1():
    file1 = open('input2_1.txt', 'r')
    lines = file1.readlines()
    lines = [l.strip() for l in lines]
    #      rock  paper scissors
    map1 = {'A': 'Z', 'B': 'X', 'C': 'Y'}  # x beats y
    map2 = {'X': 1, 'Y': 2, 'Z': 3}
    map3 = {'A': 'X', 'B': 'Y', 'C': 'Z'}  # x equals y

    score = 0
    for l in lines:
        him = l[0]
        me = l[-1]
        inc = map2[me]
        if map3[him] == me:
            inc += 3
        elif map1[him] != me:
            inc += 6
        print(inc)
        score += inc

    print("Solution day 2.1:", score)


def day2_2():
    # Using readlines()
    file1 = open('input2_1.txt', 'r')
    lines = file1.readlines()
    lines = [l.strip() for l in lines]
    #      rock  paper scissors
    map1 = {'A': 'Z', 'B': 'X', 'C': 'Y'}  # x beats y
    map2 = {'X': 1, 'Y': 2, 'Z': 3}
    map3 = {'A': 'X', 'B': 'Y', 'C': 'Z'}  # x equals y
    map4 = {'X': {'A': 'Z', 'B': 'X', 'C': 'Y'}, 'Y': {'A': 'X', 'B': 'Y', 'C': 'Z'},
            'Z': {'A': 'Y', 'B': 'Z', 'C': 'X'}}
    score = 0
    for l in lines:
        him = l[0]
        me = map4[l[-1]][him]
        inc = map2[me]
        if map3[him] == me:
            inc += 3
        elif map1[him] != me:
            inc += 6
        print(inc)
        score += inc

    print("Solution day 2.2:", score)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    day2_2()
