# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 16:01:31 2021

@author: CHENLF
"""
#%%
'''
#####  用来通过每一个私募管理人的页面爬取每一个私募产品的链接，
####   再爬取每一个链接下面的信息
'''


'''
* 获取私募基金管理人信息
'''

import requests,json, time
r = requests.post('', verify=False)
html=r.content
html_doc=str(html,'utf-8')
import requests
import pandas as pd

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


sites = 'https://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.667889619748349&page=%d&size=100'

data = json.dumps({
        'page':'0',
        'size':'100'
        })

## 设置头文件
headers = { 
"Accept": "application/json, text/javascript, */*; q=0.01",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
"Connection": "keep-alive",
"Content-Length": "1",
"Content-Type": "application/json",
"Cookie": "Hm_lvt_a0d0f99af80247cfcb96d30732a5c560=1630548738,1630550291,1630840416,1631168789",
"Host": "gs.amac.org.cn",
"Origin": "https://gs.amac.org.cn",
"Referer": "https://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html",
"sec-ch-ua": '''"Microsoft Edge";v="93", " Not;A Brand";v="99", "Chromium";v="93"''',
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": "Windows",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-origin",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47",
"X-Requested-With": "XMLHttpRequest"
}

respon = requests.post(sites,data, headers = headers ,stream = True,verify=False,allow_redirects=False)
respon.json()

Datas = pd.DataFrame(respon.json()['content'])

for page in range(1,245):
    data = data = json.dumps({
        'page':'%d' % page,
        'size':'100'
        })
    respon = requests.post(sites % page,data, headers = headers ,stream = True,verify=False,allow_redirects=False)
    print(page)
    Datas = Datas.append(pd.DataFrame(respon.json()['content']))
    
Datas.to_excel(r'E:\Demos\基金业协会\会员信息.xlsx')
Datas.loc[:,'info']= ''
Datas.index = range(24427)
Sites = 'https://gs.amac.org.cn/amac-infodisc/res/pof/manager/%s'
Datas.loc[0,'url']

for index, row in Datas.iterrows():
    url = row['url']
    sites = 'https://gs.amac.org.cn/amac-infodisc/res/pof/manager/%s' % url
    info = pd.read_html(sites)
    info = info[5]
    ff.columns = ['时间', '任职单位', '任职部门', '职务']
    dd = ff[ff.时间 == '工作履历'].职务
    strs = ''
    for i in dd:
        strs = strs + i
    strs = strs.replace('时间','').replace('任职单位','').replace('任职部门','').replace('职务','').replace(' ','')
    Datas.loc[index,'info'] = strs
    time.sleep(0.005)
    print(row['managerName'], index)
import requests,json, time
import pandas as pd

Datas = pd.read_excel(r'E:\Demos\基金业协会\会员信息.xlsx')
Datas = Datas[Datas.primaryInvestType == '私募证券投资基金管理人']
Datas.index = range(8875)
for index, row in Datas.iterrows():
    if index >= 0:
        url = row['url']
        sites = 'https://gs.amac.org.cn/amac-infodisc/res/pof/manager/%s' % url
        try:
            info = pd.read_html(sites)
            info_ = info[5]
            info_.columns = ['时间', '任职单位', '任职部门', '职务']
            dd = info_[info_.时间 == '工作履历'].职务
            strs = ''
            for i in dd:
                strs = strs + i
        except:
            try:
                info = pd.read_html(sites)
                info_ = info[6]
                info_.columns = ['时间', '任职单位', '任职部门', '职务']
                dd = info_[info_.时间 == '工作履历'].职务
                strs = ''
                for i in dd:
                    strs = strs + i
            except:
                pass
        strs = strs.replace('时间','').replace('任职单位','').replace('任职部门','').replace('职务','').replace(' ','')
        Datas.loc[index,'info'] = strs
        #time.sleep(0.005)
        print(row['managerName'], index)


import requests,json, time
import pandas as pd

Datas = pd.read_excel(r'E:\Demos\基金业协会\会员信息.xlsx')
Datas.index = range(24427)


Datas = Datas[Datas.primaryInvestType == '私募证券投资基金管理人']
Datas.index = range(8875)
Datas = Datas[5000:5999]
Datas.index = range(999)

for index, row in Datas.iterrows():
    if index >= 0:
        url = row['url']
        sites = 'https://gs.amac.org.cn/amac-infodisc/res/pof/manager/%s' % url
        try:
            info = pd.read_html(sites)
            info_ = info[5]
            info_.columns = ['时间', '任职单位', '任职部门', '职务']
            dd = info_[info_.时间 == '工作履历'].职务
            strs = ''
            for i in dd:
                strs = strs + i
        except:
            try:
                info = pd.read_html(sites)
                info_ = info[6]
                info_.columns = ['时间', '任职单位', '任职部门', '职务']
                dd = info_[info_.时间 == '工作履历'].职务
                strs = ''
                for i in dd:
                    strs = strs + i
            except:
                pass
        strs = strs.replace('时间','').replace('任职单位','').replace('任职部门','').replace('职务','').replace(' ','')
        Datas.loc[index,'info'] = strs
        time.sleep(0.005)
        print(row['managerName'], index)

Datas.to_excel('证券类.xlsx')




import requests,json, time
import pandas as pd

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

data = json.dumps({
        'rand':'0.10404161764410946',
        'page':'1',
        'size':'100'
        })

sites = 'https://gs.amac.org.cn/amac-infodisc/api/pof/fund?rand=0.10404161764410946&page=2&size=10'
## 设置头文件
headers = { 
"Accept": "application/json, text/javascript, */*; q=0.01",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
"Connection": "keep-alive",
"Content-Length": "2",
"Content-Type": "application/json",
"Cookie": "Hm_lvt_a0d0f99af80247cfcb96d30732a5c560=1630840416,1631168789,1631951774,1632276782; Hm_lpvt_a0d0f99af80247cfcb96d30732a5c560=1632276845",
"Host": "gs.amac.org.cn",
"Origin": "https://gs.amac.org.cn",
"Referer": "https://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html",
"sec-ch-ua": '''"Microsoft Edge";v="93", " Not;A Brand";v="99", "Chromium";v="93"''',
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": "Windows",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-origin",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52",
"X-Requested-With": "XMLHttpRequest"
}



respon = requests.post(sites,data, headers = headers ,stream = True,verify=False,allow_redirects=False)
requests.post(sites, json = data, headers = headers,verify=False,stream = True,allow_redirects=False )
respon.json()
respon.raise_for_status

sites = 'https://gs.amac.org.cn/amac-infodisc/api/pof/manager/query?rand=0.5478532234795108&page=0&size=8000'

jsons = {"primaryInvestType":"smzqtzjjglr","regiProvinceFsc":"province","offiProvinceFsc":"province",
 "fundScale":"scope01","establishDate":{"from":"1900-01-01","to":"9999-01-01"},
 "registerDate":{"from":"1900-01-01","to":"9999-01-01"}}

headers = { 
"Accept": "application/json, text/javascript, */*; q=0.01",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
"Connection": "keep-alive",
"Content-Length": "2",
"Content-Type": "application/json",
"Cookie": "Hm_lvt_a0d0f99af80247cfcb96d30732a5c560=1630840416,1631168789,1631951774,1632276782; Hm_lpvt_a0d0f99af80247cfcb96d30732a5c560=1632276845",
"Host": "gs.amac.org.cn",
"Origin": "https://gs.amac.org.cn",
"Referer": "https://gs.amac.org.cn/amac-infodisc/res/pof/manager/managerList.html",
"sec-ch-ua": '''"Microsoft Edge";v="93", " Not;A Brand";v="99", "Chromium";v="93"''',
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": "Windows",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-origin",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52",
"X-Requested-With": "XMLHttpRequest"
}

respon = requests.post(sites, json = jsons, headers = headers,verify=False,stream = True,allow_redirects=False )
data = respon.json()['content']
DataFrame = pd.DataFrame(data)
DataFrame1 = pd.DataFrame(data)
DataFrame2 = pd.DataFrame(data)
DataFrame3 = pd.DataFrame(data)
DataFrame4 = pd.DataFrame(data)
DataFrame5 = pd.DataFrame(data)

DataFrame.groupby('officeAdrAgg',as_index=False)['managerName'].count()
DataFrame1.groupby('officeAdrAgg',as_index=False)['managerName'].count()
DataFrame2.groupby('officeAdrAgg',as_index=False)['managerName'].count()
DataFrame3.groupby('officeAdrAgg',as_index=False)['managerName'].count()
DataFrame4.groupby('officeAdrAgg',as_index=False)['managerName'].count()
DataFrame5.groupby('officeAdrAgg',as_index=False)['managerName'].count()

