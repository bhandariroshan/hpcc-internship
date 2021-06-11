import subprocess

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