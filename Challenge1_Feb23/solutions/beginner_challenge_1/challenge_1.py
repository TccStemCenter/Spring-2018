
"""
print a random joke to stdout
"""

from random import randint

# list of jokes
jokes = [
    "Why did the turtle cross the road?\n\t> To get to the other side.",
    "Why did the fat turkey cross the road?\n\t> To get hit by my car.",
    "What did the fish say when he/she hit a concrete wall?\n\t> Dam.",
]

# print a random joke
print( jokes[randint(0, len(jokes) - 1)] )

