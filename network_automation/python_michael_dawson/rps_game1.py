#!/usr/bin/env python

# Rock Papaer Scissors Game

import random, sys

computerMove = random.randint(1, 3)
#print("computerMove is ", computerMove)
if computerMove == 1:
    computerMove = 'r'
    #print("ROCK")
if computerMove == 2:
    computerMove = 'p'
    #print('PAPER')
if computerMove == 3:
    computerMove = 's'
    #print("SCISSORS")

playerMove = input("Enter your move, r for rock,"\
                   " p for paper, s for scissors or q for quit: ")

if playerMove == 'r':
    print("Your move is ROCK")
if playerMove == 'p':
    print("Your move is PAPER")
if playerMove == 's':
    print("Your move is SCISSORS")
if playerMove == 'q':
    sys.exit()
if playerMove != 'r' or playerMove != 'p' or playerMove != 's':
    print("Please type in r, p, s or q.")
    playerMove = input()


if computerMove == 'r' and playerMove == 'r':
    print("It is a Tie!")
if computerMove == 'r' and playerMove == 'p':
    print("You win!")
if computerMove == 'r' and playerMove == 's':
    print("You loose!")
if computerMove == 's' and playerMove == 's':
    print("It is a Tie!")
if computerMove == 's' and playerMove == 'p':
    print("You loose!")
if computerMove == 's' and playerMove == 'r':
    print("You win!")
if computerMove == 'p' and playerMove == 'p':
    print("It is a Tie!")
if computerMove == 'p' and playerMove == 'r':
    print("You loose!")
if computerMove == 'p' and playerMove == 's':
    print("You win!")

input("\n\nPress the enter key to exit.")
