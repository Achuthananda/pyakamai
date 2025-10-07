from pyakamai import pyakamai
import json

from pyakamai import pyakamai
from datetime import datetime,timedelta
import pandas as pd
from tabulate import tabulate

accountSwitchKey = 'F-AC-407:1-2RBL'
pyakamaiObj = pyakamai(accountSwitchKey)
reportingClient = pyakamaiObj.client('reporting')

endIsoTime = datetime.today().strftime('%Y-%m-%d')
startIsoTime = (datetime.today()-timedelta(days=29)).strftime('%Y-%m-%d')

cpcodeList = [1531585,1572777,1577513,1584676,1633127]

status,result = reportingClient.getURLOffload(startIsoTime,endIsoTime,cpcodeList)
print(json.dumps(result,indent=2))



# Convert your result JSON to DataFrame
df = pd.json_normalize(result['data'])

# Type casting
df['allHitsOffload'] = df['allHitsOffload'].astype(float)
df['allEdgeHits'] = df['allEdgeHits'].astype(int)
df['allOriginHits'] = df['allOriginHits'].astype(int)

# Extract file extension
df['extension'] = df['hostname.url'].str.extract(r'\.([a-z0-9]+)(?:[\?#]|$)', expand=False)

# Top 20 URLs with highest offload
top20 = df.sort_values('allHitsOffload', ascending=False).head(50)

# Bottom 20 URLs with lowest offload
bottom20 = df.sort_values('allHitsOffload', ascending=True).head(100)

# Average offload by extension
avg_offload_by_ext = (
    df.groupby('extension')['allHitsOffload']
    .mean()
    .reset_index()
    .sort_values('allHitsOffload', ascending=False)
)

# Pretty print
print("🔝 Top 20 URLs by Offload %:")
print(tabulate(top20[['hostname.url', 'allHitsOffload']], headers='keys', tablefmt='pretty'))

print("\n🔻 Bottom 20 URLs by Offload %:")
print(tabulate(bottom20[['hostname.url', 'allHitsOffload']], headers='keys', tablefmt='pretty'))

print("\n📊 Average Offload % by Extension:")
print(tabulate(avg_offload_by_ext, headers='keys', tablefmt='pretty'))