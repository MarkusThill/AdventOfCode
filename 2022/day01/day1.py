def day1_1(name):
    file1 = open('input1_1.txt', 'r')
    lines = file1.readlines()

    cals_list = list()
    calories = 0
    for l in lines:
        l = l.strip()
        if len(l) == 0:
            #print("calories:", calories)
            cals_list.append(calories)
            calories = 0
            continue
        calories += int(l)
    cals_list.append(calories)
    print("Solution day 1:", max(cals_list))

def day1_2(name):
    file1 = open('input1_1.txt', 'r')
    lines = file1.readlines()

    cals_list = list()
    calories = 0
    for l in lines:
        l = l.strip()
        if len(l) == 0:
            cals_list.append(calories)
            calories = 0
            continue
        calories += int(l)
    cals_list.append(calories)
    print("Solution day2:", sum(sorted(cals_list)[-3:]) )

if __name__ == '__main__':
    day1_1()
    day1_2()

