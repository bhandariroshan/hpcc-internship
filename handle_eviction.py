#!/usr/bin/python

import json
import socket
# import urllib2
import requests
import time

metadata_url = "http://169.254.169.254/metadata/scheduledevents?api-version=2019-08-01"
this_host = socket.gethostname()

def test():
    user, passwd = 'admin', '@dmin123#'
    url = 'http://157.56.182.115/eviction/'
    count = 0
    while True:
        machine_started = False
        if count == 0:
            machine_started = True

        vm_name ='Roshan'
        vm_size = 'Roshan'
        vm_region = 'Roshan'
        cluster_name = 'Roshan'
        cluster_region = 'Roshan'

        requests.post(
            url,
            data={
                'machine_started':machine_started,
                'vm_name': vm_name,
                'vm_size': vm_size,
                'vm_region': vm_region,
                'cluster_name': cluster_name,
                'cluster_region': cluster_region
            },
            auth=(user, passwd),
            verify=False
        )

        count += 1

        time.sleep(30)

# def get_scheduled_events():
#     req = urllib2.Request(metadata_url)
#     req.add_header('Metadata', 'true')
#     resp = urllib2.urlopen(req)
#     data = json.loads(resp.read())
#     return data


# def handle_scheduled_events(data):
#     for evt in data['Events']:
#         eventid = evt['EventId']
#         status = evt['EventStatus']
#         resources = evt['Resources']
#         eventtype = evt['EventType']
#         resourcetype = evt['ResourceType']
#         notbefore = evt['NotBefore'].replace(" ", "_")
#         description = evt['Description']
#         eventSource = evt['EventSource']
#         if this_host in resources:
#             print("+ Scheduled Event. This host " + this_host +\
#                 " is scheduled for " + eventtype + " by " + eventSource + \
#                 " with description " + description +\
#                 " not before " + notbefore)

#             # Add logic for handling events here

def main():
    # data = get_scheduled_events()
    # handle_scheduled_events(data)
    test()

if __name__ == '__main__':
    main()