import random
from chess.game import Game, WHITE, BLACK
from chess.players import HumanPlayer, MinimaxPlayer

if __name__ == "__main__":
    g = Game(random.randint(0, 7), random.randint(0, 7))
    white = MinimaxPlayer(WHITE, max_time=3)
    black = MinimaxPlayer(BLACK, max_time=3)

    while True:
        moves = g.generate_valid_moves()
        game_over, winner = g.check_terminal(moves)

        if game_over:
            if winner == WHITE:
                print("White wins!")
            elif winner == BLACK:
                print("Black wins!")
            else:
                print("Stalemate!")
            break

        if g.get_current_color() == WHITE:
            print("White to play:")
            print(g)
            move = white.select_move(moves, g)
            g.apply_move(move)
            print("White played", move)
        else:
            print("Black to play:")
            print(g)
            move = black.select_move(moves, g)
            g.apply_move(move)
            print("Black played", move)
        print()