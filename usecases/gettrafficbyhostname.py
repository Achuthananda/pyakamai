from pyakamai import pyakamai
import json

from pyakamai import pyakamai
from datetime import datetime,timedelta
accountSwitchKey = '1-43D6QQ'
pyakamaiObj = pyakamai(accountSwitchKey)
reportingClient = pyakamaiObj.client('reporting')

startIsoTime = ((datetime.today()-timedelta(days=1)).replace(hour=15,minute=30,second=0,microsecond=0) - timedelta(hours=5, minutes=30)).isoformat()
endIsoTime =   ((datetime.today()-timedelta(days=1)).replace(hour=17,minute=30,second=0,microsecond=0) - timedelta(hours=5, minutes=30)).isoformat()


hostname = "www.contents.irctc.co.in"
print(startIsoTime)
print(endIsoTime)

status,data = reportingClient.getTrafficByHostname(startIsoTime,endIsoTime,hostname)
print(json.dumps(data,indent=2))