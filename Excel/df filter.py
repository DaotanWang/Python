import pandas as pd
import warnings
warnings.simplefilter("ignore")
# 读取Excel文件
df = pd.read_excel('D:\\Documents\\Desktop\\精分类.xlsx')
customer_code = 'CN6173'
cust_df = df[df['customer_code'] == customer_code]

print('---------------------------------%s订单数---------------------------------'%customer_code)
print(cust_df['shipper_hawbcode'].nunique())

print('---------------------------------%s目的国百分比(前5)---------------------------------'%customer_code)
kmeans_counts = cust_df['country_cnname'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
print(kmeans_counts.head(5))

print('---------------------------------%s二级分类百分比(前5)---------------------------------'%customer_code)
kmeans_counts = cust_df['二级分类'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
print(kmeans_counts.head(5))

rates = {'EUR': 0.9358, 'GBP': 0.8077, 'USD': 1}
def convert_to_usd(price, currency):
  rate = rates[currency]
  return price / rate

cust_df['invoice_totalcharge_usd'] = cust_df.apply(lambda x: convert_to_usd(x['invoice_totalcharge'], x['invoice_currencycode']),axis=1)

print('---------------------------------%s订单平均价格(USD)---------------------------------'%customer_code)
print(cust_df['invoice_totalcharge_usd'].mean())

print('---------------------------------%s物流产品分类(前5)---------------------------------'%customer_code)
kmeans_counts = cust_df['product_cnname'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
print(kmeans_counts.head(5))

country_code = '美国'
country_df = df[df['country_cnname'] == country_code]

print('物流产品分类(前5):')
kmeans_counts = country_df['product_cnname'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
print(kmeans_counts.head(5))

# top5 = cust_df['invoice_cnname'].value_counts().head(5)
# print('invoice数量top5:')
# print(top5)
#
# print('kmeans分类百分比(前5):')
# kmeans_counts = cust_df['kmeans分类'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
# print(kmeans_counts.head(5))
# print('物流产品分类(前5):')
# kmeans_counts = cust_df['product_cnname'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
# print(kmeans_counts.head(5))
# print('二级分类百分比(前5):')
# kmeans_counts = cust_df['二级分类'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
# print(kmeans_counts.head(5))
# print('一级分类百分比(前5):')
# kmeans_counts = cust_df['一级分类'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
# print(kmeans_counts.head(5))

