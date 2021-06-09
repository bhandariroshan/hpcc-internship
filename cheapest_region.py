import time
import csv
import math
import pandas as pd
import datetime
import requests
from config import *
from price_puller_azure_cli import pull_multiple
from sqlite_connector import SqliteConnector


def find_region_and_size_available():
	items = {}
	url = "https://prices.azure.com/api/retail/prices"
	while url:
		print(url)
		data = requests.get(url).json()
		for each_data in data['Items']:
			if each_data['armRegionName'] not in items:
				items['armRegionName'] = [each_data['armSkuName']]
			elif each_data['armSkuName'] not in items[each_data['armRegionName']]:
				items['armRegionName'].append(each_data['armSkuName'])

		url = data ['NextPageLink']

	return items

def find_spot_region_and_size_available():
	items = {}
	url = "https://prices.azure.com/api/retail/prices"
	while url:
		print(url)
		data = requests.get(url).json()
		for each_data in data['Items']:
			if each_data['armRegionName'] not in items and 'Spot' in each_data['meterName']:
				items[each_data['armRegionName']] = [each_data['armSkuName']]

			elif 'Spot' in each_data['meterName'] and each_data['armSkuName'] not in items[each_data['armRegionName']]:
				items[each_data['armRegionName']].append(each_data['armSkuName'])

		url = data ['NextPageLink']

	return items

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

	average = find_average_price_of_region_and_size(cheapest_region, size)

	return {
		'region': cheapest_region, 
		'price': cheapest_price, 
		'average_price': average['api_price'], 
		'average_duration': '1 days'
	}

def find_cheapest_region_at_current_time_using_cli(size):
	now_time = str(datetime.datetime.now())
	resource_names = []
	for region in list(spot_region_map.keys()):
		if size in spot_region_map[region]:
			resource_names.append(resource_prefix + region)

	data = pull_multiple(resource_names, [size], now_time)
	
	cheapest_price = float('inf')
	cheapest_region = None

	for price_data in data:
		if price_data['cli_price'] and price_data['cli_price'] < cheapest_price:
			cheapest_price = price_data['cli_price']
			cheapest_region = price_data['region']

	average = find_average_price_of_region_and_size(cheapest_region.replace(resource_prefix, ''), size)

	return {
		'region': cheapest_region.replace(resource_prefix, ''), 
		'price': cheapest_price, 
		'average_price': average['api_price'], 
		'average_duration': '1 days'
	}

def find_cheapest_region_at_sometime(size, time):
	size = size.replace('Standard_', '').replace('_', ' ')
	dbObj = SqliteConnector()
	data = dbObj.select_data_as_dataframe(region=None, size=size)
	data['time'] = pd.to_datetime(data['time'])
	data_size_subset = data[data['size']==size]

	data_size_time_subset = (data_size_subset.set_index('time')
          .between_time(time + ':00:00', time + ':59:00')
          .reset_index()
          .reindex(columns=data_size_subset.columns))

	grouped_df = data_size_time_subset.groupby("region")
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
		return {'region': api_region, 'price': api_price}

	return {'region': api_region, 'price': api_price}

def find_average_price_of_region_and_size(region, size, days=1):
	if size:
		size = size.replace('Standard_', '').replace('_', ' ')
	
	dbObj = SqliteConnector()
	data = dbObj.select_data_as_dataframe(region=region, size=size) 


	data['time'] = pd.to_datetime(data['time'])
	now_time = datetime.datetime.now(data.time[0].tzinfo)
	yesterday_time = now_time - datetime.timedelta(days=days)
	
	if size:
		data_size_subset = data[data['size']==size]
	else:
		data_size_subset = data

	if region:
		data_size_subset = data_size_subset[data_size_subset['region']==region]
	else:
		data_size_subset = data

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