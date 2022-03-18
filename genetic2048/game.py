# 2048 game logic

import math
from enum import IntFlag, Enum, auto


class Game2048:

    class MoveResult(IntFlag):
        VICTORY = 0b0001
        DEFEAT = 0b0010
        FIELD_UPDATE = 0b0100
        NOTHING = 0b1000
        GAME_CONTINUES = FIELD_UPDATE & NOTHING

    class Move(Enum):
        UP = auto()
        DOWN = auto()
        LEFT = auto()
        RIGHT = auto()

    FIELD_SIZE = 4
    GAME_GOAL = 2048
    _GAME_GOAL_LOG = math.log2(GAME_GOAL)

    # not exact numbers but log2 of them are stored
    game_field: list[list[int]]

    def __init__(self):
        """Generate initial game field state"""
        pass

    def make_move(self, move: Move) -> MoveResult:
        pass

    def get_game_field(self) -> list[list[int]]:
        pass

    def _generate_field(self):
        pass

    def _generate_random_number(self):
        pass
