from akamaiproperty import AkamaiProperty,AkamaiPropertyManager
import os
import pandas
import numpy as np

edgercLocation = '~/.edgerc'
edgercLocation = os.path.expanduser(edgercLocation) # expand tilde. Python SDK doesn't handle tilde paths on Windows
configTobehaviorDict = {}
aggregatedBehaviorList = []

finalData =[]


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
    fileName = accountSwitchKey +  '_configs.txt'
    if not os.path.isfile(fileName):
        pm = AkamaiPropertyManager(edgercLocation,accountSwitchKey)
        propertiesList = pm.getallProperties()
        np.savetxt(fileName, np.array(propertiesList), fmt="%s")

def getVersionofConfig(akconfig):
    version = 0
    prodVersion = akconfig.getProductionVersion()
    stagingVersion = akconfig.getStagingVersion()
    latestVersion = akconfig.latestVersion

    version = prodVersion
    if version == 0:
        version = stagingVersion
        if version == 0:
            version = latestVersion

    return version 


def getUsedBehaviors(configArray,accountSwitchKey):
    global configTobehaviorDict
    global aggregatedBehaviorList
    index = 1
    for config in configArray:
        print("{}.Fetching the features from the config {}".format(index,config))
        akconfig = AkamaiProperty(edgercLocation,config,accountSwitchKey)
        version = getVersionofConfig(akconfig)
        usedbehaviors = akconfig.getUsedBehaviors(version)
        availableBehaviors = akconfig.getAvailableFeatures(version)
        usedbehaviors = list(set(usedbehaviors))
        aggregatedBehaviorList = aggregatedBehaviorList + availableBehaviors
        configTobehaviorDict[config] = usedbehaviors
        index = index + 1


def mapBehaviors():
    global finalData
    for keys in configTobehaviorDict:
        item = {}
        item['Config'] = keys
        for x in aggregatedBehaviorList:
            if x in configTobehaviorDict[keys]:
                item[x] = 'Present'
            else:
                item[x] = 'Absent'
        finalData.append(item)    



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Support Ticket Raising Tool')
    parser.add_argument('--accountSwitchKey',required=True, default=None,help='Account SwitchKey')

    args = parser.parse_args()
    accountSwitchKey = args.accountSwitchKey

    if accountSwitchKey == None:
        print("Please Enter the Account SwitchKey in the format shown below")
        print("python3 featurematrix.py --accountSwitchKey B-3-TVBY9")
        exit(1)

    print("Fetching all the configs of the account!")
    getAllProperties(accountSwitchKey)
    configArray = readConfigList(accountSwitchKey)
    getUsedBehaviors(configArray,accountSwitchKey)

    print(aggregatedBehaviorList)
    print(configTobehaviorDict)    

    mapBehaviors()

    excelFileName = accountSwitchKey + '.xlsx'
    writeToExcel(finalData,excelFileName,'featureMatrix')


#accountSwitchKey = 'F-AC-1526355:1-2RBL' #eterno