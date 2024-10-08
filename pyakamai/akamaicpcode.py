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


class AkamaiCPCode():
    def __init__(self,prdHttpCaller,accountSwitchKey=None):
        self._prdHttpCaller = prdHttpCaller
        self.accountSwitchKey = accountSwitchKey
        return None
    
    def createCPCode(self,contractId,groupId,cpcodename,productId):
        """ Create a CPCode"""
        createCPCodeEndPoint = '/papi/v1/cpcodes'
        params = {}
        params["contractId"] = contractId
        params["groupId"] = groupId
        create_cpcode = {
            "productId": productId,
            "cpcodeName": cpcodename
        }
        cpcode_data = json.dumps(create_cpcode)

        if self.accountSwitchKey:
            params['accountSwitchKey'] = self.accountSwitchKey
            print(params)
            status,createResponse = self._prdHttpCaller.postResult(createCPCodeEndPoint,cpcode_data,params)
        else:
            status,createResponse = self._prdHttpCaller.postResult(createCPCodeEndPoint,cpcode_data,params)

        if status == 201:
            cpCode = createResponse['cpcodeLink'].split('?')[0].split('/')[4].split('_')[1]
            return cpCode
        else:
            return 0
        