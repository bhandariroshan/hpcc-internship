import subprocess
from config import region_codes, resource_prefix, spot_region_map


def create_resource_group(regions, prefix):
    for location in regions:
        resource_group_name = prefix + str(location)
        command = 'az group create --name {}  --location {}'.format(resource_group_name, location)
        status, result = subprocess.getstatusoutput(command)
        print(status, result)


def delete_resource_group(regions, prefix):
    for location in regions:
        resource_group_name = prefix + str(location)
        command = 'az group delete --name {} --yes'.format(resource_group_name)
        status, result = subprocess.getstatusoutput(command)
        print(status, result)

if __name__ == '__main__':
    create_resource_group(region_codes, resource_prefix)