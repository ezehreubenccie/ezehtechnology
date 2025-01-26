#!/bin/bash

# Define variables
rg="myrg"
location="southcentralus"
vnet_name="ERP-servers"
subnet_app="Applications"
subnet_db="Databases"
nsg_name="ERP-SERVERS-NSG"
admin_user="azureuser"
admin_password="T3nb3ll11p1ds!"

# Create Resource Group
az group create --name $rg --location $location

# Create Virtual Network and Application Subnet
az network vnet create \
  --resource-group $rg \
  --name $vnet_name \
  --address-prefixes 10.0.0.0/16 \
  --subnet-name $subnet_app \
  --subnet-prefixes 10.0.0.0/24

# Create Database Subnet
az network vnet subnet create \
  --resource-group $rg \
  --vnet-name $vnet_name \
  --address-prefixes 10.0.1.0/24 \
  --name $subnet_db

# Download cloud-init file for AppServer
wget -N https://raw.githubusercontent.com/MicrosoftDocs/mslearn-secure-and-isolate-with-nsg-and-service-endpoints/master/cloud-init.yml

# Create Application Server VM
az vm create \
  --resource-group $rg \
  --name AppServer \
  --vnet-name $vnet_name \
  --subnet $subnet_app \
  --nsg $nsg_name \
  --image Ubuntu2204 \
  --size Standard_DS1_v2 \
  --generate-ssh-keys \
  --admin-username $admin_user \
  --custom-data cloud-init.yml \
  --no-wait \
  --admin-password $admin_password

# Create Database Server VM
az vm create \
  --resource-group $rg \
  --name DataServer \
  --vnet-name $vnet_name \
  --subnet $subnet_db \
  --nsg $nsg_name \
  --image Ubuntu2204 \
  --size Standard_DS1_v2 \
  --generate-ssh-keys \
  --admin-username $admin_user \
  --custom-data cloud-init.yml \
  --no-wait \
  --admin-password $admin_password

# List VM details
az vm list --resource-group $rg --show-details \
  --query "[*].{Name:name, Provisioned:provisioningState, Power:powerState}" --output table

az vm list --resource-group $rg --show-details \
  --query "[*].{Name:name, PrivateIP:privateIps, PublicIP:publicIps}" --output table

# Get Public IPs of VMs
APPSERVERIP="$(az vm list-ip-addresses --resource-group $rg --name AppServer --query "[].virtualMachine.network.publicIpAddresses[*].ipAddress" --output tsv)"
DATASERVERIP="$(az vm list-ip-addresses --resource-group $rg --name DataServer --query "[].virtualMachine.network.publicIpAddresses[*].ipAddress" --output tsv)"

# SSH into the Application Server
ssh azureuser@$APPSERVERIP -o ConnectTimeout=5

# Allow SSH through NSG
az network nsg rule create \
  --resource-group $rg \
  --nsg-name $nsg_name \
  --name AllowSSHRule \
  --direction Inbound \
  --priority 100 \
  --source-address-prefixes '*' \
  --source-port-ranges '*' \
  --destination-address-prefixes '*' \
  --destination-port-ranges 22 \
  --access Allow \
  --protocol Tcp \
  --description "Allow inbound SSH"

# Add NSG rule for HTTP restriction
az network nsg rule create \
  --resource-group $rg \
  --nsg-name $nsg_name \
  --name httpRule \
  --direction Inbound \
  --priority 150 \
  --source-address-prefixes 10.0.1.4 \
  --source-port-ranges '*' \
  --destination-address-prefixes 10.0.0.4 \
  --destination-port-ranges 80 \
  --access Deny \
  --protocol Tcp \
  --description "Deny from DataServer to AppServer on port 80"

# Application Security Group creation
az network asg create --resource-group $rg --name ERP-DB-SERVERS-ASG

# Update NIC for ASG
az network nic ip-config update \
  --resource-group $rg \
  --application-security-groups ERP-DB-SERVERS-ASG \
  --name ipconfigDataServer \
  --nic-name DataServerVMNic \
  --vnet-name $vnet_name \
  --subnet $subnet_db

# Update NSG rule to use ASG
az network nsg rule update \
  --resource-group $rg \
  --nsg-name $nsg_name \
  --name httpRule \
  --direction Inbound \
  --priority 150 \
  --source-address-prefixes "" \
  --source-port-ranges '*' \
  --source-asgs ERP-DB-SERVERS-ASG \
  --destination-address-prefixes 10.0.0.4 \
  --destination-port-ranges 80 \
  --access Deny \
  --protocol Tcp \
  --description "Deny from DataServer to AppServer on port 80 using application security group"

# SSH validation commands
ssh azureuser@$APPSERVERIP -o ConnectTimeout=5
ssh azureuser@$DATASERVERIP -o ConnectTimeout=5

# Cleanup Resource Group (Optional)
# az group delete --name $rg --no-wait --yes
