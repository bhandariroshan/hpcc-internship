# HPCC on Azure

Minimizing the cost of setting up cloud infrastructure is very important for all companies. This project involves creating utilities to estimate the money saved by running spot instances in different regions at different times and also scripts to automate cluster formation in Azure Kubernetes Service (AKS). This project also involves benchmarking the cost effectiveness of several use cases revolving around HPCC spot instances. As an important task, this project also involves developing strategies for job recovery after eviction and cleaning after eviction notice. Finally, it will also identify tasks that can be used with spot instances. 

# Features:
1. Scripts to find different Azure regions and Sizes
2. Scripts to find different Spot Instances available in different Azure regions
3. Scripts to create resources on Azure
4. Scripts to deploy HPCC on Azure Kubernetes Service (AKS)
5. Scripts to find cheapest spot region for a given size
6. Scripts to find average price of a size on a region
7. Scripts to simulate eviction from Azure Spot Instance
8. Scripts to handle eviction from Azure Spot Instance 
9. Find patterns for the best use case of off business hour region use of spot instance and savings measurement.

## Find all VM Instances in different Azure Regions and Sizes Available

This allows you to finding all VM instances available in different Azure regions. To view this in command line you can call:

```
python runcheap.py --operation findvms
```

This allows you to find cheapest region using command line using api data pull:

```
python runcheap.py --operation cheapest --method api
```

This allows you to find cheapest region using command line using cli data pull:

```
python runcheap.py --operation cheapest --method cli
```

To get the results in your code for programmatic access you can import and use as shown below:

To get the spot vms:
```
from cheapest_region import find_spot_region_and_size_available  
spot_vms = find_spot_region_and_size_available()
```

The results are returned as a dictionary.
 

## Find Cheapest Region for a given size using api
```
from cheapest_region import find_cheapest_region_at_current_time_using_api
data = find_cheapest_region_at_current_time_using_api(size='Standard_DS1_v2')
```

Returns a json containing details of the cheapest region

## Find Cheapest Region for a given size using cli
```
from cheapest_region import find_cheapest_region_at_current_time_using_cli
data = find_cheapest_region_at_current_time_using_cli(size='Standard_DS1_v2')
```

Returns a json containing details of the cheapest region

## Find Average Price of a size on a region

```
from cheapest_region import find_average_price_of_region_and_size
data = find_average_price_of_region_and_size(region="eastus", size='Standard_DS1_v2',  days=1)
```

Returns a json containing details of the cheapest region


