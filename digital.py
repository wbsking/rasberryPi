#-*- coding:utf-8 -*-

from base import bcm
from base import Point
from base import Light


class Digital(object):
    DIGITAL_MAP = {
        1: {"left": [(3, 6), (4, 7), (5, 8),
                     (5, 7), (5, 6), (5, 5),
                     (5, 4), (5, 3), (5, 2),
                     (3, 1), (4, 1), (5, 1),
                     (6, 1), (7, 1)]
            },
        2: {"left": [(2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8),
                     (7, 7), (7, 6), (7, 5), (6, 5), (5, 5), (4, 5), (3, 5),
                     (2, 5), (2, 4), (2, 3), (2, 2), (2, 1), (3, 1), (4, 1),
                     (5, 1), (6, 1), (7, 1)]
            }
    }

    def __init__(self):
        self.light = Light()

    def run(self):
        for p in self.DIGITAL_MAP[2]['left']:
            self.light.light_on(Point(p[0], p[1]))

if __name__ == "__main__":
    di = Digital()
    bcm.init()
    di.run()
    bcm.close()
