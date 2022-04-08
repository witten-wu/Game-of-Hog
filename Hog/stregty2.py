import sys
from decimal import *
from functools import lru_cache

sys.setrecursionlimit(100000)
PLAYER_NAME = 'Masquerade' 

def picky_piggy(score): 
    if score == 0:
        return 1
    elif score % 6 == 1:
        return 0
    elif score % 6 == 2:
        return 4
    elif score % 6 == 3:
        return 7
    elif score % 6 == 4:
        return 6
    elif score % 6 == 5:
        return 1
    elif score % 6 == 0:
        return 9

def swine_swap(player_score, opponent_score):
    if pow(3, player_score + opponent_score) < 10:
        return True
    else:
        excitement = pow(3, player_score + opponent_score)
      
        str = repr(excitement)
        a = str[-1]
        c = str[:1]
        if a == c :
            return True
        if a != c:
            return False

@lru_cache(maxsize=None)
def final_strategy(score, opponent_score):
    best_p = 0
    best_n = 1
    for rolltimes in range(1,11):
        p = wr(score, opponent_score, rolltimes)
        if p > best_p:
            best_p = p
            best_n = rolltimes
    if (opponent_score % 6 != 1):
        k = wr(score, opponent_score, 0)
        if k > best_p:
            best_p = k
            best_n = 0
    return best_n

@lru_cache(maxsize=None)
def wr(score, opponent_score, rolltimes):
    winrate = 0
    if (rolltimes == 0):
        turnscore = picky_piggy(opponent_score)
        winrate = calculate(score + turnscore, opponent_score)
    else:
        winrate += (1-(pow(5, rolltimes) / pow(6, rolltimes)))*calculate(score + 1,opponent_score)
        for i in range(2*rolltimes,6*rolltimes + 1):
            winrate += probability(i, rolltimes) * calculate(score+i,opponent_score)
    return winrate

@lru_cache(maxsize=None)
def calculate(score, opponent_score):
    if swine_swap(score, opponent_score):
        temp = score
        score = opponent_score
        opponent_score = temp
    if score >= 100:
        return 1
    elif opponent_score >= 100:
        return 0
    opponent_final_strategy = final_strategy(opponent_score, score)
    opponent_wr = wr(opponent_score,score, opponent_final_strategy)
    return 1 - opponent_wr

@lru_cache(maxsize=None)
def possibility(score,roll):
    if score < 0:
        return 0
    if score == 0 and roll == 0:
        return 1
    if roll == 0:
        return 0
    poss = 0
    for k in range(2,7):
        poss += possibility(score - k, roll - 1)
    return poss

@lru_cache(maxsize=None)
def probability(score,roll):
    return possibility(score,roll)/pow(6,roll)
   

def main():
    # print(final_strategy(5,12))
    CLI()

if __name__=='__main__':
    main()