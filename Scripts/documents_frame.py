#! Python3
# encoding: utf8

import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

from tkinter import ttk
import tkinter as tk
from functools import partial

def DocumentsFrame(parent, items, display_method, download_method):

    if len(items) == 0:
        item_frame = ttk.Frame(parent, borderwidth=5)
        ttk.Label(parent, text="Geen resultaten gevonden.").pack(fill=tk.BOTH, padx=20, pady=20)
    else:
        item_idx = 0
        for item in items:
            item_frame = ttk.Frame(parent, borderwidth=5)

            ttk.Separator(item_frame, orient=tk.HORIZONTAL).grid(row=0, column=0, sticky="new", columnspan=3, pady=2)
            ttk.Button(item_frame, text="Meer Info", command=partial(display_method, item_idx)).grid(row=1, column=2, rowspan=2, padx=10)
            ttk.Button(item_frame, text="Download", command=partial(download_method, item_idx)).grid(row=3, column=2, padx=10)

            i = 1
            for key, value in item.items():
                ttk.Label(item_frame, text=key).grid(row=i, column=0, padx=5)
                ttk.Label(item_frame, text=value, width=50, wraplength=300).grid(row=i, column=1)
                i += 1

            item_frame.pack(fill=tk.X, padx=20)
            item_idx += 1
