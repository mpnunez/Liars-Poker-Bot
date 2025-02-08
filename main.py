#! /usr/bin/python3

import random

from dataclasses import dataclass

N_PLAYERS = 3
N_INITIAL_DICE = 4
N_SIDE_PER_DICE = 6

@dataclass(order=True)
class Bet:
    quantity: int
    value: int

def roll_dice(n_dice, n_sides):
    """
    Returns a list of quantities
    """

    count_for_num = [0] * n_sides
    for _ in range(n_dice):
        roll_value = random.randint(1, n_sides)
        count_for_num[roll_value-1] += 1
    return count_for_num

def chance_correct(total_die, n_sides, known_quantities, bet):
    n_die_known = sum(known_quantities)
    n_die_unknown = total_die - n_die_known



def main():

    for i in range(10):
        print(roll_dice(N_INITIAL_DICE,N_SIDE_PER_DICE))

def run_tests():
    b1 = Bet(6,5)
    b2 = Bet(5,6)
    assert(b1>b2)

if __name__ == "__main__":
    run_tests()
    main()
