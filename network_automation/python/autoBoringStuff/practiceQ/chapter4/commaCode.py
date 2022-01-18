#!/usr/bin/env python3


def myfunc(list1):
    str1 = ''
    for i in range(len(list1)):
        if i == len(list1) - 1:
            str1 = str1 + 'and ' + list1[i]
        else:
            str1 = str1 + list1[i] + ', '
    print(str1)
    print(type(str1))



if __name__ == '__main__':
#    spam = ['apples', 'bananas', 'tofu', 'cats']
    spam = ['Reuben', 'Hannah', 'Jaden', 'Naomi']
    myfunc(spam)
