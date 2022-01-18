#!/usr/bin/env python3


VOWELS = ('a', 'e', 'i', 'o', 'u', 'y')

print('Enter the English message to translate into Pig Latin:')
message = input()
pigLatin = []

for word in message.split():
    prefixNonLetters = ''
    while len(word) > 0 and not word[0].isalpha():
        prefixNonLetters += word[0]
#        print('prefixNonLetters is: ' + prefixNonLetters)
        word = word[1:]
    print('prefixNonLetters at the start is: ' + prefixNonLetters)

    suffixNonLetters = ''
#    print(word[-1])
    while len(word) > 0 and not word[-1].isalpha():
        suffixNonLetters += word[-1]
        word = word[:-1]
        print('word after non word suffix removed is: ' + word)
        print('suffixNonLetters is: ' + suffixNonLetters)

    print('word before if condition is: ' + word)
    print('suffixNonLetters before if statement is:')
    if len(word) > 0 and word[0].lower() in VOWELS:
        word += 'yay' + suffixNonLetters
        print('word after vowel if is: ' + word) 

    prefixConsonants = ''
    print('word before consonant while is: ' + word)
    while len(word) > 0 and not word[0].lower() in VOWELS:
        prefixConsonants += word[0]
        word = word[1:]
    print('prefixConsonants is: ' + prefixConsonants)
    if prefixConsonants:
        word += prefixConsonants + 'ay'
        print('word after consonant if is: ' + word)

#    prefixNonLetters = ''
#    while len(word) > 0 and not word[0].isalpha():
#        prefixNonLetters += word[0]
#        word = word[1:]
    print('prefixNonLetters before append to pig Latin list is: ' + prefixNonLetters)
    pigLatin.append(word)
print(pigLatin)
