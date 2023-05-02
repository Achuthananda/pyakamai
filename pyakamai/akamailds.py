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
import os
import requests
import logging
import json
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from .http_calls import EdgeGridHttpCaller

class AkamaiLDS():
    def __init__(self,prdHttpCaller,accountSwitchKey=None):
        self._prdHttpCaller = prdHttpCaller
        self.accountSwitchKey = accountSwitchKey
        return None

    def listConfigs(self,logSourceType):
        """ Get list of LDS Configs"""
        ep = '/lds-api/v3/log-sources/{}'.format(logSourceType)
        if self.accountSwitchKey:
            params = {'accountSwitchKey': self.accountSwitchKey}
            status,response = self._prdHttpCaller.getResult(ep, params)
        else:
            status,response = self._prdHttpCaller.getResult(ep)
        
        if status == 200:
            return response
        else:
            return {}

    def listLogConfigurations(self,logSourceType):
        """ Get list of LDS Configs"""
        ep = '/lds-api/v3/log-sources/{}/log-configurations'.format(logSourceType)
        if self.accountSwitchKey:
            params = {'accountSwitchKey': self.accountSwitchKey}
            status,response = self._prdHttpCaller.getResult(ep, params)
        else:
            status,response = self._prdHttpCaller.getResult(ep)

        if status == 200:
            return response
        else:
            return {}

    def listlogRedeliveries(self):
        """ Get list of LDS Log Redeliveries"""
        ep = '/lds-api/v3/log-redeliveries'
        if self.accountSwitchKey:
            params = {'accountSwitchKey': self.accountSwitchKey}
            status,response = self._prdHttpCaller.getResult(ep, params)
        else:
            status,response = self._prdHttpCaller.getResult(ep)

        if status == 200:
            return response
        else:
            return {}

