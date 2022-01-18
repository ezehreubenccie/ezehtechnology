#!/usr/bin/env python3


message = 'It was a bright cold day in April, and the clocks were striking thirteen.'

count = {}
print(len(message))
for character in message:
    print(character)
    count.setdefault(character, 0)
    print(count)
    count[character] = count[character] + 1
    print(count[character])
#print(count)
