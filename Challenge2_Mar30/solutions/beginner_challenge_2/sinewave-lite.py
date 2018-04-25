#!/usr/bin/env python3
# -*- coding: utf-8 -*-


r"""  _                                          _ _ _       
 ___(_)_ __   _____      ____ ___   _____      | (_) |_ ___ 
/ __| | '_ \ / _ \ \ /\ / / _` \ \ / / _ \_____| | | __/ _ \
\__ \ | | | |  __/\ V  V / (_| |\ V /  __/_____| | | ||  __/
|___/_|_| |_|\___| \_/\_/ \__,_| \_/ \___|     |_|_|\__\___|
                                                            
print a sine wave based on user input
"""

from math import sin, pi

def main():
    a = None
    while a is None:
        try: a = round(float(input("Amplitude of the wave: ")))
        except ValueError: warn("Amplitude must be a valid number. Try again.")
    l = None
    while l is None:
        try: l = round(float(input("Wavelength of the wave: ")))
        except ValueError: warn("Wavelength must be a valid number. Try again.")
    L = None
    while L is None:
        try: L = round(float(input("Length of the wave: ")))
        except ValueError: warn("Length must be a valid number. Try again.")

    for y in range(L):
        line = " " * (2 * a)
        x = round(a * sin(2 * pi / l * y)) + a
        line = line[:x] + "*" + line[x:]
        print(line)


def warn(msg):
    print("*WARNING* {}".format(msg))


main()
