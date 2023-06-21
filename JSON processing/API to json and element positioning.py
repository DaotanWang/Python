import requests
import json

response = requests.get(url, verify=False, headers=headers)
content = response.text
json_obj = json.loads(content)#一般API请求出来的都是Json格式字符串的（str），需要转换成python可识别的对象（json）。

#元素定位：
subscribers_count = json_obj['result']['report']['metrics']['subscribers_count']['value']
influencer_id = json_obj['result']['report']['basic']['id']

json_obj = """
{
    "result": {
        "report_state": "READY_LOW_CONFIDENCE",
        "report_quality": "WITHOUT_AUDIENCE_GEO",
        "report": {
            "basic": {
                "id": "UCn6UVeX7DF0gv6gZeJl120Q",
                "username": "wahomatsu",
                "title": "\u308f\u3063\u307b\u30fc\u307e\u3063\u3061\u3083\u3093\u306e\u65e5\u5e38",
                "avatar_url": "https://yt3.googleusercontent.com/ytc/AGIKgqMaDxzp5N2PeVws9wMvTXEwiTaOYWuPyAzgBxIDUw=s900-c-k-c0x00ffffff-no-rj",
                "description": "\u308f\u3063\u307b\u30fc\u3068\u307e\u3063\u3061\u3083\u3093\u304c\u697d\u3057\u3093\u3067\u3044\u308b\u52d5\u753b\u3067\u3059\u3002\n\u666e\u6bb5\u306e\u50d5\u305f\u3061\u306e\u30b4\u30eb\u30d5\u306e\u7df4\u7fd2\u98a8\u666f\u3084\u6d3b\u52d5\u306a\u3069\u3092\u52d5\u753b\u306b\u3057\u3066\u3044\u307e\u3059\u3002\n\u305f\u307e\u306b\u771f\u9762\u76ee\u306a\u3053\u3068\u3082\u558b\u308b\u304b\u3082\u3057\u308c\u306a\u3044\u3067\u3059\u304c\u307b\u3068\u3093\u3069\u306f\u3057\u3083\u3044\u3067\u308b\u3060\u3051\u3067\u3059\u3002\n\u3053\u306e\u52d5\u753b\u3092\u898b\u3066\u5c11\u3057\u3067\u3082\u7686\u3055\u3093\u304c\u7b11\u9854\u306b\u306a\u3063\u3066\u3044\u305f\u3060\u3051\u308c\u3070\u5b09\u3057\u3044\u3067\u3059\u3002\n\n\n\u30ec\u30c3\u30b9\u30f3\u4f1a\u3084\u30a4\u30d9\u30f3\u30c8\u306e\u544a\u77e5\u306f\u516c\u5f0fLINE\u3067\u81f4\u3057\u307e\u3059\u306e\u3067\u767b\u9332\u3088\u308d\u3057\u304f\u304a\u9858\u3044\u3057\u307e\u3059\n\n\n\u5ca9\u7537\u5065\u4e00\u3000\u3044\u308f\u304a\u3051\u3093\u3044\u3061\n\u30d7\u30ed\u30b4\u30eb\u30d5\u30a1\u30fc\n\n\u677e\u672c\u96c4\u53cb\u3000\u307e\u3064\u3082\u3068\u3086\u3046\u3059\u3051\u3000\n\u30b4\u30eb\u30d5\u7814\u4fee\u751f\n\u592a\u5e73\u6d0b\u30af\u30e9\u30d6\u6210\u7530\u30b3\u30fc\u30b9\n\n\u3010\u304a\u554f\u5408\u305b\u306f\u3053\u3061\u3089\u3011\n\u5404\u7a2e\u30e1\u30c7\u30a3\u30a2\u3001\u51fa\u6f14\u4f9d\u983c\u3001\u6848\u4ef6\u7b49\u306f\u4ee5\u4e0b\u3088\u308a\u304a\u554f\u5408\u305b\u304f\u3060\u3055\u3044\u3002\nwahomatu@proofc.com\n\n\u3010\u30b9\u30dd\u30f3\u30b5\u30fc\u3011\u306e\u304a\u554f\u3044\u5408\u308f\u305b\u306f\u3053\u3061\u3089\u306b\u304a\u9858\u3044\u3057\u307e\u3059\u3002\n\nrmnkenichi@gmail.com\n\n\n\n\n\n\n\u97f3\u697d\u7d20\u6750\u3000https://dova-s.jp/_mobile/ \u69d8\n\n\n\u52d5\u753b\u6295\u7a3f\u958b\u59cb\u65e5\u30002020\u5e744\u670823\u65e5",
                "category_name": "Entertainment",
                "is_verified": false
            },
            "metrics": {
                "subscribers_count": {
                    "value": 115000,
                    "performance": {
                        "30d": {
                            "value": 0,
                            "value_prev": 0
                        },
                        "90d": {
                            "value": 0,
                            "value_prev": 0
                        },
                        "180d": {
                            "value": 0,
                            "value_prev": 0
                        },
                        "365d": {
                            "value": 0,
                            "value_prev": 0
                        },
                        "all": {
                            "value": 0
                        }
                    }
                    ......
"""


