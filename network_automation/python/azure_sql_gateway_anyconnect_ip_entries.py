#!/usr/bin/env python

from pprint import pprint


new_azure_sql_gw_ip_list = []
azure_sql_gateway_ip_list = []
#insg_inv_list = []
#devicesNotInInsight = []

# Read device names from file
with open('New Azure SQL Gateway_2.txt') as f:
    new_azuregw_output = f.read()
new_azuregw_output = new_azuregw_output.rstrip('')
#print(new_azuregw_output)

# Read device serial# from file
with open('Azure_SQL_Gatway_Object_2.txt') as f:
    azuregw_output = f.read()
#print(azuregw_output)
#
## Read serial numbers from insight smartnet sheet
#with open('insight_global_inventory.txt') as f:
#    insg_output = f.read()
##print(insg_output)
#
#
## Build device name list from solarwinds
#for deviceName in swdeviceName_output.splitlines():
#    swdeviceName_list.append(deviceName)
##pprint(swdeviceName_list)
#
## Print number of devices
##print('Solarwinds devices number: {}'.format(len(swdeviceName_list)))
#
# Build serial number list from solarwinds
for ip in azuregw_output.splitlines():
    azure_sql_gateway_ip_list.append(ip)
#pprint(azure_sql_gateway_ip_list)
#
## Print number of serial#s from solarwinds
##print('Solarwinds inventory number: {}'.format(len(sw_inv_list)))
#
# Build serial number list from insight sheet
for serial in new_azuregw_output.splitlines():
    new_azure_sql_gw_ip_list.append(serial)
del(new_azure_sql_gw_ip_list[-1])
#pprint(new_azure_sql_gw_ip_list)
#
## Print number of serial#s from insight sheet
##print('Insight global inventory number: {}'.format(len(insg_inv_list)))
#
#
#
## Build dictionary/database from solarwinds list with deviceName as key
#sw_inv_dict = dict(zip(sw_inv_list, swdeviceName_list))
##print('****Solarwinds serial# and device name database****')
##pprint(sw_inv_dict)
#
# Convert azure_sql_gateway and new_azure_sql_gateway IP lists to sets
azure_sql_gateway_ip_set = set(azure_sql_gateway_ip_list)
new_azure_sql_gw_ip_set = set(new_azure_sql_gw_ip_list)
#
#
## Compare serial#s from insight and solarwinds and extract unique serial#s
print('****new azure sql  global unique IPs****')
new_azure_sql_gw_ip_unique_set = new_azure_sql_gw_ip_set.difference(azure_sql_gateway_ip_set)
pprint(new_azure_sql_gw_ip_unique_set)
#print(type(insgUnique_set))
#
print('****azure sql unique IPs****')
azure_sql_gateway_ip_unique_set = azure_sql_gateway_ip_set.difference(new_azure_sql_gw_ip_set)
pprint(azure_sql_gateway_ip_unique_set)
##print(type(swUnique_set))
#
## Convert unique serial sets to lists
#insgUnique_list = list(insgUnique_set)
#swUnique_list = list(swUnique_set)
##print('****Insight global unique serial# list****')
##pprint(insgUnique_list)
##print(type(insgUnique_list))
##print()
##print('****Solarwinds unique serial# list****')
##pprint(swUnique_list)
##print(type(swUnique_list))
#
##found = False
## Reconcile unique serial#s with solarwinds database
#for serial in swUnique_list:
#    for key in sw_inv_dict.keys():
#        if serial == key:
#            device = sw_inv_dict[serial]
#            devicesNotInInsight.append(device)
#
#print('****These devices are in solarwinds but not in insight sheet.****')
#pprint(devicesNotInInsight)
#print()
#print('****These devices are in insight sheet but not in solarwinds.****')
#pprint(insgUnique_list)
