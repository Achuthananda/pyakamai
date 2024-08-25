from akamai.edgegrid import EdgeGridAuth, EdgeRc
from .http_calls import EdgeGridHttpCaller
from .akamaiproperty import AkamaiProperty,AkamaiPropertyManager
from .akamaimsl import AkamaiMSL
from .akamaidatastream import AkamaiDataStream
from .akamaiedns import AkamaiEDNS
from .akamaicps import AkamaiCPS
from .akamailds import AkamaiLDS
from .akamaipurge import AkamaiPurge
from .akamaiehn import AkamaiEdgeHostName
from .akamaicasemanagement import AkamaiCaseManagement
from .akamaiapidefinition import AkamaiAPIDefinition
from .akamaichinacdn import AkamaiChinaCDN
from .akamaidiagnostictools import AkamaiDiagnosticTools
from .akamains import AkamaiNetstorage
from .akamaiss import AkamaiSiteShield
from .akamaicloudlets import AkamaiCloudlets
from .akamaireporting import AkamaiReporting
from .akamaigtm import AkamaiGTM
from .akamaiiam import AkamaiIdentity 
from .akamaicpcode import AkamaiCPCode
import sys
import os
import requests
import logging
import json

if sys.version_info[0] >= 3:
    # python3
    from urllib import parse
else:
    # python2.7
    import urlparse as parse

logger = logging.getLogger(__name__)

class pyakamai():
    def __init__(self,accountSwitchKey=None,edgercLocation='~/.edgerc',section='default',debug=False,verbose=False):
        self._prdHttpCaller = ''
        self._session = ''
        self._baseurl_prd = ''
        self._host = ''
        self.accountSwitchKey = accountSwitchKey
        
        self._edgerc = EdgeRc(edgercLocation)
        self._host = self._edgerc.get(section, 'host')
        self._baseurl_prd = 'https://%s' %self._host
        self._session = requests.Session()
        self._session.auth = EdgeGridAuth.from_edgerc(self._edgerc, section)
        self._session.headers.update({'User-Agent': "AkamaiCLI"})
        self._prdHttpCaller = EdgeGridHttpCaller(self._session, debug, verbose, self._baseurl_prd)
        
        pass
    
    def client(self, product, *args):
        if product == 'property':
            class_obj = AkamaiProperty(self._prdHttpCaller,self.accountSwitchKey,*args)

        if product == 'propertymanager':
            class_obj = AkamaiPropertyManager(self._prdHttpCaller,self.accountSwitchKey,*args)

        if product == 'cpcode':
            class_obj = AkamaiCPCode(self._prdHttpCaller,self.accountSwitchKey,*args)

        elif product == 'msl':
            class_obj = AkamaiMSL(self._prdHttpCaller,self.accountSwitchKey,*args)

        elif product == 'datastream':
             class_obj = AkamaiDataStream(self._prdHttpCaller,self.accountSwitchKey,*args)
        
        elif product == 'edns':
            class_obj = AkamaiEDNS(self._prdHttpCaller,self.accountSwitchKey,*args)

        elif product == 'cps':
            class_obj = AkamaiCPS(self._prdHttpCaller,self.accountSwitchKey,*args)

        elif product == 'lds':
            class_obj = AkamaiLDS(self._prdHttpCaller,self.accountSwitchKey,*args)

        elif product == 'gtm':
            class_obj = AkamaiGTM(self._prdHttpCaller,self.accountSwitchKey,*args)

        elif product == 'purge':
            class_obj = AkamaiPurge(self._prdHttpCaller,*args)
        
        elif product == 'ehn':
            class_obj = AkamaiEdgeHostName(self._prdHttpCaller,self.accountSwitchKey,*args)

        elif product in ['case','casemanagement']:
            class_obj = AkamaiCaseManagement(self._prdHttpCaller,self.accountSwitchKey,*args)     

        elif product in ['apidefinition','apigateway']:
            class_obj = AkamaiAPIDefinition(self._prdHttpCaller,self.accountSwitchKey,*args)     

        elif product == 'chinacdn':
            class_obj = AkamaiChinaCDN(self._prdHttpCaller,self.accountSwitchKey,*args)

        elif product == 'cloudlets':
            class_obj = AkamaiCloudlets(self._prdHttpCaller,self.accountSwitchKey,*args)

        elif product == 'reporting':
            class_obj = AkamaiReporting(self._prdHttpCaller,self.accountSwitchKey,*args)

        elif product == 'diagnostictools':
            class_obj = AkamaiDiagnosticTools(self._prdHttpCaller,self.accountSwitchKey,*args)    

        elif product in ['ns','netstorage']:
            class_obj = AkamaiNetstorage(self._prdHttpCaller,self.accountSwitchKey,*args)   

        elif product in ['ss','siteshield']:
            class_obj = AkamaiSiteShield(self._prdHttpCaller,self.accountSwitchKey,*args)  

        elif product in ['iam']:
            class_obj = AkamaiIdentity(self._prdHttpCaller,self.accountSwitchKey,*args)   

        return class_obj