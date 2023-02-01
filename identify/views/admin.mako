# coding=utf-8

<%
  u = dbo.get_user(request.params.uid)
  def checked(v,val='checked'):
    return val if v else ''
%>
<head>
  <title>用户信息修改</title>
</head>
<body>

<div style="position: absolute;
             top: 50%;
             left: 50%;
             transform: translate(-50%,-50%)">
  <h2>修改用户信息</h2>
  <label for="id">id：</label>
  <input id="id" value="${u.id}" readonly><br>
  <span></span><br>
  <label for="user">用户名：</label>
  <input type="text" id="user" value="${u.user}" ><br>
  <span></span><br>

  <label for="name">姓名：</label>
  <input type="text" id="name" value="${u.name}"><br>
  <span></span><br>

  <label for="passwd">重置用户密码：</label>
  <input id="passwd" type="text" placeholder="******"><br>
  <span></span><br>

  <label for="mask">仪器：</label>
  <input id="mask" type="text" value="${u.mask}" ><br>
  <span></span><br>

  <label for="role">权限：</label>
  <select id="role" name="role">
    <option value=1 ${checked(u.role==1,val='selected')}>管理员</option>
    <option value=3 ${checked(u.role==3,val='selected')}>开发人员</option>
    <option value=5 ${checked(u.role==5,val='selected')}>科研用户</option>
  </select><br>
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

  <label for="disable">
    <input type="checkbox" id="disable" ${checked(u.disable)}> 生效标志
  </label><br>
  <span></span><br>
  <button onclick="window.history.back()">返回</button>
  <button id="submit" onclick="submitall()">提交</button>

</div>
</body>


<script src="/static/js/jquery-3.1.0.min.js"></script>
<script src="/static/js/md5.js"></script>
<script>


    ## 提交更新信息
  function submitall() {
    a = {
      ## 传入数据
      id: parseInt(document.getElementById('id').value),
      user: document.getElementById('user').value,
      name: document.getElementById('name').value || null,
      role: parseInt(document.getElementById('role').value),
      email: document.getElementById('email').value || null,
      passwd: document.getElementById('passwd').value || undefined,
      tel: document.getElementById('tel').value || null,
      dingding: document.getElementById('dingding').value || null,
      discription: document.getElementById('discription').value || null,
      mask: document.getElementById('mask').value || null,
      disable: document.getElementById('disable').checked,
    };
    $.ajax({
      url: '/api.admin.update',
      type: 'post',
      data: {
        ## base64加密
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
          ##   重置页面
          window.location.reload();
        }
      }
    })
  }
</script>