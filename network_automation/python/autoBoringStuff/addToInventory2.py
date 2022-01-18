#!/usr/bin/env python3

from displayInventory2 import displayInventory

def addToInventory(inventory, addedItems):
    count = {}
    for item in addedItems:
        count.setdefault(item, 0)
        count[item] = count[item] + 1
    for k, v in count.items():
        inventory.setdefault(k, 0)
        inventory[k] = inventory[k] + v
    return inventory

if __name__ == '__main__':
    inv = {'gold coin': 42, 'rope': 1}
    dragonLoot = ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']
    inv = addToInventory(inv, dragonLoot)
    displayInventory(inv)
