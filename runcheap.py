import time
import argparse 
from cheapest_region import *


def run(operation, method, region, size, time=None):
    if operation == "cheapest" and method == "api" and not time:
        return find_cheapest_region_at_current_time_using_api(size)

    elif operation == "cheapest" and method == "cli" and not time:
        return find_cheapest_region_at_current_time_using_cli(size)

    elif operation == "cheapest" and method == "cli" and time:
        return find_cheapest_region_at_sometime(size, time)

    elif operation == "average":
        return find_average_price_of_region_and_size(region, size)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get Azure Spot Instance Price')
    parser.add_argument('--operation', type=str, default="cheapest",
                help='Can be one of average or cheapest. \
                \n average: Find the average Price. \
                \n cheapest: Find the cheapest region.'
            )

    parser.add_argument('--method', type=str, default="api",
                help='Can be one of api or cli. \
                \n API: Pull azure Spot price from API. \
                \n CLI: Pull azure spot price from CLI.'
            )

    parser.add_argument('--region', type=str, default="eastus",
                    help='Can be any valid region. '
                )

    parser.add_argument('--size', type=str, default="Standard_DS2_v3",
                help='Can be any valid size eg: Standard_DS2_v3. '
            )

    parser.add_argument('--days', type=int, default=1,
                help='Can be any valid size eg: Standard_DS2_v3. '
            )

    parser.add_argument('--time', type=str, default=None,
        help='Can be any valid time eg: 12. '
    )

    args = parser.parse_args()
    print(run(args.operation, args.method, args.region, args.size, args.time))
