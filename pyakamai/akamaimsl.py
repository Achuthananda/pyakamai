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

class AkamaiMSL():
    def __init__(self,prdHttpCaller,accountSwitchKey=None):
        self.name = ''
        self.format = ''
        self.contractId = ''
        self.groupId = ''
        self.propertyId = ''
        self.allowedIps = []
        self.events = []
        self.cpcode = 0
        self.ingestAccelerated = False
        self.dvrWindow = 0
        self.encoderZone = ''
        self.backupEncoderZone = ''
        self.primaryPublishingUrl = ''
        self.backupPublishingUrl = ''
        self.origin = ''
        self.backupOrigin = ''
        self.provisionStatus = ''
        self.streamjson = ''
       
        self._prdHttpCaller = prdHttpCaller
        self.accountSwitchKey = accountSwitchKey
        return None


    def stream(self,streamId):
        self.id =  streamId
        mslInfoEndPoint = "/config-media-live/v2/msl-origin/streams/" + str(streamId)
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,msl_info = self._prdHttpCaller.getResult(mslInfoEndPoint,params)
        else:
            status,msl_info = self._prdHttpCaller.getResult(mslInfoEndPoint)
        self.name = msl_info['name']
        self.format = msl_info['format']
        self.cpcode = msl_info['cpcode']
        self.ingestAccelerated = msl_info['ingestAccelerated']
        if 'dvrWindow' in msl_info:
            self.dvrWindow = msl_info['dvrWindow']
        self.encoderZone = msl_info['encoderZone']
        if 'backupEncoderZone' in msl_info:
            self.backupEncoderZone = msl_info['backupEncoderZone']
        self.primaryPublishingUrl = msl_info['primaryPublishingUrl']
        self.backupPublishingUrl = msl_info['backupPublishingUrl']
        self.origin = msl_info['origin']
        if 'backupOrigin' in msl_info:
            self.backupOrigin = msl_info['backupOrigin']
        self.provisionStatus = msl_info['provisionDetail']['status']
        self.allowedIps = msl_info['allowedIps']
        self.events = msl_info['events']
        self.streamjson = msl_info

        return None

    def printStreamInfo(self):
        print("Stream Name:",self.name)
        print("Stream Id:",self.id)
        print("Allowed IPs:",self.allowedIps)
        print("Format:",self.format)
        print("Origin:",self.origin)
        print("Provisioning Status:",self.provisionStatus)
        print('*'*80)

    def updateStream(self,jsondata):
        #print(self.provisionStatus)
        if self.provisionStatus == 'PROVISIONED':
            streamUpdateEndpoint = '/config-media-live/v2/msl-origin/streams/' + str(self.id)
            if self.accountSwitchKey:
                params = {}
                params["accountSwitchKey"] = self.accountSwitchKey
                status,updateStreamJson = self._prdHttpCaller.putResult(streamUpdateEndpoint,jsondata,headers=None,params=params)
                #print(status,updateStreamJson)
                return status,updateStreamJson
            else:
                status,updateStreamJson = self._prdHttpCaller.putResult(streamUpdateEndpoint,jsondata,headers=None)
                #print(status,updateStreamJson)
                return status,updateStreamJson
        else:
            return 400,"Not in Provisioned Status"
            

    def listStreams(self):
        """ Get list of MSL streams"""
        listStreamsEndpoint = '/config-media-live/v2/msl-origin/streams'
        if self.accountSwitchKey:
            params = {'accountSwitchKey': self.accountSwitchKey,
                    'sortKey': 'createdDate',
                    'sortOrder': 'DESC'
                    }
            status,streamList = self._prdHttpCaller.getResult(listStreamsEndpoint, params)
        else:
            params = {'sortKey': 'createdDate',
                    'sortOrder': 'DESC'
                    }
            status,streamList = self._prdHttpCaller.getResult(listStreamsEndpoint,params)
        return streamList

    def getStream(self):
        '''Get a stream details'''
        getStreamsEndpoint = '/config-media-live/v2/msl-origin/streams/{streamId}'.format(streamId=self.id)
        if self.accountSwitchKey:
            params = {'accountSwitchKey': self.accountSwitchKey
                    }
            status,streaminfo =  self._prdHttpCaller.getResult(getStreamsEndpoint, params)
        else:
            status,streaminfo =  self._prdHttpCaller.getResult(getStreamsEndpoint)
        return streaminfo

