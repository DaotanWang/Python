#目前还没遇到复杂请求情况，简单记录一下，随时更新。

import requests
#和API请求一样
url = 'https://www.xxx.com/xxx'
response = requests.get(url)
#得到网页源码
html = response.text

