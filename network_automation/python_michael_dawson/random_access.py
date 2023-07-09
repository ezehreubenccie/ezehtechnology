#!/usr/bin/env python

# Random Access
# Demonstrates string indexing

import random

word = "index"
print("The word is ", word, "\n")

high = len(word)
low = -len(word)

for i in range(10):
    position = random.randrange(low, high)
    #print(position)
    print("word[", position, "]\t", word[position])

input("\n\nPress the enter key to exit.")