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

class AkamaiAppSec():
    def __init__(self,prdHttpCaller,accountSwitchKey=None):
        self._prdHttpCaller = prdHttpCaller
        self.accountSwitchKey = accountSwitchKey
        self.configId = 0
        self.stagingVersion = 0
        self.productionVersion = 0
        self.latestVersion = 0
        self.name = ''
        self.productionHostnames = []
        self._invalidconfig = False
        return None

    def searchHostname(self,hostname):
        try:
            ep = "/appsec/v1/configs"
            params = {}
            if self.accountSwitchKey != None:
                params['accountSwitchKey'] = self.accountSwitchKey
                
            headers = {"accept": "application/json"}
            status,resultJson = self._prdHttpCaller.getResult(ep,params,headers)
            #print(json.dumps(resultJson,indent=2))
            if status == 200:
                for item in resultJson['configurations']:
                    if hostname in item['productionHostnames']:
                       return item['name']
            else:
                return ''
        except Exception as e:
            print('{}:Error fetching the Staging Version of Security Policy'.format(e),file=sys.stderr)
            return ''
        
    def getHostNameCoverage(self):
        try:
            ep = "/appsec/v1/hostname-coverage"
            params = {}
            if self.accountSwitchKey != None:
                params['accountSwitchKey'] = self.accountSwitchKey
                
            headers = {"accept": "application/json"}
            status,resultJson = self._prdHttpCaller.getResult(ep,params,headers)
            #print(json.dumps(resultJson,indent=2))
            if status == 200:
                return resultJson['hostnameCoverage']
            else:
                return []
        except Exception as e:
            print('{}:Error fetching the Staging Version of Security Policy'.format(e),file=sys.stderr)
            return []
        

    def config(self,configName):
        try:
            ep = "/appsec/v1/configs"
            params = {}
            if self.accountSwitchKey != None:
                params['accountSwitchKey'] = self.accountSwitchKey
                
            headers = {"accept": "application/json"}
            status,resultJson = self._prdHttpCaller.getResult(ep,params,headers)
            #print(json.dumps(resultJson,indent=2))
            if status == 200:
                for item in resultJson['configurations']:
                    if item['name'] == configName:
                        self.configId =  item['id']
                        self.name = configName
                        self.latestVersion = item['latestVersion']
                        if 'productionVersion' in item:
                            self.productionVersion = item['productionVersion']
                        else:
                            self.productionVersion = 0
                        if 'stagingVersion' in item:
                            self.stagingVersion = item['stagingVersion']
                        else:
                            self.stagingVersion = 0
                        if 'productionHostnames' in item:
                            self.productionHostnames = item['productionHostnames']
                        else:
                            self.productionHostnames = []
                        self._invalidconfig = True
                        return None
            else:
                return None
        except Exception as e:
            print('{}:Error fetching the Staging Version of Security Policy'.format(e),file=sys.stderr)
            return None
        
    def getStagingVersion(self):
        if self._invalidconfig == False:
            print('No Configuration Found')
            return 0
        return self.stagingVersion 
    
    def getProductionVersion(self):
        if self._invalidconfig == False:
            print('No Configuration Found')
            return 0
        return self.productionVersion 
    
    def getLatestVersion(self):
        if self._invalidconfig == False:
            print('No Configuration Found')
            return 0
        return self.latestVersion 

    def getProductionHostNames(self):
        if self._invalidconfig == False:
            print('No Configuration Found')
            return []
        return self.productionHostnames
    
    def getPolicyId(self,version,policyName):
        try:
            ep = '/appsec/v1/configs/{}/versions/{}/security-policies'.format(self.configId,version)
            params = {}
            if self.accountSwitchKey != None:
                params['accountSwitchKey'] = self.accountSwitchKey
                
            headers = {"accept": "application/json"}
            status,resultJson = self._prdHttpCaller.getResult(ep,params,headers)
            #print(json.dumps(resultJson,indent=2))
            if status == 200:
                for item in resultJson['policies']:
                    if item['policyName'] == policyName:
                       return item['policyId']
            else:
                return 0
        except Exception as e:
            print('{}:Error fetching the Staging Version of Security Policy'.format(e),file=sys.stderr)
            return 0


    def createnewVersion(self,baseVersion):
        try:
            cloneversionEP = '/appsec/v1/configs/{}/versions'.format(self.configId)
            print(cloneversionEP)
            params = {}
            if self.accountSwitchKey != None:
                params['accountSwitchKey'] = self.accountSwitchKey
            
            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }

            payload = {
                "ruleUpdate": True,
                "createFromVersion": baseVersion
            }

            datajson = json.dumps(payload,indent=2)
            #print(datajson)
            #print(params)

            status,cloneConfigJson = self._prdHttpCaller.postResult(cloneversionEP,datajson,params,headers)
            if status == 201:
                newVersion = cloneConfigJson['version']
                print('Successfully created the new version of the App Sec Policy {}'.format(self.configId))
                return newVersion
            else:
                print(status,cloneConfigJson)
                print("Failed to create the new version of the App Sec Policy")
                return 0
        except Exception as e:
            print('{}:Error create the new version of the App Sec Policy'.format(e),file=sys.stderr)
            return 0

    def addHostnamesToConfig(self,version,hostNamesArray):
        try:
            addHostNameEP = '/appsec/v1/configs/{}/versions/{}/selected-hostnames'.format(self.configId,version)
            #print(addHostNameEP)
            params = {}
            if self.accountSwitchKey != None:
                    params['accountSwitchKey'] = self.accountSwitchKey
            
            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }

            hostArrayVal = []
            for hostname in hostNamesArray:
                item = {}
                item['hostname'] = hostname
                hostArrayVal.append(item)

            payload = {
                "hostnameList": hostArrayVal,
                "mode": "append"
            }

            datajson = json.dumps(payload,indent=2)
            #print(datajson)

            status,addHostnamesJson = self._prdHttpCaller.putResult(addHostNameEP,datajson,headers,params)
            if status == 200:
                print('Successfully Added the HostNames')
                return True
            else:
                #print(status,addHostnamesJson)
                print("Failed to add the Hostnames")
                return False
        except Exception as e:
            print('{}:Error adding the Hostnames to Security Policy'.format(e),file=sys.stderr)
            return False

    def activateStaging(self,version,emailArray):
        try:
            activateEP = '/appsec/v1/activations'
            params = {}
            if self.accountSwitchKey != None:
                params['accountSwitchKey'] = self.accountSwitchKey

            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }

            payload = {
                "activationConfigs": [
                    {
                        "configId": self.configId,
                        "configVersion": version
                    }
                ],
                "notificationEmails": emailArray,
                "network": "STAGING",
                "note": "Activatiion",
                "action":"ACTIVATE"
            }

            datajson = json.dumps(payload,indent=2)

            status,activationJson = self._prdHttpCaller.postResult(activateEP,datajson,params,headers)
            if status in [202,200]:
                print('Successfully activated to staging')
                return True
            else:
                print(status)
                print("Failed to activate App Sec Policy")
                return False
        except Exception as e:
            print('{}:Error activating the config'.format(e),file=sys.stderr)
            return False

    def createSecurityPolicy(self,version,securityPolicyName,policyPrefix=None):
        import string
        try:
            createSPEP = '/appsec/v1/configs/{}/versions/{}/security-policies'.format(self.configId,version)
            params = {}
            if self.accountSwitchKey != None:
                params['accountSwitchKey'] = self.accountSwitchKey
            
            
            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }

            if policyPrefix == None:
                letters = string.ascii_letters
                policyPrefix = "".join(random.sample(letters,3))

            payload = {
                "policyName": securityPolicyName,
                "policyPrefix": policyPrefix
            }

            datajson = json.dumps(payload,indent=2)

            status,createAppSecPolicyJson = self._prdHttpCaller.postResult(createSPEP,datajson,params,headers)
            if status == 200:
                #print(createEnrollmentJson)
                policyId = createAppSecPolicyJson['policyId']
                print('Successfully created the App Sec Policy {} and  Id is {}'.format(securityPolicyName,policyId))
                return policyId
            else:
                print(status)
                print("Failed to create the App Sec Policy")
                return 0
        except Exception as e:
            print('{}:Error create the App Sec Policy'.format(e),file=sys.stderr)
            return 0

    def addMatchTarget(self,version,policyName,hostNamesArray):
        policyId = self.getPolicyId(version,policyName)
        try:
            addHostNameEP = '/appsec/v1/configs/{}/versions/{}/match-targets'.format(self.configId,version)
            #print(addHostNameEP)
            params = {}
            if self.accountSwitchKey != None:
                    params['accountSwitchKey'] = self.accountSwitchKey
            
            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }

            payload = {
                "securityPolicy" : {
                    "policyId" : policyId
                },
                "hostnames": hostNamesArray,
                "type": "website",
                "filePaths": ["/*"]
            }
            

            datajson = json.dumps(payload,indent=2)
            #print(datajson)

            status,addHostnamesJson = self._prdHttpCaller.postResult(addHostNameEP,datajson,params,headers)
            if status == 201:
                print('Successfully Added the HostNames')
                return True
            else:
                #print(status,addHostnamesJson)
                print("Failed to add the Hostnames")
                return False
        except Exception as e:
            print('{}:Error adding the Hostnames to Security Policy'.format(e),file=sys.stderr)
            return False


    def addHostnameSecurityPolicy(self,version,policyName,hostNamesArray):
        policyId = self.getPolicyId(version,policyName)
        print(policyId)
        try:
            addHostNameEP = '/appsec/v1/configs/{}/versions/{}/security-policies/{}/selected-hostnames'.format(self.configId,version,policyId)
            print(addHostNameEP)
            params = {}
            if self.accountSwitchKey != None:
                    params['accountSwitchKey'] = self.accountSwitchKey
            
            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }

            hostArrayVal = []
            for hostname in hostNamesArray:
                item = {}
                item['hostname'] = hostname
                hostArrayVal.append(item)

            payload = {
                "hostnameList": hostArrayVal,
                "mode": "append"
            }

            datajson = json.dumps(payload,indent=2)
            #print(datajson)

            status,addHostnamesJson = self._prdHttpCaller.putResult(addHostNameEP,datajson,headers,params)
            if status == 200:
                print('Successfully Added the HostNames')
                return True
            else:
                print(status,addHostnamesJson)
                print("Failed to add the Hostnames")
                return False
        except Exception as e:
            print('{}:Error adding the Hostnames to Security Policy'.format(e),file=sys.stderr)
            return False


    def createConfig(self,configName,contractId,groupId,hostNameArray):
        try:
            createConfigEP = '/appsec/v1/configs'
            params = {}
            if self.accountSwitchKey != None:
                    params['accountSwitchKey'] = self.accountSwitchKey
            
            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }
            payload = {
                "name": configName,
                "description": "Test",
                "contractId": contractId,
                "groupId": groupId,
                "hostnames": hostNameArray
            }
            datajson = json.dumps(payload,indent=2)

            status,createAppSecConfigJson = self._prdHttpCaller.postResult(createConfigEP,datajson,headers,params)
            if status == 201:
                #print(createEnrollmentJson)
                configId = createAppSecConfigJson['configId']
                print('Successfully created the App Sec Config and Config Id is {}'.format(configId))
                return configId
            else:
                print(status)
                print("Failed to create the App Sec Config")
                return 0
        except Exception as e:
            print('{}:Error create the App Sec Config'.format(e),file=sys.stderr)
            return 0

    def getCookieSetting(self,version):
        try:
            ep = '/appsec/v1/configs/{}/versions/{}/advanced-settings/cookie-settings'.format(self.configId,version)
            params = {}
            if self.accountSwitchKey != None:
                params['accountSwitchKey'] = self.accountSwitchKey
                
            headers = {"accept": "application/json"}
            status,resultJson = self._prdHttpCaller.getResult(ep,params,headers)
            if status == 200:
                return True,resultJson
            else:
                return False,''
        except Exception as e:
            print('{}:Error fetching the Staging Version of Security Policy'.format(e),file=sys.stderr)
            return False,''
    
    def getEvasivePathMatchSetting(self,version):
        try:
            ep = '/appsec/v1/configs/{}/versions/{}/advanced-settings/evasive-path-match'.format(self.configId,version)
            params = {}
            if self.accountSwitchKey != None:
                params['accountSwitchKey'] = self.accountSwitchKey
                
            headers = {"accept": "application/json"}
            status,resultJson = self._prdHttpCaller.getResult(ep,params,headers)
            if status == 200:
                return True,resultJson
            else:
                return False,''
        except Exception as e:
            print('{}:Error fetching the Staging Version of Security Policy'.format(e),file=sys.stderr)
            return False,''
        
    def getHTTPLoggingSetting(self,version):
        try:
            ep = '/appsec/v1/configs/{}/versions/{}/advanced-settings/logging'.format(self.configId,version)
            params = {}
            if self.accountSwitchKey != None:
                params['accountSwitchKey'] = self.accountSwitchKey
                
            headers = {"accept": "application/json"}
            status,resultJson = self._prdHttpCaller.getResult(ep,params,headers)
            if status == 200:
                return True,resultJson
            else:
                return False,''
        except Exception as e:
            print('{}:Error fetching the Staging Version of Security Policy'.format(e),file=sys.stderr)
            return False,''

    def getAttackPayloadLoggingSetting(self,version):
        try:
            ep = '/appsec/v1/configs/{}/versions/{}/advanced-settings/logging/attack-payload'.format(self.configId,version)
            params = {}
            if self.accountSwitchKey != None:
                params['accountSwitchKey'] = self.accountSwitchKey
                
            headers = {"accept": "application/json"}
            status,resultJson = self._prdHttpCaller.getResult(ep,params,headers)
            if status == 200:
                return True,resultJson
            else:
                return False,''
        except Exception as e:
            print('{}:Error fetching the Staging Version of Security Policy'.format(e),file=sys.stderr)
            return False,''

    






