import texttable as tt

from pyakamai import pyakamai 
import texttable as tt

accountSwitchKey = '1-5185s77UassaasN5:1-2RBL'
pyakamaiObj = pyakamai(accountSwitchKey)

china_manager  = pyakamaiObj.client('chinacdn')


#property_info = china_manager.listProperties()
#states_info = china_manager.getProvisionStatus("DEPROVISIONED")

#print(json.dumps(states_info,indent=4))


list_hostnames = ['www.example.com.cn']

ParentTable = tt.Texttable()
ParentTable.set_cols_width([30,15,15])
ParentTable.set_cols_align(['c','c','c'])
ParentTable.set_cols_valign(['m','m','m'])
Parentheader = ['HostName','Provision Status','China Provision Status']
ParentTable.header(Parentheader)

result = china_manager.getProvisionStatus('WHITELISTED')
for items in result:
    for china_info in result[items]:
        if china_info['hostname'] in list_hostnames:
            Parentrow = [ china_info['hostname'],china_info['provisionState'],china_info['partnerStates']['CNC']['provisionState']]
            ParentTable.add_row(Parentrow)
            list_hostnames.remove(china_info['hostname'])
MainParentTable = ParentTable.draw()
print(MainParentTable)
