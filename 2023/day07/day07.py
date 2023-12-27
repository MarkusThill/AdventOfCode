from collections import Counter
from functools import cmp_to_key


def get_value(hand):
    values = Counter(list(hand)).values()

    # Five/Four of a kind
    if max(values) >= 4:
        return max(values) * 2

    # Full house
    if set(values) == {3, 2}:
        return sum(values)  # 5

    # Three of a kind
    if max(values) == 3:
        return 4

    # Two pair / One pair
    if max(values) == 2:
        return 6 - len(values)  # return values: 3 / 2

    # High card
    return 1


def strongest_hand(hand, repl: list):
    """
    Bruteforcing is not the nicest way, but works in this case...
    Assumes the "Joker" is a wildcard and can be replaced by any other card.
    Bascially tries all possibilities for each Joker and finds the combination
    with the highest score.
    """
    best_h, best_v = hand, get_value(hand)
    if "J" not in hand:
        return best_h, best_v

    hand_list = list(hand)
    for i in range(len(hand)):
        if hand[i] == "J":
            for r in repl:
                hand_list[i] = r
                h, v = strongest_hand("".join(hand_list), repl)
                if v > best_v:
                    best_h, best_v = h, v

            return best_h, best_v
    return best_h, best_v


def comparator2(order, idx):
    def compare_cards(
        item_1,
        item_2,
    ):
        val_1, val_2 = get_value(item_1[idx]), get_value(item_2[idx])
        if val_1 == val_2:
            for l1, l2 in zip(list(item_1[1]), list(item_2[1])):
                if l1 == l2:
                    continue
                return order[l1] - order[l2]
            else:
                assert False, "Should not happen!"
        return val_1 - val_2

    return compare_cards


def day07():
    file1 = open("2023/day07/input_1.txt", "r")
    lines = [l.strip() for l in file1.readlines()]
    lines = [l.split(" ") for l in lines]
    hands = [[l[0], int(l[1])] for l in lines]

    order = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }

    repl = list(order.keys())
    repl.remove("J")
    hands = [tuple([strongest_hand(h[0], repl=repl)[0]] + h) for h in hands]

    # Part 1
    hands = sorted(hands, key=cmp_to_key(comparator2(order=order, idx=1)))
    winnings = [hands[i][-1] * (i + 1) for i in range(len(hands))]
    print(f"Solution Day 7.1: {sum(winnings)}")

    # Part 2
    order["J"] = 1
    hands = sorted(hands, key=cmp_to_key(comparator2(order=order, idx=0)))
    winnings = [hands[i][-1] * (i + 1) for i in range(len(hands))]
    print(f"Solution Day 7.2: {sum(winnings)}")


if __name__ == "__main__":
    day07()
