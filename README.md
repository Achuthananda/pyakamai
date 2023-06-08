# pyakamai - The Akamai SDK for Python
[![Package Version](http://img.shields.io/pypi/v/boto3.svg?style=flat)](https://pypi.org/project/pyakamai/)
[![Python Versions](https://img.shields.io/pypi/pyversions/boto3.svg?style=flat)](https://pypi.org/project/pyakamai/)

pyakamai is the Akamai CDN Software Development Kit (SDK) for Python, which allows Python developers to write software that makes use of services like Akamai Delivery ,Security Configs and many more. 

pyakamai (pronounced pie-akamai) is maintained and published by Achuthananda and a group of enthusiastic Akamai developers.

The advantage of pyakamai is application developers need not know about the underlying API calls and their usage. Application developers can just focus on getting their work done programmatically using the objects of pyakamai.


### Getting Starterd
In order to use this configuration, you need to:
* Set up your credential files as described in the [doc](https://techdocs.akamai.com/developer/docs/set-up-authentication-credentials).
* When working through this process you need to give grants for the various APIs as needed. You can have any number of sections in your .edgerc file.


### Install pip package available
```
$ pip install pyakamai
```

or install from source with:

```
$ git clone https://github.com/Achuthananda/pyakamai
$ cd pyakamai
$ python -m pip install -r requirements.txt
$ python -m pip install -e .
```


# Using pyakamai

## Using AkamaiProperty

### Print Hostnames
```
>>> from pyakamai import pyakamai
>>> akamaiconfig = pyakamaiObj.client('property')
>>> akamaiconfig.config('test_bulkseach_update_1')
>>> hostnamesList = akamaiconfig.getHostNames(akamaiconfig.getProductionVersion())
>>> for hostname in hostnamesList:
>>>     print(hostname)
```

### Print Basic Information
```
>>> akamaiconfig.printPropertyInfo()
Property Name: test_bulkseach_update_1
Contract Id: ctr_C-1IE2OHM
Group Id: grp_163363
Active Staging Version: 18
Active Production Version: 18
```

### Create a new version
```
>>> akamaiconfig.createVersion(18)
'78'
```

### Get rule Tree
```
>>>akamaiconfig.getRuleTree(18)
{'accountId': 'act_B-C-1IE2OH8', 'contractId': 'ctr_C-1IE2OHM', 'groupId': 'grp_163363', 'propertyId': 'prp_605086', 'propertyName': 'test_bulkseach_update_1', 'propertyVersion': 18, 'etag': 'd0d28a6b71e665144955f7f7e1ff214933d119d7', 'rules':.....}
```

### Activate the config
```
>>>akamaiconfig.activateStaging(18,"testing activation",["apadmana@akamai.com"])
True
```

## Using AkamaiEDNS
```
from pyakamai import pyakamai
pyakamaiObj = pyakamai('ACCOUN-SWITCH-KEY')

ednsClient = pyakamaiObj.client('edns')
for ednszone in ednsClient.listZones()['zones']:
    print(ednszone['zone'])

```
