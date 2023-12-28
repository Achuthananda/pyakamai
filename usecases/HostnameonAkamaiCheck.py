import pydig
import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from urllib.parse import urljoin
import json
import re
import sys
import os
import datetime
from time import strftime
import time
import urllib
import pandas
from pandas import ExcelWriter


edgerc = EdgeRc('/Users/apadmana/.edgerc')
section = 'default'
baseurl = 'https://%s' % edgerc.get(section, 'host')
s = requests.Session()
s.auth = EdgeGridAuth.from_edgerc(edgerc, section)

akamai_level1hostnames = ['edgesuite','edgekey','edgesuite-staging','edgekey-staging','akamaized','akamaized-staging']


def getpropctraccId(id):
    return id[4:]

def getProperties(accountSwitchKey,contractid,groupid):
    properties_path = '/papi/v1/properties'
    params = {
                'accountSwitchKey': accountSwitchKey,
                'groupId': groupid,
                'contractId': contractid
             }
    fullurl = urljoin(baseurl, properties_path)
    result = s.get(fullurl,params=params)
    code = result.status_code
    body = result.json()
    if len(body['properties']['items']) != 0:
        return body['properties']['items']
    else:
        temp = {}
        return temp

hostname_list = []

def getFirstLevelCname(hostname):
    fcname = pydig.query(hostname, 'CNAME')
    if fcname:
        if fcname[0].split('.')[-3] in akamai_level1hostnames:
            join_fcname = '.'.join(fcname)
            return join_fcname,'Yes'
        else:
            join_fcname = '.'.join(fcname)
            return join_fcname,'No'
    else:
        ip_address = pydig.query(hostname, 'A')
        if ip_address:
            return ip_address[0],'No'
        else:
            return 'SOA Record','No'

def fetchHostnames(accountSwitchKey,property_list):
    for i in property_list:
        propid = getpropctraccId(i['propertyId'])
        grpid = getpropctraccId(i['groupId'])
        ctrid =getpropctraccId(i['contractId'])
        if i['productionVersion'] == None:
            version = int(i['latestVersion'])
        else:
            version = int(i['productionVersion'])


        hostname_path = "/papi/v0/properties/"+str(propid)+"/versions/"+str(version)+"/hostnames"
        params =    {
                    'accountSwitchKey': accountSwitchKey,
                    'contractId': i['contractId'],
                    'groupId': i['groupId']
                    }
        fullurl = urljoin(baseurl, hostname_path)
        result = s.get(fullurl, params=params)
        code = result.status_code
        body = result.json()

        if code == 200:
            for item in body['hostnames']['items']:
                hostname_detail = {}
                hostname_detail['Group'] = i['groupId']
                hostname_detail['Property'] = body['propertyName']
                hostname_detail['Hostname'] = item['cnameFrom']
                hostname_detail['EdgeHostname'] = item['cnameTo']
                hostname_detail['DNS Record'],hostname_detail['Live'] = getFirstLevelCname(item['cnameFrom'])
                hostname_list.append(hostname_detail)
        else:
        	print ("Failed to retrieve hostname details.")
        	print ("Response Code: ",code)

def printHostnames(accountSwitchKey):
    headers = {'Content-Type': 'application/json'}
    #Get the list of groups in the account

    params =    {
                'accountSwitchKey': accountSwitchKey
                }

    path = '/papi/v1/groups/'
    fullurl = urljoin(baseurl, path)
    result = s.get(fullurl,params=params)
    code = result.status_code
    body = result.json()

    for i in body['groups']['items']:
        for j in i['contractIds']:
            property_list = getProperties(accountSwitchKey,j,i['groupId'])
            #print(property_list)
            if len(property_list) != 0:
                fetchHostnames(accountSwitchKey,property_list)


if __name__=="__main__":
    accountSwitchKey = input("Enter Account Switch Key:")

    file_name = str(accountSwitchKey) + '.xlsx'
    print("Fetching Hostname details and updating in file:",file_name)
    print("................")
    writer = pandas.ExcelWriter(file_name, engine='xlsxwriter')

    printHostnames(accountSwitchKey)

    df=pandas.json_normalize(hostname_list)
    pandas.set_option('display.max_rows', df.shape[0]+1)
    df.to_excel(writer, sheet_name='HostnameInfo',index = False)

    writer.save()
    print("Done")
