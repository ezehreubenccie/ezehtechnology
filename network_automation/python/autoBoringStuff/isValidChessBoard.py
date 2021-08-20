#!/usr/bin/env python

#chessBoard = {'wking': 1, 'wqueen': '1'}
from pprint import pprint

def isValidChessBoard(board):
#    answer = ''
#    answer2 = ''
    pieces = 0
    bpawns = 0
    wpawns = 0
    bking = 0
    wking = 0

    for k, v in board.items():
        if board[k] == 'bking':
            bking = bking + 1
        if board[k] == 'wking':
            wking = wking + 1
#    print(bking, wking)
        if bking == 1 and wking == 1:
        for k in board.keys():
            if board[k] == '' or board[k] == ' ':
                continue
            else:
                pieces = pieces + 1
#    print(pieces)
    if pieces == 32:
        for k, v in board.items():
            if board[k] == 'bpawn':
                bpawns = bpawns + 1
            if board[k] == 'wpawn':
                wpawns = wpawns + 1
#    print(bpawns, wpawns)
    if bpawns == 8 and wpawns == 8:
        for k in board.keys():
            row = int(k[:1])
            column = k[1:]
#    print(row <= 8, column <= 'h')
    if row <=8 and column <= 'h':
#        print(list(board.values()))
        for v in list(board.values()):
#            print(v)
#            pprint(board.values())
            if v.startswith('b') or v.startswith('w'):
                answer = True
#                print(answer)
#            if not v.startswith('b') or not v.startswith('w'):
#                answer = False
#                break
    print(answer)
#    if answer == True:
#        return 'true'
#    else:
#        return 'false'

#    return false 

board = {'1a': 'bking','2a': 'bqueen','3a': 'brook','4a': 'brook',
'5a': 'bknight','6a': 'bknight','7a':'bbishop','8a': 'bbishop',
'1b': 'bpawn','2b': 'bpawn','3b': 'bpawn','4b':'bpawn',
'5b': 'bpawn','6b': 'bpawn','7b': 'bpawn','8b': 'bpawn',
'1c': 'wking','2c': 'wqueen','3c': 'wrook','4c': 'wrook',
'5c': 'wbishop','6c': 'wbishop','7c': 'wknight','8c':'wknight',
'1e': 'zpawn','2e': 'wpawn','3e': 'wpawn','4e': 'wpawn',
'5e': 'wpawn','6e': 'wpawn','7e': 'wpawn','8e': 'wpawn',
'1f': '','2f': '','3f': '','4f': '','5f': '','6f': '','7f': '','8f': '',
'1g': '','2g': '','3g': '','4g': '','5g': '','6g': '','7g': '','8g': '',
'1h': '','2h': '','3h': '','4h': '','5h': '','6h': '','7h': '','8h': '',}

isValidChessBoard(board)
