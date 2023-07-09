#!/usr/bin/env python

# Maitre D
# Demonstrates trating a value as a condition

print("Welcome to the Chateau D' Food.")
print("It seems we are quite full this evening.\n")

money = int(input("How many dollars did"\
                " you slip the Maitre D'?: "))
#tip = int()
#print(money)

if money > 0:
    print("Ah, I am reminded of a table.",
          "Right this way.")
else:
    print("Please sit, it might",
          "take a while.")
    
input("\n\nPress the enter key to exit.")