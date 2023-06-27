#!/usr/bin/env python
# coding: utf-8

# In[1]:


#1.引入包
import pandas as pd
from pandas import Series,DataFrame
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randn
import datetime
import seaborn as sns
import os
import statsmodels.api as smx
from statsmodels.formula.api import ols
from numpy import array, cov, corrcoef


# In[2]:


df1 = pd.read_excel(r'C:\Users\t84187675\Desktop\CL1.xlsx')

df2 = pd.read_excel(r'C:\Users\t84187675\Desktop\CL2.xlsx')

df3 = pd.read_excel(r'C:\Users\t84187675\Desktop\CL3.xlsx')


# In[3]:


#2.合并数据
frames = [df1, df2,df3]
df=pd.concat(frames)
df


# In[4]:


da1=df.rename(columns={'Query':'keywords'})
da1


# In[5]:


da2=pd.read_excel(r'C:\Users\t84187675\Desktop\HSI\Q4\CL HSI\model data\CL-keywords(no use).xlsx')  


# In[6]:


#按照keywords合并每日impression和user_journey成新表impression）
da_impression=pd.merge(left=da1,right=da2,left_on= "keywords",right_on="keywords")
da_impression


# In[7]:


da3=pd.read_excel(r'C:\Users\t84187675\Desktop\HSI\Q4\CL HSI\model data\CL-sales.xlsx')#导入sales表
da3


# In[33]:


#查看use阶段关键词的前10
kku=da_impression[da_impression['user_journey']=='Use']
kkr=kku.sort_values(by='search_volume',ascending=False)
kkr.head(20)


# In[34]:


#查看各品类的sale_volume占比-sales表
kk1=da3.groupby(['product_category'],as_index=False)['sale_volume'].sum()
print(kk1)


# In[35]:


#查看各品类的impression占比-impression表
kk2=da_impression.groupby(['product_category'],as_index=False)['search_volume'].sum()
print(kk2)


# In[36]:


#查看user journey的impression占比
kk3=da_impression.groupby(['user_journey'],as_index=False)['search_volume'].sum()
print(kk3)


# # 大盘

# In[52]:


#按照日期对impression做数据透视表
da_impression=da_impression.pivot_table(index='Date',values=['search_volume'],aggfunc='sum')
da_impression.reset_index(inplace=True)
#按照日期对sale做数据透视表
da3=da3.pivot_table(index='date_sale',aggfunc='sum')
da3.reset_index(inplace=True)
#3按照date将impression和sale两个表拼接到一个表

da_th=da_impression.merge(da3,left_on = 'Date',right_on = 'date_sale',how = 'inner')
da_th


# # 后延

# In[8]:


#按照日期对impression做数据透视表
da_impression=da_impression.pivot_table(index='Date',values=['search_volume'],aggfunc='sum')
da_impression.reset_index(inplace=True)
#按照日期对sale做数据透视表
da3=da3.pivot_table(index='date_sale',aggfunc='sum')
da3.reset_index(inplace=True)
#偏移2天将impression和sale两个表拼接到一个表
da_impression['Date']=da_impression['Date']+datetime.timedelta(days =2)
da_th=da_impression.merge(da3,left_on = 'Date',right_on = 'date_sale',how = 'inner')
#相关性分析
sns.heatmap(da_th[["search_volume","sale_volume"]].corr(),annot=True, vmax=1,vmin = 0, xticklabels= True, yticklabels= True, square=True, cmap="YlGnBu")


# In[23]:


#导出
da_th.to_excel(r'C:\Users\t84187675\Desktop\output.xlsx')


# In[38]:


#将按日期处理合并后的表按weekday处理，查看数据
da_th['weekday']= da_th['date_sale'].dt.day_name()
sns.catplot(x="sale_volume", y="weekday", jitter=False, data=da_th)
print(da_th)


# In[15]:


#描述统计
desc=da_th.describe() 
print(desc)


# In[16]:


#箱型图查看异常值
plt.figure(figsize=(8,9))
sns.boxplot(y=da_th["search volume"],flierprops = {'marker':'o',#异常值形状
                          'markerfacecolor':'red',#形状填充色
                          'color':'black',#形状外廓颜色
                         },) 


# In[24]:


# 计算下四分位数和上四分位
Q1 =57760
Q3 =92048

# 基于1.5倍的四分位差计算上下须对应的值
low_whisker = Q1 - 1.5*(Q3 - Q1)
up_whisker = Q3 + 1.5*(Q3 - Q1)

# 寻找异常点
da_th.Impressions[(da_th.Impressions > up_whisker) | (da_th.Impressions < low_whisker)]


# 异常值

# In[52]:


#删除异常的数据
da_th=da_th[(da_th.Impressions < up_whisker)]
da_th


# In[25]:





# In[38]:


# 计算下四分位数和上四分位
Q1 =1622
Q3 =3270

# 基于1.5倍的四分位差计算上下须对应的值
low_whisker = Q1 - 1.5*(Q3 - Q1)
up_whisker = Q3 + 1.5*(Q3 - Q1)

# 寻找异常点
da_th.sale_volume[(da_th.sale_volume > up_whisker) | (da_th.sale_volume < low_whisker)]


# In[57]:


#时序图
sns.set_style("white")

x = da_th["Date"]
y1 = da_th["search_volume"]
y2 = da_th["sale_volume"]

plt.rcParams['figure.figsize'] = (12.0,5.0)
fig = plt.figure()

ax1 = fig.add_subplot(111)
ax1.stackplot(x, y1,color='mediumaquamarine')
ax1.set_ylabel('Search_volume',fontsize='15')

ax2 = ax1.twinx()   #组合图必须加这个
ax2.plot(x, y2, 'b',ms=10)
ax2.set_ylabel('Sale_volume',fontsize='15')
plt.show()


# In[54]:


#散点图
plt.scatter(y1, y2)
plt.xlabel("Search_volume",fontsize='15')
plt.ylabel("Sale volume",fontsize='15')
plt.show()


# In[55]:


#相关性分析
sns.heatmap(da_th[["search_volume","sale_volume"]].corr(),annot=True, vmax=1,vmin = 0, xticklabels= True, yticklabels= True, square=True, cmap="YlGnBu")


# In[43]:


#一元线性回归
lm_th=ols('sale_volume~ search_volume',data=da_th).fit()
print(lm_th.summary())


# # user-journey

# In[100]:


da_impression.info()


# In[96]:


#筛选掉missing value
da_impression1=da_impression[da_impression.user_journey.notnull()]
da_impression1.info()


# # 后延

# In[101]:


#按照日期对impression做数据透视表
da_impression2=da_impression.pivot_table(index='Date',columns='user_journey',values=['Impressions'],aggfunc='sum')
da_impression2.columns =da_impression2.columns.droplevel(0)
da_impression2.columns.name = None 
da_impression2.reset_index(inplace=True)
#按照日期对sale做数据透视表
da4=da3.pivot_table(index='date_sale',aggfunc='sum')
da4.reset_index(inplace=True)
#后延1天将impression和sale两个表拼接到一个表
da_impression2['Date']=da_impression2['Date']+datetime.timedelta(days =1)
da_th1=da_impression2.merge(da4,left_on = 'Date',right_on = 'date_sale',how = 'inner')
da_th1


# In[57]:


#按照日期对impression做数据透视表
da_impression2=da_impression1.pivot_table(index='Date',columns='user_journey',values=['Impressions'],aggfunc='sum')

da_impression2.columns =da_impression2.columns.droplevel(0)
da_impression2.columns.name = None 
da_impression2.reset_index(inplace=True)
#按照日期对sale做数据透视表
da4=da3.pivot_table(index='date_sale',aggfunc='sum')
da4.reset_index(inplace=True)
#3按照date将impression和sale两个表拼接到一个表
da_th1=da_impression2.merge(da4,left_on = 'Date',right_on = 'date_sale',how = 'inner')
da_th1


# In[102]:


#看线性回归情况
lm_th=ols('sale_volume~Discover + Consider + Purchase + Use',data=da_th1).fit()
print(lm_th.summary())

#查看品类相关性
sns.heatmap(da_th1.corr(),annot=True, vmax=1,vmin = 0, xticklabels= True, yticklabels= True, square=True, cmap="YlGnBu")


# # phone 品类（整体）

# In[173]:


# 整体
phone1=(da_impression["product_category"]=="Phones")
phone2=(da3["product_category"]=="Phones")
phone_1=da_impression.loc[phone1]
phone_2=da3.loc[phone2]
# 按照日期对impression做数据透视表
phone1_1=phone_1.pivot_table(index='Date',values=['Impressions'],aggfunc='sum')
phone1_1.reset_index(inplace=True)
# 按照日期对sale做数据透视表
phone2_1=phone_2.pivot_table(index='date_sale',aggfunc='sum')
phone2_1.reset_index(inplace=True)

print(phone1_1)
print(phone2_1)


# In[174]:


#合并
phone_decay=phone1_1.merge(phone2_1,left_on = "Date",right_on = 'date_sale',how = 'inner')
phone_decay
phone_decay.info()


# In[175]:


#描述统计
desc=phone_decay.describe() 
print(desc)


# In[176]:


#箱型图查看异常值
plt.figure(figsize=(8,9))
sns.boxplot(y=phone_decay["Impressions"],flierprops = {'marker':'o',#异常值形状
                          'markerfacecolor':'red',#形状填充色
                          'color':'black',#形状外廓颜色
                         },) 


# In[177]:


# 计算下四分位数和上四分位
Q1 =15965
Q3 =23715

# 基于1.5倍的四分位差计算上下须对应的值
low_whisker = Q1 - 1.5*(Q3 - Q1)
up_whisker = Q3 + 1.5*(Q3 - Q1)

# 寻找异常点
phone_decay.Impressions[(phone_decay.Impressions > up_whisker) | (phone_decay.Impressions < low_whisker)]


# In[178]:


#箱型图查看异常值
plt.figure(figsize=(8,9))
sns.boxplot(y=phone_decay["sale_volume"],flierprops = {'marker':'o',#异常值形状
                          'markerfacecolor':'red',#形状填充色
                          'color':'black',#形状外廓颜色
                         },) 


# In[179]:


#删除异常的数据
phone_decay=phone_decay[(phone_decay.Impressions < up_whisker)]
phone_decay


# In[180]:


#线性回归及相关性
th_phone=ols('sale_volume~ Impressions',data=phone_decay).fit()
print(th_phone.summary())

sns.set(font_scale=1.6)
sns.heatmap(phone_decay.corr(),annot=True, vmax=1,vmin = 0, xticklabels= True, yticklabels= True, square=True, cmap="YlGnBu")


# In[137]:


#时序图
sns.set_style("white")

x = phone_decay["Date"]
y1 = phone_decay["Impressions"]
y2 = phone_decay["sale_volume"]

plt.rcParams['figure.figsize'] = (12.0,5.0)
fig = plt.figure()

ax1 = fig.add_subplot(111)
ax1.stackplot(x, y1,color='mediumaquamarine')
ax1.set_ylabel('Impression',fontsize='15')

ax2 = ax1.twinx()   #组合图必须加这个
ax2.plot(x, y2, 'b',ms=10)
ax2.set_ylabel('Sale volume',fontsize='15')
plt.show()


# In[138]:


#散点图
plt.scatter(y1, y2)
plt.xlabel("Search Impression",fontsize='15')
plt.ylabel("Sale volume",fontsize='15')
plt.show()


# # phone 品类（user-journey)

# In[181]:


# 按照日期对impression做数据透视表
uphone1_1=phone_1.pivot_table(index='Date',columns='user_journey',values=['Impressions'],aggfunc='sum')
uphone1_1.columns = uphone1_1.columns.droplevel(0)
uphone1_1.columns.name = None 
uphone1_1.reset_index(inplace=True)
print(uphone1_1)
# 按照日期对sale做数据透视表
uphone2_1=phone_2.pivot_table(index='date_sale',aggfunc='sum')
uphone2_1.reset_index(inplace=True)
uphone_decay=uphone1_1.merge(uphone2_1,left_on = "Date",right_on = 'date_sale',how = 'inner')
uphone_decay


# In[182]:


cl_uphone=ols('sale_volume~ Consider + Purchase + Use',data=uphone_decay).fit()
print(cl_uphone.summary())

sns.heatmap(uphone_decay.corr(),annot=True, vmax=1,vmin = 0, xticklabels= True, yticklabels= True, square=True, cmap="YlGnBu")


# # wearables品类（整体）

# In[224]:


# 整体
wearables1=(da_impression["product_category"]=="Wearables")
wearables2=(da3["product_category"]=="Wearables")
wearables_1=da_impression.loc[wearables1]
wearables_2=da3.loc[wearables2]
# 按照日期对impression做数据透视表
wearables1_1=wearables_1.pivot_table(index='Date',values=['Impressions'],aggfunc='sum')
wearables1_1.reset_index(inplace=True)
# 按照日期对sale做数据透视表
wearables2_1=wearables_2.pivot_table(index='date_sale',aggfunc='sum')
wearables2_1.reset_index(inplace=True)

print(wearables1_1)
print(wearables2_1)


# In[225]:


#合并
wearables_decay=wearables1_1.merge(wearables2_1,left_on = "Date",right_on = 'date_sale',how = 'inner')
wearables_decay
wearables_decay.info()


# In[226]:


#描述统计
desc=wearables_decay.describe() 
print(desc)


# In[227]:


#箱型图查看异常值
plt.figure(figsize=(8,9))
sns.boxplot(y=phone_decay["Impressions"],flierprops = {'marker':'o',#异常值形状
                          'markerfacecolor':'red',#形状填充色
                          'color':'black',#形状外廓颜色
                         },) 


# In[228]:


#箱型图查看异常值
plt.figure(figsize=(8,9))
sns.boxplot(y=phone_decay["sale_volume"],flierprops = {'marker':'o',#异常值形状
                          'markerfacecolor':'red',#形状填充色
                          'color':'black',#形状外廓颜色
                         },) 


# In[193]:


#线性回归及相关性
cl_wearables=ols('sale_volume~ Impressions',data=wearables_decay).fit()
print(cl_wearables.summary())

sns.set(font_scale=1.6)
sns.heatmap(wearables_decay.corr(),annot=True, vmax=1,vmin = 0, xticklabels= True, yticklabels= True, square=True, cmap="YlGnBu")


# In[194]:


#时序图
sns.set_style("white")

x = wearables_decay["Date"]
y1 = wearables_decay["Impressions"]
y2 = wearables_decay["sale_volume"]

plt.rcParams['figure.figsize'] = (12.0,5.0)
fig = plt.figure()

ax1 = fig.add_subplot(111)
ax1.stackplot(x, y1,color='mediumaquamarine')
ax1.set_ylabel('Impression',fontsize='15')

ax2 = ax1.twinx()   #组合图必须加这个
ax2.plot(x, y2, 'b',ms=10)
ax2.set_ylabel('Sale volume',fontsize='15')
plt.show()


# In[195]:


#散点图
plt.scatter(y1, y2)
plt.xlabel("Search Impression",fontsize='15')
plt.ylabel("Sale volume",fontsize='15')
plt.show()


# # wearables品类（user-journey）

# In[199]:


# 按照日期对impression做数据透视表
uwearables1_1=wearables_1.pivot_table(index='Date',columns='user_journey',values=['Impressions'],aggfunc='sum')
uwearables1_1.columns = uwearables1_1.columns.droplevel(0)
uwearables1_1.columns.name = None 
uwearables1_1.reset_index(inplace=True)
print(uphone1_1)
# 按照日期对sale做数据透视表
uwearables2_1=wearables_2.pivot_table(index='date_sale',aggfunc='sum')
uwearables2_1.reset_index(inplace=True)
uwearables_decay=uwearables1_1.merge(uwearables2_1,left_on = "Date",right_on = 'date_sale',how = 'inner')
uwearables_decay


# In[201]:


cl_uwearables=ols('sale_volume~ Consider',data=uwearables_decay).fit()
print(cl_uwearables.summary())

sns.heatmap(uwearables_decay.corr(),annot=True, vmax=1,vmin = 0, xticklabels= True, yticklabels= True, square=True, cmap="YlGnBu")


# # tablets（整体）

# In[232]:


# 整体
tablets1=(da_impression["product_category"]=="Tablets")
tablets2=(da3["product_category"]=="Tablets")
tablets_1=da_impression.loc[tablets1]
tablets_2=da3.loc[tablets2]
# 按照日期对impression做数据透视表
tablets1_1=tablets_1.pivot_table(index='Date',values=['Impressions'],aggfunc='sum')
tablets1_1.reset_index(inplace=True)
# 按照日期对sale做数据透视表
tablets2_1=tablets_2.pivot_table(index='date_sale',aggfunc='sum')
tablets2_1.reset_index(inplace=True)

print(tablets1_1)
print(tablets2_1)


# In[233]:


#合并
tablets_decay=tablets1_1.merge(tablets2_1,left_on = "Date",right_on = 'date_sale',how = 'inner')
tablets_decay
tablets_decay.info()


# In[234]:


#箱型图查看异常值-sale_volume
plt.figure(figsize=(8,9))
sns.boxplot(y=tablets_decay["sale_volume"],flierprops = {'marker':'o',#异常值形状
                          'markerfacecolor':'red',#形状填充色
                          'color':'black',#形状外廓颜色
                         },) 


# In[237]:


#箱型图查看异常值-Impressions
plt.figure(figsize=(8,9))
sns.boxplot(y=tablets_decay["Impressions"],flierprops = {'marker':'o',#异常值形状
                          'markerfacecolor':'red',#形状填充色
                          'color':'black',#形状外廓颜色
                         },) 


# In[218]:


#描述统计
desc=tablets_decay.describe() 
print(desc)


# In[235]:


# 计算下四分位数和上四分位
Q1 =90
Q3 =179

# 基于1.5倍的四分位差计算上下须对应的值
low_whisker = Q1 - 1.5*(Q3 - Q1)
up_whisker = Q3 + 1.5*(Q3 - Q1)

# 寻找异常点
tablets_decay.sale_volume[(tablets_decay.sale_volume > up_whisker) | (tablets_decay.sale_volume < low_whisker)]


# In[238]:


#删除异常的数据
tablets_decay=tablets_decay[(tablets_decay.sale_volume < up_whisker)]
tablets_decay


# In[239]:


#线性回归及相关性
cl_tablets=ols('sale_volume~ Impressions',data=tablets_decay).fit()
print(cl_tablets.summary())

sns.set(font_scale=1.6)
sns.heatmap(tablets_decay.corr(),annot=True, vmax=1,vmin = 0, xticklabels= True, yticklabels= True, square=True, cmap="YlGnBu")


# In[240]:


#时序图
sns.set_style("white")

x = tablets_decay["Date"]
y1 = tablets_decay["Impressions"]
y2 = tablets_decay["sale_volume"]

plt.rcParams['figure.figsize'] = (12.0,5.0)
fig = plt.figure()

ax1 = fig.add_subplot(111)
ax1.stackplot(x, y1,color='mediumaquamarine')
ax1.set_ylabel('Impression',fontsize='15')

ax2 = ax1.twinx()   #组合图必须加这个
ax2.plot(x, y2, 'b',ms=10)
ax2.set_ylabel('Sale volume',fontsize='15')
plt.show()


# In[241]:


#散点图
plt.scatter(y1, y2)
plt.xlabel("Search Impression",fontsize='15')
plt.ylabel("Sale volume",fontsize='15')
plt.show()


# # tablets品类（user-journey）

# In[242]:


# 按照日期对impression做数据透视表
utablets1_1=tablets_1.pivot_table(index='Date',columns='user_journey',values=['Impressions'],aggfunc='sum')
utablets1_1.columns = utablets1_1.columns.droplevel(0)
utablets1_1.columns.name = None 
utablets1_1.reset_index(inplace=True)
print(utablets1_1)
# 按照日期对sale做数据透视表
utablets2_1=tablets_2.pivot_table(index='date_sale',aggfunc='sum')
utablets2_1.reset_index(inplace=True)
utablets_decay=utablets1_1.merge(utablets2_1,left_on = "Date",right_on = 'date_sale',how = 'inner')
utablets_decay


# In[244]:


th_utablets=ols('sale_volume~ Consider',data=utablets_decay).fit()
print(th_utablets.summary())

sns.heatmap(utablets_decay.corr(),annot=True, vmax=1,vmin = 0, xticklabels= True, yticklabels= True, square=True, cmap="YlGnBu")


# # laptops（整体）

# In[248]:


# 整体
laptops1=(da_impression["product_category"]=="Laptops")
laptops2=(da3["product_category"]=="Laptops")
laptops_1=da_impression.loc[laptops1]
laptops_2=da3.loc[laptops2]
# 按照日期对impression做数据透视表
laptops1_1=laptops_1.pivot_table(index='Date',values=['Impressions'],aggfunc='sum')
laptops1_1.reset_index(inplace=True)
# 按照日期对sale做数据透视表
laptops2_1=laptops_2.pivot_table(index='date_sale',aggfunc='sum')
laptops2_1.reset_index(inplace=True)

print(laptops1_1)
print(laptops2_1)


# In[251]:


#合并
laptops_decay=laptops1_1.merge(laptops2_1,left_on = "Date",right_on = 'date_sale',how = 'inner')
laptops_decay
laptops_decay.info()


# In[252]:


#箱型图查看异常值-sale_volume
plt.figure(figsize=(8,9))
sns.boxplot(y=laptops_decay["sale_volume"],flierprops = {'marker':'o',#异常值形状
                          'markerfacecolor':'red',#形状填充色
                          'color':'black',#形状外廓颜色
                         },) 


# In[253]:


#箱型图查看异常值-Impressions
plt.figure(figsize=(8,9))
sns.boxplot(y=laptops_decay["Impressions"],flierprops = {'marker':'o',#异常值形状
                          'markerfacecolor':'red',#形状填充色
                          'color':'black',#形状外廓颜色
                         },) 


# In[254]:


#描述统计
desc=laptops_decay.describe() 
print(desc)


# In[ ]:


#均值处理异常值


# In[279]:


#线性回归及相关性
th_laptops=ols('sale_volume~ Impressions',data=laptops_decay).fit()
print(th_laptops.summary())

sns.set(font_scale=1.6)
sns.heatmap(laptops_decay.corr(),annot=True, vmax=1,vmin = 0, xticklabels= True, yticklabels= True, square=True, cmap="YlGnBu")


# In[280]:


#时序图
sns.set_style("white")

x = laptops_decay["Date"]
y1 = laptops_decay["Impressions"]
y2 = laptops_decay["sale_volume"]

plt.rcParams['figure.figsize'] = (12.0,5.0)
fig = plt.figure()

ax1 = fig.add_subplot(111)
ax1.stackplot(x, y1,color='mediumaquamarine')
ax1.set_ylabel('Impression',fontsize='15')

ax2 = ax1.twinx()   #组合图必须加这个
ax2.plot(x, y2, 'b',ms=10)
ax2.set_ylabel('Sale volume',fontsize='15')
plt.show()


# # laptops（user-journey）

# In[282]:


# 按照日期对impression做数据透视表
ulaptops1_1=laptops_1.pivot_table(index='Date',columns='user_journey',values=['Impressions'],aggfunc='sum')
ulaptops1_1.columns = ulaptops1_1.columns.droplevel(0)
ulaptops1_1.columns.name = None 
ulaptops1_1.reset_index(inplace=True)
print(ulaptops1_1)
# 按照日期对sale做数据透视表
ulaptops2_1=laptops_2.pivot_table(index='date_sale',aggfunc='sum')
ulaptops2_1.reset_index(inplace=True)
ulaptops_decay=ulaptops1_1.merge(ulaptops2_1,left_on = "Date",right_on = 'date_sale',how = 'inner')
ulaptops_decay


# In[283]:


th_ulaptops=ols('sale_volume~ consideration + purchase ',data=ulaptops_decay).fit()
print(th_ulaptops.summary())

sns.heatmap(ulaptops_decay.corr(),annot=True, vmax=1,vmin = 0, xticklabels= True, yticklabels= True, square=True, cmap="YlGnBu")


# # audio（整体）

# In[37]:


# 整体
audio1=(da_impression["product_category"]=="audio")
audio2=(da3["product_category"]=="audio")
audio_1=da_impression.loc[audio1]
audio_2=da3.loc[audio2]
# 按照日期对impression做数据透视表
audio1_1=audio_1.pivot_table(index='Date',values=['Impressions'],aggfunc='sum')
audio1_1.reset_index(inplace=True)
# 按照日期对sale做数据透视表
audio2_1=audio_2.pivot_table(index='date_sale',aggfunc='sum')
audio2_1.reset_index(inplace=True)

print(audio1_1)
print(audio2_1)


# In[38]:


#合并
audio_decay=audio1_1.merge(audio2_1,left_on = "Date",right_on = 'date_sale',how = 'inner')
audio_decay
audio_decay.info()


# In[39]:


#箱型图查看异常值
plt.figure(figsize=(8,9))
sns.boxplot(y=audio_decay["sale_volume"],flierprops = {'marker':'o',#异常值形状
                          'markerfacecolor':'red',#形状填充色
                          'color':'black',#形状外廓颜色
                         },) 


# In[40]:


#描述统计
desc=audio_decay.describe() 
print(desc)


# In[41]:


# 计算下四分位数和上四分位
Q1 =36
Q3 =62

# 基于1.5倍的四分位差计算上下须对应的值
low_whisker = Q1 - 1.5*(Q3 - Q1)
up_whisker = Q3 + 1.5*(Q3 - Q1)

# 寻找异常点
audio_decay.sale_volume[(audio_decay.sale_volume > up_whisker) | (audio_decay.sale_volume < low_whisker)]


# In[293]:


#线性回归及相关性
th_audio=ols('sale_volume~ Impressions',data=audio_decay).fit()
print(th_audio.summary())

sns.set(font_scale=1.6)
sns.heatmap(audio_decay.corr(),annot=True, vmax=1,vmin = 0, xticklabels= True, yticklabels= True, square=True, cmap="YlGnBu")


# In[294]:


#时序图
sns.set_style("white")

x = audio_decay["Date"]
y1 = audio_decay["Impressions"]
y2 = audio_decay["sale_volume"]

plt.rcParams['figure.figsize'] = (12.0,5.0)
fig = plt.figure()

ax1 = fig.add_subplot(111)
ax1.stackplot(x, y1,color='mediumaquamarine')
ax1.set_ylabel('Impression',fontsize='15')

ax2 = ax1.twinx()   #组合图必须加这个
ax2.plot(x, y2, 'b',ms=10)
ax2.set_ylabel('Sale volume',fontsize='15')
plt.show()


# # 异常值处理

# In[42]:


audio_decay['sale_volume'][(audio_decay['sale_volume'] > 102)] = 52


# In[43]:


#线性回归及相关性
th_audio=ols('sale_volume~ Impressions',data=audio_decay).fit()
print(th_audio.summary())

sns.set(font_scale=1.6)
sns.heatmap(audio_decay.corr(),annot=True, vmax=1,vmin = 0, xticklabels= True, yticklabels= True, square=True, cmap="YlGnBu")


# # audio（user-journey）

# In[288]:


# 按照日期对impression做数据透视表
uaudio1_1=audio_1.pivot_table(index='Date',columns='user_journey',values=['Impressions'],aggfunc='sum')
uaudio1_1.columns = uaudio1_1.columns.droplevel(0)
uaudio1_1.columns.name = None 
uaudio1_1.reset_index(inplace=True)
print(uaudio1_1)
# 按照日期对sale做数据透视表
uaudio2_1=audio_2.pivot_table(index='date_sale',aggfunc='sum')
uaudio2_1.reset_index(inplace=True)
uaudio_decay=uaudio1_1.merge(uaudio2_1,left_on = "Date",right_on = 'date_sale',how = 'inner')
uaudio_decay


# In[289]:


th_uaudio=ols('sale_volume~ consideration + purchase ',data=uaudio_decay).fit()
print(th_uaudio.summary())

sns.heatmap(uaudio_decay.corr(),annot=True, vmax=1,vmin = 0, xticklabels= True, yticklabels= True, square=True, cmap="YlGnBu")


# # accessories（整体）

# In[290]:


# 整体
accessories1=(da_impression["product_category"]=="accessories")
accessories2=(da3["product_category"]=="accessories")
accessories_1=da_impression.loc[accessories1]
accessories_2=da3.loc[accessories2]
# 按照日期对impression做数据透视表
accessories1_1=accessories_1.pivot_table(index='Date',values=['Impressions'],aggfunc='sum')
accessories1_1.reset_index(inplace=True)
# 按照日期对sale做数据透视表
accessories2_1=audio_2.pivot_table(index='date_sale',aggfunc='sum')
accessories2_1.reset_index(inplace=True)

print(accessories1_1)
print(accessories2_1)


# In[295]:


#合并
accessories_decay=accessories1_1.merge(accessories2_1,left_on = "Date",right_on = 'date_sale',how = 'inner')
accessories_decay
accessories_decay.info()


# In[296]:


#线性回归及相关性
th_accessories=ols('sale_volume~ Impressions',data=accessories_decay).fit()
print(th_accessories.summary())

sns.set(font_scale=1.6)
sns.heatmap(accessories_decay.corr(),annot=True, vmax=1,vmin = 0, xticklabels= True, yticklabels= True, square=True, cmap="YlGnBu")


# In[297]:


#时序图
sns.set_style("white")

x = accessories_decay["Date"]
y1 = accessories_decay["Impressions"]
y2 = accessories_decay["sale_volume"]

plt.rcParams['figure.figsize'] = (12.0,5.0)
fig = plt.figure()

ax1 = fig.add_subplot(111)
ax1.stackplot(x, y1,color='mediumaquamarine')
ax1.set_ylabel('Impression',fontsize='15')

ax2 = ax1.twinx()   #组合图必须加这个
ax2.plot(x, y2, 'b',ms=10)
ax2.set_ylabel('Sale volume',fontsize='15')
plt.show()


# # accessories（user-journey）

# In[298]:


# 按照日期对impression做数据透视表
uaccessories1_1=accessories_1.pivot_table(index='Date',columns='user_journey',values=['Impressions'],aggfunc='sum')
uaccessories1_1.columns = uaccessories1_1.columns.droplevel(0)
uaccessories1_1.columns.name = None 
uaccessories1_1.reset_index(inplace=True)
print(uaudio1_1)
# 按照日期对sale做数据透视表
uaccessories2_1=accessories_2.pivot_table(index='date_sale',aggfunc='sum')
uaccessories2_1.reset_index(inplace=True)
uaccessories_decay=uaccessories1_1.merge(uaccessories2_1,left_on = "Date",right_on = 'date_sale',how = 'inner')
uaccessories_decay


# In[300]:


th_uaccessories=ols('sale_volume~ consideration + use ',data=uaccessories_decay).fit()
print(th_uaccessories.summary())

sns.heatmap(uaccessories_decay.corr(),annot=True, vmax=1,vmin = 0, xticklabels= True, yticklabels= True, square=True, cmap="YlGnBu")


# # routers（整体）

# In[302]:


# 整体
routers1=(da_impression["product_category"]=="routers")
routers2=(da3["product_category"]=="routers")
routers_1=da_impression.loc[routers1]
routers_2=da3.loc[routers2]
# 按照日期对impression做数据透视表
routers1_1=routers_1.pivot_table(index='Date',values=['Impressions'],aggfunc='sum')
routers1_1.reset_index(inplace=True)
# 按照日期对sale做数据透视表
routers2_1=audio_2.pivot_table(index='date_sale',aggfunc='sum')
routers2_1.reset_index(inplace=True)

print(routers1_1)
print(routers2_1)


# In[303]:


#合并
routers_decay=routers1_1.merge(routers2_1,left_on = "Date",right_on = 'date_sale',how = 'inner')
routers_decay
routers_decay.info()


# In[ ]:




