#!/usr/bin/env python3

from displayInventory import displayInventory
inventory = {'gold coin': 42, 'rope': 1}
dragonLoot = ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']
count = {}
def addToInventory(inventory, addeditems):
    for item in addeditems:
        count.setdefault(item, 0)
        count[item] = count[item] + 1
#    print(count)
    for k, v in count.items():
#        print(inventory.get(k, 0))
#        v = inventory.get(k, 0) + count.get(k, 0)
#        print(v)
        if k in inventory.keys():
            inventory[k] = inventory[k] + count.get(k, 0)
        else:
            inventory.setdefault(k, 0)
#        print(inventory)
    return inventory
inv = addToInventory(inventory, dragonLoot)
#print(inv)
displayInventory(inv)
