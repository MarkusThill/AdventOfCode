# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def day1_1(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.

    # Using readlines()
    file1 = open('input1_1.txt', 'r')
    lines = file1.readlines()

    cals_list = list()
    calories = 0
    for l in lines:
        l = l.strip()
        #print(l)
        if len(l) == 0:
            #print("calories:", calories)
            cals_list.append(calories)
            calories = 0
            continue
        calories += int(l)
    cals_list.append(calories)
    print("Solution day 1:", max(cals_list))

def day1_2(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.

    # Using readlines()
    file1 = open('input1_1.txt', 'r')
    lines = file1.readlines()

    cals_list = list()
    calories = 0
    for l in lines:
        l = l.strip()
        #print(l)
        if len(l) == 0:
            #print("calories:", calories)
            cals_list.append(calories)
            calories = 0
            continue
        calories += int(l)
    cals_list.append(calories)
    print("Solution day2:", sum(sorted(cals_list)[-3:]) )

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    day1_1('PyCharm')
    day1_2('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
