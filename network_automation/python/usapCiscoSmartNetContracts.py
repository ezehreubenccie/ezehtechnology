#!/usr/bin/env python

from pprint import pprint

usapContractList = []

with open('insight_contract_inventory.txt') as f:
    insgContracts = f.read()
#print(insgContracts)

# Read text into list
for contract in insgContracts.splitlines():
    usapContractList.append(contract)
#pprint(usapContractList)

# Convert list to set
usapContractSet = set(usapContractList)
pprint(usapContractSet)

# Convert back to list
usapContractList = list(usapContractSet)
#pprint(usapContractList)
print()
numberOfContracts = len(usapContractList)
#print('Usap has {} smartnet contracts, listed in the table below.'. format(numberOfContracts))
#print()
#print('{:^30}'.format('USAP SMARTNET CONTRACT NUMBERS'))
#print('-' * 30)
#for usapContract in usapContractList:
#    print('{:<30}'.format(usapContract))
