import time
import datetime
from pytz import timezone
import argparse
from price_puller_azure_api import pull_multiple as pull_mupliple_api
from price_puller_azure_cli import pull_multiple as pull_mupliple_cli
from csv_writer import CSVWriter
from config import region_codes, sizes, resource_prefix
from sqlite_connector import SqliteConnector


def pull_price_using_api(now_time):
    final_sizes = [size.replace('Standard_', '').replace('_', ' ') for size in sizes]
    result = pull_mupliple_api(region_codes, final_sizes, now_time)
    return result

def pull_price_using_cli(now_time):
    resource_names = [resource_prefix + region for region in region_codes]
    result = pull_mupliple_cli(resource_names, sizes, now_time)
    return result

def save_price_to_database(dbobj, api_price, cli_price, method): 
    if method.lower() == 'both':
        for each_api_price in api_price:
            for each_cli_price in cli_price:
                if each_cli_price['size'].replace('Standard_', '').replace('_', ' ') == each_api_price['size'] and \
                    each_api_price['region'] == each_cli_price['region'].replace(resource_prefix, ''):
                    result = (
                            each_api_price['time'],
                            each_api_price['region'],
                            each_cli_price['size'], 
                            each_api_price['api_price'], 
                            each_cli_price['cli_price'],
                            each_api_price['pay_as_you_go_price'],
                            each_api_price['1_year_reserved_price'],
                            each_api_price['3_year_reserved_price'],
                            each_api_price['%_saving_pay_as_you_go'],
                            each_api_price['%_saving_1y_reserved'],
                            each_api_price['%_saving_3y_reserved']
                    )

                    dbobj.create_benchmark(result)

    else:
        datas = api_price or cli_price
        for data in datas:
            result = (
                    data['time'],
                    data['region'],
                    data['size'], 
                    data['api_price'], 
                    data['cli_price'],
                    data['pay_as_you_go_price'],
                    data['1_year_reserved_price'],
                    data['3_year_reserved_price'],
                    data['%_saving_pay_as_you_go'],
                    data['%_saving_1y_reserved'],
                    data['%_saving_3y_reserved']
            )

            dbobj.create_benchmark(result)

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
                            'time': each_api_price['time'],
                            'pay_as_you_go_price': each_api_price['pay_as_you_go_price'],
                            '1_year_reserved_price': each_api_price['1_year_reserved_price'],
                            '3_year_reserved_price': each_api_price['3_year_reserved_price'],
                            '%_saving_pay_as_you_go': each_api_price['%_saving_pay_as_you_go'],
                            '%_saving_1y_reserved': each_api_price['%_saving_1y_reserved'],
                            '%_saving_3y_reserved': each_api_price['%_saving_3y_reserved']
                        }
                    )

    elif method.lower() == 'api':
        result = api_price

    else:
        result = cli_price

    writer.write_multiple(result)

def run(method, saveto, days=1, hours=1):
    if days > 1:
        hours = 24

    count = 0
    while count < days * hours:
        writeheader = False
        mode = 'a'
        if count == 0:
            writeheader = True
            mode = 'w'

        if saveto.lower() == 'csv':
            writer = CSVWriter(
                filename='price.csv', 
                headers=[
                    'time',
                    'region',
                    'size',
                    'api_price',
                    'cli_price',
                    'pay_as_you_go_price',
                    '1_year_reserved_price',
                    '3_year_reserved_price',
                    '%_saving_pay_as_you_go',
                    '%_saving_1y_reserved',
                    '%_saving_3y_reserved'
                ], 
                seperator=',', 
                line_terminator='',
                mode=mode,
                is_writeheader=writeheader
            )

        else:
            dbobj = SqliteConnector()

        count += 1
        now_time = str(datetime.datetime.now(timezone('US/Eastern')))
        api_price = {}
        cli_price = {}

        if method.lower() not in ['api', 'cli', 'both']:
            parser.error("method must be either of api or cli or both.")

        elif method.lower() == 'api':
            api_price = pull_price_using_api(now_time)

        elif method.lower() == "cli":
            cli_price = pull_price_using_cli(now_time)
        
        else:
            api_price = pull_price_using_api(now_time)
            cli_price = pull_price_using_cli(now_time)

        if saveto.lower() == 'csv':
            save_price_to_file(writer, api_price, cli_price, method)
            writer.close()
        else:
            save_price_to_database(dbobj, api_price, cli_price, method)

        print('sleeping..')
        time.sleep(60*60)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get Azure Spot Instance Price')
    parser.add_argument(
        '--method', 
        type=str, 
        default='api',
        help='Can be one of API or CLI. \
            \n API: Pull azure Spot price from API. \
            \n CLI: Pull azure spot price from CLI.'
    )

    parser.add_argument(
        '--saveto', 
        type=str, 
        default="db",
        help='Can be one of db or csv. \
            \n db: To store the data in sqlite databse. \
            \n csv: To store the data in csv file.'
    )

    parser.add_argument(
        '--days', 
        type=int,
        help='Number of days to run.',
        default=1
    )

    parser.add_argument(
        '--hours', 
        default=1,
        type=int,
        help='Number of days to run.',
    )

    args = parser.parse_args()
    run(args.method, args.saveto, args.days, args.hours)