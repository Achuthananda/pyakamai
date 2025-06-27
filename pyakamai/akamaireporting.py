""" Copyright 2015 Akamai Technologies, Inc. All Rights Reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.

 You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
import sys
import os
import requests
import logging
import json
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from .http_calls import EdgeGridHttpCaller

class AkamaiReporting():
    def __init__(self,prdHttpCaller,accountSwitchKey=None):
        self._prdHttpCaller = prdHttpCaller
        self.accountSwitchKey = accountSwitchKey
        return None

    def getURLHits(self,startTime,endTime,body):
        ep = 'reporting-api/v1/reports/urlhits-by-url/versions/1/report-data'
        headers = {'Content-Type': 'application/json'}

        recordjson = json.dumps(body)
        params = {}
        params['start'] = startTime
        params['end'] = endTime
        #print(recordjson)
        
        if self.accountSwitchKey:
            params['accountSwitchKey'] = self.accountSwitchKey
            status,result = self._prdHttpCaller.postResult(ep,recordjson,headers=headers,params=params)
        else:
            status,result = self._prdHttpCaller.postResult(ep,recordjson,headers=headers)

        if status in [201,200]:
            print("Succesfully Fetched the URL report")
            return True,result['data']
        else:
            print("Failed to fetch the URL report")
            print(json.dumps(result,indent=2))
            return False,0
        

    def getBytesTraffic(self,startTime,endTime,cpcodeList):
        ep = '/reporting-api/v1/reports/bytes-by-time/versions/1/report-data'

        metrics = [
            "bytesOffload",
            "bytesOffloadAvg",
            "bytesOffloadMax",
            "bytesOffloadMin",
            "bytesOffloadSlope",
            "edgeBitsPerSecond",
            "edgeBitsPerSecondMax",
            "edgeBitsPerSecondMin",
            "edgeBytesSlope",
            "edgeBytesTotal",
            "midgressBitsPerSecond",
            "midgressBitsPerSecondMax",
            "midgressBitsPerSecondMin",
            "midgressBytesSlope",
            "midgressBytesTotal",
            "originBitsPerSecond",
            "originBitsPerSecondMax",
            "originBitsPerSecondMin",
            "originBytesSlope",
            "originBytesTotal",
            'bytesOffloadTotal'
        ]


        payload = {
            "objectIds": cpcodeList,
            "metrics":metrics
        }

        params = {
            'interval':'FIVE_MINUTES',
            'start':startTime,
            'end':endTime
        }
        if self.accountSwitchKey:
            params['accountSwitchKey'] = self.accountSwitchKey

        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        jsondata = json.dumps(payload,indent=2)
        status,result = self._prdHttpCaller.postResult(ep,jsondata,headers=headers,params=params)
        if status in [201,200]:
            print("Succesfully Fetched the Bytes Traffic report")
            return True,result
        else:
            print("Failed to fetch the URL report")
            print(json.dumps(result,indent=2))
            return False,{}


    def getMidgressHitsTraffic(self,startTime,endTime,cpcodeList):
        ep = '/reporting-api/v1/reports/midgresshits-by-time/versions/1/report-data'

        metrics = [
            "midgressHitsPerSecond",
            "midgressHitsPerSecondMax",
            "midgressHitsPerSecondMin",
            "midgressHitsSlope",
            "midgressHitsTotal"
        ]

        payload = {
            "objectIds": cpcodeList,
            "metrics":metrics
        }
    
        params = {
            'interval':'FIVE_MINUTES',
            'start':startTime,
            'end':endTime
        }
        if self.accountSwitchKey:
            params['accountSwitchKey'] = self.accountSwitchKey

        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        jsondata = json.dumps(payload,indent=2)
        status,result = self._prdHttpCaller.postResult(ep,jsondata,headers=headers,params=params)
        if status in [201,200]:
            print("Succesfully Fetched the Midgress Traffic report")
            return True,result
        else:
            print("Failed to fetch the URL report")
            print(json.dumps(result,indent=2))
            return False,{}


    def getHitsTraffic(self,startTime,endTime,cpcodeList):
        ep = '/reporting-api/v1/reports/hits-by-time/versions/1/report-data'

        metrics = [
            "edgeHitsPerSecond",
            "edgeHitsPerSecondMax",
            "edgeHitsPerSecondMin",
            "edgeHitsSlope",
            "edgeHitsTotal",
            "hitsOffload",
            "hitsOffloadAvg",
            "hitsOffloadMax",
            "hitsOffloadMin",
            "hitsOffloadSlope",
            "originHitsPerSecond",
            "originHitsPerSecondMax",
            "originHitsPerSecondMin",
            "originHitsSlope",
            "originHitsTotal",
            "hitsOffloadTotal"
        ]

        payload = {
            "objectIds": cpcodeList,
            "metrics":metrics
        }
    
        params = {
            'interval':'FIVE_MINUTES',
            'start':startTime,
            'end':endTime
        }
        if self.accountSwitchKey:
            params['accountSwitchKey'] = self.accountSwitchKey

        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        jsondata = json.dumps(payload,indent=2)
        status,result = self._prdHttpCaller.postResult(ep,jsondata,headers=headers,params=params)
        if status in [201,200]:
            print("Succesfully Fetched the Hits Traffic report")
            return True,result
        else:
            print("Failed to fetch the URL report")
            print(json.dumps(result,indent=2))
            return False,{}

    def getHitsTrafficByResponseClass(self,startTime,endTime,cpcodeList):
        ep = '/reporting-api/v1/reports/traffic-by-response/versions/1/report-data'

        metrics = [
            "edgeHits",
            "edgeHitsPercent",
            "originHits",
            "originHitsPercent"
        ]

        payload = {
            "objectIds": cpcodeList,
            "metrics":metrics
        }
    
        params = {
            'interval':'FIVE_MINUTES',
            'start':startTime,
            'end':endTime
        }
        if self.accountSwitchKey:
            params['accountSwitchKey'] = self.accountSwitchKey

        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        jsondata = json.dumps(payload,indent=2)
        status,result = self._prdHttpCaller.postResult(ep,jsondata,headers=headers,params=params)
        if status in [201,200]:
            print("Succesfully Fetched the Hits Traffic report")
            return True,result
        else:
            print("Failed to fetch the URL report")
            print(json.dumps(result,indent=2))
            return False,{}
        
    def getTrafficByHostname(self,startTime,endTime,hostname):
        ep = '/reporting-api/v2/reports/delivery/traffic/current/data'

        metrics = [
            "edgeHitsSum",
            "edgeBytesSum",
            "edgeResponseBytesSum",
            "edgeRequestBytesSum",
            "originHitsSum",
            "originBytesSum",
            "originResponseBytesSum",
            "originRequestBytesSum",
            "midgressHitsSum",
            "midgressBytesSum",
            "midgressResponseBytesSum",
            "midgressRequestBytesSum",
            "offloadedHitsPercentage",
            "offloadedBytesPercentage",
            "offloadedRequestBytesPercentage",
            "offloadedResponseBytesPercentage"
        ]

        payload = {
            "metrics":metrics,
            "dimensions": ["hostname"],
            "filters": [{
                "dimensionName": "hostname",
                "operator": "IN_LIST",
                "expressions": [hostname]
            }]
        }
    
       
        params = {
            'start':startTime+'Z',
            'end':endTime+'Z'
        }
    
        if self.accountSwitchKey:
            params['accountSwitchKey'] = self.accountSwitchKey

        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        jsondata = json.dumps(payload,indent=2)
        status,result = self._prdHttpCaller.postResult(ep,jsondata,headers=headers,params=params)
        if status in [201,200]:
            print("Succesfully Fetched the Hits Traffic report")
            return True,result
        else:
            print("Failed to fetch the URL report")
            print(json.dumps(result,indent=2))
            return False,{}
        
    def getTrafficByCPCode(self,startTime,endTime,cpcodeList):
        ep = '/reporting-api/v2/reports/delivery/traffic/current/data'

        metrics = [
            "edgeHitsSum",
            "edgeBytesSum",
            "edgeResponseBytesSum",
            "edgeRequestBytesSum",
            "originHitsSum",
            "originBytesSum",
            "originResponseBytesSum",
            "originRequestBytesSum",
            "midgressHitsSum",
            "midgressBytesSum",
            "midgressResponseBytesSum",
            "midgressRequestBytesSum",
            "offloadedHitsPercentage",
            "offloadedBytesPercentage",
            "offloadedRequestBytesPercentage",
            "offloadedResponseBytesPercentage"
        ]

        payload = {
            "metrics":metrics,
            "dimensions": ["cpcode"],
            "filters": [{
                "dimensionName": "cpcode",
                "operator": "IN_LIST",
                "expressions": cpcodeList
            }]
        }
    
       
        params = {
            'start':startTime+'Z',
            'end':endTime+'Z'
        }
    
        if self.accountSwitchKey:
            params['accountSwitchKey'] = self.accountSwitchKey

        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        jsondata = json.dumps(payload,indent=2)
        status,result = self._prdHttpCaller.postResult(ep,jsondata,headers=headers,params=params)
        if status in [201,200]:
            print("Succesfully Fetched the Hits Traffic report")
            return True,result
        else:
            print("Failed to fetch the URL report")
            print(json.dumps(result,indent=2))
            return False,{}
        

    
        


    