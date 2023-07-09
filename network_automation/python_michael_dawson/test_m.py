#!/usr/bin/env python

# Author: Reuben Ezeh

tip = int(input("How many dollars did"\
                " you slip the Maitre D'?: "))
#tip = int()
print(tip)

if tip:
    print("Your table awaits.")
else:
    print("Please sit, it might",
          "take a while.")
    
input("\n\nPress the enter key to exit.")