#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 01:47:13 2019

@author: quintus
"""

#此部分工作為將從Bloomberg上抓下來的factor們的時間對齊

import pandas as pd
import numpy as np

price = pd.read_excel('/Users/quintus/My Nan Shan project/Factors data.xlsx', parse_dates = True)
# 可先用price.head()與price.tail()查看資料長怎樣

daily_index=pd.date_range(start="1/3/2005", end="11/21/2019", freq="B")
#建立一個只包含平日的時間index

factors = []
for i in range(len(price.columns)):
    if i % 2 == 0:
        factors.append(price.columns[i])
# 獲取每個factor的名稱

factors_data = {}
for i in range(0,len(price.columns), 2):
    to_list = zip(price[price.columns[i]], price[price.columns[i + 1]])
    a = factors[i // 2 ]
    factors_data[a] = []
    for i in to_list:
        factors_data[a].append(i)
# 建立一個名為factors_data的字典，裡面的key為factor名，value為一個list
# list內為很多個tuple，每個tuple的第一項為時間，第二項為該facotr index的值

for_create = {'day':daily_index}
for_fill = []
for i in range(len(daily_index)):
    for_fill.append(np.nan)
for i in factors:
    for_create[i] = for_fill
matched_price_data = pd.DataFrame(for_create)
matched_price_data.set_index('day', inplace = True)
# 建立一個index為時間，coluumn為factors的DataFrame，目前裡面都是NaN
# 等下會拿來建立一個時間對齊的factors data的DataFrame

for factor in factors_data:
    for n_of_day in range(len(factors_data[factor])):
        matched_price_data.at[factors_data[factor][n_of_day][0], factor]= factors_data[factor][n_of_day][1]
# 將每個因子從Bloomberg抓下來的價格填入對應的時間格
# 有點複雜，可以先看一下factors_data['SPX Index'][0][0]還有factors_data['SPX Index'][0][1]是什麼

matched_price_data.dropna(axis = 0, thresh = 2, inplace = True)
#不知道為什麼最後多一行NaN

matched_price_data.to_excel("Clean_factors_data.xlsx", sheet_name = "factors")

