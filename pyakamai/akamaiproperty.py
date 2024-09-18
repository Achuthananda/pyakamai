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
import time
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from .http_calls import EdgeGridHttpCaller
if sys.version_info[0] >= 3:
    # python3
    from urllib import parse
else:
    # python2.7
    import urlparse as parse

logger = logging.getLogger(__name__)


section = 'default'
debug = False
verbose = False


class AkamaiProperty():
    def __init__(self,prdHttpCaller,accountSwitchKey=None):
        self.name = ''
        self.contractId = ''
        self.groupId = ''
        self.propertyId = ''
        self.stagingVersion = 0
        self.productionVersion = 0
        self.lastupdatedDate = ''
        self.accountSwitchKey = ''
        self._edgerc = ''
        self._prdHttpCaller = ''
        self._session = ''
        self._baseurl_prd = ''
        self._host = ''
        self._invalidconfig = False
        self.latestVersion = 0
        self.assetId = ''

        self._criteria_stack = []
        self._condition_json = []
        self._condition_json1 = []

        self._prdHttpCaller = prdHttpCaller
        self.accountSwitchKey = accountSwitchKey
        return None
    
    def config(self,name):
        self.name = name
        data = {}
        data['propertyName'] = name
        json_data = json.dumps(data)
        propertyInfoEndPoint = "/papi/v1/search/find-by-value"
        #print(json_data)
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            #print(params)
            status,prop_info = self._prdHttpCaller.postResult(propertyInfoEndPoint,json_data,params)
        else:
            status,prop_info = self._prdHttpCaller.postResult(propertyInfoEndPoint,json_data)
        #print(status,prop_info)
        if prop_info:
            if 'versions' in prop_info and 'items' in prop_info['versions'] and len(prop_info['versions']['items']) !=0:
                self.propertyId = prop_info['versions']['items'][0]['propertyId']
                self.contractId = prop_info['versions']['items'][0]['contractId']
                self.groupId = prop_info['versions']['items'][0]['groupId']

                for item in prop_info['versions']['items']:
                    if item["productionStatus"] == "ACTIVE":
                        self.productionVersion = item["propertyVersion"]
                        self.lastupdatedDate  = item['updatedDate']
                    if item["stagingStatus"] == "ACTIVE":
                        self.stagingVersion = item["propertyVersion"]

                propertyVersionEndPoint = "/papi/v1/properties/{}".format(self.propertyId)
                newparams = {}
                if self.accountSwitchKey:
                    newparams["accountSwitchKey"] = self.accountSwitchKey

                if newparams:
                    status,getpropInfoJson = self._prdHttpCaller.getResult(propertyVersionEndPoint,params)
                else:
                    status,getpropInfoJson = self._prdHttpCaller.getResult(propertyVersionEndPoint)
                
                if getpropInfoJson :
                    if 'latestVersion' in getpropInfoJson['properties']['items'][0].keys():
                        self.latestVersion = getpropInfoJson['properties']['items'][0]['latestVersion']
                    self.assetId = getpropInfoJson['properties']['items'][0]['assetId']

            else:
                print("No Configuration with {} Found".format(name))
                self._invalidconfig = True
        return None

    def search(self,hostName):
        self.name = hostName
        data = {}
        data['hostname'] = hostName
        json_data = json.dumps(data)
        propertyInfoEndPoint = "/papi/v1/search/find-by-value"
        #print(json_data)
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            print(params)
            status,prop_info = self._prdHttpCaller.postResult(propertyInfoEndPoint,json_data,params)
        else:
            status,prop_info = self._prdHttpCaller.postResult(propertyInfoEndPoint,json_data)
        #print(status,prop_info)
        if prop_info:
            if 'versions' in prop_info and 'items' in prop_info['versions'] and len(prop_info['versions']['items']) !=0:
                return prop_info['versions']['items'][0]['propertyName']
            else:
                print("No Configuration with {} Found".format(hostName))
                return ""
        return ""
    

    def printPropertyInfo(self):
        if self._invalidconfig == True:
            print("No Configuration Found")
            return
        print("Property Name:",self.name)
        print("Property Id:",self.propertyId)
        print("Contract Id:",self.contractId)
        print("Group Id:",self.groupId)
        print("Active Staging Version:",self.stagingVersion)
        print("Active Production Version:",self.productionVersion)
        print("Latest Version:",self.latestVersion)
        print('*'*80)

    def getStagingVersion(self):
        if self._invalidconfig == True:
            print("No Configuration Found")
            return -1
        return self.stagingVersion

    def getProductionVersion(self):
        if self._invalidconfig == True:
            print("No Configuration Found")
            return -1
        return self.productionVersion

    def getRuleTree(self,version):
        if self._invalidconfig == True:
            print("No Configuration Found")
            return []
        ruleTreeEndPoint = "/papi/v1/properties/" + self.propertyId + "/versions/" +str(version) + "/rules"
        params =    {
                    'validateRules': 'false',
                    'validateMode': 'false',
                    'dryRun': 'true'
                    }
        if self.accountSwitchKey:
            params["accountSwitchKey"] = self.accountSwitchKey

        status,ruleTree = self._prdHttpCaller.getResult(ruleTreeEndPoint,params)
        return ruleTree

    def updateRuleTree(self,version,jsondata):
        if self._invalidconfig == True:
            print("No Configuration Found")
            return False
        updateRuleTreeEndPoint = '/papi/v1/properties/' + self.propertyId + '/versions/' + str(version) + '/rules'
        params =    {
                    'contractId': self.contractId,
                    'groupId': self.groupId
                    }
        if self.accountSwitchKey:
            params["accountSwitchKey"] = self.accountSwitchKey

        status,updateRuleTree = self._prdHttpCaller.putResult(updateRuleTreeEndPoint,jsondata,params=params)
        #print(updateRuleTree)
        if status == 200:
            return True
        else:
            return False

    def getHostNames(self,version):
        if self._invalidconfig == True:
            print("No Configuration Found")
            return []
        getHostNameEndPoint = '/papi/v1/properties/{property_id}/versions/{new_version}/hostnames'.format(property_id=self.propertyId ,new_version=version)
        params = {}
        params["contractId"] =self.contractId
        params["groupId"] = self.groupId

        if self.accountSwitchKey:
            params["accountSwitchKey"] = self.accountSwitchKey

        status,getHostnameJson = self._prdHttpCaller.getResult(getHostNameEndPoint,params)
        hostNameList = []
        if 'hostnames' not in getHostnameJson:
            return []
        for hostname in  getHostnameJson["hostnames"]["items"]:
            hostNameList.append(hostname["cnameFrom"])
        return hostNameList


    def createVersion(self,baseVersion):
        if self._invalidconfig == True:
            print("No Configuration Found")
            return -1
        versionCreateEndPoint = '/papi/v1/properties/' + self.propertyId + '/versions/'

        data = {}
        data['createFromVersion'] = str(baseVersion)
        json_data = json.dumps(data)

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            version_info = self._prdHttpCaller.postResult(versionCreateEndPoint,json_data,params)
        else:
            version_info = self._prdHttpCaller.postResult(versionCreateEndPoint,json_data)

        if version_info[0] == 201:
            import re
            version_link = version_info[1]['versionLink']
            #print(version_link)
            match = re.search(r'\/versions\/(\d+)', version_link)
            if match:
                version_number = match.group(1)
                print(version_number)
                return version_number
            else:
                return 0
            
    def activateStaging(self,version,notes,email_list):
        if self._invalidconfig == True:
            print("No Configuration Found")
            return False
        activationEndPoint = '/papi/v1/properties/' + self.propertyId + '/activations'

        data = {}
        data['propertyVersion'] = int(version)
        data['network'] = 'STAGING'
        data['note'] = notes
        data['acknowledgeAllWarnings'] = True
        data['notifyEmails'] = email_list
        data['fastPush'] = True
        data['useFastFallback'] = False

        json_data = json.dumps(data)

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            version_info = self._prdHttpCaller.postResult(activationEndPoint,json_data,params)
        else:
            version_info = self._prdHttpCaller.postResult(activationEndPoint,json_data)

        if version_info[0] == 201:
            return True
        else:
            return False

    def activateProduction(self,version,notes,email_list,peer_review_email,customer_email):
        if self._invalidconfig == True:
            print("No Configuration Found")
            return False
        activationEndPoint = '/papi/v1/properties/' + self.propertyId + '/activations'

        data = {}
        data['propertyVersion'] = int(version)
        data['network'] = 'PRODUCTION'
        data['note'] = notes
        data['acknowledgeAllWarnings'] = True
        data['notifyEmails'] = email_list
        data['fastPush'] = True
        data['ignoreHttpErrors'] = False
        data['useFastFallback'] = False

        complianceRecord = {}
        complianceRecord['noncomplianceReason'] = "NONE"
        complianceRecord['peerReviewedBy'] = peer_review_email
        complianceRecord['unitTested'] = True
        complianceRecord['customerEmail'] = customer_email
        data['complianceRecord'] = complianceRecord

        json_data = json.dumps(data)

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            version_info = self._prdHttpCaller.postResult(activationEndPoint,json_data,params)
        else:
            version_info = self._prdHttpCaller.postResult(activationEndPoint,json_data)

        if version_info[0] == 201:
            return True
        else:
            return False

    def __parseChildCriteriaBehaviors(self,rule_list,level=0):
        if len(rule_list) == 0:
            return
        for rule in reversed(rule_list):
            criteria_dict = {}
            criteria_dict['criteria'] = rule['criteria']
            criteria_dict['condition'] = rule['criteriaMustSatisfy']
            self._criteria_stack.append(criteria_dict)
            self.__parseChildCriteriaBehaviors(rule['children'],level+1)
            for behavior in rule['behaviors']:
                condition_dict = {}
                condition_dict['behavior'] = behavior
                condition_dict['criteria'] = self._criteria_stack.copy()
                self._condition_json.insert(0,condition_dict)
            temp = self._criteria_stack.pop()

    def _getBehaviorParsedList(self,version):
        if self._invalidconfig == True:
            print("No Configuration Found")
            return []
        self._criteria_stack = []
        self._condition_json = []
        self._condition_json1 = []

        ruleTree = self.getRuleTree(int(version))

        for default_behaviors in ruleTree['rules']['behaviors']:
            criteria_dict = {}
            criteria_dict['criteria'] = []
            criteria_dict['condition'] = 'all'

            condition_dict1 = {}
            condition_dict1['behavior'] = default_behaviors
            condition_dict1['criteria'] = criteria_dict
            self._condition_json1.append(condition_dict1)

        self.__parseChildCriteriaBehaviors(ruleTree['rules']['children'])

        behaviorParsedList = self._condition_json1 + self._condition_json
        return behaviorParsedList

    def getAvailableFeatures(self,version):
        if self._invalidconfig == True:
            print("No Configuration Found")
            return []

        behaviorList = []
        getAvailableFeaturesEndPoint = "/papi/v1/properties/{propertyId}/versions/{propertyVersion}/available-behaviors".format(propertyId=self.propertyId,propertyVersion=version)
        params = {}
        if self.accountSwitchKey:
            params["accountSwitchKey"] = self.accountSwitchKey
            status,getFeaturesjson = self._prdHttpCaller.getResult(getAvailableFeaturesEndPoint,params)
        else:
            status,getFeaturesjson = self._prdHttpCaller.getResult(getAvailableFeaturesEndPoint)
        for behaviors in getFeaturesjson["behaviors"]["items"]:
            behaviorList.append(behaviors["name"])
        return behaviorList

    def getUnusedBehaviors(self,version):
        if self._invalidconfig == True:
            print("No Configuration Found")
            return []
        
        availableFeatures = self.getAvailableFeatures(version)
        usedBehaviors = self.getUsedBehaviors(version)
        unusedBehaviors = list(set(availableFeatures) - set(usedBehaviors))
        return unusedBehaviors

    def getSiteShieldMap(self,version):
        if self._invalidconfig == True:
            print("No Configuration Found")
            return []
        behaviorParsedList = self._getBehaviorParsedList(version)
        sslist = []
        for behavior in behaviorParsedList:
            if behavior["behavior"]["name"] == 'siteShield':
                sslist.append(behavior["behavior"]["options"]['ssmap']['value'])
        sslist = list(dict.fromkeys(sslist))
        return sslist

    def getSureRouteCustomMaps(self,version):
        if self._invalidconfig == True:
            print("No Configuration Found")
            return []
        behaviorParsedList = self._getBehaviorParsedList(version)
        srlist = []
        for behavior in behaviorParsedList:
            if behavior["behavior"]["name"] == 'sureRoute':
                if behavior["behavior"]["options"]['enabled'] == True:
                    if 'type' in behavior["behavior"]["options"]:
                        if behavior["behavior"]["options"]['type'] == 'CUSTOM_MAP': 
                            srlist.append(behavior["behavior"]["options"]['customMap'])
        srlist = list(dict.fromkeys(srlist))
        return srlist

    def getUsedBehaviors(self,version):
        if self._invalidconfig == True:
            print("No Configuration Found")
            return []
        behaviorParsedList = self._getBehaviorParsedList(version)
        behaviorList = []
        for behavior in behaviorParsedList:
            behaviorList.append(behavior["behavior"]["name"])
        behaviorList = list(dict.fromkeys(behaviorList))
        return behaviorList

    def getOrigins(self,version):
        if self._invalidconfig == True:
            print("No Configuration Found")
            return []
        behaviorParsedList = self._getBehaviorParsedList(version)
        originlist = []
        for behavior in behaviorParsedList:
            if behavior["behavior"]["name"] == 'origin':
                if behavior["behavior"]["options"]['originType'] == 'CUSTOMER':
                    originlist.append(behavior["behavior"]["options"]['hostname'])
                else:
                    originlist.append(behavior["behavior"]["options"]['netStorage']['downloadDomainName'])
        originlist = list(dict.fromkeys(originlist))
        return originlist

    def getCPCodes(self,version):
        if self._invalidconfig == True:
            print("No Configuration Found")
            return []
        behaviorParsedList = self._getBehaviorParsedList(version)
        cpCodeList = []
        for behavior in behaviorParsedList:
            if behavior["behavior"]["name"] == 'cpCode':
                cpCodeList.append(behavior["behavior"]["options"]['value']['id'])

            if behavior["behavior"]["name"] == 'imageManager':
                if 'cpCodeOriginal' in behavior["behavior"]["options"]:
                    cpCodeList.append(behavior["behavior"]["options"]['cpCodeOriginal']['id'])
                if 'cpCodeTransformed' in behavior["behavior"]["options"]:
                    cpCodeList.append(behavior["behavior"]["options"]['cpCodeTransformed']['id'])
        cpCodeList = list(dict.fromkeys(cpCodeList))
        #print(cpCodeList)
        
        ruleTree = self.getRuleTree(int(version))
        cpCodeAdvancedList = self.extractCPCodes(ruleTree)
        #print(cpCodeAdvancedList)
        cpCodeList = cpCodeList + cpCodeAdvancedList
        cpCodeList = list(dict.fromkeys(cpCodeList))
        #print(cpCodeList)

        return cpCodeList
    
    def getCPCodesWithNames(self,version):
        if self._invalidconfig == True:
            print("No Configuration Found")
            return []
        behaviorParsedList = self._getBehaviorParsedList(version)
        cpCodeList = []
        for behavior in behaviorParsedList:
            if behavior["behavior"]["name"] == 'cpCode':
                item = {}
                item['CPCode'] = behavior["behavior"]["options"]['value']['id']
                item['Name'] = behavior["behavior"]["options"]['value']['name']
                cpCodeList.append(item)
        
        ruleTree = self.getRuleTree(int(version))
        cpCodeAdvancedList = self.extractCPCodes(ruleTree)
        #print(cpCodeAdvancedList)
        for x in cpCodeAdvancedList:
            item = {}
            item['CPCode'] = x
            item['Name'] = 'Advanced'
            cpCodeList.append(item)
        return cpCodeList

    def getMappings(self,productId):
        prdMappingJson = {'prd_Adaptive_Media_Delivery': 'Adaptive Media Delivery',
            'prd_Obj_Delivery': 'Object Delivery',
            'prd_Download_Delivery': 'Download Delivery',
            'prd_HTTP_Downloads': 'HTTP Downloads',
            'prd_Dynamic_Site_Del': 'Dynamic Site Delivery',
            'prd_Wholesale_Delivery': 'Wholesale Delivery',
            'prd_Site_Accel': 'Dynamic Site Accelerator',
            'prd_Fresca': 'Ion Standard',
            'prd_SPM': 'Ion Premiere',
            'prd_RM': 'Ion Media Advanced',
            'prd_Security_Failover': 'Cloud Security Failover',
            'prd_KDD': 'Kona DDoS Defender',
            'prd_Site_Defender': 'Kona Site Defender',
            'prd_Rich_Media_Accel': 'Rich Media Accelerator',
            'prd_Progressive_Media': 'Progressive Media Downloads',
            'prd_Site_Del': 'Dynamic Site Delivery(Legacy)',
            'prd_API_Accel': 'API Acceleration'}

        if productId in prdMappingJson.keys():
            return prdMappingJson[productId]
        else:
            return 'Unknown Product'
        

    def getProduct(self):
        if self._invalidconfig == True:
            print("No Configuration Found")
            return []
        version = self.getVersionofConfig()

        getVersionEP = "/papi/v1/properties/{propertyId}/versions".format(propertyId=self.propertyId)
        params = {}
        if self.accountSwitchKey:
            params["accountSwitchKey"] = self.accountSwitchKey
            status,getVersionsJson = self._prdHttpCaller.getResult(getVersionEP,params)
        else:
            status,getVersionsJson = self._prdHttpCaller.getResult(getVersionEP)
        #print(getVersionsJson)
        for versionItem in getVersionsJson["versions"]["items"]:
            if versionItem['propertyVersion'] == version:
                return self.getMappings(versionItem['productId'])
        return 'Unknown Product'


    def insertRule(self,version,rule_dict,pos=0):
        if self._invalidconfig == True:
            return False

        ruleTree = self.getRuleTree(int(version))

        if pos == 0:
            ruleTree['rules']['children'].insert(len(ruleTree['rules']['children']),rule_dict)
        else:
            ruleTree['rules']['children'].insert(pos-1,rule_dict)

        propruleInfo_json = json.dumps(ruleTree,indent=2)
        status = self.updateRuleTree(version,propruleInfo_json)
        return status

    def deleteRule(self,version,rule_name):
        if self._invalidconfig == True:
            return False

        ruleTree = self.getRuleTree(int(version))

        index = 0
        for childrule in ruleTree['rules']['children']:
            if childrule['name'] != rule_name:
                index = index + 1
            else:
                ruleTree['rules']['children'].pop(index)

        propruleInfo_json = json.dumps(ruleTree,indent=2)
        status = self.updateRuleTree(version,propruleInfo_json)
        return status

    def addVersionNotes(self,version,comment):
        if self._invalidconfig == True:
            return False

        ruleTree = self.getRuleTree(int(version))
        ruleTree['comments'] = comment

        propruleInfo_json = json.dumps(ruleTree,indent=2)
        status = self.updateRuleTree(version,propruleInfo_json)
        return status

    def addHostname(self,version,hostname,edgehostname):
        print(version,hostname,edgehostname)
        if self._invalidconfig == True:
            print("No Configuration Found")
            return []

        #Get the Hostnames
        getHostNameEndPoint = '/papi/v1/properties/{property_id}/versions/{new_version}/hostnames'.format(property_id=self.propertyId ,new_version=version)
        params = {}
        params["contractId"] =self.contractId
        params["groupId"] = self.groupId

        if self.accountSwitchKey:
            params["accountSwitchKey"] = self.accountSwitchKey

        getstatus,getHostnameJson = self._prdHttpCaller.getResult(getHostNameEndPoint,params)
        print(getHostnameJson)
        property_hostnames = getHostnameJson["hostnames"]["items"]

        if len(property_hostnames) > 0:
            for item in property_hostnames:
                if item['cnameFrom'] == 'example.edgesuite.net':
                    property_hostnames.remove(item)

            for item in property_hostnames:
                if 'edgeHostnameId' in item:
                    del item['edgeHostnameId']

        item = {}
        item["cnameType"] = "EDGE_HOSTNAME"
        print('*'*80)
        print(hostname,edgehostname)
        item["cnameFrom"] = hostname
        item["cnameTo"] = edgehostname
        item["certProvisioningType"] =  "CPS_MANAGED"
        print('*'*80)
        print(item)
        if len(property_hostnames) == 0:
            property_hostnames.insert(0, item)
        else:
            property_hostnames.append(item)

        print('----'*80)
        print(property_hostnames)

        headers = {}
        #headers['PAPI-Use-Prefixes'] = True
        #headers['If-Match'] = getHostnameJson['etag']
        headers['content-type']=  'application/json'

        property_hostname_data = json.dumps(property_hostnames)
        addHostNamesEndPoint = '/papi/v1/properties/{property_id}/versions/{newversion}/hostnames'.format(property_id=self.propertyId,newversion=version)

        retrycount = 0
        while retrycount < 2:
            status,addHostnameJson = self._prdHttpCaller.putResult(addHostNamesEndPoint,property_hostname_data,headers,params)
            print(status)
            if status == 200:
                return True
            retrycount = retrycount + 1
            time.sleep(1)
        return False   

    def getVersionofConfig(self):
        version = 0
        prodVersion = self.getProductionVersion()
        stagingVersion = self.getStagingVersion()
        latestVersion = self.latestVersion

        version = prodVersion
        if version == 0:
            version = stagingVersion
            if version == 0:
                version = latestVersion

        return version 

    def extractCPCodes(self,json_data):
        """
        Extracts the numbers from a string that contains one or more occurrences of the tag <reporting:cpcode>
        followed by the number.
        """
        start_tag = "<reporting:cpcode>"
        end_tag = "</reporting:cpcode>"
        start_index = 0
        advancedCPCodeList = []
        ruleTree = json.dumps(json_data)
        
        while True:
            start_index = ruleTree.find(start_tag, start_index)
            if start_index == -1:
                break
                
            start_index += len(start_tag)
            end_index = ruleTree.find(end_tag, start_index)
            if end_index == -1:
                break
            
            number = ruleTree[start_index:end_index].strip()
            if number.isdigit():
                advancedCPCodeList.append(int(number))
                
            start_index = end_index + len(end_tag)
        
        return advancedCPCodeList


class AkamaiPropertyManager():
    def __init__(self,prdHttpCaller,accountSwitchKey=None):
        self.name = ''
        self.contractId = ''
        self.groupId = ''
        self.propertyId = ''
        self.stagingVersion = 0
        self.productionVersion = 0
        self.lastupdatedDate = ''
        self.accountSwitchKey = ''
        self._edgerc = ''
        self._prdHttpCaller = ''
        self._session = ''
        self._baseurl_prd = ''
        self._host = ''
        self._invalidconfig = False
        self.latestVersion = 0
        self.assetId = ''

        self._criteria_stack = []
        self._condition_json = []
        self._condition_json1 = []

        self._prdHttpCaller = prdHttpCaller
        self.accountSwitchKey = accountSwitchKey
        return None
     
    def getGroups(self):
        groupsList = []
        ep = "/papi/v1/groups"
        params = {}
        if self.accountSwitchKey:
            params["accountSwitchKey"] = self.accountSwitchKey
            status,getgroupJson = self._prdHttpCaller.getResult(ep,params)
        else:
            status,getgroupJson = self._prdHttpCaller.getResult(ep)
        print(getgroupJson)
        for items in getgroupJson["groups"]["items"]:
            groupsList.append(items["groupId"])
        return groupsList

    def getContracts(self):
        contractsList = []
        ep = "/papi/v1/contracts"
        params = {}
        if self.accountSwitchKey:
            params["accountSwitchKey"] = self.accountSwitchKey
            status,getcontractJson = self._prdHttpCaller.getResult(ep,params)
        else:
            status,getcontractJson = self._prdHttpCaller.getResult(ep)
        for items in getcontractJson["contracts"]["items"]:
            contractsList.append(items["contractId"])
        return contractsList

    def listCPCodes(self,contract_id,group_id):
        cpCodeList = []
        ep = '/papi/v1/cpcodes'
        params = {}
        params['contractId'] = contract_id
        params['groupId'] = group_id
        if self.accountSwitchKey:
            params["accountSwitchKey"] = self.accountSwitchKey
        try:
            status,getcpCodesJson = self._prdHttpCaller.getResult(ep,params=params)
            for items in getcpCodesJson["cpcodes"]["items"]:
                cpCodeList.append(items["cpcodeId"])
        except Exception as e:
            return []
        return cpCodeList

    def getPropertiesofGroup(self,contractid,groupid):
        ep = '/papi/v1/properties'
        params = {}
        params['contractId'] = contractid
        params['groupId'] = groupid
        if self.accountSwitchKey:
            params["accountSwitchKey"] = self.accountSwitchKey
        
        try: 
            status,getpropertiesJson = self._prdHttpCaller.getResult(ep,params=params)
            propList = []
            if len(getpropertiesJson['properties']['items']) != 0:
                for prop in getpropertiesJson['properties']['items']:
                    propList.append(prop['propertyName'])
            return propList

        except Exception as e:
            return []
            '''import traceback
            track = traceback.format_exc() 
            print(track)
            pass'''
        
        
    def bulkSearch(self,jsonPathMatch,jsonPathQualifiers=None):
        bulkSearchEP = '/papi/v1/bulk/rules-search-requests-synch'

        data = {}
        data['bulkSearchQuery'] = {}
        data['bulkSearchQuery']['syntax'] = 'JSONPATH'
        data['bulkSearchQuery']['match'] = jsonPathMatch
        if jsonPathQualifiers:
            data['bulkSearchQuery']['bulkSearchQualifiers'] = jsonPathQualifiers

        json_data = json.dumps(data)

        try:
            if self.accountSwitchKey:
                params = {'accountSwitchKey':self.accountSwitchKey}
                version_info = self._prdHttpCaller.postResult(bulkSearchEP,json_data,params)
            else:
                version_info = self._prdHttpCaller.postResult(bulkSearchEP,json_data)

            propertiesList = []
            if version_info[0] == 200:
                for items in version_info[1]['results']:
                    propertiesList.append(items['propertyName'])
                return propertiesList
            else:
                return []
        except Exception as e:
            return []
    
    def getallProperties(self):
        propertylist = []
        groupIds = self.getGroups()
        contractIds = self.getContracts()
        for ctr in contractIds:
            for grp in groupIds:
                property_list = self.getPropertiesofGroup(ctr,grp)
                #print(property_list)
                if len(property_list) != 0:
                    for x in property_list:
                        propertylist.append(x)
        return propertylist

    def getCustomBehaviors(self):
        cbList = {}
        ep = '/papi/v1/custom-behaviors'
        params = {}
        if self.accountSwitchKey:
            params["accountSwitchKey"] = self.accountSwitchKey
        try:
            status,getcbJson = self._prdHttpCaller.getResult(ep,params=params)
            for item in getcbJson["customBehaviors"]["items"]:                
                cbList[item['name']] =  item['behaviorId']
            return cbList
        except Exception as e:
            print('Exception:',e)
            return []


    def getCustomOverrides(self):
        coList = {}
        ep = '/papi/v1/custom-overrides'
        params = {}
        if self.accountSwitchKey:
            params["accountSwitchKey"] = self.accountSwitchKey
        try:
            status,getcoJson = self._prdHttpCaller.getResult(ep,params=params)
            for items in getcoJson["customOverrides"]["items"]:
                coList[items['name']] =  items['overrideId']
            return coList
        except Exception as e:
            print('Exception:',e)
            return []
        
    def cloneProperty(self,contractId,groupId,referencePropertyId,version,newPropertyName):
        version = int(version)
        params = {}
        if self.accountSwitchKey:
            params["accountSwitchKey"] = self.accountSwitchKey
        params["contractId"] = contractId
        params["groupId"] = groupId


        clone_payload = {
            "cloneFrom": {
                #"cloneFromVersionEtag": "27b4ec45918df9a918764c944043765576f7c9a1",
                "copyHostnames": False,
                "propertyId": referencePropertyId,
                "version": version
            },
            "productId": "prd_Fresca",
            "propertyName": newPropertyName
        }

        clone_data = json.dumps(clone_payload)
       
        cloneConfigEndPoint = '/papi/v1/properties/'
        headers = {
            "accept": "application/json",
            "PAPI-Use-Prefixes": "true",
            "content-type": "application/json"
        }

        status,version_info = self._prdHttpCaller.postResult(cloneConfigEndPoint,clone_data,params,headers=headers)
        if status == 201:
            newpropetyId = version_info['propertyLink'].split('?')[0].split('/')[4].split('_')[1]
            return newpropetyId
        else:
            print('Failed to  Clone the config and status code is {}.'.format(status),file=sys.stderr)
            return 0
        