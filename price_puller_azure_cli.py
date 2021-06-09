import os
import csv
import time
import datetime
import subprocess 

from multiprocessing.pool import ThreadPool
from config import *


multi_result = []
def pull_price(resource_name, size, now_time):
    vm_name = resource_prefix + 'vm-' + '11'
    command = " az vm create \
        --resource-group {} \
        --name  {} \
        --image {} \
        --admin-username azureuser \
        --generate-ssh-keys \
        --priority {}\
        --max-price {} \
        --eviction-policy {} \
        --size {}\
        --subscription {} \
    ".format(
        resource_name, 
        vm_name,
        image, 
        priority, 
        max_price, 
        eviction_policy, 
        size,
        subscription
    )
    # print(command)
    status, res = subprocess.getstatusoutput(command) 

    result = res.split("is lower than the current spot price")
    try:
        result = result[1].split("for Azure Spot VM")
        price = result[0]
        return  (now_time, resource_name, size, float(price.replace('USD', '').replace("'",'').strip()))
    except Exception as e:
        # print("Exception occurred with {}, {}".format(size, resource_name))
        # print('************************')
        return  (now_time, resource_name, size, '')

def callback(data):
    multi_result.append({
        'time': data[0],
        'region': data[1],
        'size': data[2],
        'api_price': float('-inf'),
        'cli_price': data[3] if data[3] else float('-inf'),
        'pay_as_you_go_price': float('-inf'),
        '1_year_reserved_price': float('-inf'),
        '3_year_reserved_price': float('-inf'),
        '%_saving_pay_as_you_go': float('-inf'),
        '%_saving_1y_reserved': float('-inf'),
        '%_saving_3y_reserved': float('-inf')
    })

def pull_multiple(resource_names, instance_sizes, now_time, is_windows_instances=False):
    global multi_result
    multi_result = [] 
    p = ThreadPool(n_threads)
    for resource_name in resource_names: 
        for size in instance_sizes:
            p.apply_async(pull_price, args=(resource_name, size, now_time,), callback=callback)
    
    p.close()
    p.join()
    return multi_result

# print(pull_multiple(['ukwest'], sizes[:1], str(datetime.datetime.now())))