# coding:utf-8
import datetime
import os
import glob
import requests

# 3E预处理
# url = "http://121.36.13.81:4605/service/upload/siyh/fyhn/YFS/BM"
url = "http://10.25.26.1:4605/service/upload/fyhn/YFS/BM"

# 3El1全球拼图获取
payload = {}
files = []
filesL1=glob.glob("/STSS/FY3E_STSS/system/big-fig/gbal/*.png")
for i in filesL1:
    file = ('file', (os.path.basename(i), open(i, 'rb'), 'image/png'))
    files.append(file)
headers = {}
response = requests.request("POST", url, headers=headers, data=payload, files=files)
print(response.text)
