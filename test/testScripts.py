# -*- coding: utf-8 -*-
"""
Created on Thu May 11 4:12:13 2021

@author: jochen
"""
import pandas as pd
from modules.utils import LoadProperties
from modules.json_utils import LoadJsonFileAsDict,SaveJsonDictToFile
from modules.risktrade_utils import TestDownloadTrades

def test_risktrade_utils():
    settings = LoadProperties("properties.csv")
    settings.asof_date = "2021-05-11" #dt.datetime.today().strftime('%Y-%m-%d 00:00:00')""
    TestDownloadTrades(settings)
    
def dataFrame_test():
    df = pd.read_csv("CZ_VS_SDVF.csv")
    columns = df.columns.tolist()
    for i in columns: 
        print(i) 
        
    for index, row in df.iterrows():  
        vals = ""
        for i in columns:
            vals = vals + str(row[i]) + ","
        
        print(vals[:-1])
        
        #print( str(row["CMDTY"]) + ", " + str(row["Month"]) + ", " + str(row["DaystoExp"]) + ", " + str(row["1DayFac"]))
    
    
def test_json_utils(): 
    jsonFilePath = "properties.json"
    jsonFilePath2 = "properties2.json"
    json_dict = LoadJsonFileAsDict(jsonFilePath)
    
    print(json_dict)
    print(json_dict.get("portfolios"))
    print(json_dict["version"])
    json_dict["version"]= "v155"
    print(json_dict["version"])
    
    SaveJsonDictToFile(jsonFilePath2, json_dict)
    
priceTypes = ["Live", "Settle"]
print(priceTypes.index("Live"))     
#test_json_utils()
#dataFrame_test()       
#test_risktrade_utils()