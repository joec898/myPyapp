# -*- coding: utf-8 -*-
"""
Created on Fri May 14 21:19:46 2021

@author: jc
"""
import json

# Load json file as Python data
def LoadJsonFileAsPythonData(json_file_path):    
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

# Load json file as Dictionary
def LoadJsonFileAsDict(json_file_path):    
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        
    json_dict = json.loads(json.dumps(data))    
    return json_dict

# Save json dictionary to file, beautified
def SaveJsonDictToFile(json_file_path, json_dict):
    with open(json_file_path,'w') as json_file: 
        json.dump(json_dict, json_file, indent=4)
        
# Save json string to file, beautified
def SaveJsonStrToFile(json_file_path, json_str):
    SaveJsonDictToFile(json_file_path, json.loads(json_str))

# Save python data to file, beautified        
def SaveJsonDataToFile(json_file_path, json_data):
    SaveJsonDictToFile(json_file_path, json.loads(json.dumps(json_data)))
    

    