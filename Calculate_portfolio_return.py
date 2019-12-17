#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 01:18:45 2019

@author: quintus
"""
 
import pandas as pd

def Get_price_data(file_name, start_time):
    price = pd.read_excel(file_name, parse_dates = True, index_col = 'Time')
    # 讀取經由excel的vloopup對齊好時間的股價資料，若無收盤價vlookup將自動補前值
    price = price[price.index > start_time]
    # 資料庫資料起於2005年，將start_time設定為您所需要的資料起始日
    return price

def Read_portfoilio(file_name):
    portfolio = pd.read_excel(file_name) 
    return portfolio
    # 獲取投組組合資訊，依序包含：代碼、名稱、權重
    
def Calculate_portfolio_return():
    return_ = price / price.shift(1)
    # 計算單一個股的淨值，設定開始計算日期為淨值等於1，如果第二天漲了5%，淨值為 1.05
    
    tickers=[str(i) + ' TT EQUITY' for i in portfolio['代碼']]
    weights=[i for i in portfolio['金額比重'] ]
    return_ = return_[tickers]
    # 只保留有在投資組合內的股票的股價資訊
    return_['Portfolio'] = 0
    # 本來只有個股的報酬資料，新增一個投組報酬資料的欄位
    
    for i in range(len(tickers)):
        return_['Portfolio'] += return_[tickers[i]] * weights[i]
    return_['Portfolio'] *= 0.01 
    # 因為投組範本權重是用百分比表示
    portfolio_return = return_['Portfolio'].cumprod()
    
    return portfolio_return 

stock_data_name = input("輸入股價資料之檔案名：")
start_date = input('輸入回測起始時間(如:\'2005-01-01\'):')
portfolio_data_name = input("輸入投組資料之檔案名：")



price = Get_price_data(stock_data_name, start_date)
portfolio = Read_portfoilio(portfolio_data_name)
portfolio_return = Calculate_portfolio_return()
# 我們會得到一個計算好的投組累積報酬
portfolio_return.plot()

print(portfolio_return)

