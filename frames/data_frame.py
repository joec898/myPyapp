# -*- coding: utf-8 -*-
"""
Created on Thu May 10 9:02:13 2021

@author: jochen
"""
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext


class BlankFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.tabControl = ttk.Notebook(self)
        df = pd.DataFrame()
        tab1 = DataTreeView(self.tabControl,df)
        tab2 = DataTreeView(self.tabControl,df)
        tab3 = DataTreeView(self.tabControl,df)
 
        self.tabControl.add(tab1, text ='Existing Trades')
        self.tabControl.add(tab2, text ='New Trades')
        self.tabControl.add(tab3, text ='Zeno Trades') 
        
        #tabControl.grid(row=0, column=0, padx=2, pady=2, sticky="EWNS")
        self.tabControl.grid(row=0, column=0,  sticky="EWNS")
        self.tabControl.pack(expand = 1, fill ="both")
       
        
class DataFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.tabControl = ttk.Notebook(self)
          
        tab1 = DataTreeView(self.tabControl,controller.df_existing_trades)
        tab2 = DataTreeView(self.tabControl,controller.df_new_trades)
        tab3 = DataTreeView(self.tabControl,controller.df_zeno_trades)
        tab4 = ScollTextView(self.tabControl)
          
        self.tabControl.add(tab1, text ='Existing Trades')
        self.tabControl.add(tab2, text ='New Trades')
        self.tabControl.add(tab3, text ='Zeno Trades')
        self.tabControl.add(tab4, text ='Additional Trades')
        
        #tabControl.grid(row=0, column=0, padx=2, pady=2, sticky="EWNS")
        self.tabControl.grid(row=0, column=0,  sticky="EWNS")
        self.tabControl.pack(expand = 1, fill ="both")        


class ScollTextView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
 
        st = scrolledtext.ScrolledText(self, width=50,  height=10)
        st.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        
class DataTreeView(ttk.Notebook):
        def __init__(self, parent, df):
            super().__init__(parent)
            
            #df = controller.df_existing_trades
            columns = df.columns.tolist() 
            
            tv = ttk.Treeview(self, columns=columns, show='headings')
            tv.pack(side='left', fill='both')

            # add column headings
            for i in columns: 
                 tv.heading(i, text=i)
                 tv.column(i,width=60,anchor='center')
   
            sb = ttk.Scrollbar(self, orient='vertical')
            sb.pack(side='right', fill='y')
            
            tv.config(yscrollcommand=sb.set)
            sb.config(command=tv.yview)
                
            # insert data for each row 
            rowIndex = 0
            for index, row in df.iterrows():
                vals = ""
                for i in columns:
                    vals += str(row[i]) + ' '
                
                # exmaple for row 1
                # tv.insert(parent='', index=0, iid=0, values=("vineet", "e11", 1000000.00))
                tv.insert(parent='', index=rowIndex, iid=rowIndex, values=(vals[:-1]))
                rowIndex += 1
    
            self.grid(sticky = "NSWE" )
            self.treeview = tv
            self.grid_rowconfigure(0, weight = 1)
            self.grid_columnconfigure(0, weight = 1)
            
            
class DataTreeViewX(ttk.Notebook):
        def __init__(self, parent, controller):
            super().__init__(parent)    
 
            tv = ttk.Treeview(self, columns=(1, 2, 3), show='headings', height=8)
            tv.pack(side='left')
            
            tv.heading(1, text="name")
            tv.heading(2, text="eid")
            tv.heading(3, text="Salary")
            
            sb = ttk.Scrollbar(self, orient='vertical') 
            
            tv.config(yscrollcommand=sb.set)
            sb.config(command=tv.yview)
            
            tv.insert(parent='', index=0, iid=0, values=("vineet", "e11", 1000000.00))
            tv.insert(parent='', index=1, iid=1, values=("anil", "e12", 120000.00))
            tv.insert(parent='', index=2, iid=2, values=("ankit", "e13", 41000.00))
            tv.insert(parent='', index=3, iid=3, values=("Shanti", "e14", 22000.00))
            tv.insert(parent='', index=4, iid=4, values=("vineet", "e11", 1000000.00))
            tv.insert(parent='', index=5, iid=5, values=("anil", "e12", 120000.00))
            tv.insert(parent='', index=6, iid=6, values=("ankit", "e13", 41000.00))
            tv.insert(parent='', index=7, iid=7, values=("Shanti", "e14", 22000.00))
            tv.insert(parent='', index=8, iid=8, values=("vineet", "e11", 1000000.00))
            tv.insert(parent='', index=9, iid=9, values=("anil", "e12", 120000.00))
            tv.insert(parent='', index=10, iid=10, values=("ankit", "e13", 41000.00))
            tv.insert(parent='', index=11, iid=11, values=("Shanti", "e14", 22000.00))
            
        
class DataTreeViewXX(ttk.Notebook):
        def __init__(self, parent, controller):
            super().__init__(parent)             
            
            tv = ttk.Treeview(self)
            tv['columns'] = ('Name', 'Mobile', 'course')
            tv.heading("#0", text='RollNo', anchor='w')
            tv.column("#0", anchor="w")
            tv.heading('Name', text='Name')
            tv.column('Name', anchor='center', width=100)
            tv.heading('Mobile', text='Mobile')
            tv.column('Mobile', anchor='center', width=100)
            tv.heading('course', text='course')
            tv.column('course', anchor='center', width=100)
            
            tv.grid(sticky = "NSWE")
            self.treeview = tv
            self.grid_rowconfigure(0, weight = 1)
            self.grid_columnconfigure(0, weight = 1)
         
class DataFrameXXX(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent) 

        group1 = ttk.LabelFrame(self, text="Text Box")
        group1.grid(row=0, column=0, columnspan=3, padx=2, pady=2, sticky="EWNS")

        # Create the textbox
        txtbox = scrolledtext.ScrolledText(group1)
        txtbox.grid(row=0, column=0, sticky="EWNS")

        group1.rowconfigure(0, weight=1)
        group1.columnconfigure(0, weight=1)
        
class DataFrameX(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        tv = ttk.Treeview(self)
        tv['columns'] = ('Name', 'Mobile', 'course')
        tv.heading("#0", text='RollNo', anchor='w')
        tv.column("#0", anchor="w")
        tv.heading('Name', text='Name')
        tv.column('Name', anchor='center', width=100)
        tv.heading('Mobile', text='Mobile')
        tv.column('Mobile', anchor='center', width=100)
        tv.heading('course', text='course')
        tv.column('course', anchor='center', width=100)
        tv.grid(sticky = "NSWE")
        self.treeview = tv
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

"""
class DataFrame(tk.Canvas):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs, highlightthickness=0)

        self.detail_frame = ttk.Frame(self)
        self.detail_frame.columnconfigure(0, weight=1)

        self.scrollable_window = self.create_window((0, 0), window=self.detail_frame, anchor="nw")

        def configure_scroll_region(event):
            self.configure(scrollregion=self.bbox("all"))
        
        def configure_window_size(event):
            self.itemconfig(self.scrollable_window, width=self.winfo_width())

        self.bind("<Configure>", configure_window_size)
        self.detail_frame.bind("<Configure>", configure_scroll_region)
        self.bind_all("<MouseWheel>", self._on_mousewheel)

        scrollbar = ttk.Scrollbar(self.detail_frame, orient="vertical", command=self.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")

        self.configure(yscrollcommand=scrollbar.set)
        self.yview_moveto(1.0)
    
    # https://stackoverflow.com/a/17457843/1587271
    def _on_mousewheel(self, event):
        self.yview_scroll(-int(event.delta/120), "units")

    def update_message_widgets(self, messages, message_labels):
        existing_labels = [
            (message["text"], time["text"]) for message, time in message_labels
        ]

        for message in messages:
            message_time = datetime.datetime.fromtimestamp(message["date"]).strftime(
                "%d-%m-%Y %H:%M:%S"
            )

            if (message["message"], message_time) not in existing_labels:
                self._create_message_container(message["message"], message_time, message_labels)
    
    def _create_message_container(self, message_content, message_time, message_labels):
        container = ttk.Frame(self.detail_frame)
        container.columnconfigure(1, weight=1)
        container.grid(sticky="EW", padx=(10, 50), pady=10)

        def reconfigure_message_labels(event):
            closest_break_point = min(SCREEN_SIZE_TO_MESSAGE_WIDTH.keys(), key=lambda b: abs(b - container.winfo_width()))
            for label, _ in message_labels:
                if label.cget("wraplength") != SCREEN_SIZE_TO_MESSAGE_WIDTH[closest_break_point]:
                    label.configure(wraplength=SCREEN_SIZE_TO_MESSAGE_WIDTH[closest_break_point])

        container.bind("<Configure>", reconfigure_message_labels)
        # self._create_message_bubble(container, message_content, message_time, message_labels)
    
    def _create_message_bubble(self, container, message_content, message_time, message_labels):
        #avatar_image = Image.open("./assets/male.png")
        #avatar_photo = ImageTk.PhotoImage(avatar_image)

        #avatar_label = tk.Label(
        #    container,
        #    image=avatar_photo
        #)

        #avatar_label.image = avatar_photo
        #avatar_label.grid(
        #    row=0,
        #    column=0,
        #    rowspan=2,
        ##    sticky="NEW",
        #    padx=(0, 10),
        #    pady=(5, 0)
        #)

        time_label = ttk.Label(
            container,
            text=message_time,
        )

        time_label.grid(row=0, column=1, sticky="NEW")

        message_label = tk.Label(
            container,
            text=message_content,
            wraplength=800,
            justify="left",
            anchor="w"
        )
    
        message_label.grid(row=1, column=1, sticky="NEW")

        message_labels.append((message_label, time_label))
"""