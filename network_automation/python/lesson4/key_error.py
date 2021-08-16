#!/usr/bin/env python

my_dict = {}
#print('Before')
#my_dict['ip_addr']
#print('What is my IP address?')


# Gracefully handle exception
#try:
#    print('Statement before')
#    my_dict['ip_addr']
#    print('Statement after')
#except KeyError:
#    print('Caught exception')
#
#print('After exception')

# Catch and re-raise some exception
#try:
#    my_dict['ip_addr']
#except KeyError:
#    print('Caught exception, re-raise')
#    raise
# Catch exception and retrieve information about it
#try:
#    my_dict['ip_addr']
#except KeyError as e:
#    print(e.__class__)
#    print(str(e))
#    print('Caught exception, printed info')

# Catch multiple exceptions
#my_list = []
#try:
#    my_list[0]
#    my_dict['ip_addr']
#except (KeyError, IndexError):
#    print('Handled multiple potential exceptions')
#my_list = []
#try:
##    my_list[0]
#    my_dict['ip_addr']
#except IndexError:
#    print('Handled Index Error')
#except KeyError:
#    print('Handled Key Error')

# Add a finally clause
#try:
#    my_dict['ip_addr']
#except KeyError:
#    print('IP address not found')
#finally:
#    print('This is always executed, exception or not')

# Catch any exception - for quick and dirty code/ on-off codes
try:
    my_dict['ip_addr']
    print('A different statement')
except Exception:
    print('IP address not found')
