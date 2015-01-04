#-*- coding:utf-8 -*-

from base import bcm
from base import Point
from base import Light


class Love(object):
    def __init__(self):
        self.light = Light()

    def run(self):
        for i in xrange(16, 0, -1):
            for j in xrange(1, 9):
                self.light.light_on(Point(i, j))
        self.light.light_on(Point(8, 1))
        bcm.delay(80)
        self.light.light_on(Point(9, 1))
        bcm.delay(80)
        self.light.light_on(Point(7, 2))
        bcm.delay(80)
        self.light.light_on(Point(10, 2))
        bcm.delay(80)
        self.light.light_on(Point(6, 3))
        bcm.delay(80)
        self.light.light_on(Point(11, 3))
        bcm.delay(80)
        self.light.light_on(Point(5, 4))
        bcm.delay(80)
        self.light.light_on(Point(12, 4))
        bcm.delay(80)
        self.light.light_on(Point(5, 5))
        bcm.delay(80)
        self.light.light_on(Point(12, 5))
        bcm.delay(80)
        self.light.light_on(Point(6, 6))
        bcm.delay(80)
        self.light.light_on(Point(11, 6))
        bcm.delay(80)
        self.light.light_on(Point(7, 7))
        bcm.delay(80)
        self.light.light_on(Point(10, 7))
        bcm.delay(80)
        self.light.light_on(Point(8, 6))
        bcm.delay(80)
        self.light.light_on(Point(9, 6))

if __name__ == "__main__":
    love = Love()
    bcm.init()
    love.run()
    bcm.close()
