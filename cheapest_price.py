import time
import csv
import math
import pandas as pd
import datetime
import requests
from config import *
from price_puller_azure_cli import pull_multiple


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

	return cheapest_region, cheapest_price

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

	return cheapest_region, cheapest_price

def find_cheapest_region_at_sometime(size, time):
	size = size.replace('Standard_', '').replace('_', ' ')
	data = pd.read_csv('price.csv.csv')
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
		return api_region, api_price
	return cli_region, cli_price

def find_cheapest_region_entire_day(size, date):
	pass

def find_cheapest_region_entire_week(size):
	pass

def find_cheapest_day_for_a_size(size):
	pass


if __name__ == '__main__':
	# print(find_cheapest_region_at_current_time_using_cli('Standard_D2s_v3'))
	print(find_cheapest_region_at_sometime('Standard_DS3_v2', '00'))