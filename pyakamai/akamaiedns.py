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

class AkamaiEDNS():
    def __init__(self,prdHttpCaller,accountSwitchKey=None):
        self._prdHttpCaller = prdHttpCaller
        self.accountSwitchKey = accountSwitchKey
        return None

    def listZones(self,types='primary,secondary,alias'):
        listZonesEP = '/config-dns/v2/zones'
        params = {}
        params['types'] = types
        params['showAll'] = True
        if self.accountSwitchKey:
            params['accountSwitchKey']= self.accountSwitchKey
            status,zonesList = self._prdHttpCaller.getResult(listZonesEP,params=params)
        else:
            status,zonesList = self._prdHttpCaller.getResult(listZonesEP,params=params)
        if status == 200:
            return zonesList
        else:
            return {}


    def addRecord(self,zone,name,type,ttl,data):
        record ={}
        if type == 'AkamaiTLC':
            record['name'] = zone
        else:
            record['name'] = name + '.' + zone

        record['type'] = type
        record['ttl'] = ttl
        if record['type'] == 'MX':
            record['rdata'] = data.split('\n')
        else:
            record['rdata'] = [data]
        
        recordjson = json.dumps(record)
        #print(recordjson)

        print("Adding {} record {} for zone {}".format(type,name,zone))
        headers = {'Content-Type': 'application/json'}
        addRecordEP = '/config-dns/v2/zones/{zone}/names/{name}/types/{type}'.format(zone=zone,name=record['name'],type=type)

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,addRecordResult = self._prdHttpCaller.postResult(addRecordEP,recordjson,headers=headers,params=params)
        else:
            status,addRecordResult = self._prdHttpCaller.postResult(addRecordEP,recordjson,headers=headers)

        if status == 201:
            print("Successfully added {} record {} for zone {}".format(type,name,zone))
            return True
        else:
            print("Failed to add the record")
            print(json.dumps(addRecordResult,indent=2))
            return False


    def updateRecord(self,zone,name,recordType,payload):
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }
    
        updateRecordEndPoint = '/config-dns/v2/zones/{zone}/names/{name}/types/{type}'.format(zone=zone,name=name,type=recordType)
        
        recordjson = json.dumps(payload)
        print(recordjson)
        
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,updateRecordResult = self._prdHttpCaller.putResult(updateRecordEndPoint,recordjson,headers=headers,params=params)
        else:
            status,updateRecordResult = self._prdHttpCaller.putResult(updateRecordEndPoint,recordjson,headers=headers)

        if status == 200:
            print(json.dumps(updateRecordResult,indent=2))
            return True
        else:
            print("Failed to get the records for the zone")
            print(json.dumps(updateRecordResult,indent=2))
            return False
       

    def getZonesRecords(self,zone):
        headers = {'Accept-Type': 'application/json'}

        getZonesReecordsEP = '/config-dns/v2/zones/{zone}/recordsets'.format(zone=zone)
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,resultJson = self._prdHttpCaller.getResult(getZonesReecordsEP,headers=headers,params=params)
        else:
            status,resultJson = self._prdHttpCaller.getResult(getZonesReecordsEP,headers=headers)

        if status == 200:
            return resultJson
        else:
            print("Failed to get the records for the zone")
            return {}
        
    def getZoneFile(self,zone):
        headers = {'Accept': 'text/dns'}
        getZonesReecordsEP = '/config-dns/v2/zones/{zone}/zone-file/'.format(zone=zone)
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,result = self._prdHttpCaller.getFileResult(getZonesReecordsEP,headers=headers,params=params)
        else:
            status,result = self._prdHttpCaller.getFileResult(getZonesReecordsEP,headers=headers)

        if status == 200:
            return result
        else:
            print("Failed to get the file for the zone")
            return ''
        
    def getZoneSettings(self,zone):
        headers = {'Accept-Type': 'application/json'}

        getZoneSettingsEP = '/config-dns/v2/zones/{zone}'.format(zone=zone)
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,resultJson = self._prdHttpCaller.getResult(getZoneSettingsEP,headers=headers,params=params)
        else:
            status,resultJson = self._prdHttpCaller.getResult(getZoneSettingsEP,headers=headers)

        if status == 200:
            return resultJson
        else:
            print("Failed to get the settings of the zone")
            return {}
        
    def updateZoneSettings(self,zone,payload):
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }
    
        updateZoneEndPoint = '/config-dns/v2/zones/{zone}'.format(zone=zone)
        
        recordjson = json.dumps(payload)
        print(recordjson)
        params = {}
        params['skipSignAndServeSafetyCheck'] = False
        
        if self.accountSwitchKey:
            params['accountSwitchKey']= self.accountSwitchKey
            status,updateZoneResult = self._prdHttpCaller.putResult(updateZoneEndPoint,recordjson,headers=headers,params=params)
        else:
            status,updateZoneResult = self._prdHttpCaller.putResult(updateZoneEndPoint,recordjson,headers=headers,params=params)

        if status == 200:
            print(json.dumps(updateZoneResult,indent=2))
            return True
        else:
            print("Failed to update the settings for the zone")
            print(json.dumps(updateZoneResult,indent=2))
            return False
    