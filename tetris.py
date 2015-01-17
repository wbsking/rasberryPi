#-*- coding:utf-8 -*-

import random
import sys
import select
import termios

from base import bcm
from base import Light
from base import Point


class Shape(object):
    I_SHAPE = [(16, 5), (15, 6), (14, 5), (13, 5)]
    O_SHAPE = [(16, 5), (16, 4), (15, 5), (15, 4)]
    L_SHAPE = [(16, 5), (15, 5), (14, 5), (14, 4)]
    J_SHAPE = [(16, 4), (15, 4), (14, 4), (14, 5)]
    S_SHAPE = [(16, 4), (16, 3), (15, 4), (15, 5)]
    Z_SHAPE = [(16, 5), (16, 4), (15, 4), (15, 3)]
    T_SHAPE = [(16, 4), (15, 4), (15, 5), (15, 3)]

    SHAPE_LIST = ["I", "O", "L", "J", "S", "Z", "T"]

    def __init__(self):
        self.current_shape = {}

    def change_shape(self):
        pass

    def change_i_shape(self):
        point_list = self.current_shape['points']
        shape_type = self.current_shape['type']
        if shape_type == 0:
            self.current_shape = 1
            x, y = point_list[-1][0], point_list[-1][1]
            points = [(x, y), (x, y - 1), (x, y - 2), (x, y - 3)]
            self.current_shape['points'] = points
        if shape_type == 1:
            self.current_shape = 0
            x, y = point_list[0][0], point_list[0][1]
            points = [(x, y), (x + 1, y), (x + 2, y), (x + 3, y)]
            self.current_shape['points'] = points

    def change_o_shape(self):
        return

    def change_l_shape(self):
        pass

    def get_random_shape(self):
        return random.choice(self.SHAPE_LIST)


class Tetris(object):
    def __init__(self):
        self.light = Light()

    def init(self):
        for i in range(1, 17):
            for j in range(1, 9):
                self.light.light_off(Point(i, j))
    