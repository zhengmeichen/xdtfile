# coding=utf-8
<table width="540px">
  <thead>
  <tr>
    <th style="font-size: 15px" fwidth="70px" align="center" >id</th>
    <th style="font-size: 15px" width="170px" align="center" >user</th>
    <th style="font-size: 15px" width="70px" align="center" >name</th>
    <th style="font-size: 15px" width="70px" align="center" >role</th>
    <th style="font-size: 15px" width="90px" align="center" >操作</th>
  </tr>
  </thead>
  <tbody id="TbData">
    <%
      ROLE={5:u"科研用户",1:u"管理员",3:u"开发人员"}
    %>
    % for i in dbo.get_users():
      ## 显示id大于5的用户信息
      % if i['id']>=5:
      <tr>
        <td style="font-size: 15px">${i['id']}</td>
        <td style="font-size: 15px">${i['user']}</td>
        <td style="font-size: 15px">${i['name']}</td>
        <td style="font-size: 15px">${ROLE[i['role']]}</td>
        <td style="font-size: 15px;color: red" onclick="modify(${i['id']})">修改</td>
      </tr>
      % endif
    % endfor
  </tbody>
</table>
