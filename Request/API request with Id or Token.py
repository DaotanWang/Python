from urllib3 import disable_warnings
import requests

url = 'https://xxx.com/xxx'
disable_warnings() #HUAWEI公司有各种乱七八糟的防火墙，程序虽然不报错，但是会跳红，看着烦，用这个忽略。
headers = {
    "X-Auth-Id":"xxx",
    "X-Auth-Token":"xxx"
}

#verify=False 跳SSL证书验证，确定对方API安全的情况下可用，避免一些麻烦
response = requests.get(url, verify=False, headers=headers)
#得到请求的结果转换成str，response只是一个状态码
content = response.text
