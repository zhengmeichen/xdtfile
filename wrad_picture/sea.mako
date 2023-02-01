# coding=utf-8
<%inherit file="../base.mako"></%inherit>
<%block name="subtitle">风场雷达 雨林定标</%block>
<%block name="main">
  <%
    import  glob,os
  %>
  <style>
      <%include file="../local.css"></%include>
    .myfig[active] {
      background: #e5ffe8;
    }
  </style>
  <div class="FLEX-5">
    <div class="panel panel-primary" style="width: 800px">
      <div class="panel-heading">配置信息 / Configuration Info.</div>
      <div class="panel-body">
        <div class="row small my1">
          <div class="col-sm-8">
            类别
            <select id="s6" onchange="listfiles(this.value)" size="1">
              <option value="OMB-Sigma0-bias">无数据滤除</option>
              <option value="OMB-Sigma0-bias-wvc">WVC-L1</option>
              <option value="Lat50">中低纬-L1</option>
              <option value="addnoc-present">中低纬-L1 订正后_N</option>
              <option value="addnoc-previous">中低纬-L1 订正后_P</option>
              <option value="H-WVC">WVC-高分</option>
              <option value="H-Lat50">中低纬-高分</option>
            </select>
          </div>
          <div class="col-sm-4">

          </div>
          <div class="col-sm-12 border-top"></div>
          <div class="col-sm-2">
            波段
            <select id="KC" onchange="let ss=eval(this.selectedOptions[0].id);document.getElementById('agl_s').value=ss[0];document.getElementById('agl_e').value=ss[1];">
              <option value=".*" id="[36,44,1]" selected>不限</option>
              <option value="_Ku" id="[38,42,1]">Ku波段</option>
              <option value="_C" id="[36,44,1]">C 波段</option>
            </select>
          </div>

          <div class="col-sm-2">
            极化方向
            <select id="HV">
              <option value=".*" selected>不限</option>
              <option value="_HH">H极化</option>
              <option value="_VV">V极化</option>
            </select>
          </div>

          <div class="col-sm-2">
            统计周期
            <select id="DAY">
              <option value=".*">不限</option>
              <option value="_1D">1天</option>
              <option value="_14D" selected>14天</option>
            </select>
          </div>
          <div class="col-sm-2">
            分辨率
            <select id="KM">
              <option value=".*" selected>不限</option>
              <option value="_2.5km">2.5km</option>
              <option value="_10km">10km</option>
              <option value="_20km">20km</option>
            </select>
          </div>
          <div class="col-sm-2">
            轨道
            <select id="AD">
              <option value=".*" selected>不限</option>
              <option value="_A">升轨</option>
              <option value="_D">降轨</option>
            </select>
          </div>
          <div class="col-sm-12">
            数据文件 <span id="fcnt" style="float: right"> 筛选/总数 </span>
            <select id="files" size="10" multiple onchange="tc_update();">

            </select>
          </div>
        </div>

        <div class="row small" style="border: solid lightgray; border-width: 1px 0;height: 30px" id="t_chart">

        </div>
        <div class="row small my1">
          <div class="row small">
            <div class="col-sm-2"><b>日期/DATE</b></div>
            <div class="col-sm-6"><input id="start" type="date" style="width: 187px">~<input id="end" type="date" style="width: 187px"></div>
          </div>
          <div class="row small border-top">
            <div class="col-sm-2"><b>Y轴</b></div>
            <div class="col-sm-1">范围</div>
            <div class="col-sm-2">
              <input id="vlim" placeholder="vmin,vmax" class="w100">
            </div>
            <div class="col-sm-1"></div>
            <div class="col-sm-3"></div>
            <button class="btn btn-sm btn-primary" onclick="draw2()">随时间变化</button>
            <button class="btn btn-sm btn-primary" onclick="draw2_picture()">随时间变化图片</button>
          </div>

          <div class="row small border-top" id="agl">
            <div class="col-sm-2">
              <b>随入射角变化分布</b>
            </div>
            <div class="col-sm-1">起始</div>
            <div class="col-sm-2">
              <input type="number" id="agl_s" min="10" max="69" value="38" class="w100">
            </div>
            <div class="col-sm-1"> 结束</div>
            <div class="col-sm-2">
              <input type="number" id="agl_e" min="11" max="70" value="42" class="w100">
            </div>
            <div class="col-sm-1"> 时间间隔</div>
            <div class="col-sm-1">
              <input type="number" id="agl_space" min="1" max="365" value="1" class="w100">
            </div>
            <div class="col-sm-4"></div>
            <div class="col-sm-10"></div>
            <button class="btn btn-sm btn-primary" onclick="draw1({xlabel: 'Angel'})">随入射角变化</button>
            <button class="btn btn-sm btn-primary" onclick="draw1_picture({xlabel: 'Angel'})">随入射角变化图片</button>

          </div>

          <div class="row small border-top" id="grid">
            <div class="col-sm-2">
              <b>随网格分布</b>
            </div>
            <div class="col-sm-1">起始</div>
            <div class="col-sm-2">
              <input type="number" id="grid_s" min="0" max="69" value="30" class="w100">
            </div>
            <div class="col-sm-1"> 结束</div>
            <div class="col-sm-2">
              <input type="number" id="grid_e" min="1" max="139" value="50" class="w100">
            </div>
            <div class="col-sm-9"></div>
              <button class="btn btn-sm btn-primary" onclick="draw1({xlabel: 'WVC - Grid ',type:'wvc'})">随网格分布</button>
              <button class="btn btn-sm btn-primary" onclick="draw1_picture({xlabel: 'WVC - Grid ',type:'wvc'})">随网格分布图片</button>
          </div>
        </div>
      </div>
    </div>
    <div class="panel panel-primary" style="flex-grow:2">
      <div class="panel-heading" style="position: relative">图像呈现 / Figure Display
        <span class="small" style="margin: -2px;position: absolute;right: 10px">
        <button class="fa fa-file-word-o btn btn-sm btn-warning" onclick="doc_all('参考仪器定标质量评估')"> 导出</button>
        <button class="fa fa-cloud-download btn btn-sm btn-info" onclick="download_all()"> 保存</button>
        <button class="fa fa-recycle btn btn-sm btn-danger" onclick="clear_all()"> 删除</button>
        <button class="fa fa-file-code-o btn btn-sm btn-default" onclick="create_all_command()"> 脚本</button>
      </span>
      </div>
      <div id="show" class="panel-body" style="height: calc( 100% - 26px );overflow-y: scroll"></div>
    </div>
  </div>
  <script src="/static/js/echarts-gl.min.js"></script>
  <script src="/static/js/jsyaml.js"></script>
  <script src="/static/js/doc-saver.js"></script>
  <script src="/static/js/common.js"></script>
  <script src="/static/js/xtool.js"></script>
  <script>
    sel_value = (key, parse = parseInt) => {
      return Object.assign([], document.querySelector(key).selectedOptions).map((o) => parse(o.value))
    };
    files = document.getElementById('files');


    function base_data() {
      let bn = basename(files.value);

      let ss = bn.split('_');
      let str_s, str_e;
      {
        ## data分情况绑定不同的起始，结束控件上的信息
        if(files.value.indexOf("wvc") >= 0 ){
            if(files.value.indexOf("20km") >= 0 ){
                $('#grid_e').attr({
                    'max': 69
                });
                data = {
                filename: files.value,
                s: parseInt(document.getElementById('grid_s').value),
                e: parseInt(document.getElementById('grid_e').value) + 1,
                };
            }
            else {
                $('#grid_e').attr({
                    'max': 139
                });
                data = {
                filename: files.value,
                s: parseInt(document.getElementById('grid_s').value),
                e: parseInt(document.getElementById('grid_e').value) + 1,
                };
            }

        }
        else {
            data = {
                filename: files.value,
                s: parseInt(document.getElementById('agl_s').value),
                e: parseInt(document.getElementById('agl_e').value) + 1,
            };
        }

        ## 获取传入时间，格式为年月日，在后台将其转化为时间戳格式
        start = str_s = document.getElementById('start').value;
        end = str_e = document.getElementById('end').value;
        data.start = start;
        data.end = end;
        data.subtext = [bn.split('.')[0], str_s === str_e ? str_s : str_s + ' ~ ' + str_e].join(' ');
        ## 通过不同文件，区别图上横坐标的名称
        data.clslabel =  bn.includes('wvc')?'WVC Grid':'Incidence Angle (degree)';
        return data;
      }
    }


    /* TimeShow */
    TC = new TimeChart('t_chart', 'start', '/api.wrad.sea.get_seatime');
    let tc_update = async () => {

      ##  网格只显示网格div，入射角只显示入射角div
      if(files.value.indexOf("wvc") >= 0 ) {
          $('#grid').show();
          $('#agl').hide();
      }
      else{
          $('#agl').show();
          $('#grid').hide();
      }

      data = base_data();
      if (data) {
        await TC.show({filename: files.value});
        if (valof('#s6').startsWith('addnoc')) {
          op = TC.chart.getOption();
          d = op.series[0].data;
          _e = d[d.length - 1][0];
          _s = d[0][0];
          d.push([_s + 864e5, 0]);
          TC.chart.setOption({series: [{data: d}]});
          TC.chart.select(_s - 431e5, _e + 431e5);
        }
      }


    };


    function draw1() {
      data = base_data();
      if (data) $get_data('/api.wrad.sea.get_sea_agl', data, '#show', show1, rtype = 'json')
    }

    ## Echart转死图片
    ## 绘制时间序列图
    function draw2_picture() {
      data = base_data();
      ## 传入范围数据
      data.vlim = document.getElementById('vlim').value.split(',');
      $get_fig('/api.wrad.sea.get_sea_time_img', data, '#show');
    }
    ## 绘制入射角、网格图
    function draw1_picture() {
      ## data已经返回获取到的所有信息
      data = base_data();
      ##  alert(data.filename);
      ##  alert(typeof data.filename);
      ## 将时间间隔数据传入
      data.space=document.getElementById('agl_space').value;

      ## 绘制图片
      $get_fig('/api.wrad.sea.get_sea_picture', data, '#show');
    }


    //'Incidence Angle (degree)'
    function show1(load, d, rd, xhr) {
      let my = document.createElement('div');
      my.style.height = '400px';
      load.append(my);
      let myc = echarts.init(my);
      myc.setOption($com_option({
        title: {text: 'Incidence Angle Distribute of Sigma0 difference (NOC)', subtext: rd.subtext, left: 10},
        tooltip: {trigger: 'axis', axisPointer: {type: 'line'}},
        grid: {right: 110, left: 70, bottom: 60, top: 60},
        xAxis: {type: 'value', name: rd.clslabel, nameLocation: 'center', nameGap: 30},
        yAxis: {type: 'value', name: 'Diff (dB)', nameLocation: 'center', nameGap: 45},
        legend: {data: d.legend, right: 5, top: 25, type: 'scroll', orient: 'vertical', height: 300, selector: true, pageIconSize: 12, selected: [40]},
        animationDuration: 200,
        series: d.series.map((v, i) => {
          return {name: d.legend[i], type: 'line', data: v.map((y, i) => [d.x[i], y === -999 ? '-' : y])}
        })
      }));
      change_v2(myc);
    }

    function draw2() {
      data = base_data();
      ##  data.start = new Date(str_s = document.getElementById('start').value).getTime() / 1000.;
      ##  data.end = new Date(str_e = document.getElementById('end').value).getTime() / 1000.;
      if (data) $get_data('/api.wrad.sea.get_sea_time', data, '#show', show2, rtype = 'json')
    }

    function show2(load, d, rd, xhr) {
      let my = document.createElement('div');
      my.style.height = '400px';
      load.append(my);
      let myc = echarts.init(my);
      myc.setOption($com_option({
        title: {text: 'Time Series of Sigma0 difference (NOC)', subtext: rd.subtext, left: 10},
        tooltip: {trigger: 'axis', axisPointer: {type: 'line'}}, grid: {right: 110, left: 70, bottom: 60, top: 60},
        xAxis: {type: 'time', name: 'Time (day)', nameLocation: 'center', nameGap: 30},
        yAxis: {type: 'value', name: 'Diff (dB)', nameLocation: 'center', nameGap: 45},
        legend: {data: d.legend, right: 5, top: 25, type: 'scroll', orient: 'vertical', height: 300, selector: true, pageIconSize: 12},
        animationDuration: 200,
        series: d.series.map((v, i) => {
          return {name: d.legend[i], type: 'line', data: v.map((y, i) => [d.x[i], y === -999 ? '-' : y])}
        })
      }));
      change_v2(myc);
    }



    function get_vlim() {
      let v = document.getElementById('vlim').value.split(',');
      return {min: eval(v[0] || 'undefined'), max: eval(v[1] || 'undefined')}
    }

    function change_v2(c) {
      let vlim = get_vlim();
      c.setOption({yAxis: [vlim]});
    }

    function change_v() {
      let vlim = get_vlim();
      $('.myfig[active]').each(function (i, c) {
        echarts.getInstanceByDom(c.childNodes[0]).setOption({yAxis: [vlim]});
      })
    }

    $('#vlim').change(change_v).blur(change_v);
    document.querySelector('#show').ondblclick = function (e) {
      let t = e.target;
      for (i = 0; i < 4; i++) {
        if (t.className === 'myfig') {
          t.toggleAttribute('active');
          break;
        }
        t = t.parentNode;
      }
    };

    async function listfiles(mask) {
      d = await $.getJSON('/api.wrad.sea.listfiles?mask=' + mask);
      d.files.sort();
      $('#files').html(d.files.map(v => mk_opt(basename(v).replace('.bin', ''), undefined, v)));
      filter_files()
    }

    listfiles('OMB-Sigma0-bias');

    let KC = document.getElementById('KC');
    let HV = document.getElementById('HV');
    let DAY = document.getElementById('DAY');
    let KM = document.getElementById('KM');
    let AD = document.getElementById('AD');
    let filter_files = () => {
      let pat = '', last = '.*';
      [KC.value, AD.value, '.*', KM.value, HV.value, DAY.value].forEach(v => {
        if (v !== last) pat += v;
        last = v
      });
      pat = new RegExp(pat.trim('.*'));
      let i, op, ops = document.getElementById('files').options;
      let sel = 0;
      for (i = 0; i < ops.length; i++) {
        op = ops[i];
        chk = pat.test(op.innerText);
        op.hidden = !chk;
        sel += chk;
      }
      $('#fcnt').html(<%text>`${sel}个/${ops.length}共个`</%text>)
    };
    $([KC, AD, HV, DAY, KM]).change(filter_files)
  </script>
</%block>
