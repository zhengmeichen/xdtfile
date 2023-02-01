# coding=utf-8
<%inherit file="../base.mako"></%inherit>
<%block name="subtitle">风场雷达 雨林定标</%block>
<%block name="main">
  <%
    import  glob,os
  %>
  <style><%include file="../local.css"/></style>
  <div class="flex-h p3">
    <div class="h100 p3" style="width: 750px;user-select: none;">
      <div class="panel panel-primary flex-v">
        <div class="panel-heading">配置信息 / Configuration Info.</div>
        <div class="panel-body flex-g2 p5">
          <div class="row small my1">
            <div class="col-sm-2">
              区域
              <select id="s1" size="3">
                <option value="Amazon" data="-71, -60, -6, 3.5" selected>Amazon</option>
                <option value="Congo" data="11,29,-5,5">Congo</option>
              </select>
            </div>
            <div class="col-sm-2">
              波段
              <select id="s2" size="3" onchange="document.getElementById('area_zen').value=this.selectedOptions[0].id">
                <option value="K" selected id="38,42,1">Ku波段</option>
                <option value="C" id="36,44,1">C 波段</option>
              </select>
            </div>
            <div class="col-sm-2">
              升降轨道
              <select id="s3" multiple size="3">
                <option value="A" selected>升轨</option>
                <option value="D">降轨</option>
              </select>
            </div>
            <div class="col-sm-2">
              分辨率
              <select id="s4" multiple size="3">
                <option value="10km" selected>10千米</option>
                <option value="20km">20千米</option>
                <option value="Slice">切片</option>
              </select>
            </div>
            <div class="col-sm-2">
              极化方向
              <select id="s5" multiple size="3">
                <option value="HH" selected>H极化</option>
                <option value="VV">V极化</option>
              </select>
            </div>
            <div class="col-sm-2">&nbsp;
              <select id="s6" multiple size="3" disabled>
                <option value="HH">暂无</option>
              </select>
            </div>
            <div class="col-sm-12" style="margin: 5px 0;padding: 0;border: solid lightgray; border-width: 1px 0;height: 30px" id="t_chart"></div>
            <div class="col-sm-2"><b>日期/DATE</b></div>
            <div class="col-sm-6"><input id="start" type="date" style="width: 120px">~<input id="end" type="date" style="width: 120px"></div>
            <div class="col-sm-1" style="text-align: right;font-weight: bold">数据组</div>
            <div class="col-sm-3"><select class="opt-fa" id="data1" required></select></div>
          </div>
          <div class="row small my1" style="padding-top: 5px;margin-top: 5px">
            <div class="col-sm-2"><b>方位角分类</b>
              <select id="dwazi" class="opt-fa" multiple="multiple" style="height: 222px">
                % for i in range(36):
                  <option value="${i}">${(i*10)}~${((i+1)*10)}°</option>
                % endfor
              </select></div>
            <div class="col-sm-4" style="height: 258px" id="arc1"></div>
            <div class="col-sm-2">
              <b>天顶角分类</b>
              <select id="dszen" class="opt-fa" multiple="multiple" style="height: 222px">
                % for i in range(10,60):
                  <option value="${i}">${(i)}~${((i+1))}°</option>
                % endfor
              </select>
            </div>
            <div class="col-sm-4" style="height: 258px" id="arc2"></div>
            <div class="col-sm-12" style="border-top: 1px solid lightgray;margin: 5px 0">
              <b>筛选条件</b>
              <div id="filters"></div>
            </div>
            <div class="col-sm-12" style="border-top: 1px solid lightgray;margin: 5px 0">
              <b>标注范围</b>
              <div>
                <label class="inbox"><span>mean/bias</span><input id="lim_m" title="min,max"></label>
                <label class="inbox"><span>std(e)</span><input id="lim_s" title="min,max"></label>
                <label class="inbox"><span>rms(e)</span><input id="lim_r" title="min,max"></label>
              </div>
            </div>
          </div>
          <div class="row small my1" style="margin-top: 5px;padding-top:5px;border-top: 1px solid silver">
            <div class="col-sm-1"><b>二维分布</b></div>
            <div class="col-sm-1">子图</div>
            <div class="col-sm-2">
              <select id=subplots class="opt-fa" size="4" required>
                <option value="mean" selected>mean/bias</option>
                <option value="std">std(e)</option>
                ##             <option value="rms">rms(e)</option>

                <option value="count">count</option>
              </select>
            </div>
            <div class="col-sm-8" style="text-align: end">
              <div>
                分辨率
                <select id="ry" style="width:110px">
                  <option value="0.01">0.01°</option>
                  <option value="0.02">0.02°</option>
                  <option value="0.05">0.05°</option>
                  <option value="0.1" selected>0.1°</option>
                  <option value="0.2">0.2°</option>
                  <option value="0.5">0.5°</option>
                  <option value="1">1°</option>
                  <option value="2">2°</option>
                  <option value="3">3°</option>
                  <option value="4">4°</option>
                  <option value="5">5°</option>
                </select>
                投影区间 <input value="-71, -60, -6, 3.5" placeholder="WEST,EAST,SOUTH,NORTH" style="width:110px" id="extent">
                <button class="fa fa-area-chart btn btn-sm btn-primary" onclick="draw('gbal')"> 空间分布</button>
              </div>
              <div>
                方位区间 <input value="0,360,10" placeholder="start,end,step" style="width:110px" id="area_azi">
                入射区间 <input value="20,48,1" placeholder="start,end,step" style="width:110px" id="area_zen">
                <button class="fa fa-area-chart btn btn-sm btn-primary" onclick="draw('agls_dtbt')"
                        title="X: 入射角区间，Y:方位角区间"> 角度分布
                </button>
              </div>
              <div>
                时间 <select id="rx" style="width:110px">
                <option value="1" selected>1天</option>
                <option value="2">2天</option>
                <option value="3">3天</option>
                <option value="5">5天</option>
                <option value="10">10天</option>
                <option value="14">14天</option>
              </select>
                空间参数 <select id="vy" style="width:110px">
                <option data="area_azi" value="SensorAzimuth">SensorAzimuth</option>
                <option data="area_zen" value='SensorZenith'>SensorZenith</option>
              </select>
                <button class="fa fa-line-chart btn btn-sm btn-primary" onclick="draw('draw_tspc')"
                        title="X: 时间，Y: 空间参数，值: 子图"> 时空分布
                </button>
              </div>
            </div>
          </div>
          <div class="row small my1" style="border-top: 1px solid lightgray;padding-top: 5px;margin-top: 5px">
            <div class="col-sm-2">分布线图</div>
            <div class="col-sm-10" style="text-align: right">
              <button class="fa fa-area-chart btn btn-sm btn-primary" onclick="draw_classify('dwazi')"
                      title="X: 入射区间，Y: 数据组的值；分类系列：方位角"> 入射角分布
              </button>
              <button class="fa fa-area-chart btn btn-sm btn-primary" onclick="draw_classify('dszen')"
                      title="X: 方位区间，Y: 数据组的值；分类系列：入射角"> 方位角分布
              </button>
              <button class="fa fa-line-chart btn btn-sm btn-primary" onclick="draw_time('timesrs')"
                      title="X: 时间，Y: 数据组的值"> 时间序列
              </button>


              % if request.user in ('shangj','dev2'):

              <button class="fa fa-line-chart btn btn-sm btn-primary" onclick="draw_classify('hist')"
                      title="X: 数据组的值
Y: 频数    : 分布在一定区间的数据量
   概率    : 分布在一定区间的概率 （频数/总数）
   概率密度: 分布在单位区间的概率 （概率/组距）"> 直方图
              </button>
              <button class="fa fa-line-chart btn btn-sm btn-default" onclick="draw('rel')"
                      title="X: 数据组的值"> 相关性分析图
              </button>
              % endif
            </div>
            <div class="col-sm-12" style="text-align: right">
                ## Echart转换死图片,调用draw函数返回fig图片
              <button class="fa fa-area-chart btn btn-sm btn-primary" onclick="draw('dwazi_picture')"
                  title="X: 入射区间，Y: 数据组的值；分类系列：方位角"> 入射角分布图片
              </button>
              <button class="fa fa-area-chart btn btn-sm btn-primary" onclick="draw('dszen_picture')"
                      title="X: 方位区间，Y: 数据组的值；分类系列：入射角"> 方位角分布图片
              </button>
              <button class="fa fa-line-chart btn btn-sm btn-primary" onclick="draw('timesrs_picture')"
                      title="X: 时间，Y: 数据组的值"> 时间序列图片
              </button>
            </div>
          </div>
          <div class="row small my1" style="border-top: 1px solid lightgray" hidden>
            <div class="col-sm-2">数据相关分析</div>
            <div class="col-sm-10" style="text-align: right">
            </div>
          </div>
        </div>
        <div class="panel-footer p5"></div>
      </div>
    </div>
    <div class="h100 p3 flex-g2">
      <div class="panel panel-primary flex-v">
        <div class="panel-heading" style="position: relative">图像呈现 / Figure Display
          <span class="small" style="margin: -2px;position: absolute;right: 10px">
        <button class="fa fa-file-word-o btn btn-sm btn-warning" onclick="doc_all('参考仪器定标质量评估')"> 导出</button>
        <button class="fa fa-cloud-download btn btn-sm btn-info" onclick="download_all()"> 保存</button>
        <button class="fa fa-recycle btn btn-sm btn-danger" onclick="clear_all()"> 删除</button>
        <button class="fa fa-file-code-o btn btn-sm btn-default" onclick="create_all_command()"> 脚本</button>
      </span>
        </div>
        <div id="show" class="panel-body flex-g2 p5" style="overflow-y: scroll"></div>
        <div id="msg" class="panel-footer p5"></div>
      </div>
    </div>
  </div>
  <script src="/static/js/echarts-gl.min.js"></script>
  <script src="/static/js/jsyaml.js"></script>
  <script src="/static/js/doc-saver.js"></script>
  <script src="/static/js/common.js"></script>
  <script src="/static/js/xtool.js"></script>
  <script>

    TC = new TimeChart('t_chart', 'start', '/api.wrad.rain.get_time');
    let sel_value = (key, default_all = false, parse = parseInt) => {
      let list = document.querySelector(key).selectedOptions;
      if (default_all && list.length === 0) list = document.querySelector(key).options;
      return Object.assign([], list).map((o) => parse(o.value))
    };
    TC.show({});
    $('#s1').change(e => $('#extent').val(e.target.selectedOptions[0].getAttribute('data')));
    let FILTERS = [
      {name: 'MGrd±Nstd', dataset: {a: 'sigma_mean_value', b: 'sigma_std_value', _: '(x>a-b*v) & (x<a+b*v)'}, chkfunc: 0.0},
      {name: 'MAll±Nstd', dataset: {a: 'sigma_mean_value_all', b: 'sigma_std_value_all', _: '(x>a-b*v) & (x<a+b*v)'}, chkfunc: 0.0},
      {name: 'MGrd±Val', dataset: {a: 'sigma_mean_value', _: '(x>a-v) & (x<a+v)'}, chkfunc: 0.0},
      {name: 'MAll±Val', dataset: {a: 'sigma_mean_value_all', _: '(x>a-v) & (x<a+v)'}, chkfunc: 0.0},
      {name: 'MaxStdGrd', dataset: {a: 'sigma_std_value', _: 'a<v'}, chkfunc: 0.0},
      {name: 'Quality', dataset: {a: 'QualityFlag', _: 'a<v'}, chkfunc: 0.0},

    ].map((e) => new InputX(e, '' + e.chkfunc, Number));
    $('#filters').html(FILTERS.map(e => e.label));

    function com_data() {
      let d = document.getElementById('data1').selectedOptions[0].data;
      let v = [1, 2, 3, 4, 5].map(i => $('#s' + i).val());
      filters = [];
      FILTERS.forEach(e => {
        let chkfunc = e.val();
        if (chkfunc) filters.push({dataset: e.data.dataset, chkfunc})

      });
      <%text>
        let a = eval('[' + val_by_id('area_azi') + ']');
        if (a.length) filters.push({dataset: 'SensorAzimuth', chkfunc: `>=${a[0]}&<${a[1]}`});
        a = eval('[' + val_by_id('area_zen') + ']');
        if (a.length) filters.push({dataset: 'SensorZenith', chkfunc: `>=${a[0]}&<${a[1]}`});
      </%text>
      let r = {
        fname: v.map(x => (x.constructor.name === 'Array') ? x.join(',') : x).join('_'),
        pat: v.map(x => (x.constructor.name === 'Array') ? (x.length === 2 ? "*" : x[0]) : x).join('_') + '*',
        start: val_by_id('start'),
        end: val_by_id('end'),
        data: d.data,
        name: d.name,
        filters: filters
      };
      r.subtext = r.start === r.end ? r.start : [r.start, r.end].join(' ~ ');
      return r
    }

    MKDATA = {
      gbal: () => {
        let data = com_data();
        data.resu = parseFloat(val_by_id('ry'));
        data.extent = eval('[' + (val_by_id('extent') || '-180,180,-90,90') + ']');
        data.lim_m = val_by_id('lim_m');
        data.lim_s = val_by_id('lim_s');
        data.lim_r = val_by_id('lim_r');
        data.subplots = [$('#subplots').val()];
        return data
      },
      agls_dtbt: () => {
        let data = com_data();
        data.subplots = [$('#subplots').val()];
        data.area_azi = eval('[' + val_by_id('area_azi') + ']');
        data.area_zen = eval('[' + val_by_id('area_zen') + ']');
        data.title= <%text>`${data.fname} ${data.name} Angles Distribute`</%text>;
        return data
      },
      dwazi: () => {
        let data = com_data();
        data.dwazi = sel_value('#dwazi');
        data.area_zen = eval('[' + val_by_id('area_zen') + ']');
        g = data.dwazi.length ? '（方位角10°分组）' : '';
        data.title = <%text>`${data.fname} ${data.name} 随入射角分布${g}`</%text>;
        data.ylabel = data.name + " (dB)";
        return data
      },
      dszen: () => {
        let data = com_data();
        data.dszen = sel_value('#dszen');
        g = data.dszen.length ? '（入射角1°分组）' : '';
        data.area_azi = eval('[' + val_by_id('area_azi') + ']');
        data.title =  <%text>`${data.fname} ${data.name} 随方位角分布${g}`</%text>;
        data.ylabel = data.name + " (dB)";
        return data
      },
      hist: () => {
        let data = com_data();
        data.lim_m = val_by_id('lim_m');
        data.rx = parseInt(val_by_id('rx'));
        data.title =  <%text>`${data.fname} ${data.name}  直方图分布`</%text>;
        data.selectedMode = 'single';
        data.ylabel = ' ';
        data.xlabel = data.name + " (dB)"
        return data
      },
      timesrs: () => {
        let data = com_data();
        data.rx = parseInt(val_by_id('rx'));
        data.title =  <%text>`${data.fname} ${data.name}  TimeSeries`</%text>;
        return data
      }, draw_tspc: () => {
        let data = com_data();
        let Y = document.getElementById('vy').selectedOptions[0];
        data.lim_m = val_by_id('lim_m');
        data.lim_s = val_by_id('lim_s');
        data.lim_r = val_by_id('lim_r');
        data.subplots = [$('#subplots').val()];
        data.vy = Y.value;
        data.range = eval('[' + val_by_id(Y.getAttribute('data')) + ']');
        data.rx = parseInt(val_by_id('rx'));
        data.title=<%text>`${data.fname} ${data.name}  TimeSeries`</%text>;
        return data
      }, rel: () => {
        let data = com_data();
        data.lim_m = val_by_id('lim_m');
        data.data = 'Sigma_Dif';
        return data;
      },
      ##   Echart转死图片
      dwazi_picture: () => {
        let data = com_data();
        data.dwazi = sel_value('#dwazi');
        data.area_zen = eval('[' + val_by_id('area_zen') + ']');
        g = data.dwazi.length ? '（方位角10°分组）' : '';
        data.title = <%text>`${data.fname} ${data.name} 随入射角分布图片${g}`</%text>;
        data.ylabel = data.name + " (dB)";
        return data
      },
      dszen_picture: () => {
        let data = com_data();
        data.dszen = sel_value('#dszen');
        g = data.dszen.length ? '（入射角1°分组）' : '';
        data.area_azi = eval('[' + val_by_id('area_azi') + ']');
        data.title =  <%text>`${data.fname} ${data.name} 随方位角分布图片${g}`</%text>;
        data.ylabel = data.name + " (dB)";
        return data
      },
      timesrs_picture: () => {
        let data = com_data();
        data.rx = parseInt(val_by_id('rx'));
        data.title =  <%text>`${data.fname} ${data.name} TimeSeries Picture`</%text>;
        return data
      },
    };

    function draw(func) {
      data = MKDATA[func]();
      data.subplots=val_by_id('subplots');
      $get_fig('/api.wrad.rain.' + func, data, '#show')
    }

    function _classify(load, d, data, xhr) {
      let my = document.createElement('div');
      my.style.height = '350px';
      load.append(my);
      let myc = echarts.init(my);
      myc.setOption($com_option({
        title: {text: data.title, left: 5, subtext: data.subtext}, animation: false,
        tooltip: {trigger: 'axis', axisPointer: {type: 'line'}},
        xAxis: {type: 'value', name: d.xlabel||data.xlabel, min: d.xlim[0], max: d.xlim[1], nameLocation: 'center', nameGap: 30, position: 'bottom', scale: true},
        yAxis: {type: 'value', name: data.ylabel, nameLocation: 'center', nameGap: 45, scale: true},
        legend: {
          data: d.names, right: 50, top: 25, type: 'scroll', width: '60%',
          selectedMode: data.selectedMode || undefined
        },
        series: d.y.map((v, i) => {
          return {
            name: d.names[i],
            type: d.type || 'line',
            step: 'end', lineStyle: {width: .5},
            data: v.map((y, i) => [d.x[i], y < -9.9e9 ? '-' : y])
          }
        })
      }))
    }

    function draw_classify(func) {
      data = MKDATA[func]();
      $get_data('/api.wrad.rain.' + func, data, '#show', _classify, rtype = 'json')
    }

    function draw_time(func) {
      data = MKDATA[func]();
      $get_data('/api.wrad.rain.' + func, data, '#show', _timesrs, rtype = 'json')
    }

    function _timesrs(load, d, data, xhr) {
      let my = document.createElement('div');
      my.style.height = '350px';
      load.append(my);
      let myc = echarts.init(my);
      let t = d.t;
      myc.setOption($com_option({
        title: {text: data.title, left: 5, subtext: data.subtext}, animation: false,
        tooltip: {trigger: 'axis', axisPointer: {type: 'shadow'}},
        xAxis: {type: 'time', name: 'Date', nameLocation: 'center', nameGap: 30, position: 'bottom', scale: true, onZero: false},
        yAxis: {type: 'value', name: data.name + ' (dB)', nameLocation: 'center', nameGap: 45, scale: true, onZero: false, show: true},
        legend: {data: ['mean', 'std', 'rms', 'count'], right: 50, top: 25, type: 'scroll', width: '60%', selectedMode: 'single'},
        series: ['mean', 'std', 'count'].map((name) => {
          v = d[name];
          return {
            name: name,
            step: 'end', lineStyle: {width: .5},
            type: 'line', data: v.map((y, i) => [t[i], y])
          }
        }) // 'rms', 'count'
      }))
    }

    function draw_tspc(func) {
      data = MKDATA[func]();
      $get_data('/api.wrad.rain.' + func, data, '#show', _timespc, rtype = 'json')
    }

    function _timespc(load, d, data, xhr) {
      let my = document.createElement('div');
      my.style.height = '350px';
      load.append(my);
      let myc = echarts.init(my);
      let t = d.t;
      myc.setOption($com_option({
        title: {text: data.title, left: 5, subtext: data.subtext}, animation: false,
        tooltip: {trigger: 'axis', axisPointer: {type: 'shadow'}},
        xAxis: {type: 'time', name: 'Date', nameLocation: 'center', nameGap: 30, position: 'bottom', scale: true, onZero: false},
        yAxis: {type: 'value', name: data.name + ' (dB)', nameLocation: 'center', nameGap: 45, scale: true, onZero: false, show: true},
        legend: {data: ['mean', 'std', 'rms', 'count'], right: 50, top: 25, type: 'scroll', width: '60%', selectedMode: 'single'},
        series: ['mean', 'std', 'rms', 'count'].map((name) => {
          v = d[name];
          return {name: name, step: 'end', lineStyle: {width: .5}, type: 'line', data: v.map((y, i) => [t[i], y])}
        })
      }))
    }


    $('#data1').html([
      {name: 'Sigma0(WindRAD)', data: 'Sigma_Obs'},
      {name: 'Sigma0(RainForest)', data: 'Sigma_Ref'},
      {name: 'Diff', data: 'Sigma_Dif'},
      {name: 'Gamma', data: 'Gamma'},
      {name: 'Kpc', data: 'Kpc'}
    ].map((v) => mk_opt(v.name, v)))[0].selectedIndex = 2;

    function Arc() {
      this.arc1 = echarts.init(document.getElementById('arc1'));
      this.arc2 = echarts.init(document.getElementById('arc2'));
      data = [];
      ##  for (i = 0; i < 42; i++) {
      ##    data.push([i, 1]);
      ##    data.push([360 - i, 1]);
      ##  }
      let option = {
        polar: {},
        radiusAxis: {type: 'value', show: false, splitNumber: 0, max: 1, min: 0},
        angleAxis: {type: 'value', max: 360, startAngel: 90, axisLabel: {margin: 3}, axisTicks: {length: 3, inside: true}},
        series: {type: 'bar', data: data, areaStyle: {}, coordinateSystem: 'polar'},
        animation: false
      };
      this.arc1.setOption(option);
      this.arc2.setOption(option);
    }

    arc = new Arc();
    document.getElementById('dwazi').onchange = function () {
      let op = Object.assign([], document.getElementById('dwazi').options);
      data = op.map((v) => [v.selected ? 1 : 0, v.value + 5]);
      arc.arc1.setOption({series: {data: data, barWidth: 10}})
    };
    document.getElementById('dszen').onchange = function () {
      let op = Object.assign([], document.getElementById('dszen').options);
      data = [];
      op.forEach((v) => {
        data.push([v.selected ? 1 : 0, v.value - (-.5)]);
        data.push([v.selected ? 1 : 0, 359.5 - v.value])
      });
      arc.arc2.setOption({series: {data: data, barWidth: 1.1}})
    };
  </script>
</%block>
