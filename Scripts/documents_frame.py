#! Python3
# encoding: utf8

import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

from tkinter import ttk
import tkinter as tk

def DocumentsFrame(parent, items):

    for item in items:
        item_frame = ttk.Frame(parent, borderwidth=5)

        ttk.Separator(item_frame, orient=tk.HORIZONTAL).grid(row=0, column=0, sticky="new", columnspan=3, pady=2)
        ttk.Button(item_frame, text="Download").grid(row=1, column=2, rowspan=3, padx=10)

        i = 1
        for key, value in item.items():
            ttk.Label(item_frame, text=key).grid(row=i, column=0)
            ttk.Label(item_frame, text=value).grid(row=i, column=1)
            i += 1

        item_frame.pack(fill=tk.X, padx=20)
