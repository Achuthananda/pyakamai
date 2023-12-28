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

class AkamaiEdgeHostName():
    def __init__(self,prdHttpCaller,accountSwitchKey=None):
        self._prdHttpCaller = prdHttpCaller
        self.accountSwitchKey = accountSwitchKey
        return None
    
    def getallEdgeHostNames(self):
        ep = "/hapi/v1/edge-hostnames"
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,ehnList = self._prdHttpCaller.getResult(ep,params)
        else:
            status,ehnList = self._prdHttpCaller.getResult(ep)
        if status == 200:
            return ehnList
        else:
            return {}

    def listProducts(self):
        ep = "/hapi/v1/products/display-names"
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,productList = self._prdHttpCaller.getResult(ep,params)
        else:
            status,productList = self._prdHttpCaller.getResult(ep)
        if status == 200:
            return productList
        else:
            return {}


    def createEdgeHostname(self,contractId,groupId,productId,hostName,domainSuffix,network,ipVersion,certEnrollmentId):
        ep = '/papi/v1/edgehostnames'
        params = {}
        params["contractId"] = contractId
        params["groupId"] = groupId

        create_hostname = {
            "productId": productId,
            "domainPrefix": hostName,
            "domainSuffix": domainSuffix,
            "secureNetwork": network,
            "ipVersionBehavior": ipVersion,
            "certEnrollmentId": certEnrollmentId
        }   
        hostname_data = json.dumps(create_hostname)
        if self.accountSwitchKey:
            params['accountSwitchKey'] = self.accountSwitchKey
        
        status,createEHNJson = self._prdHttpCaller.postResult(ep,hostname_data,params=params)
        if status == 201:
            return createEHNJson
        else:
            return {}
        
    def getDnsZoneHostName(ehn):
        if ehn[-1] == '.':
            ehn = ehn[:-1]
        components = ehn.split('.')
        ehnlength = len(components)
        dnszonelist = components[ehnlength-2:ehnlength]
        hostnamelist = components[0:ehnlength-2]
        dnszone = '.'.join(dnszonelist)
        hostname = '.'.join(hostnamelist)
        return dnszone,hostname

        
    def updateTTL(self,edgehostname,ttl,comments):
        params = {}
        if self.accountSwitchKey:
            params['accountSwitchKey'] = self.accountSwitchKey

        patch_body = []
        replace_ttl_json = {
            "op": "replace",
            "path": "/ttl",
            "value": str(ttl)
        }
        patch_body.append(replace_ttl_json)

        patch_json_data = json.dumps(patch_body)
        params["comments"] = comments

        dnsZone,hostname = self.getDnsZoneHostName(edgehostname)

        ep = 'hapi/v1/dns-zones/{}/edge-hostnames/{}'.format(dnsZone, hostname)
        status,updateEHNJson = self._prdHttpCaller.patchResult(ep,patch_json_data,params)
        return status,updateEHNJson
        
    def changeIPVersion(self,edgehostname,ipversion,comments):
        params = {}
        if self.accountSwitchKey:
            params['accountSwitchKey'] = self.accountSwitchKey

        patch_body = []
        replace_ip_json = {
        "op": "replace",
        "path": "/ipVersionBehavior",
        "value": ipversion
        }
        patch_body.append(replace_ip_json)

        patch_json_data = json.dumps(patch_body)
        params["comments"] = comments

        dnsZone,hostname = self.getDnsZoneHostName(edgehostname)

        ep = 'hapi/v1/dns-zones/{}/edge-hostnames/{}'.format(dnsZone, hostname)
        status,updateEHNJson = self._prdHttpCaller.patchResult(ep,patch_json_data,params)
        return status,updateEHNJson






