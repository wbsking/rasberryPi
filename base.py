#-*- coding:utf-8 -*-

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

        self.write(0x09, 0x00, 0x09, 0x00)
        self.write(0x0a, 0x03, 0x0a, 0x03)
        self.write(0x0b, 0x07, 0x0b, 0x07)
        self.write(0x0c, 0x01, 0x0c, 0x01)
        self.write(0x0f, 0x00, 0x0f, 0x00)

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
