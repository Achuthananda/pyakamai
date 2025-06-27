from pyakamai import pyakamai
import json

def writeToExcel(arrayName,fileName,sheetName):
    import pandas
    writer = pandas.ExcelWriter(fileName, engine='xlsxwriter')
    df=pandas.json_normalize(arrayName)
    pandas.set_option('display.max_rows', df.shape[0]+1)
    df.to_excel(writer, sheet_name=sheetName,index = False)
    writer._save()


accountSwitchKey="F-AC-642606"
pyakamaiObj = pyakamai(accountSwitchKey=accountSwitchKey,edgercLocation='~/.edgerc', section='default',debug=False, verbose=False)

accountObj = pyakamaiObj.client('propertymanager')
propertiesList = accountObj.getallProperties()
print(propertiesList)

overallArray =[]
for config in propertiesList:
    print('Pulling the unused behaviors for {}'.format(config))
    akamaiconfig = pyakamaiObj.client('property')
    akamaiconfig.config(config)
    item = {}
    item['Config'] = config
    item['UsedBehaviors'] = akamaiconfig.getUsedBehaviors(akamaiconfig.getVersionofConfig())
    item['UnusedBehaviors'] = akamaiconfig.getUnusedBehaviors(akamaiconfig.getVersionofConfig())
    print(item)
    overallArray.append(item)

writeToExcel(overallArray,'UnusedBehaviors.xlsx','sheetName')
