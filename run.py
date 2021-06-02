import time
import datetime
import argparse
from price_puller_azure_api import pull_multiple as pull_mupliple_api
from price_puller_azure_cli import pull_multiple as pull_mupliple_cli
from csv_writer import CSVWriter
from config import region_codes, sizes, resource_prefix


def pull_price_using_api(now_time):
    final_sizes = [size.replace('Standard_', '').replace('_', ' ') for size in sizes]
    result = pull_mupliple_api(region_codes, final_sizes, now_time)
    return result

def pull_price_using_cli(now_time):
    resource_names = [resource_prefix + region for region in region_codes]
    result = pull_mupliple_cli(resource_names, sizes, now_time)
    return result

def save_price_to_file(writer, api_price, cli_price, method):
    result = []
    if method.lower() == 'both':
        for each_api_price in api_price:
            for each_cli_price in cli_price:
                if each_cli_price['size'].replace('Standard_', '').replace('_', ' ') == each_api_price['size'] and \
                    each_api_price['region'] == each_cli_price['region'].replace(resource_prefix, ''):
                    result.append(
                        {
                            'size': each_cli_price['size'], 
                            'api_price': each_api_price['api_price'], 
                            'cli_price': each_cli_price['cli_price'],
                            'region': each_api_price['region'],
                            'time': each_api_price['time']
                        }
                    )

    elif method.lower() == 'api':
        result = api_price

    else:
        result = cli_price

    writer.write_multiple(result)
    writer.close() 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get Azure Spot Instance Price')
    parser.add_argument('method', type=str,
                    help='Can be one of API or CLI. \n API: Pull azure Spot price from API. \n CLI: Pull azure spot price from CLI.')
    args = parser.parse_args()

    writer = CSVWriter(filename='price.csv', headers=['time', 'region', 'size', 'api_price', 'cli_price'], seperator=',', line_terminator='')
    count = 12
    while count > 0:
        count -= 1
        now_time = str(datetime.datetime.now())
        api_price = {}
        cli_price = {}

        if args.method.lower() not in ['api', 'cli', 'both']:
            parser.error("method must be either of api or cli or both.")

        elif args.method.lower() == 'api':
            api_price = pull_price_using_api(now_time)

        elif args.method.lower() == "cli":
            cli_price = pull_price_using_cli(now_time)
        
        else:
            api_price = pull_price_using_api(now_time)
            cli_price = pull_price_using_cli(now_time)

        save_price_to_file(writer, api_price, cli_price, args.method)

        time.sleep(3600)