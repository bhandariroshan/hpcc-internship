import os
import csv
import subprocess
import datetime


resource_name = "roshanHPCCOnSpot"
vm_name = "spot-testvm6-roshan"
image = "UbuntuLTS"
priority = "Spot"
max_price = "0.001"
eviction_policy = "Deallocate"
size = "Standard_DS1_v2"

status, result = subprocess.getstatusoutput(
	" az vm create \
	--resource-group {} \
	--name  {} \
	--image {} \
	--admin-username azureuser \
	--generate-ssh-keys \
	--priority {}\
	--max-price {} \
	--eviction-policy {} \
	--size {}\
".format(
	resource_name, 
	vm_name, image, 
	priority, 
	max_price, 
	eviction_policy, 
	size
)) 

result = result.split("is lower than the current spot price")
result = result[1].split("for Azure Spot VM")
price = result[0]


with open('data.csv', 'w', newline='') as csvfile:
    fieldnames = ['time', 'resource_name', 'vm_name', 'image', 'priority', 'max_price', 'eviction_policy', 'size', 'price']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({
    	'resource_name': resource_name, 
    	'vm_name': vm_name, 
    	'image': image, 
    	'priority': priority, 
    	'max_price': max_price,
    	'eviction_policy': eviction_policy,
    	'size': size,
    	'time': str(datetime.datetime.today()),
    	'price': float(price.replace('USD', '').replace("'",'').strip())
    })