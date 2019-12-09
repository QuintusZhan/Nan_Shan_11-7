# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import numpy as np
import  pandas  as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

data=pd.read_excel('standardized_price_data.xlsx')#從excel讀取數據
data.head()
data.isnull().sum()#檢查殘缺項

data['TWSE Index'] = data['TWSE Index'].interpolate()
data.dropna(inplace=True)# 插值法填充

pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)#為了全部顯示輸出結果
print(data.corr())#輸出connivance，0-0.3弱相关；0.3-0.6中相关；0.6-1强相关
sns.pairplot(data, x_vars=['SPX Index','DXY Curncy','USGG10YR Index'], y_vars='CNY curncy', size=5, aspect=0.8, kind='reg')  
plt.show()#通過seaborn添加一條最佳擬合直線和95%的置信帶，size和aspect參數來調節顯示的大小和比例
x=data.ix[:,2:10]#選取2-10列為自變量
y=data.ix[:,10:11]#選取11列為因變量，隨便選的

from sklearn.preprocessing import StandardScaler
ss_y=StandardScaler()
data_y=ss_y.fit_transform(y.values.reshape(-1,1))#變量標準化

#回歸
model= sm.OLS(y, sm.add_constant(x)).fit()
print(model.summary()) #回歸結果
print(model.params) #係數
#線性模型的殘差通常服從正態分佈（Normal distribution），繪制殘差密度來檢查正態性
plt.figure()
model.resid.plot.density()
plt.show()




