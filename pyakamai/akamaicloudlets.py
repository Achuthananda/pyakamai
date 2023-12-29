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

class AkamaiCloudlets():
    def __init__(self,prdHttpCaller,accountSwitchKey=None):
        self._prdHttpCaller = prdHttpCaller
        self.accountSwitchKey = accountSwitchKey
        return None

    def listPolicies(self):
        ep = '/cloudlets/api/v2/policies'
        params = {}
        if self.accountSwitchKey:
            params['accountSwitchKey']= self.accountSwitchKey
            status,policyList = self._prdHttpCaller.getResult(ep,params=params)
        else:
            status,policyList = self._prdHttpCaller.getResult(ep)
        return status,policyList
    
    def getPolicyVersion(self,policyId,version):
        ep = '/cloudlets/api/v2/policies/{}/versions/{}'.format(policyId,version)
        params = {}
        if self.accountSwitchKey:
            params['accountSwitchKey']= self.accountSwitchKey
            status,policyDetail = self._prdHttpCaller.getResult(ep,params=params)
        else:
            status,policyDetail = self._prdHttpCaller.getResult(ep)
        return status,policyDetail

    def updatePolicyVersion(self,policyId,version,description,matchRulesDict):
        ep = '/cloudlets/api/v2/policies/{}/versions/{}'.format(policyId,version)
        headers = {'Content-Type': 'application/json'}

        record ={}
        record['description'] = description
        record['matchRules'] = matchRulesDict
        
        recordjson = json.dumps(record)
        #print(recordjson)
        

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,result = self._prdHttpCaller.putResult(ep,recordjson,headers=headers,params=params)
        else:
            status,result = self._prdHttpCaller.putResult(ep,recordjson,headers=headers)

        if status in [201,200]:
            print("Successfully update the Policy with new ruleset")
            return True
        else:
            print("Failed to update the Policy with new ruleset")
            print(json.dumps(result,indent=2))
            return False
        
    def createPolicyVersion(self,policyId,description,matchRulesDict):
        ep = '/cloudlets/api/v2/policies/{}/versions'.format(policyId)
        headers = {'Content-Type': 'application/json'}

        record ={}
        record['description'] = description
        record['matchRules'] = matchRulesDict
        
        recordjson = json.dumps(record)
        #print(recordjson)
        

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,result = self._prdHttpCaller.postResult(ep,recordjson,headers=headers,params=params)
        else:
            status,result = self._prdHttpCaller.postResult(ep,recordjson,headers=headers)

        if status in [201,200]:
            print("Successfully created new Policy with new ruleset")
            return True,result['version']
        else:
            print("Failed to create new Policy with new ruleset")
            print(json.dumps(result,indent=2))
            return False,0
        
    def activatePolicyVersion(self,policyId,version,network):
        ep = '/cloudlets/api/v2/policies/{}/versions/{}/activations'.format(policyId,version)
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        record ={}
        record['network'] = network
        
        recordjson = json.dumps(record)
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,result = self._prdHttpCaller.postResult(ep,recordjson,headers=headers,params=params)
        else:
            status,result = self._prdHttpCaller.postResult(ep,recordjson,headers=headers)

        if status in [201,200]:
            print("Successfully activated the policy")
            return True
        else:
            print("Failed to activate the policy")
            print(json.dumps(result,indent=2))
            return False




    