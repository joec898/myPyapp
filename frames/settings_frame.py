# -*- coding: utf-8 -*-
"""
Created on Thu May 3 15:22:26 2021

@author: jochen
"""
from tkinter import ttk

class SettingsFrame(ttk.Frame):
    def __init__(self, parent, controller, show_param):
        super().__init__(parent)

        envTypes = ["production", "qa", "dev", "uat"]

        settings_container  = self

        settings_container.grid(row=0, column=0, sticky="EW", padx=5, pady=5)

        # row 1 
        title_label = ttk.Label(
            settings_container,
            text="Settings",
            font=('Helvetica', 11, 'bold')
        )
        title_label.grid(column=0, row=0, sticky="W",pady=5,columnspan=2) 

        param_button = ttk.Button(
            self,
            text="Parameters", 
            command=show_param, 
            cursor="hand2"
        )
        param_button.grid(row=0, column=3, sticky="E", padx=2, pady=(2, 0))
        
        auto_save_settings = ttk.Checkbutton(
            settings_container, 
            text="Auto Save Settings", 
            variable=controller.auto_save_settings_val,
            command=lambda: controller.save_settings_when_unchecked())
        auto_save_settings.grid(row=0, column=4, sticky="E", padx=2, pady=(2, 0))
        
        # row 2 
        env_label = ttk.Label(
            settings_container,
            text="Environment: "
        )
        env_label.grid(column=0, row=1, sticky="E")

        env_combo = ttk.Combobox(
            settings_container,
            values = envTypes, 
            textvariable=controller.env_val
        )
        env_combo.current(0)
        env_combo.grid(column=1, row=1, sticky="W",  pady=2,columnspan=2)

        # row 3 
        version_label = ttk.Label(
            settings_container,
            text="Version: " 
        )
        version_label.grid(column=0, row=2, sticky="E")

        version_input = ttk.Entry(
            settings_container,
            width=10,
            textvariable=controller.version_val 
        )
        version_input.grid(column=1, row=2, sticky="W",  pady=2,columnspan=2) 

        # row 4
        user_label = ttk.Label(
            settings_container,
            text="User: " 
        )
        user_label.grid(column=0, row=3, sticky="E")

        user_input = ttk.Entry(
            settings_container,
            width=15,
            textvariable=controller.username_val 
        )
        user_input.grid(column=1, row=3, sticky="W", pady=2,columnspan=2)

        # row 5
        password_label = ttk.Label(
            settings_container,
            text="Password: " 
        )
        password_label.grid(column=0, row=4, sticky="E")

        password_input = ttk.Entry(
            settings_container,
            width=15,
            show="*",
            textvariable=controller.password_val
        )
        password_input.grid(column=1, row=4, sticky="W",  pady=2,columnspan=2)

        # row 6
        filepath_label = ttk.Label(
            settings_container,
            text="File Path: " 
        )
        filepath_label.grid(column=0, row=5, sticky="E")

        filepath_input = ttk.Entry(
            settings_container,
            width=80,
            textvariable=controller.filepath_val 
        )
        filepath_input.grid(column=1, row=5, sticky="W",  pady=2, columnspan=2)

        # row 7
        blank_label = ttk.Label(
            settings_container,
            text=" "
        )
        blank_label.grid(column=0, row=5, sticky="W",  pady=2, columnspan=3)

        env_combo.focus()
        #self.pack(fill="both")

    def return_pressed(event):
        print('Return key pressed.')