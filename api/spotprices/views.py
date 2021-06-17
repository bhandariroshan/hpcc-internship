import json
import math
import requests
import datetime
from django.shortcuts import render
from django.contrib.auth import authenticate

# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rest_framework.permissions import IsAuthenticated 
from rest_framework.views import APIView 
from django.http import JsonResponse

import pandas as pd
from spotprices.models import SpotPrices, EvictionNotices
from django_pandas.io import read_frame
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated


def find_cheapest_region_at_current_time_using_api(size, rank):
    size = size.replace('Standard_','').replace('_', ' ')
    items = []

    url = "https://prices.azure.com/api/retail/prices?$filter=skuName eq '{} Spot' and meterName eq '{} Spot'".format(
        size, size
    )

    while url:
        data = requests.get(url).json()
        cheapest_price = float('inf')
        cheapest_region = None

        for each_data in data['Items']:
            if each_data['unitPrice'] < cheapest_price:
                cheapest_price = each_data['unitPrice']
                cheapest_region = each_data['armRegionName']

                items.append({'cheapest_region': cheapest_region, 'cheapest_price': cheapest_price})
                items = sorted(items, key=lambda i: i['cheapest_price'])
                items = items[0:10]

        url = data ['NextPageLink']

    return_data = []
    for each_item in items:
        regular_end_point = "https://prices.azure.com/api/retail/prices?$filter=skuName eq '" + \
                        str(size) + \
                        "' and meterName eq '" + \
                        str(size) + \
                        "' and armRegionName eq '" + \
                        str(each_item['cheapest_region']) + \
                        "'"

        pay_as_you_go_mean = ''
        one_year_reserved_mean = ''
        three_year_reserved_mean = ''

        mean_per_saving_paygo = ''
        mean_per_saving_three = ''
        mean_per_saving_one = ''

        regular_data = requests.get(regular_end_point).json()
        for each_data in regular_data['Items']:
            if each_data['type'] == "Consumption" and 'windows' not in each_data['productName'].lower():
                 pay_as_you_go_mean = each_data['unitPrice']
                 mean_per_saving_paygo = (pay_as_you_go_mean - cheapest_price)/pay_as_you_go_mean * 100

            if each_data['type'] == "Reservation" and 'windows' not in each_data['productName'].lower() \
                and each_data['reservationTerm'] == '1 Year':
                 one_year_reserved_mean = each_data['unitPrice'] / (365*24)
                 mean_per_saving_one = (one_year_reserved_mean - cheapest_price)/one_year_reserved_mean * 100

            if each_data['type'] == "Reservation" and 'windows' not in each_data['productName'].lower() \
                and each_data['reservationTerm'] == '3 Years':
                 three_year_reserved_mean = each_data['unitPrice'] / (3*365*24)
                 mean_per_saving_three = (three_year_reserved_mean - cheapest_price)/three_year_reserved_mean * 100

        return_data.append({
            'region': each_item['cheapest_region'],
            'size': size,
            'spot_mean_api':each_item['cheapest_price'],
            # 'spot_mean_cli':'', 
            'pay_as_you_go_mean':pay_as_you_go_mean,
            'one_year_reserved_mean':one_year_reserved_mean,
            'three_year_reserved_mean':three_year_reserved_mean,
            'saving_percentage_pay_as_you_go': mean_per_saving_paygo,
            'saving_percentage_one_year_reserved': mean_per_saving_one,
            'saving_percentage_three_year_reserved': mean_per_saving_three,
            'duration': ''
        })

    if rank:
        rank = int(rank)
        return return_data [rank-1:rank]
    else:
        return return_data


def find_average_price_of_region_and_size(region, size, days=1):
    size = size.replace('Standard_', '').replace('_', ' ')
     
    qs = SpotPrices.objects.filter(region=region, size=size) 

    data_size_subset = read_frame(qs) 
    try:
        data_size_subset['time'] = pd.to_datetime(data_size_subset['time']) 
        now_time = datetime.datetime.now(data_size_subset.time[0].tzinfo)
        yesterday_time = now_time - datetime.timedelta(days=int(days))
    except Exception as e:
        print (str(e))
        return [{
            'region': region,
            'size': size,
            'spot_mean_api':'',
            # 'spot_mean_cli':'', 
            'pay_as_you_go_mean': '',
            'one_year_reserved_mean': '',
            'three_year_reserved_mean': '',        
            'saving_percentage_pay_as_you_go': '',
            'saving_percentage_three_year_reserved': '',
            'saving_percentage_one_year_reserved': '',
            'duration': str(days) + ' days'
        }]

    
    data_size_subset = data_size_subset[data_size_subset['size']==size]
    data_size_subset = data_size_subset[data_size_subset['region']==region]
    

    data_size_subset =  data_size_subset[data_size_subset['time'] <= now_time]
    data_size_subset = data_size_subset[data_size_subset['time'] >= yesterday_time]

    mean_api_price = data_size_subset[data_size_subset['api_price'] != float('-inf')]['api_price'].mean()
    mean_cli_price = data_size_subset[data_size_subset['cli_price'] != float('-inf')]['cli_price'].mean()

    mean_price_paygo = data_size_subset[data_size_subset['pay_as_you_go_price'] != float('-inf')]['pay_as_you_go_price'].mean()
    mean_price_one = data_size_subset[data_size_subset['one_year_reserved_price'] != float('-inf')]['one_year_reserved_price'].mean()
    mean_price_three = data_size_subset[data_size_subset['three_year_reserved_price'] != float('-inf')]['three_year_reserved_price'].mean()

    mean_per_saving_paygo = data_size_subset[data_size_subset['per_saving_paygo'] != float('-inf')]['per_saving_paygo'].mean()
    mean_per_saving_one = data_size_subset[data_size_subset['per_saving_one'] != float('-inf')]['per_saving_one'].mean()
    mean_per_saving_three = data_size_subset[data_size_subset['per_saving_three'] != float('-inf')]['per_saving_three'].mean()

    return [{
        'region': region,
        'spot_mean_api': mean_api_price,
        # 'spot_mean_cli': mean_cli_price,
        'pay_as_you_go_mean': mean_price_paygo,
        'one_year_reserved_mean': mean_price_one,
        'three_year_reserved_mean': mean_price_three,
        'saving_percentage_pay_as_you_go': mean_per_saving_paygo,
        'saving_percentage_three_year_reserved': mean_per_saving_three,
        'saving_percentage_one_year_reserved': mean_per_saving_one,
        'duration': str(days) + ' days',
    }]


def find_cheapest_region_at_sometime(size, days):
    size = size.replace('Standard_', '').replace('_', ' ') 
    qs = SpotPrices.objects.filter(size=size) 

    data_size_subset = read_frame(qs) 
    try:
        data_size_subset['time'] = pd.to_datetime(data_size_subset['time']) 
        now_time = datetime.datetime.now(data_size_subset.time[0].tzinfo)
        yesterday_time = now_time - datetime.timedelta(days=int(days))
    except:
        return [{
            'region': '',
            'size': size,
            'spot_mean_api':'',
            # 'spot_mean_cli':'', 
            'pay_as_you_go_mean': '',
            'one_year_reserved_mean': '',
            'three_year_reserved_mean': '',        
            'saving_percentage_pay_as_you_go': '',
            'saving_percentage_three_year_reserved': '',
            'saving_percentage_one_year_reserved': '',
            'duration': str(days) + ' days'
        }] 

    data_size_subset =  data_size_subset[data_size_subset['time'] <= now_time]
    data_size_subset = data_size_subset[data_size_subset['time'] >= yesterday_time]

    grouped_df = data_size_subset.groupby("region")
    mean_df = grouped_df.mean()
    mean_df = mean_df.reset_index() 

    mean_api_price = mean_df.iloc[mean_df['api_price'].idxmin()]['api_price']
    mean_cli_price = mean_df.iloc[mean_df['api_price'].idxmin()]['cli_price']
    region = mean_df.iloc[mean_df['api_price'].idxmin()]['region']
    

    mean_price_paygo = mean_df.iloc[mean_df['api_price'].idxmin()]['pay_as_you_go_price'] 
    mean_price_one = mean_df.iloc[mean_df['api_price'].idxmin()]['one_year_reserved_price']
    mean_price_three = mean_df.iloc[mean_df['api_price'].idxmin()]['three_year_reserved_price']

    mean_per_saving_paygo = mean_df.iloc[mean_df['api_price'].idxmin()]['per_saving_paygo'] 
    mean_per_saving_one = mean_df.iloc[mean_df['api_price'].idxmin()]['per_saving_one']  
    mean_per_saving_three = mean_df.iloc[mean_df['api_price'].idxmin()]['per_saving_three']

    return [{
        'region': region,
        'spot_mean_api': mean_api_price,
        # 'spot_mean_cli': mean_cli_price,
        'pay_as_you_go_mean': mean_price_paygo,
        'one_year_reserved_mean': mean_price_one,
        'three_year_reserved_mean': mean_price_three,
        'saving_percentage_pay_as_you_go': mean_per_saving_paygo,
        'saving_percentage_three_year_reserved': mean_per_saving_three,
        'saving_percentage_one_year_reserved': mean_per_saving_one,
        'duration': str(days) + ' days',
    }] 


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Create your views here.
class PriceView(APIView):
    permission_classes = [] # + [IsAuthenticated]

    def get(self, request):
        operation = request.GET.get('operation', None)
        region = request.GET.get('region', None)
        size = request.GET.get('size', None)
        days = request.GET.get('days', None)
        rank = request.GET.get('rank', None)

        data = {}
        if operation.lower() == 'cheapest' and size and not days:
            data = find_cheapest_region_at_current_time_using_api(size, rank)
        
        elif operation.lower() == 'cheapest' and size and days:
            data = find_cheapest_region_at_sometime(size, days)

        elif operation.lower() == 'average' and region and size and not days:
            data = find_average_price_of_region_and_size(region, size)
        
        elif operation.lower() == 'average' and region and size and days:
            data = find_average_price_of_region_and_size(region, size, days)
        
        return JsonResponse({'items':data})

# Create your views here.
class EvictionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        evc = EvictionNotices()

        machine_started = request.POST.get('started', False)
        if machine_started:
            start_time = str(datetime.datetime.now())
            evc.start_time = start_time

        ip_address = get_client_ip(request)
        evc.ip_address = ip_address

        vm_name = request.POST.get('vm_name', None)
        evc.vm_name = vm_name

        vm_size = request.POST.get('vm_size', None)
        evc.vm_size = vm_size

        vm_region = request.POST.get('vm_region', None)
        evc.vm_region = vm_region

        cluster_name = request.POST.get('cluster_name', None)
        evc.cluster_name = cluster_name

        cluster_region = request.POST.get('cluster_region', None)
        evc.cluster_region = cluster_region

        machine_evicted = request.POST.get('evicted', False)
        if machine_evicted:
            eviction_time = str(datetime.datetime.now())
            eviction_notice = request.POST.get('eviction_notice', {})

            evc.eviction_time = eviction_time
            evc.eviction_notice = eviction_notice

        evc.save()
        print('Success')
        return JsonResponse({'message':'success'})