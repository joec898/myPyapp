# -*- coding: utf-8 -*-
"""
Created on Thu May 3 10:12:22 2021

@author: jochen
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import datetime as dt
import pandas as pd
import logging
from frames.data_frame import DataFrame, BlankFrame 
from frames.param_frame import ParamFrame
from frames.settings_frame import SettingsFrame
from modules.json_utils import LoadJsonFileAsDict,SaveJsonDictToFile
from modules.risktrade_utils import DownloadTrades,ProcessExistingTrades,ProcessNewTrades,ProcessZenoTrades

class MainFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)       
        self.logger = logging.getLogger(__name__)
        self.logger.debug("starting main frame...")
        
        self.priceTypes = ["Live", "Settle"]
        
        self.settings = LoadJsonFileAsDict("properties.json")
    
        self.today = dt.datetime.today()
        self.asOfDate=self.today
        
        # populate settings info for fields in frames
        self.date_val=tk.StringVar(value=self.asOfDate.strftime('%m/%d/%Y'))
        
        self.acquirer_val=tk.StringVar(value=self.settings["acquirer"])
        self.strategies_val=tk.StringVar(value=self.settings["strategies"])
        self.portfolios_val=tk.StringVar(value=self.settings["portfolios"])
        
        self.vol_type_val=tk.StringVar(value=self.settings.get("vol_type"))
        self.vol_type_index_val=tk.IntVar(value=self.settings.get("vol_type_index"))
        self.price_type_val=tk.StringVar(value=self.settings.get("price_type"))
        self.price_type_index_val=tk.IntVar(value=self.settings.get("price_type_index"))

        self.env_val=tk.StringVar(value=self.settings["env"])
        self.version_val=tk.StringVar(value=self.settings["version"])
        self.username_val=tk.StringVar(value=self.settings["username"])
        self.password_val=tk.StringVar(value=self.settings["password"])
        self.filepath_val=tk.StringVar(value=self.settings["filepath"])
        self.token_val=tk.StringVar(value=self.settings["token"]) 
        self.auto_save_settings_val=tk.IntVar(value=self.settings["auto_save_settings"])
        
        self.status_messsage_val = tk.StringVar(value="Ready...")
        self.top_frames = {}
        self.bottom_frames = {}
        
        top_frame = ttk.Frame(
            self,
            padding="5 2 5 2",
            borderwidth = 5,
            relief = 'sunken'
        )
        top_frame.grid(row=0, column=0, padx=2, pady=2, sticky="EWNS")
        top_frame.columnconfigure(0, weight=1) 
        top_frame.rowconfigure(0, weight=1)

        mid_frame = ttk.Frame(
            self,
            padding="2 2 2 2", 
            relief = 'sunken')
        mid_frame.grid(row=1, column=0, padx=2, pady=2, sticky="NSEW")
        mid_frame.columnconfigure(0, weight=1)
        mid_frame.rowconfigure(0, weight=1)

        self.bottom_frame = ttk.Frame(
            self,
            padding="5 2 5 2",
            borderwidth = 5,
            relief = 'sunken')
        self.bottom_frame.grid(row=2, column=0, padx=2, pady=2, sticky="NSEW")
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)

        self.status_frame = ttk.Frame(
            self,
            padding="2 2 2 2", 
            height=10,
            relief = 'sunken')
        self.status_frame.grid(row=3, column=0, padx=2, pady=2, sticky="NSEW")
        #self.status_frame.columnconfigure(0, weight=1)
        self.status_frame.rowconfigure(0, weight=1)
        
        self.status_label = ttk.Label(
            self.status_frame,
            textvariable=self.status_messsage_val
        )
        self.status_label.grid(column=0, row=0, sticky="W", pady=2)
        self.status_label.pack(expand=True, fill='both')
        
        # top_frames 
        param_frame = ParamFrame(top_frame, self, lambda: self.show_top_frame(SettingsFrame))
        param_frame.grid(row=0, column=0, sticky="NSEW", pady=2) 
        
        settings_frame = SettingsFrame(top_frame, self, lambda: self.show_top_frame(ParamFrame))
        settings_frame.grid(row=0, column=0, sticky="NSEW", pady=2)         

        self.top_frames[ParamFrame] = param_frame
        self.top_frames[SettingsFrame] = settings_frame
        
        # bottom frames
        #    Data 
        self.df_existing_trades = pd.DataFrame()
        self.df_new_trades = pd.DataFrame()
        self.df_zeno_trades = pd.DataFrame()
        
        blank_frame = BlankFrame(self.bottom_frame, self)
        blank_frame.grid(row=0, column=0, sticky="NSEW", pady=2)  
        
        data_frame = DataFrame(self.bottom_frame, self)
        data_frame.grid(row=0, column=0, sticky="NSEW")
        
        self.bottom_frames[BlankFrame] = blank_frame
        self.bottom_frames[DataFrame] = data_frame

        # buttons for main frame in mid_frame
        submit_button = ttk.Button(
            mid_frame,
            text="Submit Request",             
            command=self.download_trades,
            cursor="hand2"  
        )
        submit_button.grid(row=0, column=0, sticky="E", pady=2)

        save_button = ttk.Button(
            mid_frame,
            text="Save",             
            command=self.save_trades_to_files,
            cursor="hand2"  
        )
        save_button.grid(row=0, column=1, sticky="E", pady=2)

        clear_button = ttk.Button(
            mid_frame,
            text="Clear",             
            command=self.clear_cache,
            cursor="hand2"  
        )
        clear_button.grid(row=0, column=2, sticky="E", pady=2)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(2, weight=1)

        self.show_top_frame(ParamFrame)
        self.show_bottom_frame(BlankFrame)
        
        '''
        def configure_window_size(event):
            self.configure(top_frame, width=self.winfo_width())

        self.bind("<Configure>", configure_window_size)
        #messagebox.showinfo('title', 'hello')
        '''

    def show_top_frame(self, container):
        frame = self.top_frames[container]     
        frame.tkraise()
        
    def show_bottom_frame(self, container):
        frame = self.bottom_frames[container]     
        frame.tkraise()
        
    def clear_cache(self):
        self.df_existing_trades = pd.DataFrame()
        self.df_new_trades = pd.DataFrame()
        self.df_zeno_trades = pd.DataFrame()
        self.show_bottom_frame(BlankFrame)
        self.update_statu_message("Trades data cleared. ")

    def update_statu_message(self, msg):
        self.logger.info(msg)
        self.status_messsage_val.set(msg)
        
    def save_settings_when_unchecked(self):
        #msg.showinfo(title="checkbox", message="auto_save_settings_val: " + str(self.auto_save_settings_val.get()))
        if self.auto_save_settings_val.get() == 0:
            self.populate_settings()
            SaveJsonDictToFile("properties.json", self.settings)
            self.logger.info("Settings saved for auto save setting is unchecked.")
 
        
    def populate_settings(self):
        # update possible use inputs for settings        
        self.asOfDate = dt.datetime.strptime(self.date_val.get(),'%m/%d/%Y')        
        self.settings["asof_date"] = self.asOfDate.strftime('%Y-%m-%d')
        #print(self.settings.asof_date) 
        self.settings["acquirer"] = self.acquirer_val.get()
        self.settings["strategies"] = self.strategies_val.get()
        self.settings["portfolios"] = self.portfolios_val.get()
        self.settings["vol_type"] = self.vol_type_val.get()
        self.settings["price_type"] = self.price_type_val.get()
        self.settings["env"] = self.env_val.get()
        self.settings["version"] = self.version_val.get()
        self.settings["username"] = self.username_val.get()
        self.settings["password"] = self.password_val.get()
        self.settings["filepath"] = self.filepath_val.get()
        self.settings["token"] = self.token_val.get()
        
        self.settings["vol_type_index"] = self.priceTypes.index(self.vol_type_val.get())
        self.settings["price_type_index"] = self.priceTypes.index(self.price_type_val.get())
        
        self.settings["auto_save_settings"] = self.auto_save_settings_val.get()

        
    def download_trades(self):
        
        if len(self.token_val.get()) < 120:
            self.update_statu_message("Please make sure token is valid... ")     
            return

        self.update_statu_message("Downloading trades... ")
        self.show_bottom_frame(BlankFrame)
        
        self.populate_settings()
        
        '''
        # update possible use inputs for settings        
        self.asOfDate = dt.datetime.strptime(self.date_val.get(),'%m/%d/%Y')        
        self.settings.asof_date = self.asOfDate.strftime('%Y-%m-%d')
        #print(self.settings.asof_date) 
        self.settings.acquirer = self.acquirer_val.get()
        self.settings.strategies = self.strategies_val.get()
        self.settings.portfolios = self.portfolios_val.get()
        self.settings.vol_type = self.vol_type_val.get()
        self.settings.price_type = self.price_type_val.get()
        self.settings.env = self.env_val.get()
        self.settings.version = self.version_val.get()
        self.settings.username = self.username_val.get()
        self.settings.password = self.password_val.get()
        self.settings.filepath = self.filepath_val.get()
        self.settings.token = self.token_val.get()

        self.settings["vol_type_index"] = self.priceTypes.index(self.vol_type_val.get())
        self.settings["price_type_index"] = self.priceTypes.index(self.price_type_val.get())
        
        self.settings["auto_save_settings"] = self.auto_save_settings_val.get()
        '''
        
        if self.settings["auto_save_settings"]  == 1:
            self.logger.info("Settings saved")
            SaveJsonDictToFile("properties3.json", self.settings)
            
        try:
            # download data in dataFrames
            self.df_detail = DownloadTrades(self.settings)
            
            # update the timestamp    
            self.today = dt.datetime.today()
    
            df_main = ProcessExistingTrades(self.df_detail)
            self.df_existing_trades = df_main
           
            self.df_new_trades = ProcessNewTrades(df_main, self.settings)          
            
            self.df_zeno_trades = ProcessZenoTrades(df_main, self.settings)
            
            #print("loading data_frame...")
            self.update_statu_message("Downloading trades completed. ")
            #if not self.df_existing_trades.empty: 
            data_frame = DataFrame(self.bottom_frame, self)
            data_frame.grid(row=0, column=0, sticky="NSEW")        
            self.bottom_frames[DataFrame] = data_frame    
            self.show_bottom_frame(DataFrame)
        except Exception as e:
            print(e.args)
            self.update_statu_message("Unexpected errors during trade data download. ")

                   
    def save_trades_to_files(self):
        # save trades        
        if self.df_existing_trades.empty == False:
            self.update_statu_message("Saving trade data to files... ")
            
            file_date = self.today.strftime('%m%d %H%M%S')  
            file_name = 'rt_existing_db_' + file_date + '.csv'
            print('writing rt existing trades to '+ file_name)
            self.df_existing_trades.to_csv(self.settings.filepath + file_name, index=False)
    
            filename = 'rt_db_'+file_date+'.csv'
            print('writing new rt trades to '+ filename)
            self.df_new_trades.to_csv(self.settings.filepath + filename, index=False)
            
            filename = 'zeno_db_'+file_date+'.xlsx'
            print('writing zeno trades to ' +filename)
            self.df_zeno_trades.to_excel(self.settings.filepath + filename, index=False)
            self.update_statu_message("Trade data to files saved. ")
        else:
            self.update_statu_message("Not trades data to save...")
            #print("Not trades data to save...")

     
