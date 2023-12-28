from akamaiproperty import AkamaiPropertyManager
import pandas
import os
import argparse
import traceback



edgercLocation = '~/.edgerc'
edgercLocation = os.path.expanduser(edgercLocation) # expand tilde. Python SDK doesn't handle tilde paths on Windows


directory = 'Outputs/SS_SR_Review'
if not os.path.exists(directory):
    os.makedirs(directory)  # Create the 'output' directory if it doesn't exist


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='SS and SR Review')
    # Storage migration
    parser.add_argument('--accountSwitchKey',required=True, default=None,help='Account SwitchKey')
    args = parser.parse_args()
    print(args)

    try:
        file_name = os.path.join(directory, args.accountSwitchKey + '_ssreview.xlsx')

        pmHandler = AkamaiPropertyManager(edgercLocation,args.accountSwitchKey)

        jsonPath = "$..behaviors[?(@.name == 'siteShield')]"
        print("Fetching Configs with SS Implemented")
        ssproperties = pmHandler.bulkSearch(jsonPath)
        print(ssproperties)
        

        jsonPath = "$..behaviors[?(@.name == 'sureRoute')]"
        print("Fetching Configs with SR Implemented")
        srproperties = pmHandler.bulkSearch(jsonPath)
        print(srproperties)

        print("Fetching Configs with SS Implemented and SR Unimplemented")
        unimplementedProperties = list(set(ssproperties) - set(srproperties))

        sspropertiesMap = []
        for prop in ssproperties:
            item = {}
            item['SS Properties'] = prop
            sspropertiesMap.append(item)

        srpropertiesMap = []
        for prop in srproperties:
            item = {}
            item['SR Properties'] = prop
            srpropertiesMap.append(item)

        unimplementedPropertiesMap = []
        for prop in unimplementedProperties:
            item = {}
            item['SR Unimplemented Properties'] = prop
            unimplementedPropertiesMap.append(item)


        writer = pandas.ExcelWriter(file_name, engine='xlsxwriter')

        #Write the SS Properties in Sheet1
        df1=pandas.json_normalize(sspropertiesMap)
        pandas.set_option('display.max_rows', df1.shape[0]+1)
        df1.to_excel(writer, sheet_name='SS Properties',index = False)

        #Write the SR Properties in Sheet2
        df2=pandas.json_normalize(srpropertiesMap)
        pandas.set_option('display.max_rows', df2.shape[0]+1)
        df2.to_excel(writer, sheet_name='SR Properties',index = False)

        #Write the SS without SR Properties in Sheet3
        df3=pandas.json_normalize(unimplementedPropertiesMap)
        pandas.set_option('display.max_rows', df3.shape[0]+1)
        df3.to_excel(writer, sheet_name='SS Without SR Properties',index = False)

        writer._save()
        print("Done! Please check SS_SRInfo.xlsx file in the directory")


    except Exception as e:
        track = traceback.format_exc()
        print(track)
    

'''
python3 SS_SR_Info.py --accountSwitchKey 1-1asdasddsa5LAXIF
'''