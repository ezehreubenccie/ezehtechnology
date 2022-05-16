#!/usr/bin/env python3


class Dog:
    '''
    This class model's a dog
    '''

    def __init__(self, name, age):
        '''
        Initialize name and age attributes.
        '''
        self.name = name
        self.age = age

    def sit():
        print(f'{self.name} is now sitting')


def main():
    my_dog = Dog('Willie', 6)
    print(f"My dog's name is {my_dog.name}")

if __name__ == '__main__':
    main()
