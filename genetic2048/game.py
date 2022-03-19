# 2048 game logic

import math
from enum import IntFlag, Enum

import numpy as np
from numpy import random


class Game2048:

    class MoveResult(IntFlag):
        VICTORY = 0b0001
        DEFEAT = 0b0010
        FIELD_UPDATE = 0b0100
        NOTHING = 0b1000
        GAME_CONTINUES = FIELD_UPDATE & NOTHING

    class Move(Enum):
        UP = np.array(0, 1)
        DOWN = np.array(0, -1)
        LEFT = np.array(-1, 0)
        RIGHT = np.array(1, 0)

    FIELD_SIZE = 4
    GAME_GOAL = 2048
    _GAME_GOAL_LOG = math.log2(GAME_GOAL)

    _NATURAL_GENERATION_NUMBERS_LOG = np.array([1, 2])  # 2, 4
    _NATURAL_GENERATION_NUMBERS_WEIGHTS = np.array([9, 1])

    # not exact numbers but log2 of them are stored; for empty cell, 0 is stored
    _game_field: np.ndarray
    _number_of_moves: int = 0
    _score: int = 0

    def __init__(self):
        """Generate initial game field state"""
        self._generate_field()

    def make_move(self, move: Move) -> MoveResult:
        pass

    def get_game_field(self) -> np.ndarray:
        return np.vectorize(lambda x: 0 if x == 0 else 2**x)(self._game_field)

    def get_number_of_moves(self) -> int:
        """N.B.: moves that do not change the field are npt counted"""
        return self._number_of_moves

    def get_score(self) -> int:
        return self._score

    def _point(self, point: np.ndarray) -> int:
        return self._game_field[point[0]][point[1]]

    def _set_point(self, point: np.ndarray, value: int) -> None:
        self._game_field[point[0]][point[1]] = value

    def _generate_field(self):
        self._game_field = np.zeros((self.FIELD_SIZE, self.FIELD_SIZE), np.int8)

        self._generate_random_number()
        self._generate_random_number()

    def _choose_natural_gen_number(self):
        return random.choice(self._NATURAL_GENERATION_NUMBERS_LOG, p=self._NATURAL_GENERATION_NUMBERS_WEIGHTS)

    def _choose_random_empty_cell(self) -> np.ndarray:
        while True:
            point = random.randint(self.FIELD_SIZE, size=2)
            if self._point(point) == 0:
                return point

    def _generate_random_number(self):
        num = self._choose_natural_gen_number()
        point = self._choose_random_empty_cell()
        self._set_point(point, num)

