# 2048 game logic

import math
import random
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

    _NATURAL_GENERATION_NUMBERS_LOG = [1, 2]  # 2, 4
    _NATURAL_GENERATION_NUMBERS_WEIGHTS = [9, 1]

    # not exact numbers but log2 of them are stored; for empty cell, 0 is stored
    _game_field: list[list[int]]
    _number_of_moves: int = 0
    _score: int = 0

    def __init__(self):
        """Generate initial game field state"""
        self._generate_field()

    def make_move(self, move: Move) -> MoveResult:
        pass

    def get_game_field(self) -> list[list[int]]:
        pass

    def get_number_of_moves(self) -> int:
        """N.B.: moves that do not change the field are npt counted"""
        pass

    def get_score(self) -> int:
        pass

    def _generate_field(self):
        game_field = [[0 for i in range(self.FIELD_SIZE)] for i in range(self.FIELD_SIZE)]

        self._generate_random_number()
        self._generate_random_number()

    def _choose_natural_gen_number(self):
        return random.choices(self._NATURAL_GENERATION_NUMBERS_LOG, self._NATURAL_GENERATION_NUMBERS_WEIGHTS)

    def _choose_random_empty_cell(self) -> tuple[int, int]:
        while True:
            x, y = (random.randrange(0, self.FIELD_SIZE) for i in range(2))
            if self._game_field[x][y] == 0:
                return x, y

    def _generate_random_number(self):
        num = self._choose_natural_gen_number()
        x, y = self._choose_random_empty_cell()
        self._game_field[x][y] = num

