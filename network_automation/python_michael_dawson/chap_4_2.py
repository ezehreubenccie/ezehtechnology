#!/usr/bin/env python

message = input("Enter a message: ")
#print()
print("This is your message backwards:\n")

for xter in range(len(message) - 1, -1, -1):
    print(message[xter], end="")

input("\n\nPress the enter key to exit.")