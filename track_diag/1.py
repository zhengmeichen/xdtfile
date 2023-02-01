import sys
import numpy
import h5py

# from PIL import Image
# img = Image.open('D:\\src\\track_diag\\AREA_CHECK.png')
# img = numpy.array(img)
# print(type(img))

a = [1, 2, 3, 4, 5]
b = [2, 3, 4, 5, 2]
bb = [2, 3, 4, 5, 2]
cc = [2, 3, 4, 5, 2]
dd = [2, 3, 4, 5, 2]
f = []
out = [[a[i], b[i], bb[i], cc[i], dd[i]] for i in range(5)]
out1 = [[a[i], bb[i], b[i], cc[i], dd[i]] for i in range(5)]
f.extend(out)
f.extend(out1)
print(f)
# c = list(map(lambda x: x[0] - x[1], zip(b, a)))
# print(c)

# list1 = [1,2,3]
# list2 = [4,5,6]
#
#
# length = len(list1)
#
# list3 = [[list1[i],list2[i]] for i in range(length)]
#
# print(type(list3),list3)

# with h5py.File('D:\\src\\track_diag\\FY3E\\SEM\\L1\\HEP\\2022\\20221120\\FY3E_SEM--_ORBT_L1_20221120_0023_HEP--_V0.HDF', 'r') as f:
#     # 读取时间
#     Year = f['/Time/Year'][:]
# Year=Year.tolist()
# print(Year)
# print(type(Year))

##  data.forEach(value => {
                ##      ## value==data[i]
                ##      value.type = 'scatterGL';
                ##      ##  value.symbolSize = 5;
                ##      value.symbolSize = symsize;
                ##      ##  value.opacity = 0.5;
                ##      value.geoIndex=0;
                ##      value.coordinateSystem = 'geo';
                ##      value.itemStyle = {
                ##          color: itemcolor
                ##      };
                ##      ##  console.log(value.data[1][2]);
                ##      ##  console.log(value.data.length);
                ##  });
                ##
                ##  myChart.setOption({
                ##      //背景全黑
                ##       backgroundColor: {
                ##           image: '/static/IGRF_F_201607--600km15000-55000.png'
                ##       },
                ##      // 在 option 根部声明 tooltip 以整体开启 tooltip 功能。
                ##      tooltip: {
                ##          formatter: function (params, ticket, callback) {
                ##              console.log(params);
                ##              a = params.data;
                ##
                ##              ##  $.get('detail?name=' + params.name, function (content) {
                ##              ##      callback(ticket, toHTML(content));
                ##              ##  });
                ##
                ##              return ['轨道：' + params.seriesName, '经度：' + a[0], '纬度：' + a[1]].join(', ');
                ##          }
                ##      },
                ##      geo: [{
                ##          map: 'china',
                ##          left: 0,
                ##          top: 0,
                ##          right: 0,
                ##          bottom: 0,
                ##          boundingCoords: [[-180, 90], [180, -90]],
                ##          aspectScale: 1,
                ##          // 启用缩放和平移。
                ##          roam: true,
                ##          zoom: 1,
                ##      }],
                ##      legend: {
                ##          data: data.map(z => z.name)
                ##      },
                ##      series: data
                ##  });


##  // data是中国各个省份的矢量地图数据
            ##  data = await $.getJSON('/static/ne_110m_land.geojson');
            ##  // 使用 registerMap 注册的地图名称。
            ##  echarts.registerMap('china', data);



// 绘制选择中日期当天的轨道线
        async function filedata() {
            ##  // data是中国各个省份的矢量地图数据
            ##  data = await $.getJSON('/static/ne_110m_land.geojson');
            ##  // 使用 registerMap 注册的地图名称。
            ##  echarts.registerMap('china', data);
            ## 通过日期控件获取选择的日期
            time = document.getElementById('time').value;

            symsize = (v, p) => {
                ##  console.log(v,p);
                // 目前是将处于白色区域且时间<5分钟的事件定为报警
                return (v[2] && v[3] % 3600 < 300) ? 7 : 3
            };

            itemcolor = (p) => {
                ##  console.log(p);
                // 将轨道颜色在白色区域mask=1定为当前颜色，黑色区域mask=0定为灰色
                return p.data[2] ? p.color : '#80808066'
            };

            ##  let data = await $.getJSON('/api.track_diag.get_files?time=' + time, 'json')
            $.get('/api.track_diag.get_files?time=' + time, 'json', function (data) {
                data.forEach(value => {
                    ## value==data[i]
                    value.type = 'scatter';
                    ##  value.symbolSize = 5;
                    value.symbolSize = symsize;
                    ##  value.opacity = 0.5;
                    ##  value.roam = 'true';

                    ##  value.geoIndex = 0;
                    ##  value.coordinateSystem = 'geo';
                    value.coordinateSystem = 'leaflet';
                    value.itemStyle = {
                        color: itemcolor
                    };
                    ##  console.log(value.data[1][2]);
                    ##  console.log(value.data.length);
                 });

                myChart.setOption({
                    //背景全黑
                    ##  backgroundColor: {
                    ##      image: '/static/IGRF_F_201607--600km15000-55000.png'
                    ##  },
                    // 在 option 根部声明 tooltip 以整体开启 tooltip 功能。
                    tooltip: {
                        formatter: function (params, ticket, callback) {
                            console.log(params);
                            ##  params就等同于每个点包含的所有信息
                            a = params.data;
                            ##  $.get('detail?name=' + params.name, function (content) {
                            ##      callback(ticket, toHTML(content));
                            ##  });
                            return [params.marker + '轨道：' + params.seriesName + "</br>" + '经度：' + a[0] + "</br>" + '纬度：' + a[1]].join(', ');
                        }
                    },
                    leaflet: {
                        center: [0, 0],
                        zoom: 1,

                        leafletOption: {
                            center: [0, 0],
                            zoom: 1,
                            crs: L.CRS.EPSG4326,
                            link: {},
                            //起始地图中心点设置为[0,0]就可以
                            layers: [],

                            zoomDelta: 0.2,
                            zoomSnap: 0.2,

                            minZoom: 1,
                            maxZoom: 7,
                            zoomControl: false,
                            attributionControl: false,
                        },
                        roam: true,
                    },
                    ##  geo: [{
                    ##      map: 'china',
                    ##      left: 0,
                    ##      top: 0,
                    ##      right: 0,
                    ##      bottom: 0,
                    ##      boundingCoords: [[-180, 90], [180, -90]],
                    ##      aspectScale: 1,
                    ##      // 启用缩放和平移。
                    ##      roam: true,
                    ##      zoom: 1,
                    ##  }],
                    legend: {
                        data: data.map(z => z.name)
                    },
                    series: data
                });

            })

        }

symsize = (v, p) = > {
    console.log(v, p);
// 目前是将处于白色区域且时间 < 5
分钟的事件定为报警
return (v[2] & & v[3] % 3600 < 300) ? 7: 3
};


itemcolor = (p) = > {
##  console.log(p);
// 将轨道颜色在白色区域mask = 1
定为当前颜色，黑色区域mask = 0
定为灰色
return p.data[2] ? p.color: '#80808066'
};
