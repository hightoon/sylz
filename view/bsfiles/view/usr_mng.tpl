%include ('./view/bsfiles/view/html_hdr.tpl')

%include ('./view/bsfiles/view/navbar.tpl')

    <div class="container-fluid">
      <div class="row">
      	%include ('./view/bsfiles/view/nav_sidebar.tpl')
      	<div class="col-xs-9 col-xs-offset-3 col-sm-9 col-sm-offset-3 
                    col-md-10 col-md-offset-2 col-lg-10 col-lg-offset-2 main">
      	  <h3 class="sub-header">已存在用户</h3>
      	    <table class="table table-striped">
              <thead>
                <tr>
                  <th>用户名</th>
                  <th>姓名</th>
                  <th>备注</th>
                  <th>所属用户组</th>
                  <th>注册时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
              	%for usr in usrs:
	                <tr>
	                  <td>{{usr.usrname}}</td>
	                  <td>{{usr.nickname}}</td>
	                  <td>{{usr.desc}}</td>
	                  <td>{{usr.role}}</td>
	                  <td>{{usr.regtime}}</td>
	                  <td><form action="/del_user/{{usr.usrname}}"  method="POST">
	                  	<button class="btn btn-xs btn-warning">删除
	                    </button></form>
	                  </td>
	                </tr>
	           	 	%end
              </tbody>
            </table>
          <h3 class="sub-header">添加用户</h3>
          	<table class="table table-striped">
          		<thead>
          			<tr>
                  <th>用户名</th>
                  <th>密码</th>
                  <th>姓名</th>
                  <th>备注</th>
                  <th>所属用户组</th>
                  <th>操作</th>
                </tr>
                <tr>
                	<form action="/update_user" method="POST">
                	<td><input type="text" class="form-control input-sm" name="usrname" required></td>
                	<td><input type="text" class="form-control input-sm" name="passwd" required></td>
                	<td><input type="text" class="form-control input-sm" name="nickname"></td>
                	<td><input type="text" class="form-control input-sm" name="desc"></td>
                	<td>
                		<select class="form-control input-sm" name="role">
                			<option value="系统管理员">超级管理员</option>
                			<option value="管理员">管理员</option>
                			<option value="操作员">操作员</option>
                			<option value="来宾">来宾</option>
                		</select>
                	</td>
                	<td>
                		<button type="submit" class="btn btn-xs btn-primary" name="op" value="update">添加</button>
                		<button type="submit" class="btn btn-xs btn-default" name="op" value="cancel">取消</button>
                	</td>
                	</form>
                </tr>
          		</thead>
          	</table>
      	</div>
      </div>
  	</div>

	<!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="/static/view/bsfiles/js/jquery.min.js"></script>
    <script src="/static/view/bsfiles/js/bootstrap.min.js"></script>

%include ('./view/bsfiles/view/html_footer.tpl')
