Beginner Challenge 1
====================

## The Challenge

* Create a random joke generator.
    - When run, your program should print one random joke to the screen.

## The Solution

* Watch [the beginner solution video for Challenge 1 on YouTube](https://www.youtube.com/watch?v=o4MPGe4mLXA) for a guided overview of the solution.
    - The video uses [repl.it](https://repl.it/) to solve the challenge and provides a comprehensive explanation that is suitable for beginners and even intermediate programmers.

```python
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
```

