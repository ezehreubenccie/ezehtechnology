#! python3

# mclip.py - A multi-clipboard program.


TEXT = {'agree': """Yes. I agree. That sounds fine to me.""",
        'busy': """Sorry, can we do this later this week or next week?""",
        'upsell': """Would you consider making this a monthly donaton?"""}

import sys
if len(sys.argv) < 2:
    print('Usage: python mclip.py [keyphrase] - copy phrase text')
    sys.exit()

keyPhrase = sys.argv[1] #first command line arg is the keyphrase

import pyperclip
if keyPhrase in TEXT:
    pyperclip.copy(TEXT[keyPhrase])
    print('Text for ' + keyPhrase + ' copied to clipboard.')
else:
    print('There is no text for ' + keyphrase)
