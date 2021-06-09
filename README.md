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
10. Use Jenkins and Azure Spot Instances for HPCC Systems Development work.
11. Potential spot instance use cases for HPCC Systems related jobs.


## Find all VM Instances in different Azure Regions and Sizes Available

This allows you to finding all VM instances available in different Azure regions. To view this in command line you can call:

`
	python runcheap.py --operation findvms
`

To get the results in your code for programmatic access you can import and use as shown below:
`
	from cheapes_region import find_region_and_size_available
	vms = find_region_and_size_available()
`

To get the spot vms:

`
	from cheapes_region import find_spot_region_and_size_available
	spot_vms = find_spot_region_and_size_available()
`

The results are returned as a dictionary.

## Find all Spot Instances in different regions and Sizes Available

## Find Cheapest Region for a given size

## Find Average Price of a size on a region