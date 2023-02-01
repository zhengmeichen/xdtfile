# coding=utf8
<%def name="navitem(name,url='#',child=None,target=None,title=None)">
  % if child:
    <% active=(' active' if [i for i in child if i['url']==current_url] else '') %>
    <li class="dropdown${active}"${(' title="%s"'% title if title else '')}>
      <a class="dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-haspopup="true"
         aria-expanded="false">${name}<span class="caret"></span></a>
      <ul class="dropdown-menu">
        %for i in child:
           ${navitem(**i)}
        % endfor
      </ul>
    </li>
  % else:
    <li${(' class=active' if current_url==url else'')}${(' title="%s"'% title if title else '')}><a href="${url}"${(' target="'+target+'"' if target else '')}>${name}</a></li>
  % endif
</%def>
<%
  data=tool.nav()
  current_url=request.path
%>
<!DOCTYPE html>
<html lang="zh-cn">
<head>
  <title><%block name="subtitle"/> ${data.get('sysname',u'- 数据分析平台')}</title>
  <%block name="head"/>
  <link href="/static/css/bootstrap.min.css" rel="stylesheet">
  <link href="/static/css/bootstrap-theme.min.css" rel="stylesheet">
  <link href="/static/css/font-awesome.min.css" rel="stylesheet">
  <link href="/static/css/style.css?112" rel="stylesheet">
  <script src="/static/js/jquery-3.1.0.min.js"></script>
  <script src="/static/js/bootstrap.min.js"></script>
  <%block name="jscript">
    <script src="/static/js/echarts.min.js"></script>
  </%block>
  ##   <style>    html {filter: progid:DXImageTransform.Microsoft.BasicImage(grayscale=1); -webkit-filter: grayscale(100%);}  </style>
</head>
<body>
<nav class="navbar ${data.get('style','navbar-default')} navbar-fixed-top">
  <div class="container-fluid">
    <div class="navbar-header">
      <a class="navbar-brand">${data.get('name','[nav.name]')}</a>
    </div>
    <ul class="nav navbar-nav">
      %for i in data['pages']:
            ${navitem(**i)}
      % endfor
    </ul>
    <ul class="nav navbar-nav" style="float: right">
      %for i in data.get('pages-right',[]):
            ${navitem(**i)}
      % endfor
    </ul>
  </div>
</nav>
<div style="height: calc(100vh - 41px);margin-top: 41px;position:relative;background: #d0d9e8;overflow-y: auto;">
  <%block name="main"></%block>
</div>
</body>
</html>