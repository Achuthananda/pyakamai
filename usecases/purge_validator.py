#!/usr/bin/env python3.6
import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from urllib.parse import urlparse, parse_qs,urljoin
import json
import re
import sys
import os
import datetime
from time import strftime
import time
from urllib.parse import urlencode
import pydig
import urllib3
import http.client
import os.path
from os import path

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http.client._MAXHEADERS = 1000


if(len(sys.argv) != 4):
    print("Incorrect arguments: Correct format is python purge_validator.py <delete/invalidate> <staging/production> <file_containing_urls>")
    print("Example:python purge_validator.py delete staging urls.txt")
    sys.exit()

#Get Method  and Network name from Command Line
method = sys.argv[1]
if method not in ['delete','invalidate']:
    print("Invalid Method.Please enter delete or invalidate")
    sys.exit()

environment = sys.argv[2]
if environment not in ['staging','production']:
    print("Invalid Network.Please enter staging or production")
    sys.exit()

file_name = sys.argv[3]
if path.exists(file_name) == False:
    print("File doesnt exist.Please enter valid filename")
    sys.exit()


edgerc = EdgeRc('/Users/apadmana/.edgerc')
section = 'ccu'
baseurl = 'https://%s' % edgerc.get(section, 'host')

s = requests.Session()
s.auth = EdgeGridAuth.from_edgerc(edgerc, section)

headers = {'Content-Type': 'application/json'}

purgepath = "/ccu/v3/"+method+"/url/"+environment
#Help : python3 purge_validator.py delete staging

#Read url file line by line.
# Using readlines()
file = open(file_name, 'r')
url_list = file.readlines()

essl_staging_ip = '23.35.146.27'
ff_staging_ip = '23.48.169.27'
essl_production_ip = '104.114.80.28'
ff_production_ip = '184.25.108.19'


def getnetwork(hostname):
    network = 'essl'
    akamai_level1hostnames = ['edgesuite','edgekey','edgesuite-staging','edgekey-staging']
    akamai_leve2hostnames = ['akamai','akamaiedge']

    fcname = pydig.query(hostname, 'CNAME')
    if fcname:
        if fcname[0].split('.')[-3] not in akamai_level1hostnames:
            if fcname[0].split('.')[-3] not in akamai_leve2hostnames:
                print("Not a valid Akamai Hostname")
            else:
                print("Hostnames directly cnamed to second level. Not supported for now.")
        else:
            if fcname[0].split('.')[-3] == 'edgesuite':
                network = 'ff'
    return network



for url in url_list:
    purge_url = url.strip()
    print(purge_url)

    parsed_components = urlparse(purge_url)
    hostname = parsed_components.netloc
    path = parsed_components.path
    scheme = parsed_components.scheme
    network = getnetwork(hostname)
    pragma_headers = {'Pragma':'akamai-x-get-client-ip, akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-extracted-values, akamai-x-get-nonces, akamai-x-get-ssl-client-session-id, akamai-x-get-true-cache-key, akamai-x-serial-no, akamai-x-feo-trace, akamai-x-get-request-id, x-akamai-a2-trace,x-akamai-rua-debug,x-akamai-a2-enable, x-akamai-cpi-trace, akamai-x-get-brotli-status',
                      'Host': hostname}

    #Staging Test:

    if environment == 'staging':
        if network == 'essl':
            full_path = scheme + '://' + essl_staging_ip + path
        elif network == 'ff':
            full_path = scheme + '://' + ff_staging_ip + path


    if environment == 'production':
        if network == 'essl':
            full_path = scheme + '://' + essl_prod_ip + path
        elif network == 'ff':
            full_path = scheme + '://' + ff_prod_ip + path

    response = requests.get(full_path,headers=pragma_headers,verify=False)
    status = response.status_code
    cache_status = response.headers["X-Cache"].split(' ')[0]
    if cache_status == "TCP_MISS":
            while cache_status == 'TCP_MISS':
                print("Retrying..")
                response = requests.get(full_path,headers=pragma_headers,verify=False)
                cache_status = response.headers["X-Cache"].split(' ')[0]
    print('Cache-Status:',cache_status)


    data={}
    objects = []
    objects.append(purge_url)

    data['objects'] = objects
    json_data = json.dumps(data)


    fullurl = urljoin(baseurl, purgepath)
    print("Purging....")
    result = s.post(fullurl, headers=headers, data = json_data)
    code = result.status_code
    body = result.json()

    if code == 201:
        time.sleep( 7 )
        response = requests.get(full_path,headers=pragma_headers,verify=False)
        status = response.status_code
        cache_status = response.headers["X-Cache"].split(' ')[0]
        print('Cache-Status:',cache_status)
        if method == 'delete':
            if cache_status == "TCP_MISS":
                print("Purged Successfully")
            else:
                print("Not Purged Successfully!!")
        elif method == 'invalidate':
            if cache_status == "TCP_REFRESH_HIT" or cache_status == "TCP_MEM_HIT":
                print("Purged Successfully")
            else:
                print("Not Purged Successfully!!")


    print('-------------')
