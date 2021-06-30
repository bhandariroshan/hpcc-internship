import time
import requests
import datetime
import subprocess 
from config import *
from price_puller_azure_api import pull_price
import pytz
from aks import *


def invoke_spot_eviction_notice_streaming(resource_group, cluster_name):
    azure_run_command = 'az aks get-credentials --resource-group {} --name {} && '
    azure_run_command += 'git clone https://github.com/bhanduroshan/hpcc-internship.git && '
    azure_run_command += 'cd hpcc-internship && '
    azure_run_command += 'cd aks_node_installer && '
    azure_run_command += 'kubectl apply -f ./k8s '
    azure_run_command = azure_run_command.format(
        resource_group,
        cluster_name
    )

    print(azure_run_command)

    status, result = subprocess.getstatusoutput(azure_run_command)
    print(status, result)


def update_vm_created_status(resource_group_name, region_code, cluster_name, spot_max_price, size):
    user, passwd = 'admin', '@dmin123#'
    url = 'http://40.76.43.103/eviction/'

    est = pytz.timezone('US/Eastern')
    requests.post(
        url,
        data={
            'cluster_name': cluster_name,
            'vm_size': size, 
            'vm_region': region_code,
            'start_time': str(datetime.datetime.now(datetime.timezone.utc)),
            'price':spot_max_price
        },
        auth=(user, passwd),
        verify=False
    ) 
    

def invoke_spot_aks_eviction_notice_streaming(resource_group, cluster_name):
    command = '''
        az aks command invoke -g {} -n {} -c "cd /home && mkdir roshan && cd roshan"    
    '''.format(resource_group, cluster_name)
    status, result = subprocess.getstatusoutput(command)


def run_eviction_streamer_cluster():
    # Define resources
    region_code = 'eastus'
    sizes = ['Standard_D2s_v3', 'Standard_D4s_v3']

    node_pool_count = 4
    data =  pull_price(region_code, sizes[0].replace('Standard_', '').replace('_',' '))
    spot_max_price = data[3]
    resource_group_name = resource_prefix + region_code
    cluster_name = 'test-roshan-hpcc-10'
    pod_name = 'hpccpod'
    
    # Create AKS Cluster
    print("Spot max price is: ", spot_max_price)
    create_aks_create_cluster(
        resource_group_name=resource_prefix + region_code, 
        cluster_name=cluster_name, 
        size=sizes[0],
        price=spot_max_price
    )

    # Install HPCC on Cluster
    print("Adding resource group to the cluster...")
    install_hpcc(resource_group_name, cluster_name, pod_name)
    for i in range(node_pool_count):
        size = sizes[0] if i%2 == 0 else sizes[1]
        data =  pull_price(region_code, size.replace('Standard_', '').replace('_',' '))
        spot_max_price = data[3]

        add_node_pool(
            resource_group_name=resource_prefix + region_code, 
            cluster_name=cluster_name, 
            node_pool_name="nodepool" + str(i+2), 
            spot_max_price=round(spot_max_price, 5),
            priority="Spot",
            size=size[0] if i%2 == 0 else sizes[1]
        )

    # Trigger Eviction Streamer
    invoke_spot_eviction_notice_streaming(resource_group, cluster_name)

    # update_vm_created_status
    update_vm_created_status(
        resource_group_name, 
        region_code, 
        cluster_name, 
        spot_max_price, 
        size[1]
    )



if __name__ == '__main__':
    run_eviction_streamer_cluster()