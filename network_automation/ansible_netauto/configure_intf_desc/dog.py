#!/usr/bin/env python

class Dog:
    """A simple attempt to model a dog."""

    def __init__(self, name, age):
        """Initialize name and age attributes."""
        self.name = name
        self.age = age

    def sit(self):
        """simulate a dog sitting in response to a command."""
        print(f"{self.name} is now sitting.")

    def roll_over(self):
        """simulate rolling over in response to a command."""
        print(f"{self.name} rolled over!")


my_dog = Dog('Rocky', 2)

print(f"My dog's name is {my_dog.name}")
print(f"My dog is {my_dog.age} years old.")
        
