#!/usr/bin/env python3

#chessBoard = {'wking': 1, 'wqueen': '1'}
from pprint import pprint

def isValidChessBoard(board):
    validBoard = {'bking': 1, 'wking': 1}
    player = {'player1': {'bpawns': 8, 'brook': 2, 'bbishop': 2, 'bknight': 2, 'bking': 1, 'bqueen': 1},
              'player2': {'wpawns': 8, 'wrook': 2, 'wbishop': 2, 'wknight': 2, 'wking': 1, 'wqueen': 1}}
    validSpace = ['1a', '1b', '1c', '1d', '1e', '1f', '1g', '1h',
                  '2a', '2b', '2c', '2d', '2e', '2f', '2g', '2h',
                  '3a', '3b', '3c', '3d', '3e', '3f', '3g', '3h',
                  '4a', '4b', '4c', '4d', '4e', '4f', '4g', '4h',
                  '5a', '5b', '5c', '5d', '5e', '5f', '5g', '5h',
                  '6a', '6b', '6c', '6d', '6e', '6f', '6g', '6h',
                  '7a', '7b', '7c', '7d', '7e', '7f', '7g', '7h',
                  '8a', '8b', '8c', '8d', '8e', '8f', '8g', '8h']

    pieceNames = ['brook', 'bqueen', 'bbishop', 'bking', 'bknight', 'bpawn',
                  'wrook', 'wqueen', 'wbishop', 'wking', 'wknight', 'wpawn']

    count = {}
    for v in board.values():
        count.setdefault(v, 0)
        count[v] = count[v] + 1
    print(count)
    
    if ('bking' in count.keys()) and ('wking' in count.keys()):
        if (count['bking'] == validBoard['bking'] and count['wking'] == validBoard['wking']   
            and count['bking'] != '' and count['bking'] != ' ' and count['wking'] != '' and count['wking'] != ' '):
            print('1 bking and 1 wking is verified.')
            criteria1 = 'true'
    else:
        criteria1 = 'false'
    numPiecesPlayer1 = 0
    numPiecesPlayer2 = 0
    numPiecesBoard = 0
    for k, v in player['player1'].items():
#        print(k)
#        print(v)
        numPiecesPlayer1 = numPiecesPlayer1 + v
    print(numPiecesPlayer1)
    for k, v in player['player2'].items():
        numPiecesPlayer2 = numPiecesPlayer2 + v
    print(numPiecesPlayer2)
    del count['']
    print(count)
    for k, v in count.items():
        numPiecesBoard = numPiecesBoard + v
    print(numPiecesBoard)
    if numPiecesPlayer1 + numPiecesPlayer2 == numPiecesBoard:
        criteria2 = 'true'
    else:
        criteria2 = 'false'

    boardSpace = []
    for k in board.keys():
        boardSpace.append(k)
#    print(boardSpace)
#    print(type(boardSpace))

    space = 0
    match = 0
    print(len(boardSpace))
    print(len(validSpace))
    while space != len(boardSpace):
        if boardSpace[space] in validSpace:
            space = space + 1
            match = match + 1
        else:
            break
    print(space, match)
    if match == len(validSpace):
        criteria3 = 'true'
    else:
        criteria3 = 'false'
#    print(count)
    beginsWithborw = 0
    boardNames = []
    for v in count.keys():
        boardNames.append(v)
#    del boardNames['']
#    del boardNames[' ']
    print(boardNames)
    for name in boardNames:
        if name.startswith('b') or name.startswith('w'):
            beginsWithborw = beginsWithborw + 1
#            match = match + 1
        else:
            break
#    print(beginsWithborw, len(boardNames))
    if beginsWithborw == len(boardNames):
        criteria4 = 'true'
    else:
        criteria4 = 'false'

    print(criteria1, criteria2, criteria3, criteria4)
    if criteria1 == criteria2 == criteria3 == criteria4:
        return True
    else:
        return False
board = {'1a': 'bking','2a': 'bqueen','3a': 'brook','4a': 'brook',
'5a': 'bknight','6a': 'bknight','7a':'bbishop','8a': 'bbishop',
'1b': 'bpawn','2b': 'bpawn','3b': 'bpawn','4b':'bpawn',
'5b': 'bpawn','6b': 'bpawn','7b': 'bpawn','8b': 'bpawn',
'1c': 'wking','2c': 'wqueen','3c': 'wrook','4c': 'wrook',
'5c': 'wbishop','6c': 'wbishop','7c': 'wknight','8c':'wknight',
'1e': 'wpawn','2e': '','3e': 'wpawn','4e': 'wpawn',
'5e': 'wpawn','6e': 'wpawn','7e': 'wpawn','8e': 'wpawn',
'1f': '','2f': '','3f': '','4f': '','5f': '','6f': '','7f': '','8f': '',
'1g': '','2g': '','3g': '','4g': '','5g': '','6g': '','7g': '','8g': '',
'1h': '','2h': '','3h': 'wpawn','4h': '','5h': '','6h': '','7h': '','8h': '',}

answer = isValidChessBoard(board)
if answer == True:
    print('chess board is valid!')
else:
    print('Invalid chess board!.')
