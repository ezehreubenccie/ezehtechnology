#!/usr/bin/env python

#inventory = {'rope': 1, 'torch': 6, 'gold coin': 42, 'dagger': 1, 'arrow': 12}

def displayInventory(inventory):
    total = 0
    print('{}'.format('Inventory:'))
    for k, v in inventory.items():
        print('{} {}'. format(v, k))
        total = total + v
    print('Total number of items: {}'.format(total))

if __name__== "__main__":
    inventory = {'rope': 1, 'torch': 6, 'gold coin': 42, 'dagger': 1, 'arrow': 12}
    displayInventory(inventory)


