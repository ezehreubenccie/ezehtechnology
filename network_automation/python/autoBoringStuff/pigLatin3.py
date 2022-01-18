#!/usr/bin/env python3


# English to Pig Latin
print('Enter the English message to translate to Pig Latin:')
message = input()


VOWELS = ('a', 'e', 'i', 'o', 'u', 'y')

pigLatin = [] # A list of the words in Pig Latin
print('first pigLatin List before for loop is  ', pigLatin)
print('message.split() is ', message.split())
for word in message.split():
    print('first word after for loop is: ' + word)
    # Seperate the non-letters at the start of this word:
    prefixNonLetters = ''
    print('first pig Latin in for loop is: ', pigLatin)
    while len(word) > 0 and not word[0].isalpha():
        prefixNonLetters += word[0]
        print('prefixNonLetters is after first while loop is:  ' + prefixNonLetters)
        word = word[1:]
        print('word after first while loop is: ' + word)
    if len(word) == 0:
        print('word in first if is: ' + word)
        print('pigLatin after first if is: ', pigLatin)
        pigLatin.append(prefixNonLetters)
        print('second pigLatin after first if is: ', pigLatin)
        continue
    # Seperate the non-letters at the end of this word:
    suffixNonLetters = ''
    print('This is the suffix section and word is ' + word + ' word[-1] is ' + word[-1])
    while not word[-1].isalpha():
        suffixNonLetters += word[-1]
        print('suffixNonLetters in second while loop is: ' + suffixNonLetters)
        word = word[:-1]
        print('word in second while loop is: ' + word)
    # Remember if the word was in uppercase or title case.
    wasUpper = word.isupper()
    wasTitle = word.istitle()

    word = word.lower() # Make the word lower case for translation
##
##
##
    # Seperate the consonants at the start of this word:
    prefixConsonants = ''
    print('word before third while loop is: ' + word)
    while len(word) > 0 and not word[0] in VOWELS:
        prefixConsonants += word[0]
        print('prefix consonant in 3rd while loop  is: ' + prefixConsonants)
        word = word[1:]

    # Add the pig Latin ending to the word:
    print('prefixConsonants is: ' + prefixConsonants)
    if prefixConsonants != '':
        word += prefixConsonants + 'ay'
    else:
        word += 'yay'

    # Set the word back to uppercase or title case:
    if wasUpper:
        word = word.upper()
    if wasTitle:
        word = word.title()
##
##
    # Add the non-letters back to the start or end of the word.
    print('pig latin  before append is:', pigLatin)
    print('word is ' + word)
    print('prefixNonLetters before append is: ' + prefixNonLetters)
    print('suffixNonLetters before append is: ' + suffixNonLetters)
    pigLatin.append(prefixNonLetters + word + suffixNonLetters)
    print('pig Latin after append is: ', pigLatin)
##
### Join all the words back together into a single string:
##print(' '.join(pigLatin)) 
