# coding:utf-8
import requests
import glob
import os
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# 质检3E
# url = "http://121.36.13.81:4605/service/upload/siyh/fyhn/YFS/BM"
url = "http://10.25.26.1:4605/service/upload/fyhn/YFS/QC"

payload={}
files=[]
for i in glob.glob('/STSS/FY3E_STSS/system/big-fig/figures/*png'):
    file=('file',(os.path.basename(i),open(i,'rb'),'image/png'))
    files.append(file)
headers = {}
response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)