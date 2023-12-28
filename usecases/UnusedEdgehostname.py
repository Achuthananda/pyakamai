from pandas._config import config
import pydig
from akamaiproperty import AkamaiProperty,AkamaiPropertyManager
from akamaihttp import AkamaiHTTPHandler
import pandas
import logging
import optparse
import os
from openpyxl import load_workbook
import numpy as np

logging.basicConfig(filename='unusededgehostname_scan.txt',format='%(asctime)s %(message)s',level=logging.INFO)

edgercLocation = '~/.edgerc'
edgercLocation = os.path.expanduser(edgercLocation) # expand tilde. Python SDK doesn't handle tilde paths on Windows
accountSwitchKey = ''

parser = optparse.OptionParser()
parser.add_option(
        '-a', '--accountSwitchKey',
        action='store', type='string', dest='accountSwitchKey',
        help='AccountSwitchKey.')

parser.add_option(
        '-c', '--count',
        action='store', type='int', dest='count',default=1000,
        help='count.')

def writeToExcel(arrayName,fileName,sheetName):
    writer = pandas.ExcelWriter(fileName, engine='xlsxwriter')
    df=pandas.json_normalize(arrayName)
    pandas.set_option('display.max_rows', df.shape[0]+1)
    df.to_excel(writer, sheet_name=sheetName,index = False)
    writer.save()

def readConfigList():
    fp = open('config.txt','r')
    arr = fp.readlines()
    arr = [x.strip() for x in arr]
    return arr

def getAllProperties():
    if not os.path.isfile('config.txt'):
        pm = AkamaiPropertyManager(edgercLocation,accountSwitchKey)
        propertiesList = pm.getallProperties()
        np.savetxt("config.txt", np.array(propertiesList), fmt="%s")


akamai_level1hostnames = ['edgesuite','edgekey','edgesuite-staging','edgekey-staging','akamaized','akamaized-staging']

ehn_list = []

hostnameList = []

ehn_cname_mapping = {}



def getFirstLevelCname(hostname):
    fcname = pydig.query(hostname, 'CNAME')
    if fcname:
        if fcname[0].split('.')[-3] in akamai_level1hostnames:
            join_fcname = '.'.join(fcname)
            return join_fcname
        else:
            join_fcname = '.'.join(fcname)
            return join_fcname
    else:
        ip_address = pydig.query(hostname, 'A')
        if ip_address:
            return ip_address[0]
        else:
            return 'SOA Record'

def fetchEHNfromConfig(contractId,groupId,propId,config,version):
    akhttp = AkamaiHTTPHandler('/Users/apadmana/.edgerc')
    ep = "/papi/v0/properties/"+str(propId)+"/versions/"+str(version)+"/hostnames"
    params = {}
    params['accountSwitchKey'] = accountSwitchKey
    params['contractId'] = contractId
    params['groupId'] = groupId
    result = akhttp.getResult(ep,params)
    if result[0] == 200:
        body = result[1]
        for item in body['hostnames']['items']:
            hostnameList.append(item['cnameFrom'])
            found = False
            for ehn in ehn_list:
                if ehn['EdgeHostname'] == item['cnameTo']:
                    #ehn['Hostname'].append(item['cnameFrom'])
                    #ehn['Config'].append(config)
                    found = True
            if found == False:      
                hostname_detail = {}
                hostname_detail['EdgeHostname'] = item['cnameTo']
                #hostname_detail['Hostname'] = [item['cnameFrom']]
                #hostname_detail['Config'] = [config]
                hostname_detail['Existing Cnames'] = []
                hostname_detail['Active'] = False
                ehn_list.append(hostname_detail)
    else:
        logging.info("Failed to retrieve hostname details for {}".format(config))

def getEdgeHostnameUsage(configArray):
    iter = 0
    for config in configArray:
        if iter > options.count:
           break
        logging.info("{}.Checking the EHNs present in {}".format(iter+1,config))
        print("{}.Checking the EHNs present in {}".format(iter+1,config))
        akaconfig = AkamaiProperty(edgercLocation,config,accountSwitchKey)
        propId = akaconfig.propertyId
        contractId = akaconfig.contractId
        groupId = akaconfig.groupId
        version = akaconfig.getProductionVersion()
        if version == 0:
            version = akaconfig.getStagingVersion()
            if version == 0:
                version = akaconfig.latestVersion
        if version != 0:
            fetchEHNfromConfig(contractId,groupId,propId,config,version)

        iter = iter + 1


allEHNList = []


def getallEdgeHostNames():
    akhttp = AkamaiHTTPHandler('/Users/apadmana/.edgerc')
    ep = "/hapi/v1/edge-hostnames"
    params = {}
    params['accountSwitchKey'] = accountSwitchKey
    result = akhttp.getResult(ep,params)
    if result[0] == 200:
        for ehn in result[1]['edgeHostnames']:
            temp = ehn['recordName'] + '.' + ehn['dnsZone']
            allEHNList.append(temp)
    return allEHNList



def getCNamesofHostnames():
    #print(hostnameList)
    for host in hostnameList:
        cname = getFirstLevelCname(host)
        #print(host,'-',cname)
        if cname[:-1] in ehn_cname_mapping.keys():
            ehn_cname_mapping[cname[:-1]].append(host)

    #print(ehn_cname_mapping)
    #print('*'*80)
        

def checkIfEHNActive():
    logging.info("Now checking if the EHNs are active or not !!")
    #print("Now checking if the EHNs are active or not !!")
    #print(ehn_list)
    for ehn in ehn_list:
        #print(ehn['EdgeHostname'])
        if ehn['EdgeHostname'] in ehn_cname_mapping.keys():
            if len(ehn_cname_mapping[ehn['EdgeHostname']]) != 0:
                ehn['Active'] = True
                ehn['Existing Cnames'] = ehn_cname_mapping[ehn['EdgeHostname']]
    #print('*'*80)

def checkforOutliers():
    ehnconfig = []
    for ehn in ehn_list:
        ehnconfig.append(ehn['EdgeHostname'])

    unusededgehostames = list(set(allEHNList) - set(ehnconfig))
    for x in unusededgehostames:
        if len(ehn_cname_mapping[x]) == 0:
            hostname_detail = {}
            hostname_detail['EdgeHostname'] = x
            #hostname_detail['Hostname'] = []
            #hostname_detail['Config'] = 'NA'
            hostname_detail['Existing Cnames'] = []
            hostname_detail['Active'] = False
            ehn_list.append(hostname_detail)
        else:
            #Not used in the delivery Configs. But have been CNAMED To.
            hostname_detail = {}
            hostname_detail['EdgeHostname'] = x
            #hostname_detail['Hostname'] = []
            #hostname_detail['Config'] = 'NA'
            hostname_detail['Existing Cnames'] = ehn_cname_mapping[x]
            hostname_detail['Active'] = True
            ehn_list.append(hostname_detail)

    

if __name__ == "__main__":
    (options, args) = parser.parse_args()
    #print(options)
    if options.accountSwitchKey == None:
        print("Please Enter the Account SwitchKey in the format shown below")
        print("python3 UnusedEdgeHostname.py -a B-C-1IE2OH8")
        exit(1)
    else:
        accountSwitchKey = options.accountSwitchKey

    allEHNList = getallEdgeHostNames()
    ehn_cname_mapping = dict([(key, []) for key in allEHNList])
    
    getAllProperties()
    configArray = readConfigList()
    #configArray = ['site-delivery-walkthrough']
    getEdgeHostnameUsage(configArray)
    getCNamesofHostnames()

    checkIfEHNActive()
    checkforOutliers()
    
    sheetName = 'EHNInfo'
    fileName = 'EHNUsage_Scan.xlsx'
    writeToExcel(ehn_list,fileName,sheetName)

    print("Done!")
