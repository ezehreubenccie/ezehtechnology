#!/usr/bin/env python3

import sys

while True:
    print('Type exit to exit')
    response = input()
    if response == 'exit':
        sys.exit()
    print('You typed ' + response + '.' )



