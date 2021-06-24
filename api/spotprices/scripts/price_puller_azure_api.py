import time
import requests
import datetime
from multiprocessing.pool import ThreadPool
from .config import n_threads, spot_region_map


def call_end_point(url):
    return requests.get(url).json()['Items']

multi_result = {}
def pull_price(region_name, sizes, start, end, now_time=str(datetime.datetime.now()), is_windows_instance=False):
    is_windows_instance = is_windows_instance
 
    data = []
    end_point = "https://prices.azure.com/api/retail/prices?$filter="
    params = ''
    for count, instance_size in enumerate(sizes):
        params += "skuName eq '" + str(instance_size).replace('Standard_', '').replace('_', ' ') + " Spot' or "
        if (count+1)%19 == 0:
            spot_end_point = end_point + params[:-3] + "and armRegionName eq '" + str(region_name) + "'" 
            data += call_end_point(spot_end_point)
            params = ''

    if params:
        spot_end_point = end_point + params[:-3] + "and armRegionName eq '" + str(region_name) + "'" 
        data += call_end_point(spot_end_point) 

    params = ''
    for count, instance_size in enumerate(sizes):
        params += "skuName eq '" + str(instance_size).replace('Standard_', '').replace('_', ' ') + "' or "
        if (count+1)%19 == 0:
            regular_end_point = end_point + params[:-3] + "and armRegionName eq '" + str(region_name) + "'" 
            data += call_end_point(regular_end_point)
            params = ''

    if params:
        regular_end_point = end_point + params[:-3] + "and armRegionName eq '" + str(region_name) + "'" 
        data += call_end_point(regular_end_point)
    
    if region_name not in multi_result:
        multi_result [region_name] = {}

    for each_instance in data:
        instance_size = each_instance['armSkuName']

        if instance_size not in multi_result[region_name]:
            multi_result[region_name][instance_size] = [now_time, region_name, instance_size, float('-inf'), float('-inf'), float('-inf'), float('-inf')]

        if not is_windows_instance and 'windows' not in each_instance['productName'].lower() and \
            'spot' in each_instance['meterName'].lower() and each_instance['type'] == 'Consumption':
            multi_result[region_name][instance_size][3] = each_instance['unitPrice']
 
        if not is_windows_instance and 'windows' not in each_instance['productName'].lower() and \
            'spot' not in each_instance['meterName'].lower() and each_instance['type'] == 'Consumption':
            multi_result[region_name][instance_size][4] = each_instance['unitPrice']

        if not is_windows_instance and 'windows' not in each_instance['productName'].lower() and \
            each_instance['type'] == 'Reservation' and each_instance['reservationTerm'] == '1 Year':
            multi_result[region_name][instance_size][5] = each_instance['unitPrice']/(365*24)

        if not is_windows_instance and 'windows' not in each_instance['productName'].lower() and \
            each_instance['type'] == 'Reservation' and each_instance['reservationTerm'] == '3 Years':
            multi_result[region_name][instance_size][6] = each_instance['unitPrice']/(365*24)
 
def process_savings(data): 
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
        return {
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
        }

def pull_multiple(now_time, is_windows_instances=False):
    global multi_result
    multi_result = {}


    p = ThreadPool(n_threads)

    return_data = []
    count = 0
    for region in spot_region_map.keys():
        price = p.apply_async(pull_price, args=(region, spot_region_map[region], now_time, is_windows_instances, ))

    p.close()
    p.join()

    for region  in multi_result.keys():
        for size in multi_result[region].keys(): 
            result = process_savings(multi_result[region][size])
            if result:
                return_data.append(result)

    return return_data