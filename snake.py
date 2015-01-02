#-*- coding:utf-8 -*-

import random
import sys
import select
import termios

import PyBCM2835 as pybcm


class BCM(object):

    def write_byte(self, data):
        pybcm.gpio_write(pybcm.RPI_GPIO_P1_24, pybcm.LOW)
        pybcm.spi_transfer(data)

    def write(self, addr1, data1, addr2, data2):
        pybcm.gpio_write(pybcm.RPI_GPIO_P1_24, pybcm.LOW)
        self.write_byte(addr1)
        self.write_byte(data1)
        self.write_byte(addr2)
        self.write_byte(data2)
        pybcm.gpio_write(pybcm.RPI_GPIO_P1_24, pybcm.HIGH)

    def init(self):
        pybcm.init()
        pybcm.spi_begin()
        pybcm.spi_setBitOrder(pybcm.SPI_BIT_ORDER_MSBFIRST)
        pybcm.spi_setDataMode(pybcm.SPI_MODE0)
        pybcm.spi_setClockDivider(pybcm.SPI_CLOCK_DIVIDER_256)
        pybcm.gpio_fsel(pybcm.RPI_GPIO_P1_24, pybcm.GPIO_FSEL_OUTP)

        pybcm.gpio_write(0x3c, pybcm.HIGH)
        pybcm.delay(50)

        for i in xrange(1, 9):
            self.write(i, 0x0, i, 0x0)

    def close(self):
        pybcm.spi_end()
        pybcm.close()

    def delay(self, ms):
        pybcm.delay(ms)


bcm = BCM()


class Point(object):
    L_CHIP = 1
    R_CHIP = 2

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.setup()

    def __eq__(self, obj):
        if self.x == obj.x and self.y == obj.y:
            return True
        return False

    def setup(self):
        if self.x < 9:
            self.real_x = 2 ** (self.x - 1)
            self.real_y = self.y
            self.flag = Point.L_CHIP
        else:
            self.real_x = 2 ** (self.x - 9)
            self.real_y = self.y
            self.flag = Point.R_CHIP


class Light(object):
    l_lighted = []
    r_lighted = []

    def light_on(self, point):
        if point.flag == Point.L_CHIP:
            x = point.real_x
            for light in Light.l_lighted:
                if light.real_y == point.real_y:
                    x += light.real_x
            Light.l_lighted.append(point)
            bcm.write(point.real_y, x, 0, 0)
        else:
            x = point.real_x
            for light in Light.r_lighted:
                if light.real_y == point.real_y:
                    x += light.real_x
            Light.r_lighted.append(point)
            bcm.write(0, 0, point.real_y, x)

    def light_off(self, point):
        x = 0
        del_index = None
        if point.flag == Point.L_CHIP:
            for index, light in enumerate(Light.l_lighted):
                if light.real_y == point.real_y:
                    if light.real_x == point.real_x:
                        del_index = index
                        continue
                    x += light.real_x
            if del_index is not None:
                del Light.l_lighted[del_index]
            bcm.write(point.real_y, x, 0, 0)
        else:
            for index, light in enumerate(Light.r_lighted):
                if light.real_y == point.real_y:
                    if light.real_x == point.real_x:
                        del_index = index
                        continue
                    x += light.real_x
            if del_index is not None:
                del Light.r_lighted[del_index]
            bcm.write(0, 0, point.real_y, x)


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
