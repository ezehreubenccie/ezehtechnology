#!/usr/bin/env python3

from displayInventory2 import displayInventory

inv = {'gold coin': 42, 'rope': 1}
dragonLoot = ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']
count = {}
for item in dragonLoot:
    count.setdefault(item, 0)
    count[item] = count[item] + 1
print(count)
for k,v in count.items():
    inv.setdefault(k, 0)
    inv[k] = inv[k] + v
print(inv)
