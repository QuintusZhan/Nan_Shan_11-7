import pandas as pd
import numpy as np


def Match_the_factors_data(file_name):

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
    return price


def interpolate():

    global price
    price.iloc[:, :] = price.iloc[:, :].interpolate(method = "time")
    return price
    # 用時間做內差，填遺漏值（未開盤）
    

def standardize(time):

    global price
    standardized_price = price[price.index >= time]
    standardized_price = (standardized_price - np.mean(standardized_price, axis = 0)) / np.std(standardized_price)
    return standardized_price
    # 標準化



def ReturnRate(mydataframe):

    global price
    length = len(price.columns)
    for i in range(len(price.columns)):
        tmp = price.iloc[0, i]
        for j in range(1, len(price.index)):
            now = 100*(price.iloc[j, i] - tmp)/tmp
            tmp = price.iloc[j, i]
            price.iloc[j, i] = now

    return price.iloc[1:length,]


factors_data_name = input("請輸入從Bloomberg上抓下來的因子檔案名:")
# /Users/irenehuang/desktop/pfl.xlsx
sttime = input('輸入起始日期，如：2005-01-01:')
# 2005-01-04
price = Match_the_factors_data(factors_data_name)
price = ReturnRate(price)
price = interpolate()
std_price = standardize(sttime)
# print(price.head(20))

print(std_price)
















