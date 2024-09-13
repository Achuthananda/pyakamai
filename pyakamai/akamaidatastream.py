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

class AkamaiDataStream():
    def __init__(self,prdHttpCaller,accountSwitchKey=None):
        self._prdHttpCaller = prdHttpCaller
        self.accountSwitchKey = accountSwitchKey
        return None
    
    def listGroups(self):
        """ List the groups associated with the account """
        listGroupEndpoint = '/datastream-config-api/v2/log/groups'
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,groupList = self._prdHttpCaller.getResult(listGroupEndpoint,params)
        else:
            status,groupList = self._prdHttpCaller.getResult(listGroupEndpoint)
        return(groupList)

    def listConnectors(self):
        """ List the type of connectors available with the datastream .
        Can use one of the connector types as a destination for log delivery in a data stream configuration"""

        listConnectorEndpoint = 'datastream-config-api/v2/log/connectors'

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,connectorList = self._prdHttpCaller.getResult(listConnectorEndpoint,params)
        else:
            status,connectorList = self._prdHttpCaller.getResult(listConnectorEndpoint)
        return(connectorList)

    def listProducts(self):
        listProductEndpoint = 'datastream-config-api/v2/log/products'

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,productsList = self._prdHttpCaller.getResult(listProductEndpoint,params)
        else:
            status,productsList = self._prdHttpCaller.getResult(listProductEndpoint)
        return(productsList)

    def listStreamTypes(self):
        """ List the type of streams available with the datastream."""

        listStreamTypeEndpoint = 'datastream-config-api/v2/log/streamTypes'

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,streamTypeList = self._prdHttpCaller.getResult(listStreamTypeEndpoint,params)
        else:
            status,streamTypeList = self._prdHttpCaller.getResult(listStreamTypeEndpoint)
        return(streamTypeList)

    def listStreams(self):
        """ List the type of Streams available with the Group """

        listStreamsEndpoint = 'datastream-config-api/v2/log/streams'

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,streamList = self._prdHttpCaller.getResult(listStreamsEndpoint,params)
        else:
            status,streamList = self._prdHttpCaller.getResult(listStreamsEndpoint)
        return(streamList)

    def listProperties(self,groupId,productId):
        """ List the type of Properties available with the Group """

        listPropertiesEndpoint = 'datastream-config-api/v2/log/properties/product/'+str(productId)+'/group/'+str(groupId)

        if self.accountSwitchKey:
            params = {
                        'accountSwitchKey':self.accountSwitchKey
                    }
            status,propertiesList = self._prdHttpCaller.getResult(listPropertiesEndpoint,params)
        else:
            status,propertiesList = self._prdHttpCaller.getResult(listPropertiesEndpoint)
        return(propertiesList)


    def listErrorStreams(self,groupId):
        """ List the type of Error Streams available with the Group """
        listErrorStreamsEndpoint = 'datastream-config-api/v2/log/error-streams/groups/' + str(groupId)
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,errorstreamList = self._prdHttpCaller.getResult(listErrorStreamsEndpoint,params)
        else:
            status,errorstreamList = self._prdHttpCaller.getResult(listErrorStreamsEndpoint)
        return(errorstreamList)

    def getStream(self,streamId):
        """Get the Details of the Stream """

        getStreamDetailEndpoint = '/datastream-config-api/v2/log/streams/{}'.format(streamId)
        
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,streamDetail = self._prdHttpCaller.getResult(getStreamDetailEndpoint,params)
        else:
            status,streamDetail = self._prdHttpCaller.getResult(getStreamDetailEndpoint)
        return(streamDetail)

    def getStreamActHistory(self,streamId):
        streamActHistoryEndpoint = '/datastream-config-api/v2/log/streams/'+ str(streamId) + '/activationHistory'

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,streamActHistory = self._prdHttpCaller.getResult(streamActHistoryEndpoint,params)
        else:
            status,streamActHistory = self._prdHttpCaller.getResult(streamActHistoryEndpoint)
        return(streamActHistory)


    def getStreamHistory(self,streamId):
        streamHistoryEndpoint = '/datastream-config-api/v2/log/streams/'+ str(streamId) + '/history'
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,streamHistory = self._prdHttpCaller.getResult(streamHistoryEndpoint,params)
        else:
            status,streamHistory = self._prdHttpCaller.getResult(streamHistoryEndpoint)
        return(streamHistory)

    def getDatasets(self):
        datasetsEndpoint = '/datastream-config-api/v2/log/datasets-fields'
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,datasetList = self._prdHttpCaller.getResult(datasetsEndpoint,params)
        else:
            status,datasetList = self._prdHttpCaller.getResult(datasetsEndpoint)
        return(datasetList)


    def createStream(self,data,activate=False):
        """ Create a Stream"""
        createEndpoint = '/datastream-config-api/v2/log/streams'
        params = {}
        params['activate'] = activate
        if self.accountSwitchKey:
            params['accountSwitchKey'] = self.accountSwitchKey
            cstatus,createResponse = self._prdHttpCaller.postResult(createEndpoint,data,params)
        else:
            status,createResponse = self._prdHttpCaller.postResult(createEndpoint,data,params)
        return(createResponse)

    def updateStream(self,data,streamid):
        print(streamid)
        updateEndpoint = '/datastream-config-api/v2/log/streams/{}'.format(str(streamid))
        print(updateEndpoint)
        headers = {'content-type': 'application/json'}
        if self.accountSwitchKey:
            params = {}
            params['accountSwitchKey']= self.accountSwitchKey
            params['activate'] = 'true'
            status,updateResponse = self._prdHttpCaller.putResult(updateEndpoint,data,headers,params)
        else:
            status,updateResponse = self._prdHttpCaller.putResult(updateEndpoint,headers,data)
        print(status,updateResponse)
        return(updateResponse)


    def activateStream(self,streamId):
        """ Activate a particular Datastream"""
        activateEndpoint = '/datastream-config-api/v2/log/streams/' + str(streamId) +'/activate/'
        data = {}
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,activateResponse = self._prdHttpCaller.putResult(activateEndpoint,data,params)
        else:
            status,activateResponse = self._prdHttpCaller.putResult(activateEndpoint,data)
        return(activateResponse)

    def deActivateStream(self,streamId):
        """ Deactivate a particular stream"""
        deactivateEndpoint = '/datastream-config-api/v2/log/streams/' + str(streamId) +'/deactivate/'
        data = {}
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,deactivateResponse = self._prdHttpCaller.putResult(deactivateEndpoint,data,params)
        else:
            status,deactivateResponse = self._prdHttpCaller.putResult(deactivateEndpoint,data)
        return(deactivateResponse)

    def deleteStream(self,streamId):
        """ Delete a particular stream"""
        deleteEndpoint = '/datastream-config-api/v2/log/streams/' + str(streamId)
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,deleteResponse = self._prdHttpCaller.deleteResult(deleteEndpoint,params)
        else:
            status,deleteResponse = self._prdHttpCaller.deleteResult(deleteEndpoint)
        return(deleteResponse)
