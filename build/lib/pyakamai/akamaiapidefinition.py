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

class AkamaiAPIDefinition():
    def __init__(self,prdHttpCaller,accountSwitchKey=None):
        self._prdHttpCaller = prdHttpCaller
        self.accountSwitchKey = accountSwitchKey
        return None

    def listAPIDefinitions(self,page=1,pageSize=25):
        ep = '/api-definitions/v2/endpoints'
        params = {}
        params[page] = page
        params[pageSize] = pageSize
        if self.accountSwitchKey:
            params['accountSwitchKey'] = self.accountSwitchKey
            status,result = self._prdHttpCaller.getResult(ep,params)
        else:
            status,result = self._prdHttpCaller.getResult(ep,params)
        if status == 200:
            return(result)
        else:
            return {}
        
    def listCacheSettings(self,apiEndPointId,versionNumber):
        ep = '/api-definitions/v2/endpoints/{apiEndPointId}/versions/{versionNumber}/settings/cache'.format(apiEndPointId=apiEndPointId,versionNumber=versionNumber)
        print(ep)
        if self.accountSwitchKey:
            params = {}
            params['accountSwitchKey'] = self.accountSwitchKey
            status,result = self._prdHttpCaller.getResult(ep,params)
        else:
            status,result = self._prdHttpCaller.getResult(ep)
        if status == 200:
            return(result)
        else:
            return {}