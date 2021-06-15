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
from spotprices.models import SpotPrices
from django_pandas.io import read_frame


def find_cheapest_region_at_current_time_using_api(size):
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

        url = data ['NextPageLink']

    return {
        'region': cheapest_region, 
        'price': cheapest_price, 
        'average_price':cheapest_price, 
        'average_duration': '1 days'
    }


def find_average_price_of_region_and_size(region, size, days=1):
    size = size.replace('Standard_', '').replace('_', ' ')
     
    qs = SpotPrices.objects.filter(region=region, size=size) 

    data_size_subset = read_frame(qs) 
    try:
        data_size_subset['time'] = pd.to_datetime(data_size_subset['time']) 
        now_time = datetime.datetime.now(data_size_subset.time[0].tzinfo)
        yesterday_time = now_time - datetime.timedelta(days=int(days))
    except:
        return {'region': '', 'price':'', 'duration': str(days) + ' days', 'size': size}

    
    data_size_subset = data_size_subset[data_size_subset['size']==size]
    data_size_subset = data_size_subset[data_size_subset['region']==region]
    

    data_size_subset =  data_size_subset[data_size_subset['time'] <= now_time]
    data_size_subset = data_size_subset[data_size_subset['time'] >= yesterday_time]

    mean_api_price = data_size_subset[data_size_subset['api_price'] != float('-inf')]['api_price'].mean()
    mean_cli_price = data_size_subset[data_size_subset['cli_price'] != float('-inf')]['cli_price'].mean()

    return {
        'region': region,
        'mean_api_price': mean_api_price,
        'mean_cli_price': mean_cli_price,
        'mean_duration': str(days) + ' days'
    }


def find_cheapest_region_at_sometime(size, days):
    size = size.replace('Standard_', '').replace('_', ' ') 
    qs = SpotPrices.objects.filter(size=size) 

    data_size_subset = read_frame(qs) 
    try:
        data_size_subset['time'] = pd.to_datetime(data_size_subset['time']) 
        now_time = datetime.datetime.now(data_size_subset.time[0].tzinfo)
        yesterday_time = now_time - datetime.timedelta(days=int(days))
    except:
        return {'region': '', 'price':'', 'duration': str(days) + ' days', 'size': size}

    data_size_subset =  data_size_subset[data_size_subset['time'] <= now_time]
    data_size_subset = data_size_subset[data_size_subset['time'] >= yesterday_time]

    grouped_df = data_size_subset.groupby("region")
    mean_df = grouped_df.mean()
    mean_df = mean_df.reset_index() 

    api_price = mean_df.iloc[mean_df['api_price'].idxmax()]['api_price']
    api_region = mean_df.iloc[mean_df['api_price'].idxmax()]['region']

    cli_price = float('inf')
    cli_region = None

    if not math.isnan(mean_df['cli_price'].idxmax()):
        cli_price = mean_df.iloc[mean_df['cli_price'].idxmax()]['cli_price']
        cli_region = mean_df.iloc[mean_df['cli_price'].idxmax()]['region']

    if api_price < cli_price:
        return {'region': api_region, 'price': api_price, 'duration': str(days) + ' days', 'size': size}

    return {'region': api_region, 'price': api_price, 'duration': str(days) + ' days', 'size': size}


# Create your views here.
class PriceView(APIView):
    permission_classes = [] # + [IsAuthenticated]

    def get(self, request):
        operation = request.GET.get('operation', None)
        region = request.GET.get('region', None)
        size = request.GET.get('size', None)
        days = request.GET.get('days', None)

        data = {}
        if operation.lower() == 'cheapest' and size and not days:
            data = find_cheapest_region_at_current_time_using_api(size)
        
        elif operation.lower() == 'cheapest' and size and days:
            data = find_cheapest_region_at_sometime(size, days)

        elif operation.lower() == 'average' and region and size and not days:
            data = find_average_price_of_region_and_size(region, size)
        
        elif operation.lower() == 'average' and region and size and days:
            data = find_average_price_of_region_and_size(region, size, days)
        
        return JsonResponse(data)