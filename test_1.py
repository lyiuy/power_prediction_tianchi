# -*- coding: utf-8 -*-
"""
Created on Sat May 27 17:29:08 2017

@author: yliu.Edward
"""


import pandas as pd
import datetime
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor 


data_power = pd.read_csv('power.csv', index_col=0)
data_power.index = [datetime.datetime.strptime(item, '%Y/%m/%d') for item in data_power.index]


def datetime_offset_by_month(datetime1, n = 1):
    one_day = datetime.timedelta(days = 1)
    q,r = divmod(datetime1.month + n, 12)
    datetime2 = datetime.datetime(datetime1.year + q, r + 1, 1) - one_day
    if datetime1.month != (datetime1 + one_day).month:
        return datetime2
    if datetime1.day >= datetime2.day:
        return datetime2 
    return datetime2.replace(day = datetime1.day)

def gen_data_range(date_start, date_stride):
    '''
    input must be the format of datetime
    date_stride unit： month
    '''   
    return_date_list = []
    for i in range(date_stride):
        tran_date_list = [datetime_offset_by_month(date_start, n = i),
                          datetime_offset_by_month(date_start, n = i+1)]
        return_date_list.append(tran_date_list)
    return return_date_list
    
    
date_range = gen_data_range(datetime.datetime(2015,1,1), 20)
date_inclu = pd.DataFrame(data_power.loc[:,'power_consumption'].groupby(data_power.index).sum())

for item in date_range:
    sum_by_month = np.sum(date_inclu.loc[item[0]:item[1], ])
    print(str(item) + ': '+str(sum_by_month))
date_inclu['weekday']= [item.weekday() for item in date_inclu.index]    

vacation_list = [datetime.datetime(2015,1,1)]
