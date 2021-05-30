# -*- coding: utf-8 -*-
"""
Created on Thu May 4 10:09:13 2021

@author: jochen
"""
import pandas as pd
import os
from modules.models import Settings

# load settings from properties.csv file
def LoadProperties(propertiesFilePath):
    #df = pd.read_csv("properties.csv")
    df = pd.read_csv(propertiesFilePath)
    #print(df['Name' )
    
    settings = Settings()
    
    for name,value in zip(df['Name'], df['Value'].dropna()):
        #print (name, value)   
        if (name=="acquirer"):
            settings.acquirer=value
        elif (name=="vol_type"):
            settings.vol_type=value
        elif (name=="price_type"):
            settings.price_type=value
        elif (name=="portfolios"):
            settings.portfolios=value
        elif (name=="strategies"):
            settings.strategies=value
        elif (name=="filepath"):
            settings.filepath=value
        elif (name=="env"):
            settings.env=value
        elif (name=="version"):
            settings.version=value
        elif (name=="username"):
            settings.username=value
        elif (name=="password"):
            settings.password=value
        elif (name=="token"):
            settings.token=value
        elif (name=="base_url_prod"):
            settings.base_url_prod=value
        elif (name=="base_url_uat"):
            settings.base_url_uat=value
        elif (name=="base_url_qa"):
            settings.base_url_qa=value
        elif (name=="base_url_dev"):
            settings.base_url_dev=value
        elif (name=="proxy_url"):
            settings.proxy_url=value
        elif (name=="auto_save_settings"):
            settings.auto_save_settings=value       
            
    return settings

# function to save dataframe to excel file
def SaveFile(self, df, filename):
    file_path=self.file_path_val.get()
    
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_date = self.today.strftime('%m%d_%H%M%S')
    
    filename = filename+file_date+'.xlsx'
    print('writing zeno trades to ' + filename)
    df.to_excel(filepath + filename, index=False)
    
    