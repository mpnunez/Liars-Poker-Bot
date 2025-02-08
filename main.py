import random
from dataclasses import dataclass
import numpy as np
import math
import itertools
from collections import deque

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
    if n > n_die:
        return 0
    return np.pow(1/n_sides,n) * np.pow( (n_sides-1)/n_sides, n_die-n ) * math.comb(n_die, n)

def at_least_n_rolls(n_die, n_sides, n):
    if n > n_die:
        return 0
    return sum( exactly_n_rolls(n_die, n_sides, i) for i in range(n,n_die+1) )

def chance_correct(total_die, n_sides, known_quantities, bet):
    n_die_known = sum(known_quantities)
    n_die_unknown = total_die - n_die_known
    n_matches_needed = bet.quantity - known_quantities[bet.value-1]
    if n_matches_needed <= 0:
        return 1
    return at_least_n_rolls(n_die_unknown,n_sides,n_matches_needed)


def get_bet_next_highest(total_die, n_sides, my_die, previous_bet: Bet):
    """
    Dumbest next bet possible
    """
    if previous_bet is None:
        return Bet(1,1)
    return previous_bet.next_biggest_bet(n_sides)

def get_bet_least_pareto_aggressive(total_die, n_sides, my_die, previous_bet: Bet):
    """
    Return most probable bet higher than previous bet
    If multiple bets have same probability, use the most aggressive one
    """
    if previous_bet is None:
        previous_bet = Bet(0,n_sides+1)

    # While next bet is more probable than previous bet in the stack
    pareto_bets = deque()
    for next_bet in previous_bet.increasing_bets(n_sides,total_die):
        p = chance_correct(total_die, n_sides, my_die, next_bet)
        while len(pareto_bets) > 0 and pareto_bets[-1][1] <= p:
            pareto_bets.pop()
        pareto_bets.append((next_bet,p))
    print(pareto_bets)
    return pareto_bets[0][0]

def is_true(set_of_die, bet):
    if bet is None:
        return True
    return set_of_die[bet.value-1] >= bet.quantity

def main():

    N_TOTAL_DIE = N_PLAYERS * N_INITIAL_DICE

    last_bet = None
    player_die = [roll_dice(N_INITIAL_DICE,N_SIDE_PER_DICE) for _ in range(N_PLAYERS)]
    total_quantities = [sum(pd[i] for pd in player_die) for i in range(N_SIDE_PER_DICE)]
    player_ind = 0
    while True:
        print(f"\nPlayer {player_ind} turn")

        prob_last_bet = chance_correct(N_TOTAL_DIE,N_SIDE_PER_DICE,player_die[player_ind],last_bet) if last_bet is not None else 1
        print(f"Probability last bet is true: {prob_last_bet}")
        if prob_last_bet < 0.5:
            print("Calling")
            print(f"Actual counts: {total_quantities}")
            winner = (player_ind-1) % N_PLAYERS if is_true(total_quantities,last_bet) else player_ind
            print(f"Player {winner} wins!")
            return

        last_bet = get_bet_least_pareto_aggressive(
            N_TOTAL_DIE,
            N_SIDE_PER_DICE,
            player_die[player_ind],
            last_bet
        )
        print(player_die[player_ind])
        print(f"Placing bet: {last_bet}")

        player_ind = (player_ind+1) % N_PLAYERS

def run_tests():
    b1 = Bet(6,5)
    b2 = Bet(5,6)
    assert(b1>b2)

    tol = 0.01
    p = exactly_n_rolls(12, 6, 3)
    assert(np.abs(p-0.19739571242092258)<tol)

    p = at_least_n_rolls(12, 6, 3)
    assert(np.abs(p-0.3225738051009249)<tol)

    orig_bet = Bet(1,0)
    assert len(list(orig_bet.increasing_bets(6,12))) == 72

    assert(is_true([1,0,0,0,0,0], Bet(1,1)))

    assert(not is_true([0,0,0,0,0,1], Bet(1,1)))

if __name__ == "__main__":
    run_tests()
    main()
