import os,json
from pyakamai import pyakamai


def writeToExcel(arrayName,fileName,sheetName):
    import pandas
    from openpyxl import load_workbook
    writer = pandas.ExcelWriter(fileName, engine='xlsxwriter')
    df=pandas.json_normalize(arrayName)
    pandas.set_option('display.max_rows', df.shape[0]+1)
    df.to_excel(writer, sheet_name=sheetName,index = False)
    writer._save()

excelList = []
def getNSGroup(accountSwitchKey):
    pyakamaiObj = pyakamai(accountSwitchKey)
    nsconfig = pyakamaiObj.client('ns')
    status,result = nsconfig.liststorageGroups()
    for item in result['items']:
        excelEntry = {}
        excelEntry['StorageGroupName'] = item['storageGroupName']
        excelEntry['StorageGroupId'] = item['storageGroupId']
        excelEntry['CPCode'] = item['cpcodes'][0]['cpcodeId']
        excelEntry['NumberofFiles'] = item['cpcodes'][0]['numberOfFiles']
        excelEntry['Bytes'] = item['cpcodes'][0]['numberOfBytes']
        excelList.append(excelEntry)

    writeToExcel(excelList,'Novi_NSInfo.xlsx','NSInfo')
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='List Storgae Groups')
    parser.add_argument('--accountSwitchKey',required=False, default=None,help='Account SwitchKey')
    args = parser.parse_args()
    accountSwitchKey = args.accountSwitchKey


    getNSGroup(accountSwitchKey)

'''
python3 liststoragegroup.py --accountSwitchKey alsdlsad
'''




   
