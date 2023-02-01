# coding=utf-8
<%inherit file="../base.mako"></%inherit>
<%block name="subtitle">轨道告警显示</%block>
<%block name="jscript">
    <script src="/static/1.7.1/leaflet.js"></script>

    <link rel="stylesheet" href="/static/1.7.1/leaflet.css">
    ##         <script src="/static/js/xtool.js"></script>

    <script src="/static/js/echarts.min.js"></script>
    ##     <script src="/static/js/echarts-gl.min.js"></script>
    ##     <script src="/static/1.7.1/ec-lfl.js"></script>


    ##     <script src="https://cdn.jsdelivr.net/npm/echarts@4.8.0/dist/echarts.min.js"></script>

    <script src="/static/js/xtool.js"></script>
    <script src="/static/1.7.1/echarts-leaflet.js"></script>
</%block>
<%block name="main">
    <%
        import glob,os
        basename=os.path.basename
        end_t =( datetime.now()).date()
        start_t=( datetime.now() - timedelta(days=5)).date()
    %>

    <div style="position: absolute;bottom:10px;top: 10px;left: 10px;right: 10px;
    display: flex;flex-direction: column;
    padding: 5px;background: #fffc;border: #aaa;font-size: 15px">
        <div style="width: 100%;display: flex;">
            报警仪器：
            <div style="margin-right: 5px">
                <select id=Device>
                    <option>FY3E_GNOS</option>
                    <option>FY3E_HIRAS</option>
                    <option>FY3E_MERSI</option>
                    <option>FY3E_MWHS</option>
                    <option>FY3E_MWTS</option>
                    <option value="FY3E_SEM--">FY3E_SEM</option>
                    <option>FY3E_SIM</option>
                    <option>FY3E_SSIM</option>
                    <option>FY3E_TRIPM</option>
                    <option>FY3E_WindRAD</option>
                    <option>FY3E_XEUVI</option>
                    <option>单粒子事件</option>
                </select>
            </div>
            时间：<input id="start" style="margin-right: 5px" type="date" value="${start_t}"> -
            <input id="end" style="margin-right: 5px" type="date" value="${end_t}">
            ##  日期：<input type=date onmouseleave="file_guidao_data()" id=time value="${init_t}">
            ##             报警仪器：
            ##             <div>
            ##                 <select id=Device required onchange="draw_diag()">
            ##
            ##                 </select>
            ##             </div>
            ##             报警参数：
            ##             <div>
            ##                 <select id=Parameter required>
            ##                 </select>
            ##             </div>
            ## onchange="baselayer3.setOpacity(this.value),


            地图透明度：<input type=range style="width: 150px;margin-right: 5px" value=0.6 min=0.0 max=1.0 step=0.01
                         onchange="baselayer_s.setOpacity(this.value)">
            ##             <div style="margin-right: 5px">
            ##                 保留历史：<input type="checkbox" id=history>
            ##             </div>


            底图：
            <div style="margin-right: 5px">
                <select id=bg_img onchange="set_bg(this.selectedOptions[0])">
                    <option value="/static/img/IGRF_F_201607--600km15000-55000.png"
                            data-cb="/static/img/IGRF-colorbar-15000-55000_600km.png" selected>磁场图
                    </option>
                    <option value="/static/img/1.png" data-cb="/static/img/3.png">粒子图</option>
                </select>
            </div>

            告警级别：
            <div style="margin-right: 5px" id=Diag>
                <input type="checkbox" name="diag_level" value=1 checked="checked">一级
                <input type="checkbox" name="diag_level" value=2>二级
                <input type="checkbox" name="diag_level" value=3>三级
            </div>

            显示轨道：
            <input id=guidao style="margin-right: 5px" type="checkbox"></input>

            绘制方法：
            <div style="margin-right: 5px">
                <select id=diag_method>
                    <option value="draw_diag_point">开始点</option>
                    <option value="draw_diag_line">持续段</option>
                </select>
            </div>
        </div>
        ## 时间控件及时间条

        <div style="width: 100%;display: flex;border: solid lightgray;border-width: 1px 0;height: 30px">
            <div style="flex: auto;margin-left: 15px;margin-right: 15px" id="t_chart"></div>
        </div>

        ## 轨道图设置,echarts,初始时在div中添加背景图片代码
        ## background: url('/FY3E/IGRF_F_201607--600km15000-55000.png')

        <div style="flex-grow: 2;position: relative;">
            <div id='left' style="position: absolute;left: 10px;bottom: 10px;
            background: #0008;z-index: 1000;">
                ## 显示底图colorbar
                ## <img src="/static/img/IGRF-colorbar-15000-55000_600km.png" style="margin: 10px">
                <img id="colorbar" src style="margin: 10px">
            </div>

            <div id='statistic' style="position: absolute;left: 10px;top: 10px;
            background: #fff5;z-index: 1000;padding: 10px">
                告警个数统计：
                <br>
                <br>
                一级：<input type="text" name="level1" value=0 style="width: 80px;
                background: #fff5;font-style: italic;font-weight: bolder;text-align: center">
                <br>
                <br>
                二级：<input type="text" name="level2" value=0 style="width: 80px;
                background: #fff5;font-style: italic;font-weight: bolder;text-align: center">
                <br>
                <br>
                三级：<input type="text" name="level3" value=0 style="width: 80px;
                background: #fff5;font-style: italic;font-weight: bolder;text-align: center">
            </div>

            <div id='right' style="position: absolute;right: 10px;top: 10px;
            background: #fff5;z-index: 1000;padding: 10px">
                报警图例：
                <div>
                    ## 显示不同报警级别对应不同的图标形状

                    <div>
                        <div class="D1"></div>
                        一级报警
                    </div>
                    <div>
                        <div class="D2"></div>
                        二级报警
                    </div>
                    <div>
                        <div class="D3"></div>
                        三级报警
                    </div>
                </div>
            </div>
            <div id="chart" style="height: 100%;"></div>
        </div>

    </div>

    <style>
        /*right显示告警图例*/
        #right > div {
            margin: 3px;
            padding: 3px 15px;
            color: black;
            ## text-shadow: 2px 1px 1px #fff;
            font-weight: bold;
            cursor: pointer;
        }

        /*0px 直接写0就行*/
        hr {
            margin: 3px 0;
            height: 0;
        }

        /*画告警点样式得设置在before之前，才能加载出content(⭐,▲,■)*/
        .D1:before {
            color: #B0171Faa;
            content: "★";
        }

        .D2:before {
            color: #9933FAaa;
            content: "▲";
        }

        .D3:before {
            color: #191970aa;
            content: "■";
        }

        /*设置画点的时候的告警图例的尺寸和高宽*/
        .D1, .D2, .D3 {
            font-size: 20px;
            display: inline-block;
            width: 40px;
            height: 20px;
            margin-right: 5px;
            text-align: center;
        }

        /*绘制线段时使用line,line方法会覆盖之前的D1中的的content属性*/
        .line:before {
            content: "——" !important;
        }

        .leaflet-tooltip {
            white-space: pre;
            ##     margin: 0;
            ##     padding: 10px;border-radius: 5px;
            ##     border: 1px solid #00adff;background: #FFFD;
        }
    </style>

    <script>
        // 全局调色盘。
        colors = [
            '#8dc1a9',
            '#ea7e53',
            '#eedd78',
            '#73a373',
            '#73b9bc',
            '#7289ab',
            '#91ca8c',
            '#f49f42',
            '#37A2DA',
            '#32C5E9',
            '#67E0E3',
            '#9FE6B8',
            '#FFDB5C',
            '#ff9f7f',
            '#fb7293',
            '#E062AE',
            '#E690D1',
            '#e7bcf3',
            '#9d96f5',
            '#8378EA',
            '#96BFFF',
            '#c23531',
            '#2f4554',
            '#61a0a8',
            '#d48265',
            '#91c7ae',
            '#749f83',
            '#ca8622',
            '#bda29a',
            '#6e7074',
            '#546570',
            '#dd6b66',
            '#759aa0',
            '#e69d87'
        ];
        // 页面初始化加载内容
        window.onload = async (e) => {
            //加载选定日期有哪些仪器进行了报警
            ##  await Device();
            // 加载各个仪器参数
            ##  Parameter();
            // 加载时间条
            Get_time();
            //页面加载当前日期+仪器的告警信息
            ##  draw_diag();
            // 页面加载显示当前日期的轨道图
            ##  file_guidao_data();
        };

        // 读取开始结束时间
        $('#start,#end').change(function () {
            start = document.getElementById('start').value;
            end = document.getElementById('end').value;
            deltad = (new Date(end).getTime() - new Date(start).getTime()) / 864e5;
            // 当开始结束时间晚于结束时间，自动调换起止时间
            if (deltad < 0) {
                deltad = -deltad;
                document.getElementById('start').value = end;
                document.getElementById('end').value = start;
                tmp = start;
                start = end;
                end = tmp;
                delete tmp;
            }
            // 有效文档时间显示条相关配置
            TC.chart.select(new Date(start).getTime() - 432e5, new Date(end).getTime() + 432e5);
        });
        // 初始化时间条控件,加载时直接全选了
        let TC = new TimeChart('t_chart', 'start', '/api.track_diag.get_time', 'end');

        // 选取仪器后自动加载对应存在告警信息的时间条
        async function Get_time() {
            // 获取时间，查找仪器名称，获取select对象
            device = document.getElementById('Device').value;
            // 设置有效文档时间显示条的样式,show时才调用传参device给get_time,false不自动change绘制全部事情
            TC.show({data: device}, false);
        }

        // 仪器种类改变，时间条控件改变显示内容
        $('#Device').change(Get_time);


        // 根据diag——data列出各个仪器,onmouseleave引发事件[目前没有用]
        async function Device() {
            ## 获取时间，查找仪器名称，获取select对象
            time = document.getElementById('time').value;
            $.ajax({
                url: '/api.track_diag.get_device?time=' + time,    //后台controller中的请求路径
                type: 'POST',
                datatype: 'json',
                ## 同步调用
                async: false,
                success: function (data) {
                    ##  console.log(data);
                    if (data) {
                        var devicenames = [];
                        if (data.length === 0) {
                            ##  alert('当前日期无报警仪器！！！');
                            $("#Device").html('<option value=""> 当前日期无报警仪器！！！ </option>');
                        } else {
                            for (var i = 0, len = data.length; i < len; i++) {
                                var devicedata = data[i];
                                //拼接成多个<option><option/>
                                devicenames.push('<option value="' + devicedata + '">' + devicedata.replace(/-/g, '') + '</option>')
                            }
                            $("#Device").html(devicenames.join(' '));    //根据字段所在位置填充到select标签中
                        }

                    }
                },
                error: function () {
                    alert('文件查询失败,未查询到仪器信息！！！');
                }
            });
        }

        // 根据仪器数据绑定数据参数[目前没有用]
        async function Parameter() {
            ## 获取仪器名称，获取select对象
            var myselect = document.getElementById('Device');
            ## 获取选中项的索引
            var index = myselect.selectedIndex;
            ## 获取选中项options的text/value：
            device = myselect.options[index].text;
            $.ajax({
                url: '/api.track_diag.get_para?device=' + device,    //后台controller中的请求路径
                type: 'POST',
                datatype: 'json',
                success: function (data) {
                    ##  console.log(data);
                    if (data) {
                        var paranames = [];
                        for (var i = 0, len = data.length; i < len; i++) {
                            var paradata = data[i];
                            //拼接成多个<option><option/>
                            paranames.push('<option value="' + paradata[0] + '">' + paradata[0] + '</option>')
                        }
                        $("#Parameter").html(paranames.join(' '));    //根据字段所在位置填充到select标签中
                    }
                },
                error: function () {
                    alert('文件查询失败,未查询到报警信息！！！');
                }
            });
        }

        // 初始化echarts实例
        // var myChart = echarts.init(document.getElementById('chart'));
        // leaflet初始化地图控件
        map = new L.Map('chart', {
            crs: L.CRS.EPSG4326,
            link: {},
            //起始地图中心点设置为[0,0]就可以
            center: [0, 0],
            zoomDelta: 0.2,
            zoomSnap: 0.2,
            zoom: 1.4,
            minZoom: 1.4,
            maxZoom: 7,
            zoomControl: false,
            attributionControl: false
        });

        // 设置图片初始化位置,如果在前面加入了zoomSnap,minZoom等元素,但是要是在使用map.setView,相当于按照map.setView的参数重置了地图
            ##  map.setView([0, 0], 1);
        L.control.scale({maxWidth: 200, position: 'bottomright'}).addTo(map);
        //  var bounds = L.latLngBounds({lat: 90, lng: -180}, {lat: -90, lng: 180});
        var bounds = [[90, -180], [-90, 180]];
        // 添加双层底图
        // 初始化底图背景
        // 海岸线背景图
        var baselayer = L.imageOverlay('/static/img/earth/bmng.jpg', bounds, {opacity: 1});
        // 自定义底图
        var baselayer_s = L.imageOverlay('#', bounds, {opacity: 0.7});
        baselayer.addTo(map);
        baselayer_s.addTo(map);
        // 当选择的底图option变化时，colorbar跟着一起改变
        colorbar = document.getElementById('colorbar');
        set_bg = (opt) => {
            baselayer_s._image.src = opt.value;
            colorbar.src = opt.getAttribute('data-cb');
        };
        // 调用上方的set_bg函数
        set_bg(document.getElementById("bg_img").selectedOptions[0]);


        //在地图上加入海岸线
            ##  $.getJSON('/static/ne_110m_land.geojson', function (data) {
            ## 设置只有海岸线，无底图，线宽为1.5，线色为黑色
            ##   L.geoJson(data, {fillOpacity: 0, weight: 1.5, color: 'black'}).addTo(map);
        ##  });

        // 全局变量，告警变量，用于保存轨道信息的ployline线段和告警信息的ployline线段
        var all_line = [];
        var diag_line = [];

        // 绘制选择中日期当天的SEM轨道线,并显示当天选中仪器的告警信息
        async function file_guidao_data() {
            ##  // data是中国各个省份的矢量地图数据
            ##  data = await $.getJSON('/static/ne_110m_land.geojson');
            ##  // 使用 registerMap 注册的地图名称。
            ##  echarts.registerMap('china', data);
            ## 通过日期控件获取选择的日期
            s_time = document.getElementById('start').value;
            e_time = document.getElementById('end').value;
            // 时间改变，等待仪器加载，为后方告警做准备
            ##  await Device();
            ## 函数
            datalayer = (d) => d.map(v => [v[1], v[0]]);
            ## 分段绘制
            poly = (data) => {
                ##  para = data.map(v => [v[1], v[0]]);
                para = data;
                ##  index = [];
                last = 0;
                para2 = [];
                for (i = 1; i < para.length; i++) {
                    ## 前后位置纬度相差3，就分为两段线去绘制
                    if (Math.abs(para[i][0] - para[i - 1][0]) > 3) {
                        para2.push(para.slice(last, i));
                        ##  index.push([last, i]);
                        last = i;
                    }
                }
                if (last < para.length - 1) {
                    para2.push(para.slice(last));
                    ##  index.push([last, para.length]);
                }
                return para2
            };
            ## 时间转换
            ttom = (second) => {
                ##  console.log((new Date(second * 1000).toISOString().slice(11)));
                return s_time + ' ' + (new Date(second * 1000).toISOString().slice(11, 19))
            };

            // 显示轨道信息，才进行展示
            if (document.getElementById('guidao').checked) {
                ##  $('#right').show();
                ## 未选中保留历史信息，全部清空轨道信息
                ##  if (!document.getElementById('history').checked) {
                ##      ## all_line包含所有polyline线条信息
                ##      all_line.forEach(a => a.remove());
                ##      all_line = [];
                ##      diag_line.forEach(b => b.remove());
                ##      diag_line = [];
                ##  }
                all_line.forEach(a => a.remove());
                all_line = [];
                diag_line.forEach(b => b.remove());
                diag_line = [];
                ##  let data = await $.getJSON('/api.track_diag.get_files?time=' + time, 'json')
                 $.get('/api.track_diag.get_files?s_time=' + s_time + '&e_time=' + e_time, 'json', function (data) {
                    console.log(data);
                    ## 未选中保存历史，清空之前绘图信息,只绘制选中日期的轨道
                    ##  绘制自定义colorbar
                    data.map((value, index) => {
                        ##  value==data[i],包含3055个数组
                        ## 添加到div上
                        ##  div = document.createElement('div');
                        ##  div.innerHTML = value.name;
                        ##  div.style.backgroundColor = colors[index];
                        ##  div.data = [];
                        ##  绘制所有轨道信息
                        para2 = poly(value.data);
                        ##  console.log(para2)
                        var polyline_all = L.polyline(para2.map(v => datalayer(v)), {
                            ##  color: colors[index],
                            // 灰色轨道线
                            color: '#888',
                            weight: 5,
                            opacity: 0.5,
                        }).addTo(map);
                        ##  div.data.push(polyline_all);
                        all_line.push(polyline_all);
                        polyline_all.bindTooltip('<i class="fa fa-spin fa-globe" style="color: blue"></i> 轨道时次：'
                                + value.name, {sticky: true,});
                        ##  通过添加过滤条件，绘制mask==1的点,高发区域存在tooltip提示
                        mask = poly(value.data.filter(v => v[2]));
                        mask.forEach(m => {
                            var polyline_mask = L.polyline([datalayer(m)], {
                                ##  color: colors[index],
                                // 灰色加粗高发区
                                color: '#ffe',
                                weight: 7.5
                            }).addTo(map);
                            ##  div.data.push(polyline_mask);
                            all_line.push(polyline_mask);
                            ## 添加tooltip提示框，style添加标识样式
                            ##   polyline_mask.bindTooltip('<i class="fa fa-spin fa-superpowers" style="color: ' + colors[index] + '"></i> 轨道时次：'
                            polyline_mask.bindTooltip('<i class="fa fa-spin fa-superpowers" style="color: orangered"></i> 轨道时次：'
                                    + value.name + "<br>" + '开始时间：'
                                    + ttom(m[0][3]) + "<br>" + '结束时间：' + ttom(m[m.length - 1][3]), {sticky: true,});
                        });
                        ##  return div
                    });
                    ## 显示轨道的上层显示告警
                    ## 根据绘制方法显示不同的告警图例及绘制点还是线的方法
                    draw_diag()
                });
            } else {
                // 显示轨道不勾选，直接清空轨道信息
                ## 将保留历史的复选框设置为false
                ##  document.getElementById("history").checked = false;
                all_line.forEach(a => a.remove());
                all_line = [];
                ##  $("#right").hide();
                ## 只显示告警信息
                ## 根据绘制方法显示不同的告警图例及绘制点还是线的方法draw_diag里自行判断
                draw_diag()
            }
        }

        // 显示轨道选中状态改变引发事件
        $('#guidao').change(file_guidao_data);

        // 设置绑定popup变量
        let diag_feature_group = null;

        // Popup事件
        function Popup() {
            let _popup = null; // L.popup({keepInView: true, closeButton: false,})      //  let _popup = L.tooltip({keepInView: true})
            let _obj = null;
            // 鼠标移动，tooltip改变显示内容
            _move = (e) => {
                // 鼠标所在位置的经纬度信息
                latlngs = e.layer._latlngs;
                let tt;
                let diags;

                if (latlngs) {
                    // 从地图上获取layer.diags（后台传来的diags所有信息）;
                    diags = e.layer.diags;
                    // 后台传入的latlng信息
                    t = e.latlng;
                    delta = 10;
                    tt = t;
                    // 鼠标移动到polyline的附近5经纬度范围内就开始显示tooltip
                    latlngs.forEach(p => p.forEach(q => {
                        if (Math.abs(q.lat - t.lat) > 5) return;
                        if (Math.abs(q.lng - t.lng) > 5) return;
                        d = Math.sqrt(Math.pow(q.lat - t.lat, 2) + Math.pow(q.lng - t.lng, 2));
                        if (d < delta) {
                            delta = d;
                            tt = q
                        }
                    }));
                } else {
                    // 从地图上获取layer.diags（后台传来的diags所有信息）和鼠标当前位置经纬度信息;
                    tt = e.layer._latlng;
                    diags = [e.layer.diags];
                }

                <%text>
                    _popup._tooltip.setLatLng(tt);
                    // 设置提示框显示内容,单粒子告警存在yiqi字段,只有单粒子有,当选中其他仪器时返回''(v.yiqi||'')
                    _popup._tooltip.setContent(`<i class= "fa fa-clock-o" style = "color: black" ></i> ${new Date(tt.alt*1000).toISOString().slice(11,19)}    <i class="fa fa-map-marker" style="color: dodgerblue"></i > Lat:${tt.lat.toFixed(3)},Lon:${tt.lng.toFixed(3)}<hr>${diags.map(v => {
                        return `<i class="fa fa-bug" style="color: ${diagcolors[v.level]}"> ${diaglevels[v.level]}</i>  <b>${v.yiqi||''}</b> ${v.name}( ${v.msg} )\n<i class="fa fa-calendar"></i> ${v.st_time} ~ ${v.et_time}`
                        }).join('<hr>')}`);
                </%text>
            };

            // 初始化
            this.init = function (obj) { //ialize
                ##  obj.bindPopup(_popup)
                // 提示框跟随鼠标移动
                _popup = obj.bindTooltip('', {sticky: true,}); //permanent:true
                ##  obj.on('mouseover', (e) => {
                ##    _move(e)
                ##    ##  _popup.openOn(map)
                ##  })
                ##  obj.on('mouseout', (e) => _popup.close())
                // mousemove鼠标移动，调用_move函数
                obj.on('mousemove', _move);
                ##  if (_obj) _obj.unbindPopup()
                // 存在，情况之前的提示框信息
                if (_obj) _obj.unbindTooltip();
                _obj = obj
            };
        }

        // 初始化Popup控件
        let my_popup = new Popup();

        //设置告警等级和颜色
        diagcolors = [null, '#B0171F', '#9933FA', '#191970'];
        diaglevels = [null, '一级', '二级', '三级'];

        // 使用L.divIcon设置一个类，使用时调用类里是内容
        // 设置告警的形状和级别
        diagflags = [null, L.divIcon({className: 'D1'}), L.divIcon({className: 'D2'}), L.divIcon({className: 'D3'})];

        // 在原有leaflet上绘制选中参数的告警信息(使用polyline)
        DRAW_DIAG = {
            // 在原有leaflet上绘制选中参数的告警信息（绘制线段）
            draw_diag_line: async function () {
                // 显示图例
                $("#right").show();
                // 这里加载等待时间的变换
                ##  await Get_time();
                // 通过日期控件获取选择的日期，时间改变了获取新的开启和结束时间
                s_time = document.getElementById('start').value;
                e_time = document.getElementById('end').value;
                // 获取选中的仪器
                device = document.getElementById('Device').value;
                // 获取告警级别
                var diag_level = [];
                //遍历每一个名字为diag_level的复选框，其中选中的执行函数
                $('input[name="diag_level"]:checked').each(function () {
                    //将选中的值添加到数组diag_level中
                    diag_level.push($(this).val());
                });
                var diag = diag_level.join(",");


                // 获取告警信息
                $.get('/api.track_diag.get_diag_line?s_time=' + s_time + '&e_time=' + e_time + '&device=' + device + '&diag=' + diag, 'json', function (data) {
                    console.log('data', data);
                    // 告警复选框，全没选择全部清空（无选中等级）
                    if (!document.getElementById('Diag').checked) {
                        // all_line包含所有polyline线条信息
                        diag_line.forEach(a => a.remove());
                        diag_line = [];
                    }
                    // 绘制告警点信息
                    data.forEach((value, index) => {
                        ##  console.log(value);
                    ##  console.log(value.data);
                    ##  console.log(value.data[0], value.data[1]);
                    color = diagcolors[value.diags.map(v => v.level).reduce((a, b) => a < b ? a : b)];
                        var polyline_diag = L.polyline(value.data, {color: color, weight: 8.5});
                        polyline_diag.diags = value.diags;
                        ##  console.log(value.data);
                    diag_line.push(polyline_diag);
                        ## 添加bug样式小标识,与polyline_diag--addtomap一起省略
                    ##  polyline_diag.bindTooltip(value.diags.map(v =>
                    ##    '<i class="fa fa-clock-o" style="color: black" ></i> ' + '1111' + '&nbsp' +
                    ##    '<i class="fa fa-map-marker" style="color: dodgerblue" ></i> ' + v.level + "<br>" +
                    ##    '<i class="fa fa-spin fa-bug" style="color: red" ></i> ' + v.level + '&nbsp&nbsp' +
                    ##    '<font color="orange" >' + v.name + '(' + v.msg + ')' + '</font>' + "<br>" +
                    ##    '<i class="fa fa-calendar" style="color: black" ></i> ' + v.st_time + "&nbsp" + "~" + "&nbsp" + v.et_time + "<br>"
                    ##  ).join('<hr>'));
                });
                    // 鼠标移动改变popup绑定事件,鼠标进入polyline线上，出现提示框，移除线外提示框消除
                    if (diag_feature_group) {
                        diag_feature_group.remove() /*From(map);*/
                    }
                    // 信息绑定
                    diag_feature_group = L.featureGroup(diag_line);
                    diag_feature_group.addTo(map);
                    // 提示框初始化
                    my_popup.init(diag_feature_group);

                    // 将上次写入的告警统计个数清空
                    $("input[name='level1']").val(0);
                    $("input[name='level2']").val(0);
                    $("input[name='level3']").val(0);
                    //统计告警个数
                    // 返回的data带有counter返回的统计个数，格式为count：{1：3，2：4，3：9}
                    //jquery通过name属性获取html对象并赋值为对应统计的个数，存在写入并改变，否则一致为默认值0
                    if (data[0].count[1]) {
                        $("input[name='level1']").val(data[0].count[1]);
                    }
                    if (data[0].count[2]) {
                        $("input[name='level2']").val(data[0].count[2]);
                    }
                    if (data[0].count[3]) {
                        $("input[name='level3']").val(data[0].count[3]);
                    }
                })
            },

            // 在原有leaflet上绘制选中参数的告警信息（绘制点）
            draw_diag_point: async function () {
                // 显示图例
                $("#right").show();
                // 这里加载等待时间的变换
                ##  await Get_time();
                // 通过日期控件获取选择的日期，时间改变了获取新的开启和结束时间
                s_time = document.getElementById('start').value;
                e_time = document.getElementById('end').value;
                // 获取选中的仪器
                device = document.getElementById('Device').value;
                ##  console.log(device);
                ##  alert(device);
                // 获取告警级别
                var diag_level = [];
                //遍历每一个名字为diag_level的复选框，其中选中的执行函数
                $('input[name="diag_level"]:checked').each(function () {
                    //将选中的值添加到数组diag_level中
                    diag_level.push($(this).val());
                });
                var diag = diag_level.join(",");

                // 获取告警信息
                $.get('/api.track_diag.get_diag_point?s_time=' + s_time + '&e_time=' + e_time + '&device=' + device + '&diag=' + diag, 'json', function (data) {
                    console.log(data);
                    // 未选中告警级别，全部清空
                    if (!document.getElementById('Diag').checked) {
                        // all_line包含所有polyline线条信息
                        diag_line.forEach(a => a.remove());
                        diag_line = [];
                    }
                    // 绘制告警点信息
                    data.forEach((value, index) => {
                        // 根据级别选定颜色
                        color = diagcolors[value.level];
                        // 绘制单点圆形
                        ##  var polyline_diag = L.circleMarker(value.data,
                        ##          {
                        ##              fillColor: color,
                        ##              fillOpacity: 1,
                        ##              radius: 10,
                        ##              stroke: '#fff'
                        ##          });

                        var polyline_diag = L.marker(value.data, {
                            icon: diagflags[value.level]
                        });
                        polyline_diag.diags = value;
                        diag_line.push(polyline_diag);
                        // 添加bug样式小标识,与polyline_diag--addtomap一起省略
                        ##  polyline_diag.bindTooltip(value.diags.map(v =>
                        ##    '<i class="fa fa-clock-o" style="color: black" ></i> ' + '1111' + '&nbsp' +
                        ##    '<i class="fa fa-map-marker" style="color: dodgerblue" ></i> ' + v.level + "<br>" +
                        ##    '<i class="fa fa-spin fa-bug" style="color: red" ></i> ' + v.level + '&nbsp&nbsp' +
                        ##    '<font color="orange" >' + v.name + '(' + v.msg + ')' + '</font>' + "<br>" +
                        ##    '<i class="fa fa-calendar" style="color: black" ></i> ' + v.st_time + "&nbsp" + "~" + "&nbsp" + v.et_time + "<br>"
                        ##  ).join('<hr>'));
                        });
                    // 鼠标移动改变popup绑定事件,鼠标进入polyline线上，出现提示框，移除线外提示框消除
                    if (diag_feature_group) {
                        diag_feature_group.remove() /*From(map);*/
                    }
                    // 信息绑定
                    diag_feature_group = L.featureGroup(diag_line);
                    diag_feature_group.addTo(map);
                    // 提示框初始化
                    my_popup.init(diag_feature_group);

                    // 将上次写入的告警统计个数清空
                    $("input[name='level1']").val(0);
                    $("input[name='level2']").val(0);
                    $("input[name='level3']").val(0);
                    //统计告警个数
                    // 返回的data带有counter返回的统计个数，格式为count：{1：3，2：4，3：9}
                    //jquery通过name属性获取html对象并赋值为对应统计的个数，存在写入并改变，否则一致为默认值0
                    if (data[0].count[1]) {
                        $("input[name='level1']").val(data[0].count[1]);
                    }
                    if (data[0].count[2]) {
                        $("input[name='level2']").val(data[0].count[2]);
                    }
                    if (data[0].count[3]) {
                        $("input[name='level3']").val(data[0].count[3]);
                    }
                })
            }
        };

        // 根据不同的绘制方法绘制不同的告警信息（点/线段）
        function draw_diag() {
            device = document.getElementById('Device').value;
            if (device === '单粒子事件') {
                // 将绘制方法下来框设置为不可用
                $("#diag_method").attr("disabled", true);
                // 只绘制点
                DRAW_DIAG['draw_diag_point']();
            } else {
                // 将绘制方法下来框设置为可用
                $("#diag_method").attr("disabled", false);
                let draw_type = document.getElementById('diag_method').value;
                DRAW_DIAG[draw_type]();
                // draw_diag_line名称与diag_method的option一致
                if (draw_type === 'draw_diag_line')
                        // 当选择绘制线段时，给icon添加一个类，该类方法覆盖D1里部分内容
                    $('.D1,.D2,.D3').addClass('line');
                else
                    $('.D1,.D2,.D3').removeClass('line');
            }
        }

        // 显示仪器，时间，告警级别改变引发事件,并改变统计个数
            ##  $('#Device,#Diag,#start,#end,#diag_method').change(draw_diag,Statistic);
        $('#Device,#Diag,#start,#end,#diag_method').change(draw_diag);

        // 保留历史信息改变，清空轨道或告警信息
            ##  function clear_all() {
        ##      if (document.getElementById('history').checked && !document.getElementById('guidao').checked) {
        ##          ## all_line包含所有polyline线条信息
        ##          diag_line.forEach(a => a.remove());
        ##          diag_line = [];
        ##          draw_diag();
        ##          ##  draw_diag_start();
        ##      } else if (!document.getElementById('history').checked && document.getElementById('guidao').checked) {
        ##          all_line.forEach(a => a.remove());
        ##          all_line = [];
        ##          file_guidao_data();
        ##      } else if (!document.getElementById('history').checked && !document.getElementById('guidao').checked) {
        ##          draw_diag();
        ##          ##  draw_diag_start();
        ##      }
        ##  }

        // 如果告警仪器变化,清空历史信息，绘制新的告警信息
        // $('#history,#guidao').change(clear_all);

    </script>


</%block>