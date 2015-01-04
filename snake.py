#-*- coding:utf-8 -*-

import random
import sys
import select
import termios

from base import bcm
from base import Light
from base import Point


class GameOver(Exception):
    pass


class Snake(object):
    MAX_X = 16
    MAX_Y = 8
    DIRECTION_LIST = ["U", "D", "L", "R"]

    def __init__(self):
        self._stop = False
        self.start_point = Point(1, 1)
        self.snake_list = []
        self._all_points = None
        self.light = Light()
        self. init()
        self.current_light_point = self.light_random_point()

    @property
    def all_points(self):
        if not self._all_points:
            self._all_points = set()
            for i in xrange(1, self.MAX_X + 1):
                for j in xrange(1, self.MAX_Y + 1):
                    self._all_points.add((i, j))
        return self._all_points

    def init(self):
        self.snake_list.insert(0, self.start_point)
        self.direction = "R"
        self.light.light_on(self.start_point)
        self.setup_kb()

    def light_random_point(self):
        lighted_set = set([(point.x, point.y) for point in self.snake_list])
        unlighted_set = self.all_points - lighted_set
        pos = random.choice(list(unlighted_set))
        point = Point(pos[0], pos[1])
        self.light.light_on(point)
        return point

    def get_next_point(self):
        char = self.get_kbhit()
        if char == "w":
            self.direction = "U"
        if char == "s":
            self.direction = "D"
        if char == "a":
            self.direction = "L"
        if char == "d":
            self.direction = "R"
        snake_head = self.snake_list[0]
        if self.direction == "R":
            p_x = snake_head.x + 1
            if p_x > self.MAX_X:
                raise GameOver
            point = Point(p_x, snake_head.y)
        if self.direction == "L":
            p_x = snake_head.x - 1
            if p_x < 1:
                raise GameOver
            point = Point(p_x, snake_head.y)
        if self.direction == "U":
            p_y = snake_head.y + 1
            if p_y > self.MAX_Y:
                raise GameOver
            point = Point(snake_head.x, p_y)
        if self.direction == "D":
            p_y = snake_head.y - 1
            if p_y < 1:
                raise GameOver
            point = Point(snake_head.x, p_y)

        if point in self.snake_list:
            raise GameOver
        return point

    def run(self):
        while not self._stop:
            try:
                next_point = self.get_next_point()
            except GameOver:
                self.game_over()
                break
            self.fresh_snake(next_point)
            bcm.delay(1000)

    def fresh_snake(self, next_point):
        self.snake_list.insert(0, next_point)
        if next_point == self.current_light_point:
            self.current_light_point = self.light_random_point()
        else:
            last = self.snake_list[-1]
            self.light.light_on(next_point)
            self.light.light_off(last)
            del self.snake_list[-1]

    def game_over(self):
        print "GameOver"

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
    snake = Snake()
    snake.run()
    bcm.close()


if __name__ == "__main__":
    main()
