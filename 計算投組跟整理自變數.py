#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 16:15:57 2019

@author: quintus
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

### 下面三個用來計算投組的價格（還未換成報酬率的樣態）
def Get_stock_price_data(file_name, start_date):
    stock_price = pd.read_excel(file_name, parse_dates = True, index_col = 'Time')
    # 讀取經由excel的vloopup對齊好時間的股價資料，若無收盤價vlookup將自動補前值
    stock_price = stock_price[stock_price.index > start_date]
    # 資料庫資料起於2005年，將start_time設定為您所需要的資料起始日
    return stock_price

def Read_portfoilio(file_name):
    portfolio = pd.read_excel(file_name) 
    return portfolio
    # 獲取投組組合資訊，依序包含：代碼、名稱、權重
    
def Calculate_portfolio_price():

    global stock_price
    global portfolio
    
    tickers=[str(i) + ' TT EQUITY' for i in portfolio['代碼']]
    weights=[i for i in portfolio['金額比重'] ]
    stock_price = stock_price[tickers]
    # 只保留有在投資組合內的股票的股價資訊
    stock_price['Portfolio'] = 0
    # 本來只有個股的報酬資料，新增一個投組報酬資料的欄位
    
    for i in range(len(tickers)):
        stock_price['Portfolio'] += stock_price[tickers[i]] * weights[i] * 0.01
    # 因為投組範本權重是用百分比表示
    portfolio_price = stock_price['Portfolio']
    
    return portfolio_price


# 這一個函數將因子的時間對齊
def Match_the_factors_data(file_name, start_date):

    # 可先用price.head()與price.tail()查看資料長怎樣
    price = pd.read_excel(file_name, parse_dates = True)
    
    # 建立一個只包含平日的時間index
    daily_index = pd.date_range(start="1/3/2005", end="11/21/2019", freq="B")
    
    # 獲取每個factor的名稱
    factors = []
    for i in range(len(price.columns)):
        if i % 2 == 0:
            factors.append(price.columns[i])
    
    factors_data = {}
    # 建立一個名為factors_data的字典，裡面的key為factor名，value為一個list
    # list內為很多個tuple，每個tuple的第一項為時間，第二項為該facotr index的值
    for i in range(0,len(price.columns), 2):
        to_list = zip(price[price.columns[i]], price[price.columns[i + 1]])
        name = factors[i//2]
        factors_data[name] = []
        for i in to_list:
            factors_data[name].append(i)
    
    for_create = {'day':daily_index}
    for_fill = []
    for i in range(len(daily_index)):
        for_fill.append(np.nan)
    for i in factors:
        for_create[i] = for_fill
    price = pd.DataFrame(for_create)
    price.set_index('day', inplace = True)
    # 建立一個index為時間，coluumn為factors的DataFrame，目前裡面都是NaN
    # 等下會拿來建立一個時間對齊的factors data的DataFrame
    
    for factor in factors_data:
        for n_of_day in range(len(factors_data[factor])):
            price.at[factors_data[factor][n_of_day][0], factor]= factors_data[factor][n_of_day][1]
    # 將每個因子從Bloomberg抓下來的價格填入對應的時間格
    # 有點複雜，可以先看一下factors_data['SPX Index'][0][0]還有factors_data['SPX Index'][0][1]是什麼
    
    price.dropna(axis = 0, thresh = 2, inplace = True)
    price = price[price.index > start_date]
    return price


# 合併自變數、應變數
def merge_price_andn_portfolio_price():
    for_create = {'portfolio_price':portfolio_price}
    merge = pd.DataFrame(for_create)
    merge = merge.dropna()
    # 除去台股未開盤日
    merge = merge.asfreq('B')
    # 之前台股會在星期六開盤，因為只有幾天且那幾天交易量都很小，為了方便合併就不管他了
    
    for i in price.columns:
        for j in merge.index:        
            merge.at[j,i] = price.at[j , i]
    
    merge = merge[pd.notnull(merge['portfolio_price'])]
    return merge
    #將自變數、應變數合起來
    
    
def Interpolate():

    global merge
    merge.iloc[:, :] = merge.iloc[:, :].interpolate(method = "time")
    return merge
    # 用時間做內差，填遺漏值（未開盤）
    

def To_return_form():
    
    global merge
    merge = merge / merge.shift(1) - 1
    merge = merge.iloc[1 : ]
    # 算報酬會第一個row沒資料，所以拿掉
    return merge
    # 將因子變成報酬型態


stock_data_name = input("輸入股價資料之檔案名：")
start_date = input('輸入回測起始時間(如:\'2005-01-01\'):')
portfolio_data_name = input("輸入投組資料之檔案名：")

# 輸入股價資料之檔案名： /Users/quintus/Nan_Shan_11-7/Data/TW stock data.xlsx
# 輸入回測起始時間(如:'2005-01-01'): '2015-01-01'
# 輸入投組資料之檔案名： /Users/quintus/Nan_Shan_11-7/Data/投組範本.xlsx

stock_price = Get_stock_price_data(stock_data_name, start_date)
portfolio = Read_portfoilio(portfolio_data_name)
portfolio_price = Calculate_portfolio_price()
# 我們會得到一個計算好的投組價格

factors_data_name = input("請輸入從Bloomberg上抓下來的因子檔案名:")#Factors data.xlsx
price = Match_the_factors_data(factors_data_name, start_date)

merge = merge_price_andn_portfolio_price()
merge = Interpolate()
merge = To_return_form()

factors = input('輸入選擇的因子，用‘／’（如SPX Index/USGG10YR Index/USGG2YR Index/DXY Curncy/TWD Curncy/BCOMTR Index/CL1 COMB Comdty/XAU BGN Curncy)：').split('/')

x = merge[factors]
x_std = StandardScaler().fit_transform(x)
# 做標準化

features = x_std.T 
covariance_matrix = np.cov(features)
# 取得共變異數矩陣
eig_vals, eig_vecs = np.linalg.eig(covariance_matrix)
# eig_vecs 就是我們要找用來轉換的矩陣
projected_x = x_std.dot(eig_vecs.T)
# projected_x 就是用PCA轉換過的因子

pd.DataFrame(projected_x).to_excel('PCA過的因子.xlsx')
pd.DataFrame(eig_vecs).to_excel('eig_vecs.xlsx')


y = merge[merge.columns[0]]
y = (y - np.mean(y, axis = 0)) / np.std(y)
# 做標準化
y.to_excel('應變數標準化.xlsx')



#模型回歸部分
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns


data=pd.read_excel('PCA過的因子.xlsx')
x=data.ix[:,1:]#選取自變量
df=pd.read_excel('應變數標準化.xlsx')
y=df.ix[:,1:]#選取因變量
#修改自變量名稱
x.columns=['SPX Index','USGG10YR Index','USGG2YR Index','DXY Curncy','TWD Curncy','BCOMTR Index','CL1 COMB Comdty','XAU BGN Curncy']

variable=pd.concat([x,y],axis=1)#合并x和y

# 相关度热力图，0-0.3弱相关；0.3-0.6中相关；0.6-1强相关
corr =x.corr()
plt.figure(figsize = (20,5))
ax=sns.heatmap(corr,cmap='GnBu_r',square=True, annot=True, linewidths=1,vmin=0, vmax=1)
#通過seaborn添加一條最佳擬合直線和95%的置信帶，height和aspect參數來調節顯示的大小和比例
sns.pairplot(variable, x_vars=['SPX Index','USGG10YR Index','USGG2YR Index','DXY Curncy','TWD Curncy','BCOMTR Index','CL1 COMB Comdty','XAU BGN Curncy'], y_vars='portfolio_price', height=5, aspect=0.8, kind='reg')
plt.show()

#回歸
model= sm.OLS(y, sm.add_constant(x)).fit()
print(model.summary()) #回歸結果
print(model.params) #係數
#線性模型的殘差通常服從正態分佈（Normal distribution），繪制殘差密度來檢查正態性
plt.figure()
model.resid.plot.density()
plt.show()

model.params.to_excel('係數.xlsx')#PCA之後的回歸係數
data2=pd.read_excel('係數.xlsx',index_col=0)
coefficient=data2.ix[1:,:]#提取非常數項
matrix=coefficient.values#轉化為矩陣
c2=matrix.T#轉置
c=c2.dot(eig_vecs)#矩陣相乘，得到最終的回歸係數c
c_data= pd.DataFrame(c)#變量類型轉化為dataframe
c_data.columns=['SPX Index','USGG10YR Index','USGG2YR Index','DXY Curncy','TWD Curncy','BCOMTR Index','CL1 COMB Comdty','XAU BGN Curncy']
c_data.to_excel('最終係數.xlsx')


