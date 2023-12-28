from pyakamai import pyakamai 
import texttable as tt

accountSwitchKey = '1-5185s77UassaasN5:1-2RBL'
pyakamaiObj = pyakamai(accountSwitchKey)

china_manager  = pyakamaiObj.client('chinacdn')

file = open("hostnamelist.txt","r")
hostnames = file.readlines()

for hostname in hostnames:
    newhostname = "".join(hostname.split())
    print(newhostname)
    result = china_manager.createPropertyHostname(newhostname,287,8,156114)
    print(result)
    result = china_manager.whiteList(newhostname)
    print(result)
