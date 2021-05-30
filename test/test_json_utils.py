# -*- coding: utf-8 -*-
"""
Created on Sun May 16 15:04:08 2021

@author: jc
"""
import sys
sys.path.append("../")
#sys.path.append('C:/Projects/myPyguiPractice/')
from modules.json_utils import LoadJsonFileAsDict,SaveJsonDictToFile

def test_json_utils_loadJsonFileAsDict(): 
    jsonFilePath = "../properties.json"
    json_dict = LoadJsonFileAsDict(jsonFilePath)
    assert json_dict["env"] == "production"
        
def test_json_utils_SaveJsonDictToFile():
    jsonFilePath = "../properties.json"
    jsonFilePath2 = "../properties2.json"
    json_dict = LoadJsonFileAsDict(jsonFilePath)
    json_dict["version"] = "v100"
    SaveJsonDictToFile(jsonFilePath2,json_dict)
    json_dict = LoadJsonFileAsDict(jsonFilePath2)
    assert json_dict["version"] == "v100"