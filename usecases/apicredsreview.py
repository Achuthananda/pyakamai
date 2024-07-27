import json
from pyakamai import pyakamai
accountSwitchKey = 'YOUR-ACCOUNT-SWITCH-KEY '
pyakamaiObj = pyakamai() # For Customer, please use pyakamaiObj = pyakamai(None)
overallArray = []


def writeToExcel(arrayName,fileName,sheetName):
    import pandas
    writer = pandas.ExcelWriter(fileName, engine='xlsxwriter')
    df=pandas.json_normalize(arrayName)
    pandas.set_option('display.max_rows', df.shape[0]+1)
    df.to_excel(writer, sheet_name=sheetName,index = False)
    writer._save()


iamClient = pyakamaiObj.client('iam')
status,resultjson = iamClient.listAPIClients()
print(json.dumps(resultjson,indent=2))


for item in resultjson:
    status,credsjson = iamClient.getCredentials(item.get("clientId"))
    if len(credsjson) != 0 :
        for credsitem in credsjson:
            print(credsitem)
            excelItem = {}
            excelItem['APIClientName'] = item.get("clientName")
            excelItem['APIClientID'] = item.get("clientId")
            excelItem['AuthorizedUsers'] = item.get('authorizedUsers')
            excelItem['NotificationEmails'] = item.get('notificationEmails')
            excelItem['credentialId'] = credsitem.get('credentialId')
            excelItem['Status'] = credsitem.get('status')
            excelItem['Expires On'] = credsitem.get('expiresOn')
            overallArray.append(excelItem)


writeToExcel(overallArray,'APIClientsReview.xlsx','sheetName')

    
