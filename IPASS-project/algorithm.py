import cards as cr
import play as pl
import hands as hand_class

poker_class = pl.Poker()
cards_deck = cr.Deck()
player1 = pla.Player("Rico")
player2 = pla.Player("Luffy")
players = {player1, player2}
amount_players = len(players)

# your odds to win your current hand needs to be higher than this to correctly call
def potOdd():
    return poker_class.current_bet / (poker_class.pot + poker_class.current_bet)

# since all suits are same value we can make two differences,
# this will only apply pre-flop
# a hand (or part hand) is same suit (True) or non same suit (False)
def suit(cards):
    if any(cards.count(card.suit) for card in cards) == len(cards):
        return True
    return False

# def pre_flop_hand_strength(player):
#     hand = player.hand
#     ranking = sum(card.ranking() for card in hand)
#     # suited or not
#     if suit(hand):
#         ranking += 2
#     # difference less than 4
#     if max(hand) - min(hand) == 4:
#         ranking += 1
#     return ranking


# def combination_starting_hands():
#     # 52 C 2
#     return 169


# all the next code will be for flop, turn and river
def combination_flop():
    # 50 C 3
    return 19600

def combination_turn():
    # 52 - (2*players) - 3 C 2
    return 990

def combination_river():
    return 52 - (2*players) - 4

def chance_of_tie(stage):
    comm_cards = poker_class.table_cards
    hand = player1.hand



def probability_of_winning(player, combinations_left):
    hand = player.hand
    tie = chance_of_tie()
    # check how many cards combination would give a win (to do)
    winning = 0
    return (winning + 0.5 * tie) / combinations_left

def move(player, stage):
    if potOdd() > probability_of_winning(player, stage):
        player.fold()
    # chance of winning is bigger than opponent
    elif probability_of_winning(player, stage) >= 0.8:
        player.raise_pot()
    else:
        player.check()

def rank(hand, community=None):
    if not community:
        hand


def hand_strength(stage, player, community=community_cards):
    ahead = tied = behind = 0
    hand = player.hand
    ourrank = Rank(hand, community)

    for card_combination in possible_opponents_cards(stage, player):
        opprank = Rank(oppcards, boardcards)
        if (ourrank > opprank):
            ahead += 1
        elif (ourrank == opprank):
            tied += 1
        else:
            behind += 1

    handstrength = (ahead + tied / 2) / (ahead + tied + behind)
    return handstrength

if __name__ == "__main__":
    poker_class = pl.Poker
    print()