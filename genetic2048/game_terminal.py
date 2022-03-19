# Play 2048 from terminal

import sys
import os
import tty
import termios
from typing import Optional

import numpy as np

from game import Game2048


last_msg_size: int


class Keys:
    KEY_UP = 65
    KEY_DOWN = 66
    KEY_RIGHT = 67
    KEY_LEFT = 68


def getkey() -> Optional[Game2048.Move]:
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    try:
        while True:
            b = os.read(sys.stdin.fileno(), 3).decode()
            if len(b) == 3:
                k = ord(b[2])
            else:
                k = ord(b)
            match k:
                case Keys.KEY_UP:
                    return Game2048.Move.UP
                case Keys.KEY_DOWN:
                    return Game2048.Move.DOWN
                case Keys.KEY_RIGHT:
                    return Game2048.Move.RIGHT
                case Keys.KEY_LEFT:
                    return Game2048.Move.LEFT
            return None
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def print_game_field(field: np.ndarray) -> None:
    print('________________________________')
    for x in range(Game2048.FIELD_SIZE):
        for y in range(Game2048.FIELD_SIZE):
            print("{:4d}".format(field[x][y]), end=' ')
        print('\n')
    print('________________________________')


if __name__ == '__main__':
    print("Welcome to 2048!")
    game = Game2048()
    result: Game2048.MoveResult
    while True:
        print_game_field(game.get_game_field())

        move: Game2048.Move
        while (move := getkey()) is None:
            pass
        result = game.make_move(move)

        if result not in Game2048.MoveResult.GAME_CONTINUES:
            print_game_field(game.get_game_field())
            break

    if result == Game2048.MoveResult.VICTORY:
        print('Victory!')
    else:
        print('Defeat!')

    print('Score:', game.get_score())
    print('Number of moves:', game.get_number_of_moves())
