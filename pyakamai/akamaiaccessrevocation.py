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

class AkamaiAccessRevocation():
    def __init__(self,prdHttpCaller,accountSwitchKey=None):
        self._prdHttpCaller = prdHttpCaller
        self.accountSwitchKey = accountSwitchKey
        return None

    def getRevocationLists(self):
        ep = '/taas/v2/revocation-lists'
        params = {}
        if self.accountSwitchKey:
            params['accountSwitchKey']= self.accountSwitchKey
            status,revocationList = self._prdHttpCaller.getResult(ep,params=params)
        else:
            status,revocationList = self._prdHttpCaller.getResult(ep)
        return status,revocationList
    
    def listIdentifiers(self,revocationListId):
        ep = '/taas/v2/revocation-lists/{}/identifiers'.format(revocationListId)
        params = {}
        if self.accountSwitchKey:
            params['accountSwitchKey']= self.accountSwitchKey
            status,identifiers = self._prdHttpCaller.getFileResult(ep,params=params)
        else:
            status,identifiers = self._prdHttpCaller.getFileResult(ep)
        return status,identifiers


    def createRevocationList(self,contractId,name):
        ep = '/taas/v2/revocation-lists'
        headers = {'Content-Type': 'application/json'}

        record ={}
        record['contractId'] = contractId
        record['name'] = name
        
        recordjson = json.dumps(record)        

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,result = self._prdHttpCaller.postResult(ep,recordjson,headers=headers,params=params)
        else:
            status,result = self._prdHttpCaller.postResult(ep,recordjson,headers=headers)

        if status in [202]:
            print("Successfully created new Revocation List")
            return True
        else:
            print("Failed to create new Policy with new ruleset")
            print(json.dumps(result,indent=2))
            return False
        
    def deleteRevocationList(self,id):
        ep = '/taas/v2/revocation-lists/{}'.format(id)
        params = {}
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,result = self._prdHttpCaller.deleteResult(ep,params=params)
        else:
            status,result = self._prdHttpCaller.deleteResult(ep)

        if status == 204:
            return True
        else:
            return False 
        
    def revokeToken(self,revocationListId,revocationTTL,tokenIdArray):
        ep = '/taas/v2/revocation-lists/{}/identifiers/add'.format(revocationListId)
        headers = {'Content-Type': 'application/json'}

        record =[]
        for tokenId in tokenIdArray:
            item = {}
            item['durationSeconds'] = revocationTTL
            item['id'] = tokenId
            record.append(item)
        
        recordjson = json.dumps(record)        

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,result = self._prdHttpCaller.postResult(ep,recordjson,headers=headers,params=params)
        else:
            status,result = self._prdHttpCaller.postResult(ep,recordjson,headers=headers)

        if status in [202]:
            print("Successfully Added to theRevocation List")
            return True
        else:
            print("Failed to Add to theRevocation List")
            print(json.dumps(result,indent=2))
            return False
        

    def unRevokeToken(self,revocationListId,tokenIdArray):
        if len(tokenIdArray) == 0:
            print("Add 1 or more tokens in the array and call the API")
            return False
        
        ep = '/taas/v2/revocation-lists/{}/identifiers/remove'.format(revocationListId)
        headers = {'Content-Type': 'application/json'}

        record =[]
        for x in tokenIdArray:
            record.append(x)
        
        recordjson = json.dumps(record)        

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,result = self._prdHttpCaller.postResult(ep,recordjson,headers=headers,params=params)
        else:
            status,result = self._prdHttpCaller.postResult(ep,recordjson,headers=headers)

        if status in [202]:
            print("Successfully Unrevoked the token from theRevocation List")
            return True
        else:
            print("Failed to unreove from theRevocation List")
            print(json.dumps(result,indent=2))
            return False





    