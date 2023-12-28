import pandas
import logging
import optparse
import os
from openpyxl import load_workbook
import numpy as np
import json
from akamaiproperty import AkamaiProperty,AkamaiPropertyManager


edgercLocation = '~/.edgerc'
edgercLocation = os.path.expanduser(edgercLocation)
accountSwitchKey = 'AANA-asdasd6WET7X:1-2RBL'

hostname_list = []

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

    return latestVersion

def readConfigList():
    fp = open('config.txt','r')
    arr = fp.readlines()
    arr = [x.strip() for x in arr]
    return arr

def getAllProperties():
    pm = AkamaiPropertyManager(edgercLocation,accountSwitchKey)
    propertiesList = pm.getallProperties()
    np.savetxt("config.txt", np.array(propertiesList), fmt="%s")


def writeToExcel(arrayName,fileName,sheetName):
    writer = pandas.ExcelWriter(fileName, engine='xlsxwriter')
    df=pandas.json_normalize(arrayName)
    pandas.set_option('display.max_rows', df.shape[0]+1)
    df.to_excel(writer, sheet_name=sheetName,index = False)
    writer.save()

honororiginSettingsArray = []


honorArray = ['CACHE_CONTROL_AND_EXPIRES','CACHE_CONTROL','EXPIRES']

def fetchOriginSettings(configList):
    for config in configList:
        print("Config:",config)
        myconfig = AkamaiProperty(edgercLocation,config,accountSwitchKey)
        version = getVersionofConfig(myconfig)
        behaviorList = myconfig._getBehaviorParsedList(version)
        honorPresent = False
        hostnameList = myconfig.getHostNames(version)
        item = {}
        item['Config'] = hostnameList
        for pmbehaviors in behaviorList:
            if pmbehaviors['behavior']['name'] == 'caching':
                if pmbehaviors['behavior']['options']['behavior'] in honorArray:
                    item['Honor Origin Settings'] = 'Present'
                    item
                    honorPresent = True
                    break
        if honorPresent == False:
            item['Honor Origin Settings'] = 'Absent'

        honororiginSettingsArray.append(item)
        print('*'*80)


if __name__ == "__main__":
    #getAllProperties()
    configArray = readConfigList()
    fetchOriginSettings(configArray)
    sheetName = 'OriginInfo'
    fileName = accountSwitchKey+'.xlsx'
    writeToExcel(honororiginSettingsArray,fileName,sheetName)






   
