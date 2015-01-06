#-*- coding:utf-8 -*-

from base import bcm
from base import Point
from base import Light


class Love(object):
    LOVE_POINTS = [
        (8, 1), (7, 2), (6, 3), (5, 4), (4, 5),
        (4, 6), (5, 7), (6, 8), (7, 7), (8, 6),
        (8, 2), (8, 3), (8, 4), (8, 5),
        (7, 3), (7, 4), (7, 5), (7, 6),
        (6, 4), (6, 5), (6, 6), (6, 7),
        (5, 5), (5, 6)
    ]

    def __init__(self):
        self.light = Light()

    def run(self):
        for i in xrange(16, 0, -1):
            for j in xrange(1, 9):
                self.light.light_off(Point(i, j))
        for point in self.LOVE_POINTS:
            self.light.light_on(Point(point[0], point[1]))
            self.light.light_on(Point(17 - point[0], point[1]))
            bcm.delay(100)

        while True:
            for point in self.LOVE_POINTS:
                self.light.light_off(Point(point[0], point[1]))
                self.light.light_off(Point(17 - point[0], point[1]))
            bcm.delay(420)
            for point in self.LOVE_POINTS:
                self.light.light_on(Point(point[0], point[1]))
                self.light.light_on(Point(17 - point[0], point[1]))
            bcm.delay(580)


if __name__ == "__main__":
    love = Love()
    bcm.init()
    love.run()
    bcm.close()
