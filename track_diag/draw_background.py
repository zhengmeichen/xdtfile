# coding=utf-8
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

# 所有使用plt的地方都要加facecolor=(0, 0, 0, 0)，包括save
fig = plt.figure(figsize=(5.12, 2.56), facecolor=(0, 0, 0, 0), dpi=400)
ax = fig.add_axes([0, 0, 1, 1], frameon=0, facecolor=(0, 0, 0, 0))
m = Basemap(llcrnrlon=-180, llcrnrlat=-90, urcrnrlon=180, urcrnrlat=90, ax=ax)
m.drawcoastlines(linewidth=0.2)


# 初始化 map


def drawMap():
    # 绘制地图
    # 绘制海岸线
    m.drawcoastlines(linewidth=0.2)
    # 绘制国界线
    # m.drawcountries()

    # 填充陆地、胡泊、海洋的颜色
    # m.fillcontinents(color='darkolivegreen',
    # 陆地颜色
    # lake_color='aqua',
    # 湖泊颜色
    # )
    # m.drawmapboundary(fill_color='aqua')
    # 填充海洋


def set_lonlat(_m, lon_list, lat_list, lon_labels, lat_labels, lonlat_size):
    # def set_lonlat(_m, lon_list, lat_list, lonlat_size):
    """
    为Basemap实例画带tick标的经纬度注释
    自带画水平线和竖直线标注方式不带刻度标
    当然函数仍调用了自带标注函数只是在此基础上加了tick标
    :param _m: Basemap实例
    :param lon_list: 经度 详见Basemap.drawmeridians函数介绍
    :param lat_list: 纬度 同上
    :param lon_labels: 标注位置 [左, 右, 上, 下] bool值 默认只标注左上待完善 可使用twinx和twiny实现
    :param lat_labels: 同上
    :param lonlat_size: 字体大小
    :return:
    """
    lon_dict = _m.drawmeridians(lon_list, labels=lon_labels, color='grey', fontsize=lonlat_size, linewidth=0.5)
    lat_dict = _m.drawparallels(lat_list, labels=lat_labels, color='grey', fontsize=lonlat_size, linewidth=0.5)
    # lon_dict = _m.drawmeridians(lon_list, color='grey', fontsize=lonlat_size, linewidth=0.5)
    # lat_dict = _m.drawparallels(lat_list, color='grey', fontsize=lonlat_size, linewidth=0.5)

    lon_list = []
    lat_list = []
    for lon_key in lon_dict.keys():
        try:
            lon_list.append(lon_dict[lon_key][1][0].get_position()[0])
        except:
            continue

    for lat_key in lat_dict.keys():
        try:
            lat_list.append(lat_dict[lat_key][1][0].get_position()[1])
        except:
            continue
    ax = plt.gca()
    ax.xaxis.tick_top()
    ax.set_yticks(lat_list)
    ax.set_xticks(lon_list)
    ax.tick_params(labelcolor='none')


# drawMap()
set_lonlat(m, range(0, 360, 30), range(-90, 90, 30), [0, 0, 1, 0], [1, 0, 0, 0], 12)
# set_lonlat(m, range(0, 360, 30), range(-90, 90, 30), 12)

# 你也可以根据经纬度标注点
# m.plot(54.23, 65.16, marker='o', color="r")

# plt.show()
plt.savefig('background_grid.png', facecolor=(0, 0, 0, 0))
