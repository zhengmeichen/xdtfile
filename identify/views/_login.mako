# coding=utf-8
<div style="width: 500px;margin: 30px auto 0" class="layui-card layui-bg-black">
##     <div class="layui-card-body" style="background-image: url(/static/favicon.png);background-size: cover">
    <div class="layui-card-body" style="background-image: url(/static/img/11.jpg);background-size: cover">
        <div class="layui-form" style="padding: 55px 25px;background-color: #33333399">
            ##  已经登录账号
            % if request.user:
                <h2>Welcome ${request.user}</h2>
                <br><br>
                <div class="layui-form" style="padding: 0 80px">
                    <div>(${request.session['role']})</div>
                    <div>Login From: ${('%s' % request.remote_addr)}</div>
                    <div>Welcome ${request.user}</div>
                    <hr>
                    <button class="layui-btn layui-btn-primary" onclick="window.history.back()"> 返回</button>&nbsp;
                    <button class="layui-btn layui-btn-primary" onclick="logout()"> 注销</button>
                </div>

            %else:
                ##  登录
                <h2>Please Login</h2>
                <br> <br>
                <div class="layui-form-item">
                    <label class="layui-form-label" for="username">用户</label>
                    <div class="layui-input-inline">
                        <input id="username" placeholder="请输入用户" autocomplete="off" class="layui-input">
                    </div>
                </div>
                <div class="layui-form-item">
                    <label class="layui-form-label" for="password">密码</label>
                    <div class="layui-input-inline">
                        <input type="password" id="password" placeholder="请输入密码" autocomplete="off"
                               class="layui-input">
                    </div>
                    <div id="info" class="layui-form-mid layui-word-aux" style="color: red"></div>
                </div>
                <hr>
                <div class="layui-form-item">
                    <label class="layui-form-label"></label>
                    <div class="layui-input-inline">
                        <button class="layui-btn layui-btn-fluid layui-btn-normal" onclick="login()">Login</button>
                    </div>
                </div>
            % endif
        </div>
    </div>
</div>
<script src="/static/js/jquery.min.js"></script>
<script src="/static/js/md5.js"></script>
<script>
    function login() {
        $.ajax({
            url: '/api.auth.login',
            type: 'post',
            data: {
                user: document.getElementById('username').value,
                ## 将密码用MD5加密
                key: md5('${request.remote_addr}:' +
                        document.getElementById('password').value +
                        ':${request.session.uu_key('AuthKey')}'),
            }, success: function (s) {
                if (s.isok) {
                    window.location.reload()
                } else {
                    document.getElementById('info').innerText = "登录失败"
                }
            }
        })
    }

    function logout() {
        $.ajax({
            url: '/api.auth.logout',

        })
    }
</script>