#!/usr/bin/env python3

from pprint import pprint


board = {'1a': 'bk','2a': 'bq','3a': 'br','4a': 'br',
'5a': 'bk','6a': 'bk','7a':'bb','8a': 'bb',
'1b': 'bp','2b': 'bp','3b': 'bp','4b':'bp',
'5b': 'bp','6b': 'bp','7b': 'bp','8b': 'bp',
'1c': 'wk','2c': 'wq','3c': 'wr','4c': 'wr',
'5c': 'wb','6c': 'wb','7c': 'wk','8c':'wk',
'1d': '  ','2d': '  ','3d': '  ','4d':'  ',
'5d': '  ','6d': '  ','7d': '  ','8d': '  ',
'1e': 'wp','2e': 'wp','3e': 'wp','4e': 'wp',
'5e': 'wp','6e': 'wp','7e': 'wp','8e': 'wp',
'1f': '  ','2f': '  ','3f': '  ','4f': '  ','5f': '  ','6f': '  ','7f': '  ','8f': '  ',
'1g': '  ','2g': '  ','3g': '  ','4g': '  ','5g': '  ','6g': '  ','7g': '  ','8g': '  ',
'1h': '  ','2h': '  ','3h': '  ','4h': '  ','5h': '  ','6h': '  ','7h': '  ','8h': '  '}

def printChessBoard(board):
    print()
    print('---------------------------------------')
    print(board['1a'] + ' | ' + board['2a'] + ' | ' + board['3a'] + ' | ' + board['4a'] + ' | ' 
          + board['5a'] + ' | ' + board['6a'] + ' | ' + board['7a'] + ' | ' + board['8a'] + ' | ')
    print('---+----+----+----+----+----+----+-----')
    print(board['1b'] + ' | ' + board['2b'] + ' | ' + board['3b'] + ' | ' + board['4b'] + ' | ' 
          + board['5b'] + ' | ' + board['6b'] + ' | ' + board['7b'] + ' | ' + board['8b'] + ' | ')
    print('---+----+----+----+----+----+----+-----')
    print(board['1c'] + ' | ' + board['2c'] + ' | ' + board['3c'] + ' | ' + board['4c'] + ' | ' 
          + board['5c'] + ' | ' + board['6c'] + ' | ' + board['7c'] + ' | ' + board['8c'] + ' | ')
    print('---+----+----+----+----+----+----+-----')
    print(board['1d'] + ' | ' + board['2d'] + ' | ' + board['3d'] + ' | ' + board['4d'] + ' | ' 
          + board['5d'] + ' | ' + board['6d'] + ' | ' + board['7d'] + ' | ' + board['8d'] + ' | ')
    print('---+----+----+----+----+----+----+-----')
    print(board['1e'] + ' | ' + board['2e'] + ' | ' + board['3e'] + ' | ' + board['4e'] + ' | ' 
          + board['5e'] + ' | ' + board['6e'] + ' | ' + board['7e'] + ' | ' + board['8e'] + ' | ')
    print('---+----+----+----+----+----+----+-----')
    print(board['1f'] + ' | ' + board['2f'] + ' | ' + board['3f'] + ' | ' + board['4f'] + ' | ' 
          + board['5f'] + ' | ' + board['6f'] + ' | ' + board['7f'] + ' | ' + board['8f'] + ' | ')
    print('---+----+----+----+----+----+----+-----')
    print(board['1g'] + ' | ' + board['2g'] + ' | ' + board['3g'] + ' | ' + board['4g'] + ' | ' 
          + board['5g'] + ' | ' + board['6g'] + ' | ' + board['7g'] + ' | ' + board['8g'] + ' | ')
    print('---+----+----+----+----+----+----+-----')
    print(board['1h'] + ' | ' + board['2h'] + ' | ' + board['3h'] + ' | ' + board['4h'] + ' | ' 
          + board['5h'] + ' | ' + board['6h'] + ' | ' + board['7h'] + ' | ' + board['8h'] + ' | ')
    print('---------------------------------------')



#def isValidChessBoard(board):


print('This is a Vaild Chess board!!')
printChessBoard(board)

print('This is your board!')


#isValidChessBoard(board)
