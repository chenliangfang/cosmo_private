# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 16:19:19 2022

@author: CHENLF
"""

writer = pd.ExcelWriter(r'E:\项目文件夹\陈良方\我的坚果云\中信银行\华润-2022.xlsx')

path = r'E:\项目文件夹\陈良方\我的坚果云\中信银行\开放日'
files = os.listdir(path)

data = pd.read_excel(r'E:\项目文件夹\陈良方\我的坚果云\中信银行\华润.xlsx')




for i in range(1,13):
    data = pd.read_excel(r'E:\项目文件夹\陈良方\我的坚果云\中信银行\华润.xlsx')
    for file in files:
        da = pd.read_excel(os.path.join(r'E:\项目文件夹\陈良方\我的坚果云\中信银行\开放日', file))
        if i >=10:
            ss = da[da.开放日.str.contains('2022-%s' % i)]
        else:
            ss = da[da.开放日.str.contains('2022-0%s' % i)]
        if ss.shape[0] == 1:
            inedx = data[data.产品名称 == file[:-5]].index[0]
            data.iloc[[inedx],4] = ss.values[0][1]
            if ss["申购许可"].values[0] != "关申购":
                
                data.iloc[[inedx],5] = ss.values[0][2]
                data.iloc[[inedx],6] = ss.values[0][3]
            if ss["是否可以赎回"].values[0] == True:
                data.iloc[[inedx],7] = ss.values[0][4]
                data.iloc[[inedx],8] = ss.values[0][5]
            data.iloc[[inedx],9] = ss.values[0][6]
            data.iloc[[inedx],10] = ss.values[0][7]
    data.to_excel(writer, '%s月' %i)  # 这里假设df是一个pandas的dataframe

writer.save()
writer.close()
