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
        move_vector = move.value

        x_range: np.ndarray
        if move_vector[0] != 1:
            x_range = np.arange(self.FIELD_SIZE)
        else:
            x_range = np.arange(self.FIELD_SIZE, 0, -1)

        y_range: np.ndarray
        if move_vector[1] != 1:
            y_range = np.arange(self.FIELD_SIZE)
        else:
            y_range = np.arange(self.FIELD_SIZE, 0, -1)

        result = self.MoveResult.NOTHING
        can_make_move = False
        for x in x_range:
            for y in y_range:
                point = np.array([x, y])
                new_point = point + move_vector
                point_value = self._point(point)
                if self._is_empty(point) and self._is_valid_point(new_point):
                    # that point is not last and is not empty
                    new_point_value = self._point(new_point)
                    if self._is_empty(new_point):
                        new_point_2 = new_point + move_vector
                        if self._is_valid_point(new_point_2) and self._is_empty(new_point_2):
                            new_point = new_point_2
                            new_point_value = 0
                        self._set_point(new_point, point_value)
                        self._set_point(point, 0)
                        result = self.MoveResult.FIELD_UPDATE

                        can_make_move = can_make_move or (self._is_valid_point((n_p := new_point + move_vector))
                                                          and self._point(n_p) == point_value)
                    elif new_point_value == point_value:
                        new_point_value = point_value + 1
                        self._score += 2**new_point_value
                        self._set_point(new_point, new_point_value)
                        self._set_point(point, 0)
                        if new_point_value == self._GAME_GOAL_LOG:
                            result = self.MoveResult.VICTORY
                        else:
                            result = self.MoveResult.FIELD_UPDATE
                    else:
                        new_point = point
                        new_point_value = point_value

                    next_point = new_point + move_vector
                    can_make_move = can_make_move or (self._is_valid_point(next_point) and
                                                      self._point(next_point) == new_point_value)
                    perp_point = new_point + np.vectorize(lambda z: -1 if z == 0 else 0)(move_vector)
                    can_make_move = can_make_move or (self._is_valid_point(perp_point) and
                                                      self._point(perp_point) == new_point_value)

        if result != self.MoveResult.NOTHING:
            self._number_of_moves += 1

        if not can_make_move and result != self.MoveResult.VICTORY:
            result = self.MoveResult.DEFEAT

        return result

    def get_game_field(self) -> np.ndarray:
        return np.vectorize(lambda x: 0 if x == 0 else 2**x)(self._game_field)

    def get_number_of_moves(self) -> int:
        """N.B.: moves that do not change the field are npt counted"""
        return self._number_of_moves

    def get_score(self) -> int:
        return self._score

    def _is_valid_point(self, point: np.ndarray) -> bool:
        return point[0] < self.FIELD_SIZE and point[1] < self.FIELD_SIZE

    def _is_empty(self, point: np.ndarray) -> bool:
        return self._point(point) == 0

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
