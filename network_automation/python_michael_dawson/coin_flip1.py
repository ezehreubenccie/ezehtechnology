#!/usr/bin/env python

# Coin Flip

import random

heads = 0
tails = 0

flip = random.randint(1, 2)

if flip == 1:
    flip = 'head'
    heads += 1
if flip == 2:
    flip = 'tails'
    tails += 1

print(f'number of heads is {heads} and',
      f"number of tails is {tails}.")

input("\n\nPress the enter key to exit.")