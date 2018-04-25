Beginner Challenge 2
====================

## The Challenge

* Create a program that prints out an ascii sine wave and that expects user input (or, optionally, command-line args) that dictate the `amplitude` and `wavelength` of the wave.
    - When run, your program should prompt the user for the `amplitude` and `wavelength` (if not provided in args); then, it should print a sinusoidal wave with the correct amplitude and wavelength, given the user input or args.

## The Solution

#### sinewave-lite

###### vertical (easier)

```python
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
```

#### sinewave

###### horizontal (slightly harder)

```python
#!/usr/bin/env python3

r"""     _
 ___(_)_ __   _____      ____ ___   _____   _ __  _   _
/ __| | '_ \ / _ \ \ /\ / / _` \ \ / / _ \ | '_ \| | | |
\__ \ | | | |  __/\ V  V / (_| |\ V /  __/_| |_) | |_| |
|___/_|_| |_|\___| \_/\_/ \__,_| \_/ \___(_) .__/ \__, |
small fun ascii sine wave generator        |_|    |___/"""

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from math import pi, sin
from sys import stderr


def main():
    parser = ArgumentParser(
        formatter_class = RawDescriptionHelpFormatter,
        description = __doc__
    )
    parser.add_argument('-A', '--amplitude', type=float, default=None, help='Amplitude of the wave', metavar='{amp}')
    parser.add_argument('-l', '--wavelen', type=float, default=None, help='Wavelength of each cycle', metavar='{wlen}')
    parser.add_argument('-L', '--length', type=float, default=None, help='Length of the wave', metavar='{len}')
    args = parser.parse_args()

    while args.amplitude is None:
        try: args.amplitude = float(input("Amplitude of wave: "))
        except ValueError: warn("Amplitude must be a number. Try again.")
    while args.wavelen is None:
        try: args.wavelen = float(input("Wavelength of wave: "))
        except ValueError: warn("Wavelength must be a number. Try again.")
    while args.length is None:
        try: args.length = float(input("Length of wave: "))
        except ValueError: warn("Length must be a number. Try again.")

    args.amplitude = round(args.amplitude)
    args.wavelen = round(args.wavelen)
    args.length = round(args.length)

    wave = []
    for y in range(args.amplitude * 2 + 1):
        wave.append([" "] * args.length)

    for x in range(args.length):
        y = args.amplitude * ( -sin(2 * pi / args.length * x) + 1 )
        wave[round(y)][x] = "*"

    for line in wave:
        print("".join(line))


def warn(msg):
    stderr.write("*WARNING* {}\n".format(msg))
    stderr.flush()


if __name__ == '__main__':
    main()
```
