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


class AkamaiChinaCDN():
    def __init__(self,prdHttpCaller,accountSwitchKey=None):
        self._prdHttpCaller = prdHttpCaller
        self.accountSwitchKey = accountSwitchKey
   
        icpinfoEndPoint = "/chinacdn/v1/icp-numbers"
        if accountSwitchKey:
            self.accountSwitchKey = accountSwitchKey
            params = {'accountSwitchKey':accountSwitchKey}
            headers = {"Accept": "application/vnd.akamai.chinacdn.icp-numbers.v1+json"}
            self._icp_info = self._prdHttpCaller.getResult(icpinfoEndPoint,headers,params)
        else:
            self._icp_info = self._prdHttpCaller.getResult(icpinfoEndPoint,headers)

        return None

    def listProperties(self):
        listPropertiesEndPoint = '/chinacdn/v1/property-hostnames'
        headers = {"Accept": "application/vnd.akamai.chinacdn.property-hostnames.v1+json"}
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            properties_info = self._prdHttpCaller.getResult(listPropertiesEndPoint,headers,params)
        else:
            properties_info = self._prdHttpCaller.getResult(listPropertiesEndPoint,headers)
        return properties_info

    def getProvisionStatus(self,status_filter=None):
        getProvisionStatusEndPoint = '/chinacdn/v1/current-provision-states'
        headers = {"Accept": "application/vnd.akamai.chinacdn.provision-states.v1+json"}
        if status_filter:
            if status_filter in ['WHITELISTED','DEPROVISIONED','PROVISIONED']:
                params = {}
                params["provisionState"] = status_filter
            else:
                error_json = {"Status":"Invalid Filter"}
                return error_json

            if self.accountSwitchKey:
                params['accountSwitchKey'] = self.accountSwitchKey
            properties_info = self._prdHttpCaller.getResult(getProvisionStatusEndPoint,headers,params)

        else:
            if self.accountSwitchKey:
                params = {'accountSwitchKey':self.accountSwitchKey}
                properties_info = self._prdHttpCaller.getResult(getProvisionStatusEndPoint,headers,params)
            else:
                properties_info = self._prdHttpCaller.getResult(getProvisionStatusEndPoint,headers)

        return properties_info

    def createPropertyHostname(self,hostname,icpNumberId,serviceCategory,groupId):
        createPropertiesEndPoint = '/chinacdn/v1/property-hostnames/' +hostname
        headers = {"Accept": "application/vnd.akamai.chinacdn.property-hostname.v1+json",
                   "Content-Type":"application/vnd.akamai.chinacdn.property-hostname.v1+json"}

        create_body = {}
        create_body['hostname'] = hostname
        create_body['icpNumberId'] = icpNumberId
        create_body['serviceCategory'] = serviceCategory

        jsondata = json.dumps(create_body,sort_keys=False)

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey,
                      'groupId':groupId}
            create_propertyInfo = self._prdHttpCaller.putResult(createPropertiesEndPoint,jsondata,headers,params)
        else:
            params = {'groupId':groupId}
            create_propertyInfo = self._prdHttpCaller.putResult(createPropertiesEndPoint,jsondata,headers,params)
        return create_propertyInfo

    def whiteList(self,hostname):
        whiteListEndPoint = '/chinacdn/v1/property-hostnames/' + hostname + '/provision-state-changes'
        headers = {"Accept": "application/vnd.akamai.chinacdn.provision-state-change.v1+json;charset=UTF-8",
                  "Content-Type":"application/vnd.akamai.chinacdn.provision-state-change.v1+json;charset=UTF-8"}

        whitelist_body = {}
        whitelist_body['hostname'] = hostname
        whitelist_body['targetState'] = "WHITELISTED"
        whitelist_body['sendEmail'] = True

        json_data = json.dumps(whitelist_body,sort_keys=False)
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,version_info = self._prdHttpCaller.postResult(whiteListEndPoint,json_data,headers,params)
        else:
            status,version_info = self._prdHttpCaller.postResult(whiteListEndPoint,json_data,headers)

        return version_info
