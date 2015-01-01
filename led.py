#-*- coding:utf-8 -*-

import PyBCM2835 as bcm


def write_byte(data):
    bcm.gpio_write(bcm.RPI_GPIO_P1_24, bcm.LOW)
    bcm.spi_transfer(data)


def write(addr1, data1, addr2, data2):
    bcm.gpio_write(bcm.RPI_GPIO_P1_24, bcm.LOW)
    write_byte(addr1)
    write_byte(data1)
    write_byte(addr2)
    write_byte(data2)
    bcm.gpio_write(bcm.RPI_GPIO_P1_24, bcm.HIGH)


def init():
    write(0x09, 0x00, 0x09, 0x00)
    write(0x0a, 0x03, 0x0a, 0x03)
    write(0x0b, 0x07, 0x0b, 0x07)
    write(0x0c, 0x01, 0x0c, 0x01)
    write(0x0f, 0x00, 0x0f, 0x00)


bcm.init()
bcm.spi_begin()
bcm.spi_setBitOrder(bcm.SPI_BIT_ORDER_MSBFIRST)
bcm.spi_setDataMode(bcm.SPI_MODE0)
bcm.spi_setClockDivider(bcm.SPI_CLOCK_DIVIDER_256)
bcm.gpio_fsel(bcm.RPI_GPIO_P1_24, bcm.GPIO_FSEL_OUTP)

bcm.gpio_write(0x3c, bcm.HIGH)
bcm.delay(50)

init()
write(1, 0x10, 1, 0x3c)

bcm.delay(1000)

bcm.spi_end()
bcm.close()
