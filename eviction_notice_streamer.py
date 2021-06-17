import requests
import subprocess


def invoke_spot_eviction_notice_streaming(resource_group, vm_name):
	command = '''
		Sudo apt-get install git && git clone https://github.com/bhanduroshan/hpcc-internship.git && cd hpcc-internship && 
		python handle_eviction.py
	'''


	azure_run_command = "az vm run-command invoke -g {} -n {} --command-id RunShellScript --scripts '{}' ".format(
		resource_group,
		vm_name,
		command
	)

	status, result = subprocess.getstatusoutput(command)
	print(status, result)

def invoke_spot_aks_eviction_notice_streaming(resource_group, cluster_name):
	command = '''
		az aks command invoke -g {} -n {} -c "cd /home && mkdir roshan && cd roshan"	
	'''.format(resource_group, cluster_name)
	status, result = subprocess.getstatusoutput(command)

def invoke_spot_aks_eviction_notice_streaming(resource_group, cluster_name, node_pool_name):
	url = "https://management.azure.com/subscriptions/ec0ba952-4ae9-4f69-b61c-4b96ff470038/resourcegroups/{}/\
		providers/Microsoft.ContainerService/managedClusters/{}/agentPools/{}/simulateEviction?api-version=2021-03-01".format(
			resource_group, cluster_name, node_pool_name
	)

	token  ""
	header = {
		'Authorization': "Bearer " + token
	}
	requests.post(url, header=header)