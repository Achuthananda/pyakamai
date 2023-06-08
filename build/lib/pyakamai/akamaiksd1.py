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
        return None


    def getAppSecConfigStagingVersion(self,ecurityConfigId,accountSwitchKey):
        try:
            getVersionEP = "/appsec/v1/configs/{}/versions?page=1&pageSize=25&detail=true".format(securityConfigId)
            params = {}
            if self.accountSwitchKey != None:
                params['accountSwitchKey'] = self.accountSwitchKey
                
            headers = {"accept": "application/json"}
            status,versionDetailjson = self._prdHttpCaller.getResult(getVersionEP,headers,params)
            if status == 200:
                if 'stagingActiveVersion' in versionDetailjson:
                    return versionDetailjson['stagingActiveVersion']
                else:
                    return 0
            else:
                print("The status of the get staging version is {}".format(status))
                return 0
        except Exception as e:
            print('{}:Error fetching the Staging Version of Security Policy'.format(e),file=sys.stderr)
            return 0
        

    def getAppSecConfigProductionVersion(securityConfigId,accountSwitchKey):
        try:
            getVersionEP = "/appsec/v1/configs/{}/versions?page=1&pageSize=25&detail=false".format(securityConfigId)
            params = {}
            if self.accountSwitchKey != None:
                params['accountSwitchKey'] = self.accountSwitchKey
                
            headers = {"accept": "application/json"}
            status,versionDetailjson = self._prdHttpCaller.getResult(getVersionEP,headers,params)
            if status == 200:
                if 'productionActiveVersion' in versionDetailjson:
                    return versionDetailjson['productionActiveVersion']
                else:
                    return 0
            else:
                print("The status of the get production version is {}".format(status))
                return 0
        except Exception as e:
            print('{}:Error fetching the Production Version of Security Policy'.format(e),file=sys.stderr)
            return 0


    def getAppSecConfiglatestVersion(self,securityConfigId,accountSwitchKey):
        try:
            getVersionEP = "/appsec/v1/configs/{}/versions?page=1&pageSize=25&detail=false".format(securityConfigId)
            params = {}
            if self.accountSwitchKey != None:
                params['accountSwitchKey'] = self.accountSwitchKey
                
            headers = {"accept": "application/json"}
            status,versionDetailjson = self._prdHttpCaller.getResult(getVersionEP,headers,params)
            if status == 200:
                if 'lastCreatedVersion' in versionDetailjson:
                    return versionDetailjson['lastCreatedVersion']
                else:
                    return 0
            else:
                print("The status of the get latest version is {}".format(status))
                return 0
        except Exception as e:
            print('{}:Error fetching the latest Version of Security Policy'.format(e),file=sys.stderr)
            return 0


    def createNewSecConfigVersion(securityConfigId,accountSwitchKey):
        try:
            stagingVersion = self.getAppSecConfigStagingVersion(securityConfigId,self._prdHttpCaller,accountSwitchKey)
            productionVersion = self.getAppSecConfigProductionVersion(securityConfigId,self._prdHttpCaller,accountSwitchKey)
            latestVersion = self.getAppSecConfiglatestVersion(securityConfigId,self._prdHttpCaller,accountSwitchKey)
            version = latestVersion
            if productionVersion > 0:
                version = productionVersion
            elif stagingVersion > 0:
                version = stagingVersion
    
            cloneversionEP = '/appsec/v1/configs/{}/versions'.format(securityConfigId)
            params = {}
            if self.accountSwitchKey != None:
                params['accountSwitchKey'] = self.accountSwitchKey
            
            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }

            payload = {
                "ruleUpdate": True,
                "createFromVersion": version
            }

            datajson = json.dumps(payload,indent=2)

            status,cloneConfigJson = self._prdHttpCaller.postResult(cloneversionEP,datajson,headers,params)
            if status == 201:
                newVersion = cloneConfigJson['version']
                print('Successfully created the new version of the App Sec Policy {}'.format(securityConfigId))
                return newVersion
            else:
                print(status)
                print("Failed to create the new version of the App Sec Policy")
                return 0
        except Exception as e:
            print('{}:Error create the new version of the App Sec Policy'.format(e),file=sys.stderr)
            return 0

    def activateStagingAppSecConfig(self,securityConfigId,version,accountSwitchKey):
        try:
            activateEP = '/appsec/v1/activations'
            params = {}
            if self.accountSwitchKey != None:
                params['accountSwitchKey'] = self.accountSwitchKey

            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }

            emailList = getEmailNotificationList()
            emailArray = emailList[0].split(',')

            payload = {
                "activationConfigs": [
                    {
                        "configId": securityConfigId,
                        "configVersion": version
                    }
                ],
                "notificationEmails": emailArray,
                "network": "STAGING",
                "note": "Activatiion",
                "action":"ACTIVATE"
            }

            datajson = json.dumps(payload,indent=2)

            status,activationJson = self._prdHttpCaller.postResult(activateEP,datajson,headers,params)
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



    def addHostnametoSecConfig(self,securityConfigId,version,hostNamesArray,accountSwitchKey):
        try:
            addHostNameEP = '/appsec/v1/configs/{}/versions/{}/selected-hostnames'.format(securityConfigId,version)
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
            print(datajson)

            status,addHostnamesJson = self._prdHttpCaller.putResult(addHostNameEP,datajson,headers,params)
            if status == 200:
                print('Successfully Added the HostNames')
                return True
            else:
                print(status)
                print("Failed to add the Hostnames")
                return False
        except Exception as e:
            print('{}:Error adding the Hostnames to Security Policy'.format(e),file=sys.stderr)
            return False


    def createSecurityPolicy(self,configId,version,securityPolicyName,policyPrefix=None):
        try:
            createSPEP = '/appsec/v1/configs/{}/versions/{}/security-policies'.format(configId,version)
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

            status,createAppSecPolicyJson = self._prdHttpCaller.postResult(createSPEP,datajson,headers,params)
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

        return configId


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

        return configId

    def createSecurityPolicy(self,configId,version,securityPolicyName):
        try:
            createSPEP = '/appsec/v1/configs/{}/versions/{}/security-policies'.format(configId,version)
            params = {}
            if self.accountSwitchKey != None:
                params['accountSwitchKey'] = self.accountSwitchKey
            
            
            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }

            letters = string.ascii_letters
            policyPrefix = "".join(random.sample(letters,3))

            payload = {
                "policyName": securityPolicyName,
                "policyPrefix": policyPrefix
            }

            datajson = json.dumps(payload,indent=2)

            status,createAppSecPolicyJson = self._prdHttpCaller.postResult(createSPEP,datajson,headers,params)
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

        return configId


    def createAppSecConfig(self,configName,contractId,groupId,securityPolicyName,hostNameArray):
        try:
            configId = self.createConfig(configName,contractId,groupId,hostNameArray)
            if configId != 0 :
                policyId = createSecurityPolicy(accountSwitchKey,configId,1,securityPolicyName)
                if policyId != 0:
                    print("Config {} and Security Policy {} has been created".format(configName,securityPolicyName))
                else:
                    print("Config {} and Security Policy {} creation Failed".format(configName,securityPolicyName))
            else:
                print("Security Config {} Creation Failed".format(configName))

            return configId,policyId

        except Exception as e:
            print('{}:Error Creating the Enrollment'.format(e),file=sys.stderr)
            exit(1)
