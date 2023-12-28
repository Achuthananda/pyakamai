
import json
import pandas 
from openpyxl import load_workbook
from pyakamai import pyakamai
accountSwitchKey = 'BAC-asC-1IE2OasdasdH8'
pyakamaiObj = pyakamai(accountSwitchKey)    
ldsClient = pyakamaiObj.client('lds')


def writeToExcel(arrayName,fileName,sheetName):
    writer = pandas.ExcelWriter(fileName, engine='xlsxwriter')
    df=pandas.json_normalize(arrayName)
    pandas.set_option('display.max_rows', df.shape[0]+1)
    df.to_excel(writer, sheet_name=sheetName,index = False)
    writer.save()

ldsList = ldsClient.listLogConfigurations('cpcode-products')
#print(len(ldsList))

fp = open('iplcpcodes.txt','r').readlines()
fp = [int(x.strip()) for x in fp]

ldsArray = []

for cpcode in fp:
    item = {}
    item['CPCode'] = cpcode
    item['Status'] = 'Inactive'
    item['StorageDestinaionType'] = ''
    item['NSGroup'] = ''
    item['NSCPCode'] = ''
    item['NSDirectory'] = ''
    for lds in ldsList:
        if str(cpcode) in lds['logSource']['id']:
            item['Status'] = lds['status']
            item['StorageDestinaionType'] = lds['deliveryDetails']['type']
            item['NSGroup'] = lds['deliveryDetails']['domainPrefix']
            item['NSCPCode'] = lds['deliveryDetails']['cpcodeId']
            item['NSDirectory'] = lds['deliveryDetails']['directory']

    ldsArray.append(item)
    

writeToExcel(ldsArray,'LDS.xlsx','LDS')



'''ldsList = akamaiLDS.listConfigs('gtm-properties')
ldsList = akamaiLDS.listConfigs('cpcode-products')
ldsList = akamaiLDS.listConfigs('cpcode-products')'''