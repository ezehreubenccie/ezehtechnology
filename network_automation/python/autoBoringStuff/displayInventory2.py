#!/usr/bin/env python3


def displayInventory(inventory):
    total = 0
    print('Inventory:')
    for k, v in inventory.items():
        print(f'{v} {k}')
        total = total + v
    print()
    print('Total number of items: ' + str(total))


if __name__ == '__main__':
    dict1 = {'rope': 1, 'torch': 6, 'gold coin': 42, 'dagger': 1, 'arrow': 12}
    displayInventory(dict1)
