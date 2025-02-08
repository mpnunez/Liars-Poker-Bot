import random
from dataclasses import dataclass
import numpy as np
import math

N_PLAYERS = 3
N_INITIAL_DICE = 4
N_SIDE_PER_DICE = 6

@dataclass(order=True)
class Bet:
    quantity: int
    value: int

    def next_biggest_bet(self,max_value):
        return Bet(self.quantity, self.value+1) if self.value < max_value else Bet(self.quantity+1, 1)

    def increasing_bets(self,max_value,max_quantity):
        bet = self
        while True:
            bet = bet.next_biggest_bet(max_value)
            if bet.quantity > max_quantity:
                return
            yield bet


def roll_dice(n_dice, n_sides):
    """
    Returns a list of quantities
    """

    count_for_num = [0] * n_sides
    for _ in range(n_dice):
        roll_value = random.randint(1, n_sides)
        count_for_num[roll_value-1] += 1
    return count_for_num

def exactly_n_rolls(n_die, n_sides, n):
    return np.pow(1/n_sides,n) * np.pow( (n_sides-1)/n_sides, n_die-n ) * math.comb(n_die, n)

def at_least_n_rolls(n_die, n_sides, n):
    return sum( exactly_n_rolls(n_die, n_sides, i) for i in range(n,n_die+1) )

def chance_correct(total_die, n_sides, known_quantities, bet):
    n_die_known = sum(known_quantities)
    n_die_unknown = total_die - n_die_known



def get_bet(n_players, n_sides, my_die, previous_bet: Bet):
    """
    Return most probable bet higher than previous bet
    If multiple bets have same probability, use the most aggressive one
    """
    print(f"My die are {my_die}")
    return Bet(0,0)

    

def main():

    last_bet = Bet(1,0)
    player_die = [roll_dice(N_INITIAL_DICE,N_SIDE_PER_DICE) for _ in range(N_PLAYERS)]
    for i in range(10):
        player_ind = i % N_PLAYERS
        last_bet = get_bet(N_INITIAL_DICE,N_SIDE_PER_DICE,player_die[player_ind],last_bet)
        print(player_ind)
        print(last_bet)

    

    orig_bet = Bet(1,0)
    print(len(list(orig_bet.increasing_bets(6,12))))
    for bet in orig_bet.increasing_bets(6,12):
        print(bet)


def run_tests():
    b1 = Bet(6,5)
    b2 = Bet(5,6)
    assert(b1>b2)

    p = exactly_n_rolls(12, 6, 3)
    print(p)
    assert(p>0)
    assert(p<1)

    p = at_least_n_rolls(12, 6, 3)
    print(p)
    assert(p>0)
    assert(p<1)

if __name__ == "__main__":
    run_tests()
    main()
