import pandas as pd
import re

file_path = './test.xlsx'   # 源数据文件路径


def match_keywords(targ, kwargs, double=False):
    if double:
        for key, val in kwargs.items():
            kwargs[key] = [re.sub(r' ', r'\\s+', i) for i in val]  # 把空格替换成模式\s+

    category = ''
    for key, val in kwargs.items():
        pattern = '|'.join(val)  # 合并模式串
        res = re.findall(fr'({pattern})', targ, re.I)  # 忽略大小写，匹配关键词kw
        if res:
            if not category:
                category = key
            else:
                category = ''  # 冲突词出现
                break

    return category


def calc_value(row):
    targ = str(row[0])

    # user_journey
    # 先匹配两个词
    kwargs = {
        'consider': ['huawei phone', 'huawei router', 'huawei P50', 'huawei earphones', 'huawei mobile', 'huawei nova',
                     'mobile nova', 'huawei earphone', 'huawei bluetooth earphone', 'huawei bluetooth earphones',
                     'huawei freepods', 'huawei freebuds'],
        'purchase': ['black friday', 'how much'],
        'use': ['how to', 'phone search']
    }
    user_journey = match_keywords(targ, kwargs, double=True)

    # 无结果再匹配一个词
    if not user_journey:
        kwargs = {
            'discover': ['phone', 'watch', 'huawei', 'apple', 'router', 'mobile'],
            'consider': ['ipad', 'iphone', 'nova', 'matepad', 'matebook'],
            'purchase': ['sale', 'store', 'price'],
            'use': ['download', 'connect', 'search', 'password', 'setting']
        }
        user_journey = match_keywords(targ, kwargs)

    # 均未匹配到，设为默认值
    if not user_journey:
        user_journey = 'share'

    # scenaio
    kwargs = {
        'workout': ['workout', 'sports'],
        'game': ['game', 'PUBG', 'gaming'],
    }
    scenaio = match_keywords(targ, kwargs)

    if not scenaio:
        scenaio = 'null'

    # brand
        # 先匹配两个词
    kwargs = {
            'Gentle Monster': ['Gentle Monster']
        }
    brand = match_keywords(targ, kwargs, double=True)

    # 无结果再匹配一个词
    if not brand:

        kwargs = {
            'huawei': ['huawei', 'nova', 'y9'],
            'apple': ['iphone', 'ipad', 'icloud', 'airpods'],
            'samsung': ['galaxy', 'samsung'],
            'xiaomi': ['xiaomi'],
            'redmi': ['redmi'],
            'oppo': ['oppo'],
            'vivo': ['vivo'],
            'honor':['honor']
        }
        brand = match_keywords(targ, kwargs)

    if not brand:
        brand = 'null'

    # generic_category
    if brand != 'huawei':  # brand不为huawei才填充
        kwargs = {
            'phone': ['phone', 'iphone'],
            'tablet': ['pad', 'ipad', 'tablet']
        }
        generic_category = match_keywords(targ, kwargs)

        if not generic_category:
            generic_category = 'null'
    else:
        generic_category = 'null'

    # product_category
    if brand == 'huawei':  # brand为huawei才填充
        # 先匹配两个词
        kwargs = {
            'Tablet': ['matepad pro']
        }
        product_category = match_keywords(targ, kwargs, double=True)

        # 无结果再匹配一个词
        if not product_category:
            kwargs = {
                'Phone': ['P50', 'P40', 'p30', 'nova', 'y9', 'y8'],
                'Headphones': ['earphones', 'earphone', 'freepods', 'freebuds'],
                'Tablet': ['matepad'],
                'Accessories': ['charger', 'keyboard', 'pen']
            }
            product_category = match_keywords(targ, kwargs)

        if not product_category:
            product_category = 'null'
    else:
        product_category = 'null'

    # product_line
    if product_category != 'null':  # generic_category不为null才填充
        kwargs = {
            'p series': ['p50', 'p40', 'p3'],
            'nova series': ['nova'],
            'y series': ['y9', 'y8']
        }
        product_line = match_keywords(targ, kwargs)

        if not product_line:
            product_line = 'null'
    else:
        product_line = 'null'

    # product_model
    if product_line != 'null':  # product_line不为null才填充
        # 先匹配两个词
        kwargs = {
            'huawei p50 pro': ['p50 pro']
        }
        product_model = match_keywords(targ, kwargs, double=True)

        # 无结果再匹配一个词
        if not product_model:
            kwargs = {
                'huawei p50': ['p50']
            }
            product_model = match_keywords(targ, kwargs)

        if not product_model:
            product_model = 'null'
    else:
        product_model = 'null'

    weight_type = 'main'
    tag_type = 'auto'
    update = ''

    return (targ, weight_type, user_journey, scenaio, brand, generic_category,
            product_category, product_line, product_model, tag_type, update)


def main():
    data = pd.read_excel(file_path).to_numpy()
    for ind in range(data.shape[0]):  # 逐行遍历
        row = data[ind, :]
        val = list(calc_value(row))
        data[ind, :] = val

    df = pd.DataFrame(data)
    df.columns = ['', 'weight_type', 'user_journey', 'scenaio', 'brand', 'generic_category',
                  'product_category', 'product_line', 'product_model', 'tag_type', 'update']
    df.to_excel('./result.xlsx', index=False)  # 存储到同级目录下面result.xlsx文件


if __name__ == '__main__':
    main()
