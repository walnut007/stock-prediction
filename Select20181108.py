#coding:utf-8
import pandas as pd
from pandas import Series
import datetime as dt
import tushare as ts
import operator as op
#获取出现3、6金叉的股票数据
code=pd.read_csv(r"./data/Table.csv") #读取A股列表，2016年12月10日整理
list_buy=[]#  5日均线抬头股票列表
start="2017-01-01"
n=1  #定义最后日期是现在时间的前几天
m=50
now=dt.datetime.now() - dt.timedelta(days=n)#获取前一天日期
enddate=now.strftime("%Y-%m-%d")#获取当前年月日并转换为字符串作为文件名
for i in range(0,len(code['Code']),1):
    # """从tushare获取数据"""
    #data = ts.get_k_data(code['Code'][i][2:8],start,end)
    data = ts.get_hist_data(code['Code'][i][2:8], start, enddate)#最近的日期在0，倒序排列
    if(data is None or data.empty or op.ne(str(data.index[0]),enddate) or len(data.index)<m):#跳过空值的股票和最后一天没有收盘价的股票（去除停牌股票）,股票收盘天数小于m天的（去除新股） 2.0 cmp(str(data.index[0]),enddate)!=0
        continue
    else:
        data =data.sort_index(ascending=True)#按照索引升序排列
        #定义均线天数
        dates_1={'name':'1d','days':1}
        dates_2 = {'name': '5d', 'days': 5}
        dates_3 = {'name': '21d', 'days': 21}
        dates_4 = {'name': '55d', 'days': 55}
        dates_5 = {'name': '144d', 'days': 144}
        # 计算各日均线数值
        data[dates_1['name']] = Series.rolling(data['close'], window=dates_1['days']).mean()
        data[dates_2['name']] = Series.rolling(data['close'], window=dates_2['days']).mean()
        data[dates_3['name']] = Series.rolling(data['close'], window=dates_3['days']).mean()
        data[dates_4['name']] = Series.rolling(data['close'], window=dates_4['days']).mean()
        data[dates_5['name']] = Series.rolling(data['close'], window=dates_5['days']).mean()
        #找出购买的日期
        if ((data[dates_1['name']][-1:] < data[dates_2['name']][-1:])[0] or (data[dates_1['name']][-2:-1] > data[dates_2['name']][-2:-1])[0]):#1,2两条均线金叉
            continue
        else:
            list_buy.append(code['Code'][i])
    #tushare结束
now=dt.datetime.now()
filename=now.strftime("%Y%m%d")#获取当前年月日并转换为字符串作为文件名
df=pd.DataFrame(list_buy)#列表转换为dataframe
df.to_csv('./data/result/%s'%filename+'560.csv')#写入结果文件夹
print ("Select stock560 has finished")


