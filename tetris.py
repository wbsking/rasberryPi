#-*- coding:utf-8 -*-

import random
import sys
import select
import termios

from base import bcm
from base import Light
from base import Point


class Tetris(object):
    def __init__(self):
        self.light = Light()

    