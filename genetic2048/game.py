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
        GAME_CONTINUES = FIELD_UPDATE | NOTHING

    class Move(Enum):
        UP = (-1, 0)
        DOWN = (1, 0)
        LEFT = (0, -1)
        RIGHT = (0, 1)

    FIELD_SIZE = 4
    GAME_GOAL = 2048
    _GAME_GOAL_LOG = math.log2(GAME_GOAL)

    _NATURAL_GENERATION_NUMBERS_LOG = np.array([1, 2])  # 2, 4
    _NATURAL_GENERATION_NUMBERS_WEIGHTS = np.array([0.9, 0.1])

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
            x_range = np.arange(0, self.FIELD_SIZE)
        else:
            x_range = np.arange(self.FIELD_SIZE - 1, -1, -1)

        y_range: np.ndarray
        if move_vector[1] != 1:
            y_range = np.arange(0, self.FIELD_SIZE)
        else:
            y_range = np.arange(self.FIELD_SIZE - 1, -1, -1)

        collide_table = np.full(self._game_field.shape, False)

        result = self.MoveResult.NOTHING
        zeroes_count = 0
        for x in x_range:
            for y in y_range:
                point = np.array([x, y])
                new_point = point
                point_value = self._point(point)
                if self._is_empty(point):
                    zeroes_count += 1
                    continue

                while self._is_valid_point(new_point := new_point + move_vector) and self._is_empty(new_point):
                    pass

                if self._is_valid_point(new_point) and not collide_table[new_point[0], new_point[1]] \
                        and self._point(new_point) == point_value:
                    new_point_value = point_value + 1
                    self._score += 2**new_point_value
                    self._set_point(new_point, new_point_value)
                    self._set_point(point, 0)
                    collide_table[new_point[0], new_point[1]] = True
                    zeroes_count += 1
                    if new_point_value == self._GAME_GOAL_LOG:
                        result = self.MoveResult.VICTORY
                    else:
                        result = self.MoveResult.FIELD_UPDATE
                else:
                    new_point -= move_vector
                    if self._is_empty(new_point):
                        self._set_point(new_point, point_value)
                        self._set_point(point, 0)
                        result = self.MoveResult.FIELD_UPDATE

        if zeroes_count == 0 and result != self.MoveResult.NOTHING:
            self._number_of_moves += 1
            return self.MoveResult.DEFEAT

        if result != self.MoveResult.NOTHING:
            self._generate_random_number()
            self._number_of_moves += 1
        if zeroes_count < 2 and not self._can_make_move():
            return self.MoveResult.DEFEAT

        return result

    def get_game_field(self) -> np.ndarray:
        return np.vectorize(lambda x: 0 if x == 0 else 2**x)(self._game_field)

    def get_number_of_moves(self) -> int:
        """N.B.: moves that do not change the field are npt counted"""
        return self._number_of_moves

    def get_score(self) -> int:
        return self._score

    def _can_make_move(self) -> bool:
        for x in range(self.FIELD_SIZE):
            for y in range(self.FIELD_SIZE):
                point_value = self._game_field[x][y]
                if point_value == 0:
                    return True
                if x + 1 < self.FIELD_SIZE and self._game_field[x+1][y] in [point_value, 0]:
                    return True
                if y + 1 < self.FIELD_SIZE and self._game_field[x][y+1] in [point_value, 0]:
                    return True
        return False

    def _is_valid_point(self, point: np.ndarray) -> bool:
        return 0 <= point[0] < self.FIELD_SIZE and 0 <= point[1] < self.FIELD_SIZE

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
        count = np.count_nonzero(self._game_field == 0)
        point_number = random.randint(count) + 1
        zero_count = 0
        for x in range(self.FIELD_SIZE):
            for y in range(self.FIELD_SIZE):
                if self._game_field[x][y] == 0:
                    zero_count += 1
                    if zero_count == point_number:
                        return np.array([x, y])

    def _generate_random_number(self):
        num = self._choose_natural_gen_number()
        point = self._choose_random_empty_cell()
        self._set_point(point, num)
