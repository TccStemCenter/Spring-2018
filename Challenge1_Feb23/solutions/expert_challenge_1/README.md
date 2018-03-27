Expert Challenge 1
==================

# The Challenge

* create a program that parses a joke website and print a random joke to the screen

# The Solution

* please watch the youtube video if you need some help

```python
"""
print a random joke from the website, goodbadjokes.com

note that all web parsing is specific to goodbadjokes.com, but the video guide
can be helpful in parsing other joke websites, as well.
"""

from bs4 import BeautifulSoup
from bs4 import NavigableString
from random import randint
from urllib.error import URLError
from urllib.request import urlopen

# the url used a the source of jokes
url = "https://www.goodbadjokes.com/"

try:
    with urlopen(url) as request:
        # try to read in raw html from website into `html`
        html = request.read()
except URLError:
    # if this fails, the internet connection must be down
    print("There was an error opening url {}".format(url))
    exit(1)

# use BeautifulSoup to parse web page
soup = BeautifulSoup(html, "html.parser")

# find all `div` tags where `class` equals "joke-body-wrap"
joke_containers = soup.findAll("div", {"class": "joke-body-wrap"})

# all jokes on the page
jokes = []
for joke_container in joke_containers:
    # all the lines in each joke
    joke = []
    for line in joke_container.findChildren("a", {"class": "permalink"})[0].contents:
        if type(line) == NavigableString:
            # if it's a NavigableString, create one-item tuple for consistency
            clean_lines = (str(line),)
        else:
            # otherwise, it should be a Tag, so use `.stripped_lines` to get list of lines
            clean_lines = line.stripped_strings
        for clean_line in clean_lines:
            # run through each `clean_line`
            if clean_line:
                # if not empty, add `clean_line` to `joke` list
                joke.append(clean_line.strip(" \n\r"))
    if joke:
        # if `joke` not empty, add to `jokes` list
        jokes.append(joke)

# print a random joke with nice formatting, and BOOM! :) ~ enjoy
print("\n\t> ".join(jokes[randint(0, len(jokes) - 1)]))
```

