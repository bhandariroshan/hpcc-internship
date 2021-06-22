import time
import requests
import datetime
import subprocess 
from config import *
from price_puller_azure_api import pull_price
import pytz


# def invoke_spot_aks_eviction_notice_streaming(resource_group, cluster_name, node_pool_name):
#   url = "https://management.azure.com/subscriptions/ec0ba952-4ae9-4f69-b61c-4b96ff470038/resourcegroups/{}/\
#       providers/Microsoft.ContainerService/managedClusters/{}/agentPools/{}/simulateEviction?api-version=2021-03-01".format(
#           resource_group, cluster_name, node_pool_name
#   )

#   token  ""
#   header = {
#       'Authorization': "Bearer " + token
#   }
#   requests.post(url, header=header)


def create_vm(resource_group_name, vm_name, image, priority, max_price, eviction_policy, size, subscription):
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
        --ssh-key-values ./roshan-api_key.pem \
    ".format(
        resource_group_name, 
        vm_name,
        image, 
        priority, 
        max_price, 
        eviction_policy, 
        size,
        subscription
    )
    print(command)
    status, res = subprocess.getstatusoutput(command) 
    print(status, res)


def invoke_spot_eviction_notice_streaming(resource_group, vm_name):
    azure_run_command = 'az vm run-command invoke --resource-group {} --name {} --command-id RunShellScript --scripts '
    azure_run_command += '"sudo apt-get update && sudo apt-get -y install git && sudo apt-get -y install python3-pip && '
    azure_run_command += 'sudo python3 -m pip install requests && sudo python3 -m pip install pytz && sudo git clone https://github.com/bhanduroshan/hpcc-internship.git && '
    azure_run_command += 'cd hpcc-internship && sudo nohup python3 handle_eviction.py &"'
    azure_run_command = azure_run_command.format(
        resource_group,
        vm_name
    )

    print(azure_run_command)

    status, result = subprocess.getstatusoutput(azure_run_command)
    print(status, result)


def update_vm_created_status(resource_group_name, region_code, vm_name, spot_max_price, size):
    user, passwd = 'admin', '@dmin123#'
    url = 'http://40.76.43.103/eviction/'

    est = pytz.timezone('US/Eastern')
    requests.post(
        url,
        data={
            'vm_name': vm_name,
            'vm_size': size, 
            'vm_region': region_code,
            'start_time': str(datetime.datetime.now(datetime.timezone.utc)),
        },
        auth=(user, passwd),
        verify=False
    ) 
    

def invoke_spot_aks_eviction_notice_streaming(resource_group, cluster_name):
    command = '''
        az aks command invoke -g {} -n {} -c "cd /home && mkdir roshan && cd roshan"    
    '''.format(resource_group, cluster_name)
    status, result = subprocess.getstatusoutput(command)


def run_eviction_streamer_spot():
    # Define resources
    region_code = 'eastus'
    size = 'Standard_D2s_v3' 

    data =  pull_price(region_code, size.replace('Standard_', '').replace('_',' '))
    spot_max_price = data[3]
    resource_group_name = resource_prefix + region_code
    vm_name = resource_prefix + 'vm-' + '22'
    print("Spot max price is: ", spot_max_price)

    # create a VM
    create_vm(resource_group_name, vm_name, image, 'Spot', spot_max_price, 'Delete', size, subscription)

    # Update the VM creation state in the API
    update_vm_created_status(resource_group_name, region_code, vm_name, spot_max_price, size)

    # Get inside a VM and pull the script for monitoring and run it
    invoke_spot_eviction_notice_streaming(resource_group_name, vm_name)
    print("Success.")


if __name__ == '__main__':
    run_eviction_streamer_spot()