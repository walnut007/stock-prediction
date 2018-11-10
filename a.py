#coding:utf-8
import pandas as pd
from pandas import Series
import datetime as dt
import tushare as ts
import numpy as np
import operator as op
#获取出现3、6金叉的股票数据
code=pd.read_csv(r"./data/Table.csv") #读取A股列表，2016年12月10日整理
list_buy_date=[]#  5日均线抬头股票列表
list_buy_price=[]
list_sale_date=[]
list_sale_price=[]
# df = pd.DataFrame(columns=['A', 'B', 'C', 'D'])
start="2017-01-01"
n=1  #定义最后日期是现在时间的前几天
# m=50
now=dt.datetime.now() - dt.timedelta(days=n)#获取前一天日期
enddate=now.strftime("%Y-%m-%d")#获取当前年月日并转换为字符串作为文件名
#for i in range(0,len(code['Code']),1):
    # """从tushare获取数据"""
    #data = ts.get_k_data(code['Code'][i][2:8],start,end)
data = ts.get_hist_data('000001', start, enddate)#最近的日期在0，倒序排列
# if(data is None or data.empty or op.ne(str(data.index[0]),enddate) or len(data.index)<m):#跳过空值的股票和最后一天没有收盘价的股票（去除停牌股票）,股票收盘天数小于m天的（去除新股） 2.0 cmp(str(data.index[0]),enddate)!=0
#     continue
# else:
data =data.sort_index(ascending=True)#按照索引升序排列
        #定义均线天数
dates_1={'name':'1d','days':1}
dates_2 = {'name': '5d', 'days': 60}
# dates_3 = {'name': '21d', 'days': 21}
# dates_4 = {'name': '55d', 'days': 55}
# dates_5 = {'name': '144d', 'days': 144}
        # 计算各日均线数值
data[dates_1['name']] = Series.rolling(data['close'], window=dates_1['days']).mean()
data[dates_2['name']] = Series.rolling(data['close'], window=dates_2['days']).mean()
# data[dates_3['name']] = Series.rolling(data['close'], window=dates_3['days']).mean()
# data[dates_4['name']] = Series.rolling(data['close'], window=dates_4['days']).mean()
# data[dates_5['name']] = Series.rolling(data['close'], window=dates_5['days']).mean()
for j in range(10,len(data['close'])-60,1):
        #找出购买的日期
    if ((data[dates_1['name']][j-1] < data[dates_2['name']][j-1]) and (data[dates_1['name']][j] > data[dates_2['name']][j])):
        #1,2两条均线金叉
        list_buy_date.append(data.index[j+1])
        list_buy_price.append(data.open[j+1])
        for m in range(1,100,1):
            if ((data[dates_1['name']][j - 1+m] > data[dates_2['name']][j - 1+m]) and (data[dates_1['name']][j +m] < data[dates_2['name']][j +m])):
                list_sale_date.append(data.index[j + 1+m])
                list_sale_price.append(data.open[j + 1+m])
                break;
            else:
                continue
    else:
        continue


    #tushare结束
now=dt.datetime.now()
filename=now.strftime("%Y%m%d")#获取当前年月日并转换为字符串作为文件名
# list_buy=np.hstack((list_buy_date,list_buy_price))
# df=pd.DataFrame(list_buy)#列表转换为dataframe
code['buy_date']=pd.DataFrame(list_buy_date)
code['buy_price']=pd.DataFrame(list_buy_price)
code['sale_date']=pd.DataFrame(list_sale_date)
code['sale_price']=pd.DataFrame(list_sale_price)
code.to_csv('./data/result/5days/%s'%filename+'_best.csv')#写入结果文件夹
# df.to_csv('./data/result/%s'%filename+'560.csv')#写入结果文件夹
print ("Select stock560 has finished")


