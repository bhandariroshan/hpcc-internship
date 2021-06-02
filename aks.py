import os
import csv
import time
import datetime
import subprocess

from azure.mgmt.resource import ResourceManagementClient
from azure.identity import AzureCliCredential

from multiprocessing.pool import ThreadPool
from config import *


def create_aks_create_cluster():
    resource_group_name = 'roshanHPCCOnSpot'
    cluster_name = 'roshanakscluster'
    command = "az aks create --resource-group {} --name {} --node-count 1".format(resource_group_name, cluster_name)
    status, result = subprocess.getstatusoutput(command)
    print(status, result)


def create_benchmark_azure_spot_aks():
    cluster_name = 'roshanakscluster'
    node_pool_name = 'nodepool2'
    spot_max_price = '0.0001'
    priority = 'Spot'
    command = "az aks nodepool add \
        --resource-group {} \
        --name {} \
        --cluster-name {} \
        --priority {} \
        --eviction-policy Delete \
        --spot-max-price {} \
        --enable-cluster-autoscaler \
        --min-count 1 \
        --max-count 3 \
        --node-vm-size Standard_DS1_v2 \
    ".format(
        resource_names[0],
        cluster_name,
        node_pool_name,
        priority,
        spot_max_price
    )
    print(command)
    status, result = subprocess.getstatusoutput(command) 
    print('*******************************')
    print(status, result)