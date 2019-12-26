@@ -0,0 +1,64 @@
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys as sy
import numpy as np
import pandas as pd
import tushare as ts
import pyecharts as pye
from sklearn import datasets as ds
import matplotlib as mpl
from matplotlib import pyplot as plt
import seaborn as sns
import pyecharts as pye 

data=pd.read_excel('price.xlsx')#從excel讀取數據

data.head()
data.isnull().sum()#檢查殘缺項

data['price'] = data['price'].interpolate()
data.dropna(inplace=True)# 插值法填充

#计算日均收益,报酬率由小到大依序排列，并依照不同的信赖水准找出相对应分位数的临界报酬率。信赖水准为95%
df1 =data.sort_index(by='price',ascending=True)
df1 = pd.DataFrame(df1)
df1['date'] = df1.index
df1['date'] = df1[['date']].astype(str)
df1["rev"]= df1.price.diff(1)
df1["last_price"]= df1.price.shift(1)
df1["rev_rate"]= df1["rev"]/df1["last_price"]
df1 = df1.dropna()
print(df1.head(10))  
df1["rev_rate"]=df1["rev_rate"]*100
dd =df1.sort_index(by='rev_rate',ascending=True) 
print(dd.head(10))

 
VaR_95 = dd.quantile(0.05)
esloss=df1[df1["rev_rate"]<VaR_95["rev_rate"]]


ES=np.mean(esloss["rev_rate"])#在这里上面是取前5%的sloss的数进行加和，然后分母是前5%的数据点的个数，整个算数相当于是在求平均值

ES













