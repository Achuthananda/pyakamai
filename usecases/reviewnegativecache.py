import pandas
import logging
import optparse
import os
from openpyxl import load_workbook
import numpy as np

from pyakamai import pyakamai
pyakamaiObj = pyakamai("asdasdUN5:1BL")
akaconfig = pyakamaiObj.client('property')


edgercLocation = '~/.edgerc'
edgercLocation = os.path.expanduser(edgercLocation) # expand tilde. Python SDK doesn't handle tilde paths on Windows

checkCacheErrorArray = []

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


def check(string, sub_str):
    if (string.find(sub_str) == -1):
        print("NO")
        return 0
    else:
        print("YES")
        return 1

def checkCacheError(config,accountSwitchKey):
    pyakamaiObj = pyakamai(accountSwitchKey)
    myconfig = pyakamaiObj(config)
    print('Fetching details from {}'.format(config))
    version = myconfig.getVersionofConfig(myconfig)
    ruleTree = myconfig.getRuleTree(version)
    item = {}
    item['Config'] = config
    item['CacheErrorTTL'] = '0'

    behaviorList = myconfig._getBehaviorParsedList(version)
    for pmbehaviors in behaviorList:
        if pmbehaviors['behavior']['name'] == 'cacheError':
            if pmbehaviors['behavior']['options']['enabled'] == True:
                item['CacheErrorTTL'] = pmbehaviors['behavior']['options']['ttl']

    checkCacheErrorArray.append(item)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Review negative cache')
    parser.add_argument('--accountSwitchKey',required=True, default=None,help='Account SwitchKey')

    args = parser.parse_args()
    accountSwitchKey = args.accountSwitchKey

    if accountSwitchKey == None:
        print("Please Enter the Account SwitchKey in the format shown below")
        print("python3 cacheerror.py --accountSwitchKey F-BL")
        exit(1)

    print("Fetching all the configs of the account!")
    getAllProperties(accountSwitchKey)
    configArray = readConfigList(accountSwitchKey)

    for config in configArray:
        checkCacheError(config,accountSwitchKey)

    sheetName = 'CacheErrorSetting'
    filename =  accountSwitchKey+ '_CacheError.xlsx'
    writeToExcel(checkCacheErrorArray,filename,sheetName)
