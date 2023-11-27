#!/bin/bash

VMS="az-104-01 az-104-02 az-104-03"

for VM in $VMS
do
 az vm create \
   --resource-group ExpensiveResourceGroup \
   --location southcentralus \
   --name "$VM" \
   --image Win2019Datacenter \
   --admin-username testuser \
   --admin-password "TestPa5sw0rd!" \
   --verbose 
done
