#!/usr/bin/env python3
import datetime
import sys
import time

import CHIP_IO.GPIO as GPIO
import astral
import pytz

import tm1637


def show_clock(tm, sunset):
        t = datetime.datetime.now(pytz.utc)
        seconds = int((sunset - t).total_seconds())
        minutes = seconds // 60
        seconds -= 60 * minutes
        hours = minutes // 60
        minutes -= 60 * hours
        time.sleep(1 - time.time() % 1)
        if hours:
            d0 = tm.digit_to_segment[hours // 10] if hours // 10 else 0
            d1 = tm.digit_to_segment[hours % 10]
            d2 = tm.digit_to_segment[minutes // 10]
            d3 = tm.digit_to_segment[minutes % 10]
        else:
            d0 = tm.digit_to_segment[minutes // 10] if minutes // 10 else 0
            d1 = tm.digit_to_segment[minutes % 10]
            d2 = tm.digit_to_segment[seconds // 10]
            d3 = tm.digit_to_segment[seconds % 10]
        tm.set_segments([d0, 0x80 + d1, d2, d3])
        time.sleep(.5)
        tm.set_segments([d0, d1, d2, d3])


if __name__ == "__main__":
    tm = tm1637.TM1637(clk='XIO-P1', dio='XIO-P0')
    location = astral.Location()
    location.latitude, location.longitude, location.elevation = (float(n) for n in sys.argv[1:])
    try:
        while True:
            show_clock(tm, location.sun()['sunset'])
    finally:
        tm.set_segments([0, 0, 0, 0])
        GPIO.cleanup()
