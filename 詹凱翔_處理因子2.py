#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 02:59:39 2019

@author: quintus
"""
# 此部分為處理遺漏值，做標準化，做ICA，最後將自變數資料與應變數資料合起來（時間有對上）

import pandas as pd
import numpy as np
from sklearn.decomposition import FastICA


def interpolate():
    price.iloc[:, :] = price.iloc[:, :].interpolate(method = "time")
    return price
    # 用時間做內差，填遺漏值（未開盤）
    
def standardize(time):
    standardized_price '= price[price.index >= time]
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
    
def merge_price_n_portfolio_return():
    for_create = {'portfolio_return':portfolio_return}
    merge = pd.DataFrame(for_create)
    merge = merge.dropna()
    # 除去台股未開盤日
    xx = merge.asfreq('B')
    # 這行單存為了等一下計算用，因為在python日期2的加減需要提供頻率，在這設了一個只算上班日的頻率，因為如果把整個merge頻率弄成上班日，會填補進剛剛drop掉的
    merge.to_excel('ddsda.xlsx')
    
    for i in price.columns:
        for j in merge.index:        
            merge.at[j,i] = price.at[j - 1 * xx.index.freq, i]
    return merge
    #將自變數、應變數合起來（自變數已取成前一期的價格，可以直接拿來對當期的應變數跑回歸）

price = interpolate()
# 用時間做內差，填遺漏值（未開盤）
time = input('輸入標準化時間起點:')
price = standardize(time)
# 標準化
price = ICA()
# 做ICA

print(price)

merge = merge_price_n_portfolio_return()
# merge 為最後我們會拿來跑回歸的DataFrame
