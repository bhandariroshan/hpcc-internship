import os
import csv
import time
import datetime
import subprocess

from azure.mgmt.resource import ResourceManagementClient
from azure.identity import AzureCliCredential

from multiprocessing.pool import ThreadPool
from config import *


def create_aks_create_cluster(resource_group_name, cluster_name, size):
    command = "az aks create \
            --resource-group {} \
            --name {} \
            --node-count 1 \
            --node-vm-size {}".format(resource_group_name, cluster_name, size)
    status, result = subprocess.getstatusoutput(command)
    print(status, result)


def add_node_pool(cluster_name, node_pool_name, spot_max_price, priority, size):
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
        --node-vm-size {} \
    ".format(
        resource_names[0],
        cluster_name,
        node_pool_name,
        priority,
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

    helm_install_command = 'helm repo add hpcc https://hpcc-systems.github.io/helm-chart/'
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
    resource_group_name = resource_prefix + region_codes[0]
    cluster_name = 'test-roshan-123'
    pod_name = 'hpccpod'
    
    create_aks_create_cluster(
        resource_group_name=resource_prefix + region_codes[0], 
        cluster_name=cluster_name, 
        size=sizes[0]
    )

    install_hpcc(resource_group_name, cluster_name, pod_name)

if __name__ == '__main__':
    run()