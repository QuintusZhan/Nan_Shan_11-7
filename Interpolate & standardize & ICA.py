#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 02:59:39 2019

@author: quintus
"""

import pandas as pd
import numpy as np
from sklearn.decomposition import FastICA


def interpolate():
    price.iloc[:, :] = price.iloc[:, :].interpolate(method = "time")
    return price
    # 用時間做內差，填遺漏值（未開盤）
    
def standardize(time):
    standardized_price = price[price.index >= time]
    standardized_price = (standardized_price - np.mean(standardized_price, axis = 0)) / np.std(standardized_price)
    return standardized_price 
    # 標準化

def ICA():
    number_of_components = len(price.columns)
    
    to_ICA =[]
    for day in price.index:
        a = [i for i in price.loc[day] ]
        to_ICA.append(a)    
    to_ICA = np.array(to_ICA)
    # 弄出要丟進去ICA package的資料格式
    
    ICA = FastICA(n_components=number_of_components)
    ICA_data = ICA.fit_transform(to_ICA)
    return ICA_data
    # 取得經ICA處理後的資料

price = pd.read_excel('/Users/quintus/Nan_Shan_11-7/Clean_factors_data.xlsx', parse_dates = True, index_col = 'day')
  
price = interpolate()
# 用時間做內差，填遺漏值（未開盤）

time = input('輸入標準化時間起點:')

price = standardize(time)
# 標準化
    
price = ICA()
# 做ICA

print(price)
