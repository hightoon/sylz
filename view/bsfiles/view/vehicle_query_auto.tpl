%include ('./view/bsfiles/view/html_hdr.tpl')

%include ('./view/bsfiles/view/navbar.tpl')

    <div class="container-fluid">
      <div class="row">
      	%include ('./view/bsfiles/view/nav_sidebar.tpl')
      	<div class="ccol-xs-9 col-xs-offset-3 col-sm-9 col-sm-offset-3 
                    col-md-10 col-md-offset-2 col-lg-10 col-lg-offset-2 main">
      	  <h3 class="sub-header">数据查询（内部使用）</h3>
      	  <table class="table table-striped">
      	  	<tbody>
	      	  <form id="queryform">
	      	  	<tr>
	      	  	  <td>
		      	  	  <label class="col-xs-4 col-sm-4 col-md-4 col-lg-4 control-label">开始日期</label>
		      	  	  <div class="col-xs-5 col-sm-5 col-md-6 col-lg-6">
		        	  	<input type="text" class="form-control input-sm" id="startdate" name="startdate" 
		        	  	value={{startdate}}>
		        	  </div>
		          </td>
		          <td>
		      	  	  <label class="col-xs-4 col-sm-4 col-md-4 col-lg-4 control-label">结束日期</label>
		      	  	  <div class="col-xs-5 col-sm-5 col-md-6 col-lg-6">
		        	  	<input type="text" class="form-control input-sm" id="enddate" name="enddate" 
		        	  	value={{enddate}}>
		        	  </div>
		          </td>
		          <td>
		      	  	  <label class="col-xs-4 col-sm-4 col-md-4 col-lg-4 control-label">开始时间</label>
		      	  	  <div class="col-xs-5 col-sm-5 col-md-6 col-lg-6">
		        	  	<input type="text" class="form-control input-sm" id="starttime" name="starttime" 
		        	  	value={{starttime}}>
		        	  </div>
		          </td>
                </tr>
                <tr>
		          <td>
		      	  	  <label class="col-xs-4 col-sm-4 col-md-4 col-lg-4 control-label">结束时间</label>
		      	  	  <div class="col-xs-5 col-sm-5 col-md-6 col-lg-6">
		        	  	<input type="text" class="form-control input-sm" id="endtime" name="endtime" 
		        	  	value={{endtime}}>
		        	  </div>
		          </td>
		          <td>
		          	  <label class="col-xs-4 col-sm-4 col-md-4 col-lg-4 control-label">超限率</label>
		        	  <div class="col-xs-2 col-sm-2 col-md-2 col-lg-2">
		        	  	<input type="text" class="form-control input-sm" name="smLimitWeightPercentLow" id="smLimitWeightPercentLow" value="10" />
		        	  </div>
		        	  <div class="col-xs-1 col-sm-1 col-md-1 col-lg-1">~</div>
		        	  <div class="col-xs-2 col-sm-2 col-md-2 col-lg-2">
		        	  	<input type="text" class="form-control input-sm" name="smLimitWeightPercentHigh" id="smLimitWeightPercentHigh" value="100" />
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
		        	  <label class="col-xs-4 col-sm-4 col-md-4 col-lg-4 control-label">站点</label>
		        	  <div class="col-xs-5 col-sm-5 col-md-6 col-lg-6">
		        	  <select class="form-control input-sm" name="SiteID" id="siteid" multiple="multiple">
		        	  	%for site in sites:
		        	  		%if str(site[0]) in SiteID:
	        				<option value={{site[0]}} selected>{{site[1]}}</option>
	        				%else:
	        				<option value={{site[0]}} selected>{{site[1]}}</option>
	        				%end
	        			%end
	        			%if SiteID=="": 
	        			<!--option value="" selected>全部</option-->
	        			%else:
	        			<!--option value="">全部</option-->
	        			%end
		        	  </select>
		        	  </div>
	        	  </td>
	        	</tr>
	        	<tr>
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
	        		<td>
		        	  <label class="col-xs-4 col-sm-4 col-md-4 col-lg-4 control-label">车牌号</label>
		        	  <div class="col-xs-5 col-sm-5 col-md-6 col-lg-6">
		        	  	<input type="text" class="form-control input-sm" name="VehicheCard" value={{VehicheCard}}>
		        	  </div>
	        	  	</td>
	        	</tr>
	        	<tr>
	        	</tr>
	          </form>
	          <tr>
	        	  <td>
	        		<button onclick="postQform();" class="btn btn-md btn-primary" name="query" value="show">查询</button>
	        	  </td>
	        	</tr>
	        </tbody>
          </table>
          %if results is not None:
          	<h3 class="sub-header">数据查询结果 
          		<button class="btn btn-xs btn-info" name="refresh" value="show" id="startButton"
          		onclick="autoRefresh();$(this).prop('disabled',true);$('#stopButton').prop('disabled', false);alert('开始自动刷新纪录，刷新周期：30秒');">
          			自动刷新
          		</button>
          		<button class="btn btn-xs btn-warning" name="refresh" value="show" id="stopButton"
          		onclick="stopRefresh();$(this).prop('disabled',true);$('#startButton').prop('disabled', false);alert('已停止刷新数据!')">
          			停止刷新
          		</button>
          	</h3>

	        <table class="table" id="veh-table">  
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
	          	  <tr onclick="$('.table tr').css('background-color', 'transparent');this.style.backgroundColor='green';">
	          	  %for i, col in enumerate(res):
	          	    <td>{{col}}</td>
	          	  %end
	          	  <td>
	          	  	<button type="button" class="btn btn-sm btn-primary" 
	          	  			onclick="open_window('/details/{{res[0]}}');">
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
    <script src="/static/view/bsfiles/js/jquery-1.8.2.min.js"></script>
    <!--script src="/static/view/bsfiles/js/jquery-ui-1.11.4.custom/external/jquery/jquery.js"></script-->
    <script src="/static/view/bsfiles/js/jquery.dataTables.min.js"></script>
    <script src="/static/view/bsfiles/js/bootstrap-clockpicker.js"></script>
    <script src="/static/view/bsfiles/js/bootstrap-multiselect.js"></script>
    <script type="text/javascript">
    	$(document).ready(function() {
		    var tab = $('#veh-table').DataTable();
			$('#starttime').clockpicker();
			$('#endtime').clockpicker();
			// siteid multiselect
			$('#siteid').multiselect({
				includeSelectAllOption: true,
				onChange: function(option, checked) {
					//console.log(option, checked);
				},
	            onDropdownShown: function(event) {
	                alert('Dropdown closed.');
	            }
	        });
		} );

		function refresh() {
			$.get("/query/multisites/rawdata", function(data){
				var table = $('#veh-table').dataTable();
				var oSettings = table.fnSettings();
				table.fnClearTable(this);
				for (var i=0; i<data.data.length; i++)
			    {
			    	var row = data.data[i];
			    	var button = `<button type="button" class="btn btn-sm btn-primary" 
	          	  			onclick="open_window('/details/${row[0]}');">
	          	  		查看详情
	          	  	</button>`;
			    	row.push(button);
			      	table.oApi._fnAddData(oSettings, row);
			    }

			    $('#veh-table tbody').on('click', 'tr', function () {
			        $('#veh-table tr').css('background-color', 'transparent');
					this.style.backgroundColor='green';
			    } );

			    oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
			    table.fnDraw();
			});
		}

		function update_veh_tab(data) {
			var table = $('#veh-table').dataTable();
			var oSettings = table.fnSettings();
			table.fnClearTable(this);
			for (var i=0; i<data.data.length; i++) 
		    {
		    	var row = data.data[i];
		    	var button = `<button type="button" class="btn btn-sm btn-primary" 
          	  			onclick="open_window('/details/${row[0]}');">
          	  		查看详情
          	  	</button>`;
		    	row.push(button);
		      	table.oApi._fnAddData(oSettings, row);
		    }

		    $('#veh-table tbody').on('click', 'tr', function () {
		        $('#veh-table tr').css('background-color', 'transparent');
				this.style.backgroundColor='green';
		    } );

		    oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
		    table.fnDraw();
		}

		function autoRefresh() {
			window.refreshTid = setInterval(function(){
				console.log('refreshed...');
				refresh();
			}, 30000);
		}

		function autoRefreshTimeout() {
			refresh();
			setTimeout(function(){console.log('reload table'); autoRefresh();}, 30000);
		}

		function stopRefresh() {
			if (window.refreshTid) {
				clearInterval(window.refreshTid);
				window.refreshTid = null;
			}
		}

		function postQform() {
			//console.log($('#queryform').serialize());
			$.post( "/query/multisites", 
					$( "#queryform" ).serialize() + '&' + $.param({SiteID: $('#siteid').val().join(',')}),
					function(data){
						update_veh_tab(data);
					} 
			);
		}
    </script>

%include ('./view/bsfiles/view/html_footer.tpl')