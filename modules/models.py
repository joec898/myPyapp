# -*- coding: utf-8 -*-
"""
Created on Thu May 3 11:10:13 2021

@author: jochen
"""

class Settings:
    version = ""
    acquirer = ""
    vol_type = 0
    price_type = 1
    portfolios = ""
    strategies = ""
    username = ""
    password = ""
    filepath = ""
    token = ""
    asof_date = ""
    auto_save_settings = 1

class Settings2:
    def __init__(self,version,acquirer,vol_type,price_type,portfolios,strategies,username,password,filepath,token):
        self.version = version            
        self.acquirer= acquirer   
        self.vol_type = vol_type
        self.price_type = price_type
        self.portfolios = portfolios
        self.strategies = strategies
        self.username = username
        self.password = password
        self.filepath = filepath
        self.token = token
        self.asof_date = None
        self.auto_save_settings = None
        
class Settings3:
    def __init__(self):
        self.version = None            
        self.acquirer= None   
        self.vol_type = None
        self.price_type = None
        self.portfolios = None
        self.strategies = None
        self.username = None
        self.password = None
        self.filepath = None
        self.token = None
        self.asof_date = None
    
    @property
    def version(self):
        return self.version
    
    @property
    def acquirer(self):
        return self.acquirer
    
    @property
    def vol_type(self):
        return self.price_type
    
    @property
    def price_type(self):
        return self.price_type
    
    @property
    def portfolios(self):
        return self.portfolios
    
    @property
    def strategies(self):
        return self.strategies
   
    @property
    def username(self):
        return self.username

    @property
    def password(self):
        return self.password

    @property
    def filepath(self):
        return self.filepath

    @property
    def token(self):
        return self.token

    @property
    def asof_date(self):
        return self.asof_date

