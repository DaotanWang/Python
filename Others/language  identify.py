import langid
import pandas as pd
from langdetect import detect
from langdetect import detect_langs
from langdetect import DetectorFactory
# DetectorFactory.seed = 0
df1 = pd.read_excel('D:/test.xlsx', usecols=[0], header=None)
df1_list = df1.values.tolist()
# print(df1_list)
result = []
notneed_tran = []
need_tran = []
# print(df1_list[0])
# m = 0
for s_li in df1_list:
    result.append(s_li[0])
print(result)
n = 1
for HSI_keys in result:
    result = langid.classify(HSI_keys)
    # m = m+1
    print(n)
    n = n+1
    try:
        if type(HSI_keys) is str:
            if result[0] != 'it':
                notneed_tran.append(HSI_keys)
            else:
                need_tran.append(HSI_keys)
                # print(HSI_keys)

    except BaseException:
        pass
print(notneed_tran)
print(need_tran)
