#!/usr/bin/env python

from pprint import pprint
message = 'It was a bright and cold day in April, and the clocks were striking thirteen.'
count = {}

for character in message:
    count.setdefault(character, 0)
print(count)
