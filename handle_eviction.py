#!/usr/bin/python

import json
import socket
import requests
import time
import pytz
import datetime
from config import stream_notice_api

metadata_url = "http://169.254.169.254/metadata/scheduledevents?api-version=2019-08-01"
this_host = socket.gethostname()

def test_api():
    resp = requests.post(
        stream_notice_api,
        data={
            'vm_name': 'roshan-test-vm-126',
            'eviction_notice': {'notice': 'asdf'},
            'eviction_time': str(datetime.datetime.now())
        },
        auth=('admin', '@dmin123#'),
        verify=False
    )
    print(resp.json())

def get_scheduled_events(): 
    # return {
    #     "DocumentIncarnation":1,
    #     "Events":[
    #             {
    #                 "EventId":"A123BC45-1234-5678-AB90-ABCDEF123456",
    #                 "EventStatus":"Scheduled",
    #                 "EventType":"Preempt",
    #                 "ResourceType":"VirtualMachine",
    #                 "Resources":["myspotvm"],
    #                 "NotBefore":"Tue, 16 Mar 2021 00:58:46 GMT",
    #                 "Description":"",
    #                 "EventSource":"Platform"
    #             }
    #         ]
    # }
    headers = {'Metadata': 'true'}
    resp = requests.get(headers=headers, url=metadata_url)
    data = resp.json()
    return data


def handle_scheduled_events(eviction_data):
    user, passwd = 'admin', '@dmin123#'
    url = stream_notice_api

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

            resp = requests.post(
                url,
                data={
                    'vm_name': host,
                    'eviction_notice': eviction_data,
                    'eviction_time': notbefore
                },
                auth=(user, passwd),
                verify=False
            )
            print(resp.json())


def main():
    while True:
        data = get_scheduled_events()
        handle_scheduled_events(data)
        time.sleep(5)


if __name__ == '__main__':
    main()
    # test_api()