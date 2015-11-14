%include ('./view/bsfiles/view/html_hdr.tpl')

%include ('./view/bsfiles/view/navbar.tpl')

    <div class="container-fluid">
      <div class="row">
      	%include ('./view/bsfiles/view/nav_sidebar.tpl')
      	<div class="col-xs-9 col-xs-offset-3 col-sm-9 col-sm-offset-3 
                    col-md-10 col-md-offset-2 col-lg-10 col-lg-offset-2 main">
          <table class="table table-striped">
          <tbody>
            <form action="/blacklist_query" method="POST">
              <tr>
                <td>
                  <label class="col-xs-4 col-sm-4 col-md-4 col-lg-4 control-label">车牌号</label>
                  <div class="col-xs-5 col-sm-5 col-md-6 col-lg-6">
                  <input type="text" class="form-control input-sm" id="plate" name="plate">
                  </div>
                </td>
              </tr>
              <tr>
                <td>
                <button type="submit" class="btn btn-md btn-primary" name="query" value="show">查询</button>
                </td>
              </tr>
            </form>
          </tbody>
          </table>
            %if blist:
            <panel>黑名单列表</panel>
      	    <table class="table table-striped">
              <thead>
                <tr>
                  <th>序号</th>
                  <th>车牌号</th>
                  <th>添加时间</th>
                  <th>状态</th>
                </tr>
              </thead>
              <tbody>
              	%for b in blist:
	                <tr>
	                  <td>{{b[0]}}</td>
	                  <td>{{b[1]}}</td>
	                  <td>{{b[2]}}</td>
                    %if b[-1] == 0:
                      <td>添加待审核</td>
                    %elif b[-1] == 1:
                      <td>删除待审核</td>
                    %else:
                      <td>已审核</td>
                    %end
	                </tr>
	           	 	%end
              </tbody>
            </table>
            %else:
              <panel>无黑名单纪录</panel>
            %end
      	</div>
      </div>
  	</div>

	<!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="/static/view/bsfiles/js/jquery.min.js"></script>
    <script src="/static/view/bsfiles/js/bootstrap.min.js"></script>

%include ('./view/bsfiles/view/html_footer.tpl')
