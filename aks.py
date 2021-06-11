import os
import csv
import time
import datetime
import subprocess
from subprocess import Popen
from multiprocessing.pool import ThreadPool
from price_puller_azure_api import pull_price
from config import *


def create_aks_create_cluster(resource_group_name, cluster_name, size, price):
    command = "az aks create \
            --resource-group {} \
            --name {} \
            --node-count 1 \
            --tags price={} \
            --node-vm-size {}".format(resource_group_name, cluster_name, price, size)
    status, result = subprocess.getstatusoutput(command)
    print(status, result)

def add_node_pool(resource_group_name, cluster_name, node_pool_name, spot_max_price, priority, size):
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
        --labels price={} \
        --tags price={} \
        --node-vm-size {} \
    ".format(
        resource_group_name,
        node_pool_name,
        cluster_name,
        priority,
        spot_max_price,
        spot_max_price,
        spot_max_price,
        size
    )

    status, result = subprocess.getstatusoutput(command)  
    print(status, result)

def install_hpcc(resource_group_name, cluster_name, pod_name):
    kube_ctl_install_command = 'az aks get-credentials --resource-group {} --name {} --admin'.format(
        resource_group_name,
        cluster_name
    )

    status, result = subprocess.getstatusoutput(kube_ctl_install_command)  
    print(status, result)

    helm_install_command = 'helm repo update && helm repo add hpcc https://hpcc-systems.github.io/helm-chart/'
    status, result = subprocess.getstatusoutput(helm_install_command)  
    print(status, result)

    hpcc_install_command = "helm install {} hpcc/hpcc \
        --set global.image.version=latest \
        --set storage.dllStorage.storageClass=azurefile \
        --set storage.daliStorage.storageClass=azurefile \
        --set storage.dataStorage.storageClass=azurefile \
    ".format(pod_name)

    status, result = subprocess.getstatusoutput(hpcc_install_command)
    print(status, result)


def stop_hpcc():
    hpcc_uninstall_command = 'helm uninstall mycluster'
    status, result = subprocess.getstatusoutput(hpcc_uninstall_command)

def run():
    region_code = 'eastus'
    size = 'Standard_D2s_v3'
    node_pool_count = 2
    data =  pull_price(region_code, size.replace('Standard_', '').replace('_',' '))
    spot_max_price = data[3]
    resource_group_name = resource_prefix + region_code
    cluster_name = 'test-roshan-hpcc-3'
    pod_name = 'hpccpod'
    
    print("Spot max price is: ", spot_max_price)
    create_aks_create_cluster(
        resource_group_name=resource_prefix + region_code, 
        cluster_name=cluster_name, 
        size=size,
        price=spot_max_price
    )

    print("Adding resource group to the cluster...")
    install_hpcc(resource_group_name, cluster_name, pod_name)
    for i in range(node_pool_count):
        add_node_pool(
            resource_group_name=resource_prefix + region_code, 
            cluster_name=cluster_name, 
            node_pool_name="nodepool" + str(i+2), 
            spot_max_price=round(spot_max_price, 5),
            priority="Spot",
            size=size
        )

if __name__ == '__main__':
    run()