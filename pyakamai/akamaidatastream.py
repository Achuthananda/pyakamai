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
        listGroupEndpoint = '/datastream-config-api/v1/log/groups'
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            groupList = self._prdHttpCaller.getResult(listGroupEndpoint,params)
        else:
            groupList = self._prdHttpCaller.getResult(listGroupEndpoint)
        return(groupList)

    def listConnectors(self):
        """ List the type of connectors available with the datastream .
        Can use one of the connector types as a destination for log delivery in a data stream configuration"""

        listConnectorEndpoint = 'datastream-config-api/v1/log/connectors'

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            connectorList = self._prdHttpCaller.getResult(listConnectorEndpoint,params)
        else:
            connectorList = self._prdHttpCaller.getResult(listConnectorEndpoint)
        return(connectorList)

    def listProducts(self):
        listProductEndpoint = 'datastream-config-api/v1/log/products'

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            productsList = self._prdHttpCaller.getResult(listProductEndpoint,params)
        else:
            productsList = self._prdHttpCaller.getResult(listProductEndpoint)
        return(productsList)

    def listStreamTypes(self):
        """ List the type of streams available with the datastream."""

        listStreamTypeEndpoint = 'datastream-config-api/v1/log/streamTypes'

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            streamTypeList = self._prdHttpCaller.getResult(listStreamTypeEndpoint,params)
        else:
            streamTypeList = self._prdHttpCaller.getResult(listStreamTypeEndpoint)
        return(streamTypeList)

    def listStreams(self,groupId):
        """ List the type of Streams available with the Group """

        listStreamsEndpoint = 'datastream-config-api/v1/log/streams'

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey,
                    'groupId':int(groupId)
                    }
            streamList = self._prdHttpCaller.getResult(listStreamsEndpoint,params)
        else:
            streamList = self._prdHttpCaller.getResult(listStreamsEndpoint)
        return(streamList)

    def listProperties(self,groupId,productId):
        """ List the type of Properties available with the Group """

        listPropertiesEndpoint = 'datastream-config-api/v1/log/properties/product/'+str(productId)+'/group/'+str(groupId)

        if self.accountSwitchKey:
            params = {
                        'accountSwitchKey':self.accountSwitchKey
                    }
            propertiesList = self._prdHttpCaller.getResult(listPropertiesEndpoint,params)
        else:
            propertiesList = self._prdHttpCaller.getResult(listPropertiesEndpoint)
        return(propertiesList)


    def listErrorStreams(self,groupId):
        """ List the type of Error Streams available with the Group """
        listErrorStreamsEndpoint = 'datastream-config-api/v1/log/error-streams/groups/' + str(groupId)
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            errorstreamList = self._prdHttpCaller.getResult(listErrorStreamsEndpoint,params)
        else:
            errorstreamList = self._prdHttpCaller.getResult(listErrorStreamsEndpoint)
        return(errorstreamList)

    def getStream(self,streamId,version=None):
        """Get the Details of the Stream """

        if version:
            getStreamDetailEndpoint = '/datastream-config-api/v1/log/streams/' + str(streamId) + '/version/' + str(config.version)
        else:
            getStreamDetailEndpoint = '/datastream-config-api/v1/log/streams/' + str(streamId)

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            streamDetail = self._prdHttpCaller.getResult(getStreamDetailEndpoint,params)
        else:
            streamDetail = self._prdHttpCaller.getResult(getStreamDetailEndpoint)
        return(streamDetail)

    def getStreamActHistory(self,streamId):
        streamActHistoryEndpoint = '/datastream-config-api/v1/log/streams/'+ str(streamId) + '/activationHistory'

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            streamActHistory = self._prdHttpCaller.getResult(streamActHistoryEndpoint,params)
        else:
            streamActHistory = self._prdHttpCaller.getResult(streamActHistoryEndpoint)
        return(streamActHistory)


    def getStreamHistory(self,streamId):
        streamHistoryEndpoint = '/datastream-config-api/v1/log/streams/'+ str(streamId) + '/history'
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            streamHistory = self._prdHttpCaller.getResult(streamHistoryEndpoint,params)
        else:
            streamHistory = self._prdHttpCaller.getResult(streamHistoryEndpoint)
        return(streamHistory)

    def getDatasets(self,templatename):
        datasetsEndpoint = '/datastream-config-api/v1/log/datasets/template/'+ templatename
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            datasetList = self._prdHttpCaller.getResult(datasetsEndpoint,params)
        else:
            datasetList = self._prdHttpCaller.getResult(datasetsEndpoint)
        return(datasetList)


    def createStream(self,data):
        """ Create a Stream"""
        createEndpoint = '/datastream-config-api/v1/log/streams'
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            createResponse = self._prdHttpCaller.postResult(createEndpoint,data,params)
        else:
            createResponse = self._prdHttpCaller.postResult(createEndpoint,data)
        return(createResponse)

    def updateStream(self,data,streamid):
        """ Update a Stream"""
        updateEndpoint = '/datastream-config-api/v1/log/streams/' + str(streamid)
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            updateResponse = self._prdHttpCaller.putResult(updateEndpoint,data,params)
        else:
            updateResponse = self._prdHttpCaller.putResult(updateEndpoint,data)
        return(updateResponse)


    def activateStream(self,streamId):
        """ Activate a particular Datastream"""
        activateEndpoint = '/datastream-config-api/v1/log/streams/' + str(streamId) +'/activate/'
        data = {}
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            activateResponse = self._prdHttpCaller.putResult(activateEndpoint,data,params)
        else:
            activateResponse = self._prdHttpCaller.putResult(activateEndpoint,data)
        return(activateResponse)

    def deActivateStream(self,streamId):
        """ Deactivate a particular stream"""
        deactivateEndpoint = '/datastream-config-api/v1/log/streams/' + str(streamId) +'/deactivate/'
        data = {}
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            deactivateResponse = self._prdHttpCaller.putResult(deactivateEndpoint,data,params)
        else:
            deactivateResponse = self._prdHttpCaller.putResult(deactivateEndpoint,data)
        return(deactivateResponse)

    def deleteStream(self,streamId):
        """ Delete a particular stream"""
        deleteEndpoint = '/datastream-config-api/v1/log/streams/' + str(streamId)
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            deleteResponse = self._prdHttpCaller.deleteResult(deleteEndpoint,params)
        else:
            deleteResponse = self._prdHttpCaller.deleteResult(deleteEndpoint)
        return(deleteResponse)
