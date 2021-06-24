import time
import datetime
from pytz import timezone
import argparse
from .price_puller_azure_api import pull_multiple as pull_mupliple_api
from .price_puller_azure_cli import pull_multiple as pull_mupliple_cli
from .config import region_codes, sizes, resource_prefix
from spotprices.models import SpotPrices


def pull_price_using_api(now_time):
    result = pull_mupliple_api(now_time)
    return result

def pull_price_using_cli(now_time):
    resource_names = [resource_prefix + region for region in region_codes]
    result = pull_mupliple_cli(resource_names, sizes, now_time)
    return result

def save_price_to_database(api_price, cli_price, method): 
    datas = api_price or cli_price
    for data in datas:
        sp = SpotPrices(
                time=data['time'],
                region=data['region'],
                size=data['size'], 
                api_price=data['api_price'], 
                cli_price=data['cli_price'],
                pay_as_you_go_price=data['pay_as_you_go_price'],
                one_year_reserved_price=data['1_year_reserved_price'],
                three_year_reserved_price=data['3_year_reserved_price'],
                per_saving_paygo=data['%_saving_pay_as_you_go'],
                per_saving_one=data['%_saving_1y_reserved'],
                per_saving_three=data['%_saving_3y_reserved']
        )

        sp.save()

def run():
    method = "api"

    now_time = str(datetime.datetime.now(timezone('US/Eastern')))
    api_price = {}
    cli_price = {}

    if method.lower() == 'api':
        api_price = pull_price_using_api(now_time)

    elif method.lower() == "cli":
        cli_price = pull_price_using_cli(now_time)

    save_price_to_database(api_price, cli_price, method)
    print('success..')