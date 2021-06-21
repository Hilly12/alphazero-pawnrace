from typing import List, Optional, Tuple

import math
import time
import random
import numpy as np
from abc import abstractmethod
from chess.game import EMPTY, Game
from chess.move import Move


class Player:
    def __init__(self, col: int, max_time: int = 100):
        self.col = col
        self.max_time = max_time
    
    @abstractmethod
    def select_move(self, moves: List[Move], game: Game):
        """
        Selects the best move depending on the possible moves and the game state
        """
        ...


class RandomPlayer(Player):
    def select_move(self, moves: List[Move], game: Game):
        return random.choice(moves)


class HumanPlayer(Player):
    def select_move(self, moves: List[Move], game: Game):
        print("Valid Moves:", moves)
        move = None
        print("Please enter your move: ")
        while move is None:
            print("From:", end=" ")
            fr = input().lower()
            print("To:", end=" ")
            to = input().lower()
            for mv in moves:
                if fr in mv.__str__() and to in mv.__str__():
                    move = mv
            if move is None:
                print("Please enter a move:")
        return move


class MinimaxPlayer(Player):
    def select_move(self, moves: List[Move], game: Game):
        def static_eval(board):
            return np.sum(board)

        def minimax(game : Game, depth: int, alpha: float, beta: float, col: int, t: float) -> Tuple[float, Optional[Move]]:
            if depth == 0 or (time.time() - t) > self.max_time:
                return static_eval(game.board) * col, None

            valid_moves = game.generate_valid_moves()
            game_over, winner = game.check_terminal(valid_moves)
            if game_over:
                return math.inf * winner * col, None


            assert len(valid_moves) > 0

            best_eval = -math.inf
            best_move = random.choice(valid_moves)

            for move in valid_moves:
                game.apply_move(move)
                ev = -minimax(game, depth - 1, -beta, -alpha, -col, t)[0]
                game.unapply_move()

                if ev > best_eval:
                    best_eval = ev
                    best_move = move

                alpha = max(alpha, best_eval)
                if beta <= alpha:
                    break
            
            return best_eval, best_move

        depth = 6
        max_depth = 100
        best_move = moves[0]
        best_eval = -math.inf
        t = time.time()

        while (time.time() - t) <= self.max_time and depth <= max_depth:
            curr_eval, move = minimax(game, depth, -math.inf, math.inf, self.col, t)
            if curr_eval > best_eval:
                best_move = move
                best_eval = curr_eval
            
            depth += 1

        print(f"Depth Searched: {depth - 1}")

        return best_move

# class MCTSPlayer(Player):
#     def __init__(self, col, policy_value_function, c_puct=5, n_playout=2000, is_selfplay=0):
#         self.col = col
#         self.mcts = MCTS(policy_value_function, c_puct, n_playout)
#         self.is_selfplay = is_selfplay
    
#     def set_player_ind(self, p):
#         self.player = p

#     def reset_player(self):
#         self.mcts.update_with_move(-1)

#     def select_move(self, moves, game, temp=1e-3, return_prob=0):
#         # the pi vector returned by MCTS as in the AlphaGo Zero paper
#         move_probs = np.zeros(8 * 8)
#         acts, probs = self.mcts.get_move_probs(game, temp)
#         move_probs[list(acts)] = probs
#         if self.is_selfplay:
#             # add Dirichlet Noise for exploration (needed for
#             # self-play training)
#             move = np.random.choice(acts, p = 0.75 * probs + 0.25 * np.random.dirichlet(0.3 * np.ones(len(probs))))
#             # update the root node and reuse the search tree
#             self.mcts.update_with_move(move)
#         else:
#             # with the default temp=1e-3, it is almost equivalent
#             # to choosing the move with the highest prob
#             move = np.random.choice(acts, p=probs)
#             # reset the root node
#             self.mcts.update_with_move(-1)
#             # location = board.move_to_location(move)
#             # print("AI move: %d,%d\n" % (location[0], location[1]))

#         if return_prob:
#             return move, move_probs
#         else:
#             return move

#     def __str__(self):
#         return "MCTS {}".format(self.player)