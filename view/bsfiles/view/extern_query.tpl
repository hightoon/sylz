%include ('./view/bsfiles/view/html_hdr.tpl')

%include ('./view/bsfiles/view/navbar.tpl')

    <div class="container-fluid">
      <div class="row">
      	<div class="ccol-xs-8 col-xs-offset-2 col-sm-8 col-sm-offset-2 
                    col-md-10 col-md-offset-1 col-lg-10 col-lg-offset-1 main">
      	  <h3 class="sub-header">违章记录查询</h3>
      	  <table class="table table-striped">
      	  	<tbody>
	      	  <form action="/extern_query" method="POST">
	      	  	<tr>
		          <td>
		        	  <label class="col-xs-4 col-sm-4 col-md-4 col-lg-4 control-label">车牌号</label>
		        	  <div class="col-xs-5 col-sm-5 col-md-6 col-lg-6">
		        	  	<input type="text" class="form-control input-sm" name="VehicheCard" value={{VehicheCard}}>
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
          <br><br>
          %if results is not None:
          	<h3 class="sub-header">查询结果</h3>
	        <table class="table table-striped"> 
	          <thead>
	          	<tr>
	          	  %for col in results[0]:
	          	    <th>{{col}}</th>
	          	  %end
	          	  <th>操作</th>
	          	</tr>
	          </thead>
	          <tbody>
	          	%for res in results[1:]:
	          	  <tr>
	          	  %for col in res[1:]:
	          	    <td>{{col}}</td>
	          	  %end
	          	  <td>
	          	  	<button type="button" class="btn btn-sm btn-primary" 
	          	  			onclick="open_window('/ext/details/{{res[0]}}');">
	          	  		查看详情
	          	  	</button>
	          	  </td>
	          	  </tr>
	          	%end
	          </tbody>
	        </table>
	      %end
    	</div>
      </div>
  	</div>

	<!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="/static/view/bsfiles/js/jquery.min.js"></script>
    <script src="/static/view/bsfiles/js/bootstrap.min.js"></script>
    <!--script src="/static/view/bsfiles/js/jquery-ui-1.11.4.custom/external/jquery/jquery.js"></script-->

%include ('./view/bsfiles/view/html_footer.tpl')