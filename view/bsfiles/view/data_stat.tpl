%include ('./view/bsfiles/view/html_hdr.tpl')

%include ('./view/bsfiles/view/navbar.tpl')

    <div class="container-fluid">
      <div class="row">
      	%include ('./view/bsfiles/view/nav_sidebar.tpl')
      	<div class="col-xs-9 col-xs-offset-3 col-sm-9 col-sm-offset-3 
                    col-md-10 col-md-offset-2 col-lg-10 col-lg-offset-2 main">
      	  <h3 class="sub-header">数据统计</h3>
      	  <table class="table table-striped">
      	  	<tbody>
	      	  <form action="/query" method="POST">
	      	  	<tr>
	      	  	  <td>
		      	  	  <label class="col-xs-3 col-sm-3 col-md-3 col-lg-3 control-label">超限状态</label>
		      	  	  <div class="col-sm-3">
		        	  <select class="form-control input-sm" name="overweight" id="overweight">
	        			<option value="是">超限</option>
	        			<option value="否">未超限</option>
		        	  </select>
		        	  </div>
		          </td>
		          <td>
		        	  <label class="col-xs-3 col-sm-3 col-md-3 col-lg-3 control-label">处理状态</label>
		        	  <div class="ccol-xs-3 col-sm-3 col-md-3 col-lg-3">
		        	  <select class="form-control input-sm" name="proceeded" id="proceeded">
	        			<option value="是">已处理</option>
	        			<option value="否">需处理</option>
		        	  </select>
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
    	</div>
      </div>
  	</div>

	<!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="/static/view/bsfiles/js/jquery.min.js"></script>
    <script src="/static/view/bsfiles/js/bootstrap.min.js"></script>

%include ('./view/bsfiles/view/html_footer.tpl')