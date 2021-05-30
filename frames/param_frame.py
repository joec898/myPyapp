# -*- coding: utf-8 -*-
"""
Created on Thu May 3 9:02:13 2021

@author: jochen
"""
from tkinter import ttk

class ParamFrame(ttk.Frame):
    def __init__(self, parent, controller, show_settings):
        super().__init__(parent)

        priceTypes = ["Live", "Settle"]

        param_container = self
        param_container.grid(row=0, column=0, sticky="EW", padx=5, pady=5)
        param_container.pack(expand = 1, fill ="both")

        # row 1
        title_label = ttk.Label(
            param_container,
            text="Parameters for Downloading Trades",
            font=('Helvetica', 11, 'bold')
        )
        title_label.grid(column=0, row=0, sticky="W", pady=2, columnspan=4)

        settings_button = ttk.Button(
            self,
            text="Settings",
            command=show_settings,
            cursor="hand2"
        )
        settings_button.grid(row=0, column=5, sticky="E", padx=2)

        ### row 2
        date_label = ttk.Label(
            param_container,
            text="Date: "
        )
        date_label.grid(column=0, row=1, sticky="E", pady=2)

        date_input = ttk.Entry(
            param_container,
            width=12,
            textvariable=controller.date_val
        )
        date_input.grid(column=1, row=1, sticky="W",  pady=2)

        vol_type_label = ttk.Label(
            param_container,
            text="Vol Type: "
        )
        vol_type_label.grid(column=2, row=1, sticky="E", pady=2)

        vol_type_combo = ttk.Combobox(
            param_container,
            values=priceTypes,
            textvariable=controller.vol_type_val
        )
        # vol_type_index = priceTypes.index(controller.vol_type_val.get())
        vol_type_combo.current(controller.vol_type_index_val.get())
        vol_type_combo.grid(column=3, row=1, sticky="W",  pady=2, columnspan=2)

        # row 3
        acquirer_label = ttk.Label(
            param_container,
            text="Acquirer: "
        )
        acquirer_label.grid(column=0, row=2, sticky="E", pady=2)

        acquirer_input = ttk.Entry(
            param_container,
            width=12,
            textvariable=controller.acquirer_val
        )
        acquirer_input.grid(column=1, row=2, sticky="W",  pady=2)

        price_type_label = ttk.Label(
            param_container,
            text="Underlying Price Type: "
        )
        price_type_label.grid(column=2, row=2, sticky="E", pady=2)

        price_type_combo = ttk.Combobox(
            param_container,
            values=priceTypes,
            textvariable=controller.price_type_val
        )
        # price_type_index = priceTypes.index(controller.price_type_val.get())
        price_type_combo.grid(column=3, row=2, sticky="W", pady=2, columnspan=2)
        price_type_combo.current(controller.price_type_index_val.get())
        price_type_combo.pack

        # row 4
        portfolios_label = ttk.Label(
            param_container,
            text="Portfolios: "
        )
        portfolios_label.grid(column=0, row=3, sticky="E", pady=2)

        portfolios_input = ttk.Entry(
            param_container,
            width=80,
            textvariable=controller.portfolios_val
        )
        portfolios_input.grid(column=1, row=3, sticky="W",  pady=2, columnspan=4)

        ## row 5
        strategies_label = ttk.Label(
            param_container,
            text="Strategies: "
        )
        strategies_label.grid(column=0, row=4, sticky="E", pady=2)

        strategies_input = ttk.Entry(
            param_container,
            width=80,
            textvariable=controller.strategies_val
        )
        strategies_input.grid(column=1, row=4, sticky="W",  pady=2, columnspan=4)

        token_label = ttk.Label(
            param_container,
            text="Token: "
        )
        token_label.grid(column=0, row=6, sticky="E")

        token_input = ttk.Entry(
            param_container,
            width=80,
            textvariable=controller.token_val
        )
        token_input.grid(column=1, row=6, sticky="W",  pady=2,columnspan=4)

        #strategies_input.pack(side="left", padx=5, pady=5)
        date_input.focus()
        self.pack(fill="both")




