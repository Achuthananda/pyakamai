
from pyakamai import pyakamai 
from pandas import pd

accountSwitchKey = '1-5185s77UassaasN5:1-2RBL'
pyakamaiObj = pyakamai(accountSwitchKey)

ehn_manager  = pyakamaiObj.client('ehn')

missed_ehnlist = []
filename = 'ehnlist.xlsx'
df = pd.read_excel(filename)
for index, row in df.iterrows():
    edgehostname = row['EdgeHostName']
    if edgehostname != 'www.example.com.edgekey.net.':
        status,updateEHNJson = ehn_manager.updateTTL(edgehostname,21600,"JIRA-123:Increase TTL")
        if status != 202:
            print("EdgeHostname:",edgehostname)
            print("Status:",status)
            print("Result:",updateEHNJson)
            missed_ehnlist.append(edgehostname)
        else:
            print("EdgeHostname:",edgehostname)
            print("Status:",status)
            print("Result:Success")
        print('*'*100)

print("Mised EHN List:")
print(missed_ehnlist)
