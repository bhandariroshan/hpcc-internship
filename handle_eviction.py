#!/usr/bin/python

import json
import socket
import requests
import time
import pytz
import datetime

metadata_url = "http://169.254.169.254/metadata/scheduledevents?api-version=2019-08-01"
this_host = socket.gethostname()


def get_scheduled_events(): 
    return {
        "DocumentIncarnation":1,
        "Events":[
                {
                    "EventId":"A123BC45-1234-5678-AB90-ABCDEF123456",
                    "EventStatus":"Scheduled",
                    "EventType":"Preempt",
                    "ResourceType":"VirtualMachine",
                    "Resources":["myspotvm"],
                    "NotBefore":"Tue, 16 Mar 2021 00:58:46 GMT",
                    "Description":"",
                    "EventSource":"Platform"
                }
            ]
    }
    headers = {'Metadata': 'true'}
    resp = requests.get(headers=headers, url=metadata_url)
    data = resp.json()
    return data


def handle_scheduled_events(eviction_data):
    user, passwd = 'admin', '@dmin123#'
    url = 'http://40.76.43.103/eviction/' 

    for evt in eviction_data['Events']:
        eventid = evt['EventId']
        status = evt['EventStatus']
        resources = evt['Resources']
        eventtype = evt['EventType']
        resourcetype = evt['ResourceType']
        notbefore = evt['NotBefore'].replace(" ", " ")
        description = evt['Description']
        eventSource = evt['EventSource']

        notbefore = str(datetime.datetime.strptime(notbefore, '%a, %d %b %Y %H:%M:%S GMT'))

        for host in resources:
            print("+ Scheduled Event. This host " + host +\
                " is scheduled for " + eventtype + " by " + eventSource + \
                " with description " + description +\
                " not before " + notbefore)

            requests.post(
                url,
                data={
                    'vm_name': host,
                    'eviction_notice': eviction_data,
                    'eviction_time': notbefore
                },
                auth=(user, passwd),
                verify=False
            )


def main():
    while True:
        data = get_scheduled_events()
        handle_scheduled_events(data)
        time.sleep(5)


if __name__ == '__main__':
    main()