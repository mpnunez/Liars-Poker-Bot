#! /usr/bin/python3

import random

def roll_dice(n_dice, n_sides):
    """
    Returns a list of quantities
    """

    count_for_num = [0] * n_sides
    for _ in range(n_dice):
        roll_value = random.randint(1, n_sides)
        count_for_num[roll_value-1] += 1
    return count_for_num

def main():

    N_PLAYERS = 3
    N_INITIAL_DICE = 4
    N_SIDE_PER_DICE = 6

    for i in range(10):
        print(roll_dice(N_INITIAL_DICE,N_SIDE_PER_DICE))



if __name__ == "__main__":
    main()
