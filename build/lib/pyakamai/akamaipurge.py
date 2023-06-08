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
import json
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from .http_calls import EdgeGridHttpCaller


class AkamaiPurge():
    def __init__(self,prdHttpCaller):
        self._prdHttpCaller = prdHttpCaller
        return None

    def deletebyCPCode(self,cpcodeList,network):
        ep = '/ccu/v3/delete/cpcode/{network}'.format(network =network)
        payload = {"objects": cpcodeList}
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        jsondata = json.dumps(payload,indent=2)
        status,result = self._prdHttpCaller.postResult(ep,jsondata,headers=headers)
        return result


    def deletebyURL(self,urlList,network):
        ep = '/ccu/v3/delete/url/{network}'.format(network =network)
        payload = {"objects": urlList}
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        jsondata = json.dumps(payload,indent=2)
        status,result = self._prdHttpCaller.postResult(ep,jsondata,headers=headers)
        return result

    def deletebyCacheTag(self,cacheTagList,network):
        ep = '/ccu/v3/delete/tag/{network}'.format(network =network)
        payload = {"objects": cacheTagList}
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        jsondata = json.dumps(payload,indent=2)
        status,result = self._prdHttpCaller.postResult(ep,jsondata,headers=headers)
        return result


    def invalidatebyCPCode(self,cpcodeList,network):
        ep = '/ccu/v3/invalidate/cpcode/{network}'.format(network =network)
        payload = {"objects": cpcodeList}
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        jsondata = json.dumps(payload,indent=2)
        status,result = self._prdHttpCaller.postResult(ep,jsondata,headers=headers)
        return result


    def invalidatebyURL(self,urlList,network):
        ep = '/ccu/v3/invalidate/url/{network}'.format(network =network)
        payload = {"objects": urlList}
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        jsondata = json.dumps(payload,indent=2)
        status,result = self._prdHttpCaller.postResult(ep,jsondata,headers=headers)
        return result

        
    def invalidatebyCacheTag(self,cacheTagList,network):
        ep = '/ccu/v3/invalidate/tag/{network}'.format(network =network)
        payload = {"objects": cacheTagList}
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        jsondata = json.dumps(payload,indent=2)
        status,result = self._prdHttpCaller.postResult(ep,jsondata,headers=headers)
        return result


