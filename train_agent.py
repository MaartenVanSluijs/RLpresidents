from argparse import ArgumentParser


def train_agent(num_games):

    cards: list[int] = [2,3,4,5,6,7,8,9,10,11,12,13,14] *4
    
    for game in num_games:
        pass
    





if __name__ == "__main__":

    argparser = ArgumentParser()

    argparser.add_argument("--num_games", type=int, default=1000)

    args = argparser.parse_args()

    train_agent(num_games=args.num_games)