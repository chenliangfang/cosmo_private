# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 17:33:21 2022

@author: CHENLF
"""
import sys
print(sys.path)
import os,time
import pandas as pd
import tushare as ts
from datetime import datetime,timedelta
import xlwings as xw
import  numpy as np
ts.set_token('d48f1a29a44d2b3cfd8aba968d44da4fe9a2a0c30305bcf57dc91a21')  ## 设置
## 初始化
pro = ts.pro_api()
#%%
## 需要每年更新节假日日期数据
jiejiari = pd.read_excel(r'E:\项目文件夹\陈良方\我的坚果云\中信银行\节假日.xlsx')
## 获取工作日时
dd = pd.to_datetime(jiejiari['节假日'],errors='coerce', format ='%Y-%m-%d') ## 转化为时间格式
jjr = list(dd.apply(lambda x: x.strftime('%Y%m%d'))) ##读取为list
## 获取周日为工作日的日期
dd = pd.to_datetime(jiejiari['调休'],errors='coerce', format ='%Y-%m-%d')
dd = dd.dropna()
gzr = list(dd.apply(lambda x: x.strftime('%Y%m%d')))
## 获取工作日的日历序列
start_date = '20211101'   ## 需要每年维护
end_date = '20221231'     ## 需要每年维护
workingday = pd.date_range(start = start_date, end = end_date ,tz='Asia/Shanghai', freq = "B")
f = lambda x: x.strftime('%Y%m%d')
workingdaylist = list(map(f, list(workingday)))

for i in workingdaylist:
    if i in jjr:
        workingdaylist.remove(i)
for i in workingdaylist:
    if i in jjr:
        workingdaylist.remove(i)
for i in workingdaylist:
    if i in jjr:
        workingdaylist.remove(i)
for i in workingdaylist:
    if i in jjr:
        workingdaylist.remove(i)
## 获取最终的节假日序列
workingdaylist.extend(gzr)
workingdaylist.sort()
## 转化为DataFrame
workingday = pd.DataFrame(workingdaylist, columns = ['work'])
## 获取交易日信息
trade_days = pro.trade_cal(exchange_id='', start_date = '20211101', end_date = '20221231')
tradingday = trade_days[trade_days.is_open == 1].cal_date.values
tradingdaylist = list(tradingday)
tradingday = pd.DataFrame(tradingdaylist, columns = ['trading'])

#%%
def get_pianli_jday(basic_day,timedaltas):
    ## basic_day 为基准日期；
    ## timedaltas 为时间偏离度，正数表表示向后偏离；
    from datetime import datetime, timedelta
    if basic_day == None:
        today = datetime.today()  
    else:
        today = datetime.strptime(basic_day, "%Y%m%d")
    start_date = today - timedelta(days=40) ## 设置起始日期
    end_date = today + timedelta(days=40)  ## 设置终止日期
    ## 获取区间内交易日情况
    try:
        trade_days = pro.trade_cal(exchange_id='', start_date = start_date.strftime('%Y%m%d'), end_date = end_date.strftime('%Y%m%d'))
    except:
        time.sleep(60)
        trade_days = pro.trade_cal(exchange_id='', start_date = start_date.strftime('%Y%m%d'), end_date = end_date.strftime('%Y%m%d'))

    ## 初始化基数    
    n = 0  ## 交易日天数
    j = 0  ## 自然日天数
    if timedaltas >0:
        while n < timedaltas:
            if trade_days[trade_days.cal_date == (today + timedelta(days = j + 1)).strftime('%Y%m%d')].is_open.values[0] == 1:
                n = n + 1
            j = j + 1
    else:
        while n > timedaltas:
            if trade_days[trade_days.cal_date == (today + timedelta(days = j - 1)).strftime('%Y%m%d')].is_open.values[0] == 1:
                n = n - 1
            j = j - 1
    return (today + timedelta(days = j)).strftime('%Y%m%d')
#%%

def get_fix_day_mounth(mounth, index = 1, rili = "working"):
    mounth = mounth[:6]
    if rili == "working":
        day = workingday[workingday.work.str.contains(mounth)].values[index - 1][0]
    elif rili == "trading":
        day = tradingday[tradingday.trading.str.contains(mounth)].values[index - 1][0]
    return day
        
#%%
def get_pianli_jday(basic_day,timedaltas):
    from datetime import datetime, timedelta
    today = datetime.strptime(basic_day, "%Y%m%d")
    ## 获取区间内交易日情况
    ## 初始化基数    
    n = 0  ## 交易日天数
    j = 0  ## 自然日天数
    if timedaltas >0:
        while n < timedaltas:
            if (today + timedelta(days = j + 1)).strftime('%Y%m%d') in tradingdaylist:
                n = n + 1
            j = j + 1
    else:
        while n > timedaltas:
            if (today + timedelta(days = j - 1)).strftime('%Y%m%d') in tradingdaylist:
                n = n - 1
            j = j - 1
    return (today + timedelta(days = j)).strftime('%Y%m%d')

#%%
def get_pianli_wday(basic_day,timedaltas):
    ## basic_day 为基准日期；
    ## timedaltas 为时间偏离度，正数表表示向后偏离；
    from datetime import datetime, timedelta
    today = datetime.strptime(basic_day, "%Y%m%d")
    ## 获取区间内交易日情况
    ## 初始化基数    
    n = 0  ## 交易日天数
    j = 0  ## 自然日天数
    if timedaltas >0:
        while n < timedaltas:
            if (today + timedelta(days = j + 1)).strftime('%Y%m%d') in workingdaylist:
                n = n + 1
            j = j + 1
    else:
        while n > timedaltas:
            if (today + timedelta(days = j - 1)).strftime('%Y%m%d') in workingdaylist:
                n = n - 1
            j = j - 1
    return (today + timedelta(days = j)).strftime('%Y%m%d')
           



#%%
def get_fixed_day(guize, day,rulue0 = 'working',rulue1 = '顺延', rulue2 = '每月'):
    ## 先获取时间序列
    days = []
    Days = []
    if '最后' not in day:
        if '每月' in rulue2:
            for i in range(1,13):
                if i >=10:
                    dd = "2022%d%s" % (i, day)
                else:
                    dd = "20220%d%s" % (i, day)
                days.append(dd)
        elif '每季度末月' in rulue2:
            for i in [3,6,9,12]:
                if i >=10:
                    dd = "2022%d%s" % (i, day)
                else:
                    dd = "20220%d%s" % (i, day)
                days.append(dd)
        elif '每季度首月' in rulue2:
            for i in [1,4,7,10]:
                if i >=10:
                    dd = "2022%d%s" % (i, day)
                else:
                    dd = "20220%d%s" % (i, day)
                days.append(dd)
        elif'每季度第二个月' in rulue2:
            for i in [2,5,8,11]:
                if i >=10:
                    dd = "2022%d%s" % (i, day)
                else:
                    dd = "20220%d%s" % (i, day)
                days.append(dd)
    elif '最后一个工作日' in day:
        if '每月' in rulue2:
            for i in range(1,13):
                if i >=10:
                    dd = "2022%d" % i
                else:
                    dd = "20220%d" % i
                ddd = workingday[workingday.work.str.contains(dd)].values[-1][0]
                days.append(ddd)
        elif '每季度末月' in rulue2:
            for i in [3,6,9,12]:
                if i >=10:
                    dd = "2022%d" %i
                else:
                    dd = "20220%d" %i
                ddd = workingday[workingday.work.str.contains(dd)].values[-1][0]
                days.append(ddd)
        elif '每季度首月' in rulue2:
            for i in [1,4,7,10]:
                if i >=10:
                    dd = "2022%d" %i
                else:
                    dd = "20220%d" %i
                ddd = workingday[workingday.work.str.contains(dd)].values[-1][0]
                days.append(ddd)
        elif'每季度第二个月' in rulue2:
            for i in [2,5,8,11]:
                if i >=10:
                    dd = "2022%d" %i
                else:
                    dd = "20220%d" %i
                ddd = workingday[workingday.work.str.contains(dd)].values[-1][0]
                days.append(ddd)
    elif '最后一个交易日' in day:
        if '每月' in rulue2:
            for i in range(1,13):
                if i >=10:
                    dd = "2022%d" % i
                else:
                    dd = "20220%d" % i
                ddd = tradingday[tradingday.trading.str.contains(dd)].values[-1][0]
                days.append(ddd)
        elif '每季度末月' in rulue2:
            for i in [3,6,9,12]:
                if i >=10:
                    dd = "2022%d" %i
                else:
                    dd = "20220%d" %i
                ddd = tradingday[tradingday.trading.str.contains(dd)].values[-1][0]
                days.append(ddd)
        elif '每季度首月' in rulue2:
            for i in [1,4,7,10]:
                if i >=10:
                    dd = "2022%d" %i
                else:
                    dd = "20220%d" %i
                ddd = tradingday[tradingday.trading.str.contains(dd)].values[-1][0]
                days.append(ddd)
        elif'每季度第二个月' in rulue2:
            for i in [2,5,8,11]:
                if i >=10:
                    dd = "2022%d" %i
                else:
                    dd = "20220%d" %i
                ddd = tradingday[tradingday.trading.str.contains(dd)].values[-1][0]
                days.append(ddd)
     
    if '每个月的倒数第6个交易日' in guize:
        for i in range(1,13):
            if i >=10:
                dd = "2022%d" % i
            else:
                dd = "20220%d" % i
            ddd = tradingday[tradingday.trading.str.contains(dd)].values[-6][0]
            Days.append(ddd)
        return Days
    elif '每月的第一个工作日（不含）之前倒算5个交易日当日' in guize:
        for i in range(1,13):
            if i >=10:
                dd = "2022%d" % i
            else:
                dd = "20220%d" % i
            ddd = workingday[workingday.work.str.contains(dd)].values[0][0]
            ddd = get_pianli_jday(ddd,-5)
            Days.append(ddd)
        return Days
        
    for dayj in days:
        if rulue0 == 'working':
            while dayj not in workingdaylist:
                if rulue1 == '顺延':
                    dayj = datetime.strptime(dayj, "%Y%m%d")
                    dayj = dayj + timedelta(days = 1) ## 设置起始日期
                    dayj = dayj.strftime("%Y%m%d")
                    #print(dayj)
                else:
                    dayj = datetime.strptime(dayj, "%Y%m%d")
                    dayj = dayj - timedelta(days = 1) ## 设置起始日期
                    dayj = dayj.strftime("%Y%m%d")
            Days.append(dayj)
        elif rulue0 == 'trading':
            while dayj not in tradingdaylist:
                if rulue1 == '顺延':
                    dayj = datetime.strptime(dayj, "%Y%m%d")
                    dayj = dayj + timedelta(days = 1) ## 设置起始日期
                    dayj = dayj.strftime("%Y%m%d")
                else:
                    dayj = datetime.strptime(dayj, "%Y%m%d")
                    dayj = dayj - timedelta(days = 1) ## 设置起始日期
                    dayj = dayj.strftime("%Y%m%d")
            Days.append(dayj)

    return Days
#%%
import  re
Data = pd.read_excel(r'E:\项目文件夹\陈良方\我的坚果云\浦发银行\开放日\开放日\浦发银行申赎规则-xmj-chenlf.xlsx', sheet_name="Sheet1")   
for index, dd in Data.iterrows():
    if re.compile('\d+').findall(dd.开放日规则):
        day = re.compile('\d+').findall(dd.开放日规则)[0]
    elif re.compile('最后一个工作日').findall(dd.开放日规则):
        day = re.compile('最后一个工作日').findall(dd.开放日规则)[0]
    elif re.compile('最后一个交易日').findall(dd.开放日规则):
        day = re.compile('最后一个交易日').findall(dd.开放日规则)[0]
    guize = dd.开放日规则     
    if '每月' in dd.开放日规则:
        rulue2 = '每月'
    elif '季度末月' in dd.开放日规则:
        rulue2 = '每季度末月'
    elif '季度首月' in dd.开放日规则:
        rulue2 = '每季度首月'
    elif '季度第二个月' in dd.开放日规则:
        rulue2 = '每季度第二个月'
    if dd.日历类型 == '工作日':
        rulue0 = 'working'
    elif dd.日历类型 == '交易日':
        rulue0 = 'trading'
    rulue1 = dd.是否顺延
    
    Days = get_fixed_day(guize,day = day, rulue0 = rulue0, rulue1 = rulue1, rulue2 =rulue2)     
    DDD = pd.DataFrame(pd.Series(Days))
    DDD.columns = ['开放日']
    if dd.日历类型 == '交易日':
        if type(dd.申购开始日) == str and len(dd.申购开始日) > 2:
            try:
                sg_start = int(dd.申购开始日[1:])
                DDD['申购开始日'] = DDD.开放日.apply(get_pianli_jday,args=(int(sg_start),))
            except:
                print(dd.申购开始日)
                if dd.申购开始日 == "未规定":
                    DDD['申购开始日'] = DDD.开放日.apply(get_fix_day_mounth, args=(1,rulue0 ))
        if type(dd.申购截止日) == str:
            sg_end = dd.申购截止日[1:]
            DDD['申购截止日'] = DDD.开放日.apply(get_pianli_jday,args=(int(sg_end),))
        else:
            sg_end = None
            DDD['申购截止日'] = DDD.开放日
             
        if type(dd.赎回开始日) == str and  len(dd.赎回开始日) > 2:
            try:
                sh_start = int(dd.赎回开始日[1:])
                DDD['赎回开始日'] = DDD.开放日.apply(get_pianli_jday,args=(int(sh_start),))
            except:
                print(dd.赎回开始日)
                if dd.赎回开始日 == "未规定":
                    DDD['赎回开始日'] = DDD.开放日.apply(get_fix_day_mounth, args=(1,rulue0 ))
        else:
            sh_start = None
            DDD['赎回开始日'] = DDD.开放日.apply(get_pianli_jday,args=(int(dd.赎回截止日[1:])-5,))
        if type(dd.赎回截止日) == str:
            sh_end = dd.赎回截止日[1:]
            DDD['赎回截止日'] = DDD.开放日.apply(get_pianli_jday,args=(int(sh_end),))
        else:
            sh_end = None
            DDD['赎回截止日'] = DDD.开放日
    if dd.日历类型 == '工作日':
        if type(dd.申购开始日) == str and len(dd.申购开始日) > 2:
            try:
                sg_start = int(dd.申购开始日[1:])
                DDD['申购开始日'] = DDD.开放日.apply(get_pianli_wday,args=(int(sg_start),))
            except:
                if dd.申购开始日 == "未规定":
                    DDD['申购开始日'] = DDD.开放日.apply(get_fix_day_mounth, args=(1,rulue0 ))
        if type(dd.申购截止日) == str:
            sg_end = dd.申购截止日[1:]
            DDD['申购截止日'] = DDD.开放日.apply(get_pianli_wday,args=(int(sg_end),))
        else:
            sg_end = None
            DDD['申购截止日'] = DDD.开放日
             
        if type(dd.赎回开始日) == str and len(dd.赎回开始日) > 2:
            try:
                sh_start = int(dd.赎回开始日[1:])
                DDD['赎回开始日'] = DDD.开放日.apply(get_pianli_wday,args=(int(sh_start),))
            except:
                if dd.赎回开始日 == "未规定":
                    DDD['赎回开始日'] = DDD.开放日.apply(get_fix_day_mounth, args=(1,rulue0 ))

        #else:
            #sh_start = None
            #DDD['赎回开始日'] = DDD.开放日.apply(get_pianli_wday,args=(int(dd.赎回截止日[1:])-5,))
        if type(dd.赎回截止日) == str:
            sh_end = dd.赎回截止日[1:]
            DDD['赎回截止日'] = DDD.开放日.apply(get_pianli_wday,args=(int(sh_end),))
        else:
            sh_end = None
            DDD['赎回截止日'] = DDD.开放日       
    ffff = lambda x: '%s-%s-%s' %(x[:4],x[4:6],x[6:8])
    DDD.开放日 = DDD.开放日.apply(ffff)
    DDD.申购开始日 = DDD.申购开始日.apply(ffff)
    DDD.申购截止日 = DDD.申购截止日.apply(ffff)
    DDD.赎回开始日 = DDD.赎回开始日.apply(ffff)
    DDD.赎回截止日 = DDD.赎回截止日.apply(ffff)
    #DDD.to_excel(r'E:\项目文件夹\陈良方\我的坚果云\浦发银行\开放日\开放日\%s.xlsx' %dd.产品名称, sheet_name = '%s' %dd.项目名称)
    #wb = xw.Book(r'E:\项目文件夹\陈良方\我的坚果云\中信银行\开放日模板.xlsx') 
    if dd.首个可赎回开放日 == '已过封闭期' or dd.首个可赎回开放日 == '无封闭期':
        DDD['首个可赎回开放日'] = True
    #elif type(dd.首个可赎回开放日) == float:
    #    DDD['是否可以赎回'] = '缺少数据'
    else:
        DDD['是否可以赎回'] = DDD.开放日.apply(lambda x: datetime.strptime(x,"%Y-%m-%d")) >= dd.首个可赎回开放日
    DDD['申购许可'] = dd.申购许可
    DDD.to_excel(r'E:\项目文件夹\陈良方\我的坚果云\浦发银行\开放日\开放日-news\%s.xlsx' %dd.产品名称, sheet_name = '%s' %dd.产品名称)
#%%

writer = pd.ExcelWriter(r'E:\项目文件夹\陈良方\我的坚果云\浦发银行\开放日\产品开放日-2022年全年-华润信托-final.xlsx')

path = r'E:\项目文件夹\陈良方\我的坚果云\浦发银行\开放日\开放日-news'
files = os.listdir(path)

for i in range(1,13):
    #file = files[0]
    #i = 1
    data = pd.read_excel(r'E:\项目文件夹\陈良方\我的坚果云\浦发银行\开放日\产品开放日-2022年全年（每月）-华润信托.xls')
    for file in files:
        da = pd.read_excel(os.path.join(path, file))
        if i >=10:
            ss = da[da.开放日.str.contains('2022-%s' % i)]
        else:
            ss = da[da.开放日.str.contains('2022-0%s' % i)]
        if ss.shape[0] == 1:
            inedx1 = data[data.产品名称 == file[:-5]].index[0]
            inedx2 = data[data.产品名称 == file[:-5]].index[1]
            if ss.values[0][-1] == '不开放申购':
                data.iloc[[inedx1],6] = ''
                data.iloc[[inedx1],7] = ''
                data.iloc[[inedx1],8] = ''
                data.iloc[[inedx1],9] = ss.values[0][-1]
            else:
                data.iloc[[inedx1],6] = ss.values[0][2]
                data.iloc[[inedx1],7] = ss.values[0][3]
                data.iloc[[inedx1],8] = ss.values[0][1]
                data.iloc[[inedx1],9] = ss.values[0][-1]
            if ss.values[0][-2]:
                data.iloc[[inedx2],6] = ss.values[0][4]
                data.iloc[[inedx2],7] = ss.values[0][5]
                data.iloc[[inedx2],8] = ss.values[0][1]
                data.iloc[[inedx2],10] = ss.values[0][-2]
            else:
                data.iloc[[inedx2],6] = ''
                data.iloc[[inedx2],7] = ''
                data.iloc[[inedx2],8] = ''
                data.iloc[[inedx2],10] = ss.values[0][-2]
                
    data.to_excel(writer, '%s月' %i)  # 这里假设df是一个pandas的dataframe
writer.save()
writer.close()
