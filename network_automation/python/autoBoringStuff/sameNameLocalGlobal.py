#!/usr/bin/env python3


def spam():
    global eggs
    eggs = 'spam' # This is the global

def bacon():
    eggs = 'bacon'  # This is a local

def ham():
    print(eggs) # this is the global

eggs = 42 this is the global
spam()
print(eggs)
