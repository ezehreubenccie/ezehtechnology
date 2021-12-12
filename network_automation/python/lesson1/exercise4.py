#!/usr/bin/env python
show_version = '*0        CISCO881-SEC-K9        FTX0000038X     '
print('show_version output:')
print(show_version)
print('\n')
print('****Removing all leading and trailing whitespace from the string****')
print(show_version.strip())
print('\n')
print('****Extract model and serial number****')
print('Model: {}\nSerial#: {}'.format(show_version.split()[1], show_version.split()[2]))
print('\n')
print('****check if cisco is in Model String****')
print('Cisco' in show_version.split()[1])
print('\n')
print('****check if "881" is in Model String****')
print('881' in show_version.split()[1])
print('\n')

