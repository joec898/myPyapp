# -*- coding: utf-8 -*-
"""
Created on Thu May 3 9:1:11 2021

@author: jochen
"""
import tkinter as tk
from frames.main_frame import MainFrame
import logging
import logging.config

class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setup_logging()
        
        self.geometry("800x600")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.minsize(width=600, height=300)
        self.title("Test App")
        
        self.option_add("*font", "lucida 8")
        
        self.main_frame = MainFrame(self)
        
        self.main_frame.grid(row=0, column=0, sticky="NSEW") 
        
    def setup_logging(self):
        if __name__ == '__main__':
            logging.config.fileConfig(fname='logging.conf')
            #logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=True)
            
        self.logger = logging.getLogger()
        self.logger.info('Starting pythong app...')
         
        
root = MyApp()
root.mainloop()
