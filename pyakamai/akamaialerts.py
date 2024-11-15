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

class AkamaiAlerts():
    def __init__(self,prdHttpCaller,accountSwitchKey=None):
        self._prdHttpCaller = prdHttpCaller
        self.accountSwitchKey = accountSwitchKey
        return None

    def listTemplates(self):
        """ List the Alert Templates associated with the account """
        endpoint = '/alerts/v2/alert-templates'
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,templateID = self._prdHttpCaller.getResult(endpoint,params)
        else:
            status,templateID = self._prdHttpCaller.getResult(endpoint)
        return(templateID)


    def getTemplate(self,templateId):
        """ Get the Template ID """
        endpoint = '/alerts/v2/alert-templates/{templateId}'.format(templateId=templateId)
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,templatelist = self._prdHttpCaller.getResult(endpoint,params)
        else:
            status,templatelist = self._prdHttpCaller.getResult(endpoint)
        return(templatelist)
    

    def createAlert(self,jsondata):
        #print(self.provisionStatus)
        endpoint  = '/alerts/v2/alert-definitions'
        if self.accountSwitchKey:
            params = {}
            params["accountSwitchKey"] = self.accountSwitchKey
            status,updateStreamJson = self._prdHttpCaller.postResult(endpoint,jsondata,headers=None,params=params)
            #print(status,updateStreamJson)
            return status,updateStreamJson
        else:
            status,updateStreamJson = self._prdHttpCaller.postResult(endpoint,jsondata,headers=None)
            #print(status,updateStreamJson)
            return status,updateStreamJson




#https://techdocs.akamai.com/case-mgmt/pdfs/case-mgmt-api-v2-deprecated.pdf
