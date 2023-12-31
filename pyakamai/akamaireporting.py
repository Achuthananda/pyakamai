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
        


    