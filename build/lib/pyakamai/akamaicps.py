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


class AkamaiCPS():
    def __init__(self,prdHttpCaller,accountSwitchKey=None):
        self._prdHttpCaller = prdHttpCaller
        self.accountSwitchKey = accountSwitchKey
        return None

    def listEnrollments(self):
        getEnrollmentEP = '/cps/v2/enrollments'
        headers = {'Accept': 'application/vnd.akamai.cps.enrollments.v10+json'}

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,enrollmentsList = self._prdHttpCaller.getResult(getEnrollmentEP,headers=headers,params=params)
        else:
            status,enrollmentsList = self._prdHttpCaller.getResult(getEnrollmentEP,headers=headers)
        
        if status == 200:
            return enrollmentsList
        else:
          return {}
        
    def getEnrollment(self,enrollmentId):
        getEnrollmentEP = '/cps/v2/enrollments/{}'.format(str(enrollmentId))
        headers = {"Accept": "application/vnd.akamai.cps.enrollment.v10+json"}

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,enrollmentInfo = self._prdHttpCaller.getResult(getEnrollmentEP,headers=headers,params=params)
        else:
            status,enrollmentInfo = self._prdHttpCaller.getResult(getEnrollmentEP,headers=headers)
        
        if status == 200:
            return enrollmentInfo
        else:
          return {}

        
    def listDeployments(self,enrollmentId):
        getdeploymentEP = '/cps/v2/enrollments/{}/deployments'.format(enrollmentId)
        headers = {'Accept': 'application/vnd.akamai.cps.deployment.v7+json"'}

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            print("Hello")
            status,deploymentList = self._prdHttpCaller.getResult(getdeploymentEP,headers=headers,params=params)
        else:
            status,deploymentList = self._prdHttpCaller.getResult(getdeploymentEP,headers=headers)
        
        if status == 200:
            return deploymentList
        else:
          print(status,deploymentList)
          return {}


    def createEnrollment(self,contract,enrollmentfile):
        createEnrollmentEP = '/cps/v2/enrollments'

        headers = {}
        headers['Content-Type'] = 'application/vnd.akamai.cps.enrollment.v10+json'
        headers['Accept'] = 'application/vnd.akamai.cps.enrollment-status.v1+json'

        params = {}
        params['Contract'] = contract

        fp = open(enrollmentfile,'r')
        data = json.load(fp)

        datajson = json.dumps(data)
        if self.accountSwitchKey:
            params['accountSwitchKey'] = self.accountSwitchKey

        status,resultjson = self._prdHttpCaller.postResult(createEnrollmentEP,datajson,headers=headers,params=params)
        if status == 202:
            return resultjson
        else:
            return {}


