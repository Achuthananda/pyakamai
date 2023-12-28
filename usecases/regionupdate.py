#Product Map: https://ac.akamai.com/thread/24508

import requests
import pandas as pd
import sys
import os
import json
import http.client
from urllib.parse import urlparse, parse_qs,urljoin
from requests.api import delete
import urllib3
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from akamaihttp import EdgeGridHttpCaller
if sys.version_info[0] >= 3:
    # python3
    from urllib import parse
else:
    # python2.7
    import urlparse as parse
import pandas,csv
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http.client._MAXHEADERS = 1000



akatoken = ''
akasso = ''
xsrf_token = ''
accountSwitchKey = ''
edgerc_location = '~/.edgerc'
email_id = 'achut@gtttt.com'

cookies = {
    'AKATOKEN': akatoken,
    'AKASSO': akasso
}

headers = {
    'Content-Length': '0',
    'X-XSRF-TOKEN': xsrf_token
}

response = requests.get('https://control.akamai.com/dashboard-manager/v1/dashboard-config', headers=headers, cookies=cookies)
if response.status_code == 200:
    print("Your session cookies are valid. Proceeding ahead with the product change...")
else:
    print("Your session cookies are invalid or expired. Please enter correct details of cookies")
    exit

section = 'default'
debug = False
verbose = False
edgerc = EdgeRc(edgerc_location)
baseurl_prd = 'https://%s' % edgerc.get(section, 'host')
session = requests.Session()
session.auth = EdgeGridAuth.from_edgerc(edgerc, section)
session.headers.update({'User-Agent': "AkamaiCLI"})
prdHttpCaller = EdgeGridHttpCaller(session, debug, verbose, baseurl_prd)

headers = {'Content-Type': 'application/json'}

#filename = 'ehnlist.xlsx'
streamList = [2027065]
#df = pd.read_excel(filename)
#for index, row in df.iterrows():
for streams in streamList:
    streamId = streams
    #preferredRegion = "".join(row['PreferredRegion'])
    #preferredRegionArray = preferredRegion.split(',')
    

    params = {}
    params["accountSwitchKey"] = accountSwitchKey
    getStreamEP = '/config-media-live/v2/msl-origin/streams/{}'.format(streamId)
    getStreamJson = prdHttpCaller.getResult(getStreamEP,params=params,headers=headers)
    print(getStreamJson)
    getStreamJson = getStreamJson[1]

    getStreamJson['primaryPreferredSettings']['primaryPreferredRegions'] = [37638,22591]
    getStreamJson['primaryPreferredSettings']['preferredPenaltyRecommended'] = True
    
    getStreamJson['backupPreferredSettings']['backupPreferredRegions'] = [37638,22591]
    getStreamJson['backupPreferredSettings']['preferredPenaltyRecommended'] = True

    
    print(getStreamJson)

    controlcenterpath = 'https://control.akamai.com/msl-stream-provision/api/v1/streams/{}'.format(streamId)

    headers = {'x-xsrf-token':xsrf_token,
               'Content-Type': 'application/json'}

    cookies = {'AKATOKEN':akatoken,
               'AKASSO':akasso}

    params = {}

    putbody = json.dumps(getStreamJson,indent=2)
    print(putbody)

   #print("Updating the Preferred Region for the edgehostname {} to product {}".format(edgehostname,target_product))
    update_ehn = requests.put(controlcenterpath,headers=headers,params=params,cookies=cookies,data=putbody)
    print(update_ehn.content)
    print(update_ehn.status_code)
    if update_ehn.status_code == 202:
        print("Updated the MSL ")
    else:
        print("Failed to update the MSL ")
    print('*'*80)
