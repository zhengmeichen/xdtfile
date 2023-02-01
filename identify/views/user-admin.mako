# coding=utf-8
<%inherit file="base.mako"></%inherit>
<%block name="main">
  <div style="display: flex;flex-direction: column;height: 100%">
    <h1 align="center">用户管理</h1>
    ##  已经登录账号
    % if request.user.role <5:
      <div style="flex-grow: 2">
        <div style="display: flex;flex-direction: row;height: 100%">
          <div style="width: 42%;height: 100%;position: relative" >
            <div id="left" style="position: absolute;width: 100%;height: 100%;overflow-y: auto">
              <%include file="showusers.mako"></%include>
            </div>
          </div>
          <div style="flex-grow: 2;position: relative">
          <iframe id="right" style="width: 100%;height: 100%;background: whitesmoke;border: none">
          </iframe></div>
        </div>
      </div>
    %else:
      <div style="display: flex;flex-direction: row;height: 100%">
        <div id="left" style="position: absolute;width: 100%;height: 100%;overflow-y: auto">
          <%include file="user.mako"></%include>
        </div>
      </div>
    %endif

  </div>
  <script>
    function modify(uid) {
      document.getElementById('right').src = '/admin?uid=' + uid;
    }
  </script>
</%block>