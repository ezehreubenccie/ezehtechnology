#!/usr/bin/env python

birthdays = {'Alice': 'Apr 1', 'Bob': 'Dec 12', 'Carol': 'Mar 4'}
print('****birthdays before adding new names.****')
print(birthdays)
while True:
    print('Enter a name: (blank to quit)')
    name = input()
    if name == '':
        break


    if name in birthdays:
        print(birthdays[name] + ' is the birthday of ' + name)
    else:
        print('I do not have birthday information for ' + name)
        print('What is their birthday')
        bday = input()
        birthdays[name] = bday
        print('Birthday database updated.')
print('****birthday after adding new names.****')
print(birthdays)
