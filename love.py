#-*- coding:utf-8 -*-

from base import Point
from base import Light


class Love(object):
    def __init__(self):
        self.light = Light()

    def run(self):
        for i in xrange(16, 0, -1):
            for j in xrange(1, 9):
                self.light.light_on(Point(i, j))


if __name__ == "__main__":
    love = Love()
    love.run()
