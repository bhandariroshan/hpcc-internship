import subprocess
from config import region_codes, resource_prefix


def create_resource_group(region_codes, prefix):
    for location in region_codes:
        resource_group_name = prefix + str(location)
        command = 'az group create --name {}  --location {}'.format(resource_group_name, location)
        status, result = subprocess.getstatusoutput(command)
        print(status, result)

if __name__ == '__main__':
    create_resource_group(region_codes, resource_prefix)