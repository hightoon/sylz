%include ('./view/bsfiles/view/html_hdr.tpl')

%include ('./view/bsfiles/view/navbar.tpl')

    <div class="container-fluid">
      <div class="row">
      	%include ('./view/bsfiles/view/nav_sidebar.tpl')
      	<div class="col-xs-9 col-xs-offset-3 col-sm-9 col-sm-offset-3 
                    col-md-10 col-md-offset-2 col-lg-10 col-lg-offset-2 main">
      	  <h3 class="sub-header">超限处理</h3>
      	  <table class="table table-responsive">
      	  	<tbody>
	      	  <form action="/proceed_query" method="POST">
	      	  	<tr>
	      	  	  <td>
		      	  	  <label class="col-xs-4 col-sm-4 col-md-4 col-lg-4 control-label">开始时间</label>
		      	  	  <div class="col-xs-5 col-sm-5 col-md-6 col-lg-6">
		        	  	<input type="text" class="form-control input-sm" id="startdate" name="startdate" 
		        	  	value={{startdate}}>
		        	  </div>
		          </td>
		          <td>
		      	  	  <label class="col-xs-4 col-sm-4 col-md-4 col-lg-4 control-label">结束时间</label>
		      	  	  <div class="col-xs-5 col-sm-5 col-md-6 col-lg-6">
		        	  	<input type="text" class="form-control input-sm" id="enddate" name="enddate" 
		        	  	value={{enddate}}>
		        	  </div>
		          </td>
	      	  	  <td>
		      	  	  <label class="col-xs-4 col-sm-4 col-md-4 col-lg-4 control-label">超限状态</label>
		      	  	  <div class="col-xs-5 col-sm-5 col-md-6 col-lg-6">
		        	  <select class="form-control input-sm" name="smState">
		        	  	%if smState == "1":
	        			  <option value="1" selected>超限</option>
	        			  <option value="0">正常</option>
	        			  <option value="">全部</option>
	        			%elif smState == "0":
	        			  <option value="1">超限</option>
	        			  <option value="0" selected>正常</option>
	        			  <option value="">全部</option>
	        			%else:
	        			  <option value="1">超限</option>
	        			  <option value="0">正常</option>
	        			  <option value="" selected>全部</option>
	        			%end
		        	  </select>
		        	  </div>
		          </td>
		        </tr>
		        <tr>
		          <td>
		        	  <label class="col-xs-4 col-sm-4 col-md-4 col-lg-4 control-label">处理状态</label>
		        	  <div class="col-xs-5 col-sm-5 col-md-6 col-lg-6">
		        	  <select class="form-control input-sm" name="ReadFlag">
		        	  	%if ReadFlag == "":
		        	  	<option value="None">未处理</option>
	        			<option value="1">已申请处理</option>
	        			<option value="2">处理申请已审核</option>
	        			<option value="3">处理已登记</option>
	        			<option value="4">处理登记已审核</option>
	        			<option value="" selected>全部</option>
	        			%elif ReadFlag == "None":
	        			<option value="None" selected>未处理</option>
	        			<option value="1">已申请处理</option>
	        			<option value="2">处理申请已审核</option>
	        			<option value="3">处理已登记</option>
	        			<option value="4">处理登记已审核</option>
	        			<option value="">全部</option>
	        			%elif ReadFlag == "1":
	        			<option value="None">未处理</option>
	        			<option value="1" selected>已申请处理</option>
	        			<option value="2">处理申请已审核</option>
	        			<option value="3">处理已登记</option>
	        			<option value="4">处理登记已审核</option>
	        			<option value="">全部</option>
	        			%elif ReadFlag == "2":
	        			<option value="None">未处理</option>
	        			<option value="1">已申请处理</option>
	        			<option value="2" selected>处理申请已审核</option>
	        			<option value="3">处理已登记</option>
	        			<option value="4">处理登记已审核</option>
	        			<option value="">全部</option>
	        			%elif ReadFlag == "3":
	        			<option value="None">未处理</option>
	        			<option value="1">已申请处理</option>
	        			<option value="2">处理申请已审核</option>
	        			<option value="3" selected>处理已登记</option>
	        			<option value="4">处理登记已审核</option>
	        			<option value="">全部</option>
	        			%elif ReadFlag == "4":
	        			<option value="None">未处理</option>
	        			<option value="1">已申请处理</option>
	        			<option value="2">处理申请已审核</option>
	        			<option value="3">处理已登记</option>
	        			<option value="4" selected>处理登记已审核</option>
	        			<option value="">全部</option>
	        			%end
		        	  </select>
		        	  </div>
	        	  </td>
	        	  <td>
		        	  <label class="col-xs-4 col-sm-4 col-md-4 col-lg-4 control-label">站点编号</label>
		        	  <div class="col-xs-5 col-sm-5 col-md-6 col-lg-6">
		        	  <select class="form-control input-sm" name="SiteID" id="siteid">
		        	  	%for i in xrange(1, 9):
	        			<option value={{i}}>{{i}}</option>
	        			%end
	        			<option value="" selected>全部</option>
		        	  </select>
		        	  </div>
	        	  </td>
	        	  <td>
		        	  <label class="col-xs-4 col-sm-4 col-md-4 col-lg-4 control-label">车轴数</label>
		        	  <div class="col-xs-5 col-sm-5 col-md-6 col-lg-6">
		        	  <select class="form-control input-sm" name="smWheelCount" id="wheels">
		        	  	%if smWheelCount == "":
			        	  	%for i in xrange(2, 7):
		        			<option value="{{i}}">{{i}}</option>
		        			%end
		        			<option value="" selected>全部</option>
	        			%else:
	        				%for i in xrange(2, 7):
	        				%if str(i) == smWheelCount:
	        				<option value="{{i}}" selected>{{i}}</option>
	        				%else:
		        			<option value="{{i}}">{{i}}</option>
		        			%end
		        			%end
		        			<option value="">全部</option>
	        			%end
		        	  </select>
		        	  </div>
	        	  </td>
	        	</tr>
	        	<tr>
	        		<td>
		        	  <label class="col-xs-4 col-sm-4 col-md-4 col-lg-4 control-label">车牌号</label>
		        	  <div class="col-xs-5 col-sm-5 col-md-6 col-lg-6">
		        	  	<input type="text" class="form-control input-sm" name="VehicheCard" value={{VehicheCard}}>
		        	  </div>
	        	  	</td>
	        	  	<td>
		        	  <label class="col-xs-4 col-sm-4 col-md-4 col-lg-4 control-label">超限率</label>
		        	  <div class="col-xs-5 col-sm-5 col-md-6 col-lg-6">
		        	  	<!--input type="text" class="form-control input-sm" name="smLimitWeightPercent"/-->
		        	  	<select class="form-control input-sm" name="smLimitWeightPercent" id="smLimitWeightPercent">
		        	  	%if smLimitWeightPercent == "":
			        	  	%for i in xrange(10, 110, 10):
		        			<option value="{{i}}">{{i}}</option>
		        			%end
		        			<option value="" selected>全部</option>
	        			%else:
	        				%for i in xrange(10, 110, 10):
		        				%if str(i) == smLimitWeightPercent:
			        			<option value="{{i}}" selected>{{i}}</option>
			        			%else:
			        			<option value="{{i}}">{{i}}</option>
			        			%end
		        			%end
		        			<option value="">全部</option>
	        			%end
		        	  	</select>
		        	  </div>
	        	  	</td>
	        	  	<td>
		        	  <label class="col-xs-4 col-sm-4 col-md-4 col-lg-4 control-label">车重</label>
		        	  <div class="col-xs-5 col-sm-5 col-md-6 col-lg-6">
		        	  	<input type="text" class="form-control input-sm" name="smTotalWeight"/>
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
          %if results is not None:
          	<h3 class="sub-header">数据查询结果</h3>
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
	          	  %for col in res:
	          	    <td>{{col}}</td>
	          	  %end
	          	  <td>
	          	  	<button type="button" class="btn btn-sm btn-primary" onclick="open_window('/details/{{res[0]}}');">
	          	  		查看详情
	          	  	</button>
	          	  	%if res[-1] == "未处理":
	          	  		<!--button class="btn btn-sm btn-primary" 
	          	  				onclick="alert('处理申请已提交!请等待审核!');location.href='/proceed/{{res[0]}}';"-->
	          	  		<button class="btn btn-sm btn-primary" 
	          	  				onclick=
	          	  				"alert('处理申请已提交!请等待审核!');
	          	  				 httpGetAsync('/proceed/{{res[0]}}', console.log);
	          	  				 location.reload();">		
	          	  			申请处理
	          	  		</button>
	          	  	%else:
	          	  		<button>处理中</button>
	          	  	%end
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

%include ('./view/bsfiles/view/html_footer.tpl')