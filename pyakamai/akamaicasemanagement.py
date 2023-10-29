# Python edgegrid module
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
if sys.version_info[0] >= 3:
    # python3
    from urllib import parse
else:
    # python2.7
    import urlparse as parse

class AkamaiCaseManagement():
    def __init__(self,prdHttpCaller,accountSwitchKey=None):
        self._prdHttpCaller = prdHttpCaller
        self.accountSwitchKey = accountSwitchKey
        return None

    def createCase(self,caseDetailsFile):  
        fp = open(caseDetailsFile,'r')
        data = json.load(fp)
        caseobj_json = json.dumps(data)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        ep = "/case-management/v2/cases"

        if self.accountSwitchKey:
            params = {'accountSwitchKey': self.accountSwitchKey}
            status,response = self._prdHttpCaller.postResult(ep,caseobj_json,headers=headers,params=params)
        else:
            status,response = self._prdHttpCaller.postResult(ep,caseobj_json,headers=headers)

        if status == 200:
           return response['caseId']
        else:
            return ''

    def listmyActiveCases(self,accountIds=None,limit=50,duration=30):
        ep = '/case-management/v3/cases'
        params = {}
        if accountIds != None:
            params['accountIds'] = accountIds
        
        params['limit'] = limit
        params['duration'] = duration
        params['type'] = 'MY_ACTIVE_CASES'

        status,response = self._prdHttpCaller.getResult(ep, params)

        if status == 200:
            return response
        else:
            return {}

    def listmyClosedCases(self,accountIds=None,limit=50,duration=30):
        ep = '/case-management/v3/cases'
        params = {}
        if accountIds != None:
            params['accountIds'] = accountIds
        
        params['limit'] = limit
        params['duration'] = duration
        params['type'] = 'MY_CLOSED_CASES'

        status,response = self._prdHttpCaller.getResult(ep, params)

        if status == 200:
            return response
        else:
            return {}

    def listAllCases(self):
        ep = '/case-management/v2/cases'
        params = {}
        
        params['type'] =  'all'
        if self.accountSwitchKey:
            params['accountSwitchKey']=  self.accountSwitchKey

        status,response = self._prdHttpCaller.getResult(ep, params)

        if status == 200:
            return response
        else:
            return {}

    def listAllClosedCases(self,accountIds=None,limit=50,duration=30):
        ep = '/case-management/v3/cases'
        params = {}
        if accountIds != None:
            params['accountIds'] = accountIds
        
        params['limit'] = limit
        params['duration'] = duration
        params['type'] = 'ALL_CLOSED_CASES'

        status,response = self._prdHttpCaller.getResult(ep, params)

        if status == 200:
            return response
        else:
            return {}
       
#https://techdocs.akamai.com/case-mgmt/pdfs/case-mgmt-api-v2-deprecated.pdf
