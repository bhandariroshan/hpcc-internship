import requests
import datetime
from multiprocessing.pool import ThreadPool
from config import n_threads


multi_result = []
def pull_price(region_name, instance_size, now_time, is_windows_instance=False):
    region_name = region_name
    instance_size = instance_size
    is_windows_instance = is_windows_instance
    end_point = "https://prices.azure.com/api/retail/prices?$filter=skuName eq '" + \
                    str(instance_size) + \
                    " Spot' and meterName eq '" + \
                    str(instance_size) + \
                    " Spot' and armRegionName eq '" + \
                    str(region_name) + \
                    "'"
    data = requests.get(end_point).json()
    for each_instance in data['Items']:
        if not is_windows_instance and 'windows' not in each_instance['productName'].lower():
            return (now_time, region_name, instance_size, min(each_instance['unitPrice'], each_instance['retailPrice']))

        elif is_windows_instance and 'windows' in each_instance['productName'].lower():
            return (now_time, region_name, instance_size, min(each_instance['unitPrice'], each_instance['retailPrice']))

    return (now_time, region_name, instance_size, '')

def callback(data):
    multi_result.append({
        'time': data[0],
        'region': data[1],
        'size': data[2],
        'api_price': data[3],
        'cli_price': ''
    })
     

def pull_multiple(region_names, instance_sizes, now_time, is_windows_instances=False):
    global multi_result
    multi_result = []

    p = ThreadPool(n_threads)
    for each_region in region_names:
        for each_instance in instance_sizes:
            price = p.apply_async(pull_price, args=(each_region, each_instance, now_time, is_windows_instances, ), callback=callback) 
        
    p.close()
    p.join()

    return multi_result