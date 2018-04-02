#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 11:34:56 2018

@author: nghia
"""

import pandas as pd
import glob
import os

path = "./dulieucophieu/"
all_files = glob.glob(os.path.join(path, "*.csv")) #make list of paths
all_files = all_files[:10]

for file in all_files:
    # Getting the file name without extension
    file_name = os.path.splitext(os.path.basename(file))[0]
    # Reading the file content to create a DataFrame
    dfn = pd.read_csv(file)
    # Setting the file name (without extension) as the index name
    dfn.index.name = file_name

print (len(all_files))