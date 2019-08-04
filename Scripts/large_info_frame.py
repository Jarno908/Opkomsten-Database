#! Python3
# encoding: utf8

import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

from tkinter import ttk

def InfoFrame(parent, info):

    i = 0
    for key, value in info.items():
        ttk.Label(parent, text=key).grid(row=i, column=0, padx=5)
        ttk.Label(parent, text=value, width=60, wraplength=500).grid(row=i, column=1, sticky="w", pady=10)
        i += 1
