# coding:utf-8
import datetime
import glob
import json

import requests

currenttime = datetime.datetime.now()
yestime = datetime.datetime.now() + datetime.timedelta(days=-1)
yesyestime = datetime.datetime.now() + datetime.timedelta(days=-2)

# 各仪器时次计划数
insplan = {"GNOS-II": 28, "HIRAS-II": 288, "MERSI-LL": 288, "MWHS-II": 28, "MWTS-III": 28, "SEM-II": 14, "SIM-II": 14,
           "SSIM": 1, "TriIPM": 14, "WindRAD": 28, "X-EUVI": 288}
insplansum = 1019

# 获取内网数据
# 故障状态数据获取
req = requests.get("http://10.25.18.28:7007/api.dd.get_m2")


def diagnosis():
    diagstatus = req.json()
    insstatus = {}
    for ins in diagstatus['ins_status']:
        if ins['stat'] == 1:
            status = "一级故障"
        elif ins['stat'] == 2:
            status = "二级故障"
        elif ins['stat'] == 3:
            status = "三级故障"
        elif ins['stat'] == 4:
            status = "状态正常"
        insstatus[ins['title']] = status
    return insstatus


# obc资源池数据获取
obcs = {"GNOS-II": "/FY3E/GNOS/1A/OBC/%Y/%Y%m%d/*", "HIRAS-II": "/FY3E/HIRAS/1A/OBC/%Y/%Y%m%d/*",
        "MERSI-LL": "/FY3E/MERSI/1A/OBC/%Y/%Y%m%d/*", "MWHS-II": "/FY3E/MWHS/1A/*/%Y/%Y%m%d/*",
        "MWTS-III": "/FY3E/MWTS/1A/*/%Y/%Y%m%d/*", "SEM-II": "/FY3E/SEM/1A/HP*/%Y/%Y%m%d/*",
        "SIM-II": "/FY3E/SIM/1A/%Y/%Y%m%d/*", "SSIM": "/FY3E/SSIM/1A/*/%Y/%Y%m%d/*",
        "TriIPM": "/FY3E/TRIPM/1A/%Y/%Y%m%d/*", "WindRAD": "/FY3E/WRAD/1A/OBC/*C/%Y/%Y%m%d/*",
        "X-EUVI": "/FY3E/XEUVI/1A/GRAN/%Y/%Y%m%d/*"}


# 今天的各仪器时次数据
def obc():
    obcstatus = {}
    for key, value in obcs.items():
        path = currenttime.strftime(value)
        obcstatus[key] = len(glob.glob(path))
    return obcstatus


# 前十五天的所有仪器一天总数据
def chartDatas():
    chartData = []
    obcsum = {}
    for i in range(15, 0, -1):
        sum = 0
        t = (datetime.datetime.now() - datetime.timedelta(days=i))
        for key, value in obcs.items():
            path = t.strftime(value)
            sum = sum + len(glob.glob(path))
            obcsum[t.strftime("%Y-%m-%d")] = sum
        datas = {"name": str(t.strftime("%Y-%m-%d")), "planQuantity": str(insplansum), "actualQuantity": str(sum)}
        chartData.append(datas)
    return chartData


# l1全球拼图获取
obcL1 = {"HIRAS-II 升轨": "/home/shk401/shinetekview-data/fyhn/YFS/BM/FY3E_HIRAS_A_BT_OBS_850.png",
         "HIRAS-II 降轨": "/home/shk401/shinetekview-data/fyhn/YFS/BM/FY3E_HIRAS_D_BT_OBS_850.png",
         "MERSI-LL 升轨": "/home/shk401/shinetekview-data/fyhn/YFS/BM/FY3E_MERSI_A_BT_OBS_05_10.8.png",
         "MERSI-LL 降轨": "/home/shk401/shinetekview-data/fyhn/YFS/BM/FY3E_MERSI_D_BT_OBS_05_10.8.png",
         "MWHS-II 升轨": "/home/shk401/shinetekview-data/fyhn/YFS/BM/FY3E_MWHS_A_BT_OBS_89.0.png",
         "MWHS-II 降轨": "/home/shk401/shinetekview-data/fyhn/YFS/BM/FY3E_MWHS_D_BT_OBS_89.0.png",
         "MWTS-III 升轨": "/home/shk401/shinetekview-data/fyhn/YFS/BM/FY3E_MWTS_A_BT_OBS_01_23.8.png",
         "MWTS-III 降轨": "/home/shk401/shinetekview-data/fyhn/YFS/BM/FY3E_MWTS_D_BT_OBS_01_23.8.png",
        }

def prodGrouplist():
    datess=open("/STSS/FY3E_STSS/system/big-fig/gbal/time",'r').read()
    lists = []
    for key,value in obcL1.items():
        url=yesyestime.strftime(value)
        lists.append({"name":key,"date":datess,"url":url})
    return lists


# 数据准备
# id="634cf848dfdb052a67dfddb5"
def reparedata():
    insstatus = diagnosis()
    obcstatus = obc()
    chartData = chartDatas()
    businessDetails = [{"name": "L1产品种类", "value": "136"},
                       {"name": "FY-3D产品种类", "value": "47"},
                       {"name": "FY-3E产品种类", "value": "64"},
                       {"name": "FY-4B产品种类", "value": "25"}]
    prodGroup = [{"name": "FY-3E L1数据生成状态", "list": prodGrouplist()}]
    prodList = []
    list1 = []
    inses = ["MWTS-III", "MWHS-II", "WindRAD", "MERSI-LL", "HIRAS-II", "GNOS-II", "X-EUVI", "TriIPM", "SIM-II", "SSIM",
             "SEM-II"]

    for ins in inses:
        ll = {"name": str(ins),
              "status": insstatus[ins],
              # "status": "状态正常",
              "updateTime": str(currenttime.strftime("%H:%M:%S")),
              "planQuantity": str(insplan[ins]),
              "actualQuantity": str(obcstatus[ins])}
        list1.append(ll)
    p1 = {"name": "FY-3E预处理系统", "time": str(currenttime.strftime("%Y-%m-%d %H:%M")), "chartData": chartData,
          "list": list1}
    prodList.append(p1)

    content = {"businessDetails": businessDetails, "prodGroup": prodGroup, "prodList": prodList}
    payload = json.dumps({"page": "研发室-预处理展示FY3E", "content": content})
    print(payload)

    # url = "http://121.36.13.81:4676/service/page"
    url = "http://10.25.26.1:4676/service/page"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text, response.status_code)


reparedata()
