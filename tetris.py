# -*- coding:utf-8 -*-

import random
import sys
import select
import termios

from base import bcm
from base import Light
from base import Point


class Shape(object):
    I_SHAPE = [(16, 5), (15, 5), (14, 5), (13, 5)]
    O_SHAPE = [(16, 5), (16, 4), (15, 5), (15, 4)]
    L_SHAPE = [(16, 5), (15, 5), (14, 5), (14, 4)]
    J_SHAPE = [(16, 4), (15, 4), (14, 4), (14, 5)]
    S_SHAPE = [(16, 3), (16, 4), (15, 4), (15, 5)]
    Z_SHAPE = [(16, 5), (16, 4), (15, 4), (15, 3)]
    T_SHAPE = [(16, 4), (15, 5), (15, 4), (15, 3)]

    SHAPE_LIST = ["I", "O", "L", "J", "S", "Z", "T"]

    SHAPE_TYPE_HASH = {
        "I": I_SHAPE,
        "O": O_SHAPE,
        "L": L_SHAPE,
        "J": J_SHAPE,
        "S": S_SHAPE,
        "Z": Z_SHAPE,
        "T": T_SHAPE
    }

    def __init__(self):
        self.current_shape = {"shape": None, "points": [], 'type': 0}

    def change_shape(self):
        change_shape_hash = {
            "I": self.change_i_shape,
            "O": self.change_o_shape,
            "L": self.change_l_shape,
            "J": self.change_j_shape,
            "S": self.change_s_shape,
            "Z": self.change_z_shape,
            "T": self.change_t_shape,
        }
        return change_shape_hash[self.current_shape['shape']]()

    def change_i_shape(self):
        '''
            shape_type: 0
                |
            shape_type: 1
                -
        '''
        point_list = self.current_shape['points']
        shape_type = self.current_shape['type']
        if shape_type == 0:
            shape_type = 1
            x, y = point_list[-1][0], point_list[-1][1]
            points = [(x, y), (x, y - 1), (x, y - 2), (x, y - 3)]
        else:
            shape_type = 0
            x, y = point_list[0][0], point_list[0][1]
            points = [(x + 3, y), (x + 2, y), (x + 1, y), (x, y)]
        return shape_type, points

    def change_o_shape(self):
        point_list = self.current_shape['points']
        shape_type = self.current_shape['type']
        return shape_type, point_list

    def change_l_shape(self):
        '''
            shape_type: 0
                #
                #
                ###
            shape_type: 1
                #####
                #
            shape_type: 2
                ###
                  #
                  #
            shape_type: 3
                    #
                #####
        '''
        point_list = self.current_shape['points']
        shape_type = self.current_shape['type']
        if shape_type == 0:
            shape_type = 1
            x, y = point_list[2][0], point_list[2][1]
            points = [(x, y), (x + 1, y), (x + 1, y - 1), (x + 1, y - 2)]
        elif shape_type == 1:
            shape_type = 2
            x, y = point_list[0][0], point_list[0][1]
            points = [(x + 2, y), (x + 2, y - 1), (x + 1, y - 1), (x, y - 1)]
        elif shape_type == 2:
            shape_type = 3
            x, y = point_list[-1][0], point_list[-1][1]
            points = [(x + 1, y), (x, y), (x, y + 1), (x, y + 2)]
        else:
            shape_type = 0
            x, y = point_list[2][0], point_list[2][1]
            points = [(x + 2, y), (x + 1, y), (x, y), (x, y - 1)]
        return shape_type, points

    def change_j_shape(self):
        '''
            shape_type: 0
                #
                #
               ##
            shape_type: 1
                #
                ######
            shape_type: 2
                ###
                #
                #
            shape_type: 3
                ######
                     #
        '''
        point_list = self.current_shape['points']
        shape_type = self.current_shape['type']
        if shape_type == 0:
            shape_type = 1
            x, y = point_list[-1][0], point_list[-1][1]
            points = [(x + 1, y), (x, y), (x, y - 1), (x, y - 2)]
        elif shape_type == 1:
            shape_type = 2
            x, y = point_list[1][0], point_list[1][1]
            points = [(x, y), (x + 1, y), (x + 2, y), (x + 2, y - 1)]
        elif shape_type == 2:
            shape_type = 3
            x, y = point_list[0][0], point_list[0][1]
            points = [(x + 1, y), (x + 1, y - 1), (x + 1, y - 2), (x, y - 2)]
        else:
            shape_type = 0
            x, y = point_list[0][0], point_list[0][1]
            points = [(x + 1, y - 1), (x, y - 1), (x - 1, y - 1), (x - 1, y)]

        return shape_type, points

    def change_s_shape(self):
        """
            shape_type: 0
                 ###
               ###
            shape_type: 1
                #
                ##
                 #
        """
        point_list = self.current_shape['points']
        shape_type = self.current_shape['type']
        if shape_type == 0:
            shape_type = 1
            x, y = point_list[-1][0], point_list[-1][1]
            points = [(x + 2, y), (x + 1, y), (x + 1, y - 1), (x, y - 1)]
        else:
            shape_type = 0
            x, y = point_list[-1][0], point_list[-1][1]
            points = [(x + 1, y - 1), (x + 1, y), (x, y), (x, y + 1)]

        return shape_type, points

    def change_z_shape(self):
        """
            shape_type: 0
                ###
                  ###
            shape_type: 1
                  #
                ##
                #
        """
        point_list = self.current_shape['points']
        shape_type = self.current_shape['type']
        if shape_type == 0:
            shape_type = 1
            x, y = point_list[2][0], point_list[2][1]
            points = [(x + 2, y - 1), (x + 1, y - 1), (x + 1, y), (x, y)]
        else:
            shape_type = 0
            x, y = point_list[-1][0], point_list[-1][1]
            points = [(x + 1, y + 1), (x + 1, y), (x, y), (x, y - 1)]

        return shape_type, points

    def change_t_shape(self):
        """
            shape_type: 0
                #
               ###
            shape_type: 1
                #
                ##
                #
            shape_type: 2
                ###
                 #
            shape_type: 3
                #
               ##
                #
        """
        point_list = self.current_shape['points']
        shape_type = self.current_shape['type']
        if shape_type == 0:
            shape_type = 1
            x, y = point_list[0][0], point_list[0][1]
            points = [(x + 1, y), (x, y), (x - 1, y), (x, y - 1)]
        elif shape_type == 1:
            shape_type = 2
            x, y = point_list[1][0], point_list[1][1]
            points = [(x, y + 1), (x, y), (x, y - 1), (x - 1, y)]
        elif shape_type == 2:
            shape_type = 3
            x, y = point_list[1][0], point_list[1][1]
            points = [(x + 1, y), (x, y), (x - 1, y), (x, y + 1)]
        else:
            shape_type = 0
            x, y = point_list[2][0], point_list[2][1]
            points = [(x + 1, y), (x, y + 1), (x, y), (x, y - 1)]

        return shape_type, points

    def get_random_shape(self):
        shape = random.choice(self.SHAPE_LIST)
        self.current_shape['shape'] = shape
        self.current_shape['points'] = self.SHAPE_TYPE_HASH[shape]
        self.current_shape['type'] = 0


class Tetris(object):
    def __init__(self):
        self.light = Light()
        self.shape = Shape()
        self.lighted_point = set()
        self.setup_kb()

    def light_off_all(self):
        for i in range(1, 17):
            for j in range(1, 9):
                self.light.light_off(Point(i, j))

    def refresh_light_points(self):
        self.light_off_all()
        for p in list(self.lighted_point):
            self.light.light_on(Point(p[0], p[1]))
        for p in self.shape.current_shape['points']:
            self.light.light_on(Point(p[0], p[1]))

    def get_next_shape(self):
        self.shape.get_random_shape()
        self.refresh_light_points()

    def change_shape(self):
        shape_type, points = self.shape.change_shape()
        if not self.check_points_ok(points):
            return False
        self.shape.current_shape['type'] = shape_type
        self.shape.current_shape['points'] = points
        self.refresh_light_points()
        return True

    def check_points_ok(self, points):
        for p in points:
            if p[0] < 1:
                return False
            if p[1] < 1 or p[1] > 8:
                return False
            if self.lighted_point & set(points):
                return False
        return True

    def drop_down(self):
        old_points = self.shape.current_shape['points']
        points = [(p[0] - 1, p[1]) for p in old_points]
        rst = self.check_points_ok(points)
        if not rst:
            self.lighted_point = self.lighted_point | set(old_points)
            self.shape.current_shape['points'] = []
        else:
            self.shape.current_shape['points'] = points
        self.refresh_light_points()
        return rst

    def move_left(self):
        old_points = self.shape.current_shape['points']
        points = [(p[0], p[1] + 1) for p in old_points]
        if self.check_points_ok(points):
            self.shape.current_shape['points'] = points
            self.refresh_light_points()
            return True
        return False

    def move_right(self):
        old_points = self.shape.current_shape['points']
        points = [(p[0], p[1] - 1) for p in old_points]
        if self.check_points_ok(points):
            self.shape.current_shape['points'] = points
            self.refresh_light_points()
            return True
        return False

    def run(self):
        self.light_off_all()
        self.get_next_shape()
        while True:
            char = self.get_kbhit()
            if char == " ":
                self.change_shape()
            elif char == "a":
                self.move_left()
            elif char == "d":
                self.move_right()
            rst = self.drop_down()
            if not rst:
                self.check_score()
                self.get_next_shape()
            bcm.delay(1000)

    def check_score(self):
        light_off_lines = {}
        for i in xrange(1, 17):
            light_off_lines[i] = []
            for p in list(self.lighted_point):
                if p[0] == i:
                    light_off_lines[i].append((i, p[1]))
        for key, value in light_off_lines.iteritems():
            if len(value) == 8:
                self.light_off_line(key)

    def light_off_line(self, line):
        new_lighted_points = set()
        for p in list(self.lighted_point):
            if p[0] > line:
                new_lighted_points.add((p[0] - 1, p[1]))
            elif p[0] < line:
                new_lighted_points.add((p[0], p[1]))
        self.lighted_point = new_lighted_points
        self.refresh_light_points()

    def get_kbhit(self):
        r = select.select([sys.stdin], [], [], 0.01)
        rcode = ""
        if len(r[0]) > 0:
            rcode = sys.stdin.read(1)
        return rcode

    def setup_kb(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        new_settings = old_settings
        new_settings[3] = new_settings[3] & ~termios.ICANON
        new_settings[3] = new_settings[3] & ~termios.ECHONL
        termios.tcsetattr(fd, termios.TCSAFLUSH, new_settings)


def main():
    bcm.init()
    tetris = Tetris()
    tetris.run()
    bcm.close()


if __name__ == "__main__":
    main()
