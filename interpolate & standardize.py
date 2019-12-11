#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 02:59:39 2019

@author: quintus
"""

import pandas as pd
import numpy as np

def interpolate():
    price.iloc[:, :] = price.iloc[:, :].interpolate(method = "time")
    return price
    # 用時間做內差，填遺漏值（未開盤）
    
def standardize(time):
    standardized_price = price[price.index >= time]
    standardized_price = (standardized_price - np.mean(standardized_price, axis = 0)) / np.std(standardized_price)
    return standardized_price 
    # 標準化
   
price = pd.read_excel('Clean_factors_data.xlsx', parse_dates = True, index_col = 'day')
  
price = interpolate()

time = input('輸入標準化時間起點:')

price = standardize(time)