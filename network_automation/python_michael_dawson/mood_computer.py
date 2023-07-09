#!/usr/bin/env python

# Mood Computer
# Demonstrates the elif clause

import random

print("I sense your energy. Your true emotions are coming",
      "accross my screen.")
print("You are...")

mood = random.randint(1, 3)

if mood == 1:
    # happy
    print(\
        """
        -----------
        |          |
        | o     o  |
        |    <     |
        |          |
        | `      ` |
        |  `....`  |
        ------------
        """)
elif mood == 2:
    # neutral
    print(\
        """
        -----------
        |          |
        | o     o  |
        |    <     |
        |          |
        |  ------  |
        |          |
        ------------
        """)
elif mood == 3:
    # sad
    print(\
        """
        -----------
        |          |
        | o     o  |
        |    <     |
        |          |
        |   . ' .  |
        |  '     ' |
        ------------
        """)
else:
    print("Illegal mood value! (You must be",
          "in a really bad mood).")
print("....today.")

input("\n\nPress the enter key to exit.")