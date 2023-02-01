# coding=utf-8
<%inherit file="base.mako"></%inherit>
<%block name="main">

  <%
    u = request.user
    def checked(v,val='checked'):
      return val if v else ''
  %>

  <div style="position: absolute;
              top: 50%;
             left: 50%;
             transform: translate(-50%,-50%);
             font-size: 16px">
    <label for="id">id：</label>
    <input id="id" value="${u.id}" readonly><br>
    <span></span><br>
    <label for="user">用户名：</label>
    <input type="text" id="user" value="${u.user}"><br>
    <span></span><br>

    <label for="name">姓名：</label>
    <input type="text" id="name" value="${u.name}"><br>
    <span></span><br>

    <label for="oldpasswd">请输入旧密码：</label>
    <input id="oldpasswd" type="password" placeholder="******" onchange="checkoldpwd()"><br>
    <span></span><br>


    <label for="passwd_new">请输入新密码：</label>
    <input id="passwd_new" type="password" placeholder="密码(不少于8位)" onchange="checkpwd()"><br>
    <span></span><br>

    <label for="repasswd">确认新密码：</label>
    <input id="repasswd" type="password" placeholder="确认密码" onchange="checktwo()"><br>
    <span></span><br>

    %if u.role<5:
      <label for="role">权限：</label>
      <select id="role" name="role">
        <option value=1 ${checked(u.role==1,'selected')}>管理员</option>
        <option value=3 ${checked(u.role==3,'selected')}>开发人员</option>
        <option value=5 ${checked(u.role==5,'selected')}>科研用户</option>
      </select><br>
    %else:
      <label for="role">权限：</label>
      <select id="role" name="role" readonly="readonly" disabled="disabled">
        <option value=1 ${checked(u.role==1,'selected')}>管理员</option>
        <option value=3 ${checked(u.role==3,'selected')}>开发人员</option>
        <option value=5 ${checked(u.role==5,'selected')}>科研用户</option>
      </select><br>
    %endif
    <span></span><br>

    <label for="email">邮箱：</label>
    <input type="text" id="email" value="${u.email}"><br>
    <span></span><br>

    <label for="tel">电话：</label>
    <input type="text" id="tel" value="${u.tel}"><br>
    <span></span><br>

    <label for="dingding">钉钉账号：</label>
    <input type="text" id="dingding" value="${u.dingding}"><br>
    <span></span><br>

    <label for="discription">备注：</label>
    <input type="text" id="discription" value="${u.discription}"><br>
    <span></span><br>

    %if u.role<5:
      <label for="mask">仪器：</label>
      <input id="mask" type="text" value="${u.mask}"><br>
      <span></span><br>

      <label for="disable">
        <input type="checkbox" id="disable" ${checked(u.disable)}> 生效标志
      </label><br>
      <span></span><br>
    %endif

    <button onclick="window.history.back()">返回</button>
    <button id="submit" onclick="submitall()">提交</button>

  </div>


  <script src="/static/js/jquery-3.1.0.min.js"></script>
  <script src="/static/js/md5.js"></script>
  <script>

      ##   检验旧密码
  function checkoldpwd() {
      ## 获取旧密码
    var oldpasswd = document.getElementById('oldpasswd').value;
      ## 验证旧密码是否与数据库中匹配
    if (oldpasswd === '${u.passwd}') {
        ##  $('#pass').hide();
      document.getElementById("submit").disabled = false;
      }
        ##  else if (oldpasswd === '') {
    ##    ##  $('#pass').hide();
    ##    document.getElementById("submit").disabled = false;
    ##  }
    else {
        ##  $('#pass').show();
      ##  document.getElementById("pass").innerHTML = "<br><font color='red'>密码错误</font>";
      ##  document.getElementById('passwd_new').value = '';
      if (oldpasswd !== '') {
          alert('密码错误');
          document.getElementById('oldpasswd').value = '';
          document.getElementById("submit").disabled = false;
        } else {
          document.getElementById('oldpasswd').value = '';
          document.getElementById("submit").disabled = false;
        }
      }
    }

      ## 检验新密码
  function checkpwd() {
      ## 填写新密码必须填写旧密码
    ## 获取旧密码
    var oldpasswd = document.getElementById('oldpasswd').value;
      var passwd_new = document.getElementById('passwd_new').value;

      if (oldpasswd === '' && passwd_new !== '') {
        alert('请先输入旧密码');
        document.getElementById('passwd_new').value = '';
        document.getElementById("submit").disabled = false;
      } else if (oldpasswd === '' && passwd_new === '') {
        ##  $('#show').hide();
      document.getElementById("submit").disabled = false;
      } else if (oldpasswd !== '${u.passwd}' && passwd_new !== '') {
        ##  $('#show').hide();
      document.getElementById('passwd_new').value = '';
        document.getElementById("submit").disabled = false;
      } else if (oldpasswd === '${u.passwd}' && passwd_new !== '') {
        ##  密码复杂度检查
      ## 密码包含大写字母、小写字母、数字、特殊符号中的至少三类，且长度在8到20之间。
      var regex = new RegExp('^(?!([A-Z]*|[a-z]*|[0-9]*|[!-/:-@\\[-`{-~]*' +
                '|[A-Za-z]*|[A-Z0-9]*|[A-Z!-/:-@\\[-`{-~]*|[a-z0-9]*|[a-z!-/:-@\\[-`{-~]*|' +
                '[0-9!-/:-@\\[-`{-~]*)$)[A-Za-z0-9!-/:-@\\[-`{-~]{8,20}$');

        ##  大小写字母、数字、特殊符号 四选三
      ##  var regex = new RegExp('^(?![a-zA-Z]+$)(?![A-Z0-9]+$)(?![A-Z\\W_]+$)' +
      ##          '(?![a-z0-9]+$)(?![a-z\\W_]+$)(?![0-9\\W_]+$)[a-zA-Z0-9\\W_]{8,20}$');

        if (!regex.test(passwd_new)) {
          ##  $('#show').show();
        ##  document.getElementById("show").innerHTML = "<br><font color='green'>您的密码复杂度太低（密码中必须包含大写字母、小写字母、数字、特殊符号中的至少三类），请及时改密码</font>";

          alert('您的密码复杂度太低（密码中必须包含大写字母、小写字母、数字、特殊符号中的至少三类），请及时改密码');
          document.getElementById('passwd_new').value = '';
          document.getElementById("submit").disabled = false;
        } else {
          ##  $('#show').hide();
        document.getElementById("submit").disabled = true;
        }
      } else if (oldpasswd === '${u.passwd}' && passwd_new === '') {
        ##  $('#show').hide();
      document.getElementById("submit").disabled = false;
      }
    }

      ## 二次验证
  function checktwo() {
      ##  输入两次密码校验
    var passwd_new = document.getElementById('passwd_new').value;
      var repassword = document.getElementById("repasswd").value;
      if (passwd_new === '') {

        ##  $('#alert').show();
      ##  document.getElementById("alert").innerHTML = "<br><font color='red'>请先输入新密码</font>";
      alert('请先输入新密码');
        document.getElementById("repasswd").value = '';
        document.getElementById("submit").disabled = false;
      } else {
        if (!repassword) {
          document.getElementById("submit").disabled = true;
          ##  $('#alert').show();
        ##  document.getElementById("alert").innerHTML = "<br><font color='red'>请输入确认密码</font>";
        alert('请输入确认密码')
        } else {
          if (passwd_new === repassword) {
            ##  $('#alert').hide();
          document.getElementById("submit").disabled = false;
            ##  document.getElementById("alert").innerHTML = "<br><font color='red'>两次输入密码不一致!请重新输入</font>";
        } else {
            ##  $('#alert').show();
          ##  document.getElementById("alert").innerHTML = "<br><font color='red'>两次输入密码不一致!请重新输入</font>";
          alert('两次输入密码不一致!请重新输入');
            document.getElementById("repasswd").value = '';
            document.getElementById("submit").disabled = true;
          }
        }
      }
    }


      ## 提交更新信息
  function submitall() {
      ## 查看权限
    role = parseInt(document.getElementById('role').value);
      if (role < 5) {
        a = {
          ## 传入数据
        id: parseInt(document.getElementById('id').value),
          user: document.getElementById('user').value,
          role: parseInt(document.getElementById('role').value),
          name: document.getElementById('name').value || null,
          email: document.getElementById('email').value || null,
          passwd: document.getElementById('passwd_new').value || undefined,
          tel: document.getElementById('tel').value || null,
          dingding: document.getElementById('dingding').value || null,
          discription: document.getElementById('discription').value || null,
          mask: document.getElementById('mask').value || null,
          disable: document.getElementById('disable').checked,
        };
      } else {
        a = {
          ## 传入数据
        id: parseInt(document.getElementById('id').value),
          user: document.getElementById('user').value,
          role: parseInt(document.getElementById('role').value),
          name: document.getElementById('name').value || null,
          email: document.getElementById('email').value || null,
          passwd: document.getElementById('passwd_new').value || undefined,
          tel: document.getElementById('tel').value || null,
          dingding: document.getElementById('dingding').value || null,
          discription: document.getElementById('discription').value || null,
        };
      }
      $.ajax({
        url: '/api.user.update',
        type: 'post',
        data: {
          ## base64加密
        ## 将密码用MD5加密
        key: md5('${request.remote_addr}:' + document.getElementById('oldpasswd').value + ':'),
          ##  newkey: md5('${request.remote_addr}:' + document.getElementById('passwd_new').value + ':${request.user.user}'),
        ## encodeURI可以将中文一并转入
        msg: btoa(encodeURI(JSON.stringify(a)))
        },
        success: function (s) {
          if (s.status) {
            ## 重新加载页面
          ##  alert(${request.session.uu_key('AuthKey')});
          alert('提交成功,信息已修改');
            window.location.reload();
          } else {
            alert('提交失败,信息未修改');
          }
        }
      })
    }
  </script>
</%block>