import pandas
import os
from openpyxl import load_workbook
import numpy as np

from pyakamai import pyakamai
pyakamaiObj = pyakamai("asdasdUN5:1BL")
akaconfig = pyakamaiObj.client('property')


edgercLocation = '~/.edgerc'
edgercLocation = os.path.expanduser(edgercLocation) # expand tilde. Python SDK doesn't handle tilde paths on Windows

domainValidationArray = []

def getVersionofConfig(myProperty):
    version = 0
    prodVersion = myProperty.getProductionVersion()
    stagingVersion = myProperty.getStagingVersion()
    latestVersion = myProperty.latestVersion

    version = prodVersion
    if version == 0:
        version = stagingVersion
        if version == 0:
            version = latestVersion

    return version

def writeToExcel(arrayName,fileName,sheetName):
    writer = pandas.ExcelWriter(fileName, engine='xlsxwriter')
    df=pandas.json_normalize(arrayName)
    pandas.set_option('display.max_rows', df.shape[0]+1)
    df.to_excel(writer, sheet_name=sheetName,index = False)
    writer.save()

def readConfigList(accountSwitchKey):
    fileName = accountSwitchKey +  '_configs.txt'
    fp = open(fileName,'r')
    arr = fp.readlines()
    arr = [x.strip() for x in arr]
    return arr

def getAllProperties(accountSwitchKey):
    pyakamaiObj = pyakamai(accountSwitchKey)
    fileName = accountSwitchKey +  '_configs.txt'
    if not os.path.isfile(fileName):
        propertiesList = pyakamaiObj.getAllProperties()
        np.savetxt(fileName, np.array(propertiesList), fmt="%s")



def addDomainValidation(config,accountSwitchKey):
    pyakamaiObj = pyakamai(accountSwitchKey)
    myconfig = pyakamaiObj(config)
    print('Fetching details from {}'.format(config))
    version = myconfig.getVersionofConfig()
    ruleTree = myconfig.getRuleTree(version)
    item = {}
    item['Config'] = config
    item['Network'] = 'Enhanced TLS'
    item['AutoDomain Validation'] = 'NA'
    if ruleTree['rules']['options']['is_secure'] == False: #Standard TLS
        item['Network'] = 'Standard TLS'
        usedbehaviors = myconfig.getUsedBehaviors(version)
        if 'autoDomainValidation' in usedbehaviors:
            item['AutoDomain Validation'] = 'Yes'
        else:
            item['AutoDomain Validation'] = 'No'
    domainValidationArray.append(item)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Support Ticket Raising Tool')
    parser.add_argument('--accountSwitchKey',required=True, default=None,help='Account SwitchKey')

    args = parser.parse_args()
    accountSwitchKey = args.accountSwitchKey

    if accountSwitchKey == None:
        print("Please Enter the Account SwitchKey in the format shown below")
        print("python3 autodomainvalidaton.py --accountSwitchKey BasdY9")
        exit(1)

    print("Fetching all the configs of the account!")
    getAllProperties(accountSwitchKey)
    configArray = readConfigList(accountSwitchKey)

    for config in configArray:
        addDomainValidation(config,accountSwitchKey)

    sheetName = 'AutoDomainValidationInfo'
    filename =  accountSwitchKey+ '_ADV.xlsx'
    writeToExcel(domainValidationArray,filename,sheetName)
