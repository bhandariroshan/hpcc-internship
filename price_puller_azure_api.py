import requests
import datetime
from multiprocessing.pool import ThreadPool
from config import n_threads, region_codes, sizes, spot_region_map 


multi_result = []
def pull_price(region_name, instance_size, now_time=str(datetime.datetime.now()), is_windows_instance=False):
    region_name = region_name
    instance_size = instance_size
    is_windows_instance = is_windows_instance
    spot_end_point = "https://prices.azure.com/api/retail/prices?$filter=skuName eq '" + \
                    str(instance_size) + \
                    " Spot' and meterName eq '" + \
                    str(instance_size) + \
                    " Spot' and armRegionName eq '" + \
                    str(region_name) + \
                    "'"

    regular_end_point = "https://prices.azure.com/api/retail/prices?$filter=skuName eq '" + \
                    str(instance_size) + \
                    "' and meterName eq '" + \
                    str(instance_size) + \
                    "' and armRegionName eq '" + \
                    str(region_name) + \
                    "'"

    regular_data = requests.get(regular_end_point).json()
    spot_data = requests.get(spot_end_point).json() 
    return_data = [now_time, region_name, instance_size, float('-inf'), float('-inf'), float('-inf'), float('-inf')]

    for each_instance in spot_data['Items']:
        if not is_windows_instance and 'windows' not in each_instance['productName'].lower() and \
            'spot' in each_instance['meterName'].lower() and each_instance['type'] == 'Consumption':
            return_data[3] = each_instance['unitPrice']

    for each_instance in regular_data['Items']: 
        if not is_windows_instance and 'windows' not in each_instance['productName'].lower() and \
            'spot' not in each_instance['meterName'].lower() and each_instance['type'] == 'Consumption':
            return_data[4] = each_instance['unitPrice']

        if not is_windows_instance and 'windows' not in each_instance['productName'].lower() and \
            each_instance['type'] == 'Reservation' and each_instance['reservationTerm'] == '1 Year':
            return_data[5] = each_instance['unitPrice']/(365*24)

        if not is_windows_instance and 'windows' not in each_instance['productName'].lower() and \
            each_instance['type'] == 'Reservation' and each_instance['reservationTerm'] == '3 Years':
            return_data[6] = each_instance['unitPrice']/(365*24*3)

    return return_data

def callback(data):
    per_saving_pay_as_you_go = float('-inf')
    if data[4] and data[3]:
        per_saving_pay_as_you_go = (data[4] - data[3])/data[4]*100
    
    per_saving_1y_reserved = float('-inf')
    if data[5] and data[3]:
        per_saving_1y_reserved = (data[5] - data[3])/data[5]*100
    
    per_saving_3y_reserved = float('-inf')
    if data[6] and data[3]:
        per_saving_3y_reserved = (data[6] - data[3])/data[6]*100

    if data[3] > 0 and data[4] > 0:
        multi_result.append({
            'time': data[0],
            'region': data[1],
            'size': data[2],
            'api_price': data[3],
            'cli_price': float('-inf'),
            'pay_as_you_go_price': data[4], 
            '1_year_reserved_price': data[5],
            '3_year_reserved_price': data[6],
            '%_saving_pay_as_you_go': per_saving_pay_as_you_go,
            '%_saving_1y_reserved': per_saving_1y_reserved,
            '%_saving_3y_reserved': per_saving_3y_reserved
        })

def pull_multiple(region_names, instance_sizes, now_time, is_windows_instances=False):
    global multi_result
    multi_result = []
    count = 0
    p = ThreadPool(n_threads)
    for each_region in region_names:
        for each_instance in instance_sizes:
            print(each_region, each_instance)
            if 'Standard_' + each_instance.replace(' ', '_') in spot_region_map[each_region]:
                count += 1
                p.apply_async(pull_price, args=(each_region.strip(), each_instance.strip(), now_time, is_windows_instances, ), callback=callback) 
    
    print("Count = ", count)
    p.close()
    p.join()

    return multi_result

# print(pull_multiple(['ukwest'], ['D16 v3'], str(datetime.datetime.now())))