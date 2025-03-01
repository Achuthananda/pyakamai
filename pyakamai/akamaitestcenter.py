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


class AkamaiTestCenter():
    def __init__(self,prdHttpCaller,accountSwitchKey=None):
        self._prdHttpCaller = prdHttpCaller
        self.accountSwitchKey = accountSwitchKey
        return None
    
    def createTestSuite(self,testSuiteName):
        ep = 'test-management/v3/functional/test-suites'
        
        data = {}
        data['isLocked'] = False
        data['isStateful'] = True
        data['testSuiteDescription'] = testSuiteName
        data['testSuiteName'] = testSuiteName

        json_data = json.dumps(data)

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            version_info = self._prdHttpCaller.postResult(ep,json_data,params)
        else:
            version_info = self._prdHttpCaller.postResult(ep,json_data)

        print(version_info)
        if version_info[0] == 201:
            return version_info[1]['testSuiteId']
        else:
            return 0

    
    def listTestSuites(self):
        ep = '/test-management/v3/functional/test-suites'
        params = {}
        if self.accountSwitchKey:
            params['accountSwitchKey']= self.accountSwitchKey
            status,testsuiteList = self._prdHttpCaller.getResult(ep,params=params)
        else:
            status,testsuiteList = self._prdHttpCaller.getResult(ep)
        if status == 200:
            return testsuiteList
        else:
            return {}
        
    def getTestSuite(self,testSuiteId):
        ep = '/test-management/v3/functional/test-suites/{testSuiteId}'.format(testSuiteId=testSuiteId)
        params = {}
        if self.accountSwitchKey:
            params['accountSwitchKey']= self.accountSwitchKey
            status,testsuite = self._prdHttpCaller.getResult(ep,params=params)
        else:
            status,testsuite = self._prdHttpCaller.getResult(ep)
        if status == 200:
            return testsuite
        else:
            return {}
        
    def listTestCases(self,testSuiteId):
        ep = '/test-management/v3/functional/test-suites/{testSuiteId}/test-cases'.format(testSuiteId=testSuiteId)
        params = {}
        if self.accountSwitchKey:
            params['accountSwitchKey']= self.accountSwitchKey
            status,testcases = self._prdHttpCaller.getResult(ep,params=params)
        else:
            status,testcases = self._prdHttpCaller.getResult(ep)
        if status == 200:
            return testcases
        else:
            return {}
        
    def listTestCenterCoditions(self):
        ep = '/test-management/v3/functional/test-catalog/conditions'
        params = {}
        if self.accountSwitchKey:
            params['accountSwitchKey']= self.accountSwitchKey
            status,testconditions = self._prdHttpCaller.getResult(ep,params=params)
        else:
            status,testconditions = self._prdHttpCaller.getResult(ep)
        if status == 200:
            return testconditions
        else:
            return {}
        
    def listTestCatalogTemplate(self):
        ep = '/test-management/v3/functional/test-catalog/template'
        params = {}
        if self.accountSwitchKey:
            params['accountSwitchKey']= self.accountSwitchKey
            status,testcatalogue = self._prdHttpCaller.getResult(ep,params=params)
        else:
            status,testcatalogue = self._prdHttpCaller.getResult(ep)
        if status == 200:
            return testcatalogue
        else:
            return {}

    def AddTestCasetoSuite(self,testSuiteId,testCaseObj):
        activationEndPoint = '/test-management/v3/functional/test-suites/{testSuiteId}/test-cases'.format(testSuiteId=testSuiteId)

        json_data = json.dumps(testCaseObj)

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            version_info = self._prdHttpCaller.postResult(activationEndPoint,json_data,params)
        else:
            version_info = self._prdHttpCaller.postResult(activationEndPoint,json_data)

        print(version_info)
        if version_info[0] == 201:
            return True
        else:
            return False




