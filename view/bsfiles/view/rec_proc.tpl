%include ('./view/bsfiles/view/html_hdr.tpl')

%include ('./view/bsfiles/view/navbar.tpl')

    <div class="container-fluid">
      <div class="row">
      	%include ('./view/bsfiles/view/nav_sidebar.tpl')
      	<div class="col-xs-9 col-xs-offset-3 col-sm-9 col-sm-offset-3 
                    col-md-10 col-md-offset-2 col-lg-10 col-lg-offset-2 main">
      	  <h3 class="sub-header">超限处理</h3>
      	  <table class="table table-striped">
            <tbody>
            <form action="/proceed" method="POST">
              <tr>
                <td>
                  <label class="col-sm-3 control-label">站点编号</label>
                  <div class="col-sm-4">
                    <select class="form-control select-sm" name="area" id="area">
                      <option value="是" selected>超限</option>
                      <option value="否">未超限</option>
                      <option value="">全部</option>
                    </select>
                ｀</div>
                </td>
                <td>
                  <label class="col-sm-2 control-label">车牌号</label>
                  <div class="col-sm-4">
                    <input type="text" class="form-control input-sm" name="plate" id="plate" />
                  </div>
                </td>
            ｀</tr>
            ｀<tr>
                <td>
                <button type="submit" class="btn btn-md btn-primary" name="submit" value="proceed">查询</button>
                </td>
            ｀</tr>
            </form>
            </tbody>
          </table>
          %if results is not None:
            <h3 class="sub-header">待处理纪录</h3>
            %for r in results:

            %end
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