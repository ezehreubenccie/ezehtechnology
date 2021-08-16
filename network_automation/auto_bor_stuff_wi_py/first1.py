#!/usr/bin/env python

passwordFile = open('SecretPasswordFile.txt')
secretPassword = passwordFile.read()
secretPassword = secretPassword.splitlines()
secretPassword = secretPassword[0]
#print(secretPassword)
print('Enter your password.')
typedPassword = input()
#print(typedPassword)
print()
if typedPassword == secretPassword:
    print('Access Granted')
elif typedPassword == '12345':
    print('That password is one that an idiot puts on their luggage.')
else:
    print('Access denied!')
