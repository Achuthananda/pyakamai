import pandas as pd
from pyakamai import pyakamai
import json
# Configure the logging
import logging
log_filename = "app.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


missedZoneList = []
accountSwitchKey = 'B-C-1IE2OH8'
pyakamaiObj = pyakamai(accountSwitchKey)    
ednsClient = pyakamaiObj.client('edns')
      
filename = 'zonelist.xlsx'
df = pd.read_excel(filename)

for index, row in df.iterrows():
    zone = row['Zone']
    if zone != '1achuthtestsecondary.com':
        message = "Fetching the zone settinsg for zone {}".format(zone)
        logging.info(message)
        zonesettings = ednsClient.getZoneSettings(zone)
        print(json.dumps(zonesettings,indent=2))
        
        del zonesettings['versionId']
        del zonesettings['lastActivationDate']
        del zonesettings['lastModifiedDate']
        del zonesettings['lastModifiedBy']
        del zonesettings['activationState']

        ipList = row["MasterDNSIP"].split(',')
        ipList = [x.strip() for x in ipList]

        zonesettings['masters'] = ipList  #If need to replace the IPs

        status = ednsClient.updateZoneSettings(zone,payload = zonesettings)
        if status == True:
            message = "Updated the IPs for the zone {}".format(zone)
            logging.info(message)
        else:
            missedZoneList.append(zone)
            message = "Failed to update the IPs for the zone {}".format(zone)
            logging.error(message)
    message = '*'*80
    print(message)
    logging.info(message)
    
print("Following zones were missed to update")
print(missedZoneList)