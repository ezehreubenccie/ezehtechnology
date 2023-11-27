#!/bin/bash

az vm create \
  --resource-group ExpensiveResourceGroup \
  --location southcentralus \
  --name az-104-20-a \
  --image Win2019Datacenter \
  --admin-username testuser \
  --admin-password "TestPa5sw0rd!" \
  --verbose \
  --no-wait
