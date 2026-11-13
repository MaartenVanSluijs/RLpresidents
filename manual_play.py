from game import Game

def print_complete_state(game: Game):

    print(f"Highest card is: {game.high_card}| Play size is: {game.play_size}")
    print("--------------------------------------")
    for index, player in enumerate(game.players):

        if index == game.current_player:
            print(f"{player.cards} --> turn to play")
        elif player.has_passed:
            print(f"{player.cards} [passed]")
        else:
            print(player.cards)
    print("--------------------------------------")

# Function that takes a comma-seperated input and converts it to a one-hot action
def input_to_action(input, cards):
    action = [0]*len(cards)

    cards_copy = cards.copy()

    for value in input:
        if value in cards_copy:
            index = cards_copy.index(value)
            action[index] = 1
            cards_copy[index] = -1

    # If not all values are found in the input we return an empty action, equal to passing
    if sum(action) != len(input):
        return [0]*len(cards)

    return action

def main():
    # Initialize game
    game = Game()
    _, terminated = game.reset()

    while not terminated:

        print_complete_state(game)

        current_hand = game.players[game.current_player].cards

        action = input("Please provide an action, enter cards comma seperated: ")

        input_list = [int(card) for card in action.split(",")]
        
        game.play(input_to_action(input_list, current_hand))
        
        # print_complete_state(game)


if __name__ == "__main__":
    main()
