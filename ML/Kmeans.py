import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
import time
start = time.time()
# 要测试的代码块

# 读取Excel,指定列为object类型
df = pd.read_excel('D:\Documents\Desktop\申报.xlsx', dtype={'invoice_cnname': object})

# 找到非字符串行索引
non_string_index = df[df['invoice_cnname'].apply(lambda x: not isinstance(x, str))].index

# 将非字符串转换为NaN
df.loc[non_string_index, 'invoice_cnname'] = np.nan

# 填充NaN
df['invoice_cnname'] = df['invoice_cnname'].fillna('')

# 特征提取
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['invoice_cnname'])

# KMeans分类
kmeans = KMeans(n_clusters=500)
y_pred = kmeans.fit_predict(X)

# 添加分类结果
df['category'] = y_pred

df.to_excel('D:\Documents\Desktop\聚类.xlsx', index=False)

print(df)

end = time.time()
print('所用时间:', end - start)
