import random
from collections import Counter

"""
Class that runs the game, needs to initialize the game, handle plays, and resets when all players are done
    
    In the game, an action is a list of 0s and 1s that indicate which cards in the player's hand need to be played
    Observations consist of the following:
        - The current highest card number in the pile,
        - The number of cards that need to be played this round
        - The cards that the current player is holding.
    A round is done when all players except one has passed
    The game is done when only one player remaining has one or more cards.
"""

# TODO: refactor players with player indices in their class
# TODO: the next observation returned to an agent should be its own hand, now it is the hand of the next person
# TODO: make a nice interface for the player to play the game

class Game:

    def __init__(self):
        self.players: list[Player] = [Player() for _ in range(5)]
        self.play_size = 0
        self.high_card = 0
        self.current_player = 0
        
    def shuffle(self):
        cards = [2,3,4,5,6,7,8,9,10,11,12,13,14]*4
        for player in self.players:
            for _ in range(10):
                card = random.choice(cards)
                player.cards.append(card)
                cards.remove(card)
            player.cards.sort()

    def reset(self):
        self.shuffle()
        self.play_size = 0
        self.high_card = 0
        self.current_player = random.randint( 0, len(self.players)-1)
        next_hand = self.players[self.current_player].cards

        return {"high_card": self.high_card, "play_size":self.play_size, "hand": next_hand}, False

    # Function an agent calls to play cards, returns a reward, the next observation, and termination criteria.
    def play(self, action):

        played_cards = self.get_played_cards(action)

        # Check if action is valid, if not pass
        if not self.validate_action(played_cards):

            # Handle game dynamics on passing
            self.current_player, next_hand = self.pass_turn()
                        
            return -1, {"high_card": self.high_card, "play_size": self.play_size, "hand": next_hand}, False

        # Play the cards, update the high card check if 10s are played or not
        self.players[self.current_player].remove_cards(played_cards)
        if played_cards in [[10], [10, 10], [10, 10, 10], [10, 10, 10, 10]]:
            self.high_card = 0
            self.play_size = 0

            next_hand = self.players[self.current_player].cards
            
        else:
            self.high_card = max(played_cards)
            if self.play_size == 0:
                self.play_size = len(played_cards)
            self.current_player, next_hand = self.next_player_and_hand()

        # If done, check if game is over
        if self.game_over():
            new_observation = self.reset()
            return 1, new_observation, True

        return 1, {"high_card": self.high_card, "play_size": self.play_size, "hand": next_hand}, False

    # Function to check if an action is valid or not
    def validate_action(self, played_cards) -> bool:

        # If one or more 10s are played, instant validate
        if played_cards in [[10], [10, 10], [10, 10, 10], [10, 10, 10, 10]]:
            return True

        # Invalidates actions without the required number of cards
        if len(played_cards) != self.play_size and self.play_size != 0:
            return False

        # Checks if more than one type of card is played,
        # should only be allowed if there is a 2 and one other type
        if len(set(played_cards)) > 1:

            if 2 in played_cards and len(set(played_cards)) == 2:
                pass
            else:
                return False

        # The cards should be higher than the current highest card
        if max(played_cards) <= self.high_card:
            return False
        
        return True

    # Function to convert action list to a list of cards played
    def get_played_cards(self, action):
        current_player = self.players[self.current_player]
        played_cards = []

        for index, item in enumerate(action):
            if item == 1:
                played_cards.append(current_player.cards[index])

        return played_cards

    # Function to handle the game transition for when a turn is passed
    def pass_turn(self):
        self.players[self.current_player].has_passed = True

        # If last pass, previous player wins
        # Else move on to a next player
        number_passed = sum([player.has_passed for player in self.players])
        if number_passed == len(self.players) - 1:
            self.high_card = 0
            self.play_size = 0
            next_player, next_hand = self.find_winner_and_hand()
            self.reset_passes()
        else:
            next_player, next_hand = self.next_player_and_hand()
        return next_player, next_hand

    # Function for finding the winner of a round if all other players have passed
    def find_winner_and_hand(self):
        for index, player in enumerate(self.players):
            if not player.has_passed:
                return index, self.players[index].cards

    # Function for finding the next eligible player if the round is not over yet
    def next_player_and_hand(self):
        for offset in range(1, len(self.players)):
            next_player = (self.current_player + offset) % len(self.players)
            if not self.players[next_player].has_passed and len(self.players[next_player].cards) != 0:
                return next_player, self.players[next_player].cards

    # Function to check if the game is over, i.e. only one player has cards left
    def game_over(self):
        count = 0
        for player in self.players:
            if player.cards != []:
                count += 1
        return True if count <= 1 else False

    # Function to reset each players' pass tag
    def reset_passes(self):
        for player in self.players:
            player.has_passed = False


class Player:

    def __init__(self):
        self.cards = []
        self.has_passed = False
        pass

    def remove_cards(self, played_cards):
        self.cards = list((Counter(self.cards) - Counter(played_cards)).elements())