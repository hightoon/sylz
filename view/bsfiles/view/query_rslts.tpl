<div class="panel panel-danger">
  <!-- Default panel contents -->
  <div class="panel-heading">站点超限统计－{{period}}</div>
  <div class="panel-body"></div>
  <!-- Table -->
  %if siteid!="":
  <h4 style="color:red;"><mark>站点超限总数</mark></h4>
  %if numofsite==0:
  	<p class="lead">站点无超限纪录！<br><br></p>
  %else:
  <table class="table">
	<thead>
		<tr>
		  <th>序号</th>
		  <th>站点</th>
		  <th>总超限车次</th>
		  <th>总车次</th>
		</tr>
	</thead>
	<tbody>
		%for i in xrange(numofsite):
		  <tr>
			<td>{{i+1}}</td>
			<td>{{sites[i]}}</td>
			<td>{{sum([res[sites[i]] for res in stat])}}</td>
			<td>{{sum(percent[sites[i]])}}</td>
		  </tr>
		%end
	</tbody>
  </table>
  %end
  <h4 style="color:red;"><mark>站点超限分时段统计</mark></h4>
  %if numofsite==0:
  	<p class="lead">站点无超限纪录！<br><br></p>
  %else:
  %for i in xrange(numofsite):
  	<span style="color: blue">{{sites[i]}}</span>
  	<table class="table">
	<thead>
		<tr>
		  <th>序号</th>
		  <th>时段</th>
		  <th>超限车次</th>
		</tr>
	</thead>
	<tbody>
		%for h in xrange(24):
		  <tr>
			<td>{{h+1}}</td>
			<td>{{h}}:00-{{h+1}}:00</td>
			<td>{{stat[h][sites[i]]}}</td>
	      </tr>
		%end
	</tbody>
  </table>
  %end
  %end
  <h4 style="color:red;"><mark>站点分时段超限率统计</mark></h4>
  %if numofsite==0:
  	<p class="lead">站点无超限纪录！<br><br></p>
  %else:
  <table class="table">
	<thead>
		<tr>
		  <th>序号</th>
		  <th>站点</th>
		  <th>未超限(0%)</th>
		  <th>超限0%~20%</th>
		  <th>超限20%~50%</th>
		  <th>超限50%~100%</th>
		  <th>超限100%以上</th>
		</tr>
	</thead>
	<tbody>
		%for i in xrange(numofsite):
		  <tr>
			<td>{{i+1}}</td>
			<td>{{sites[i]}}</td>
			%for j in xrange(5):
				<td>{{percent[sites[i]][j]}}</td>
			%end
	      </tr>
		%end
	</tbody>
  </table>
  %end
  %else:
  <h4 style="color:red;"><mark>站点超限总数</mark></h4>
  <table class="table">
	<thead>
		<tr>
		  <th>序号</th>
		  <th>站点</th>
		  <th>总超限车次</th>
		  <th>总车次</th>
		</tr>
	</thead>
	<tbody>
		%for i in range(len(sitenames)):
		  <tr>
			<td>{{i+1}}</td>
			<td>{{sitenames[i][1]}}</td>
			%if stat[0].has_key(sitenames[i][1]):
				<td>{{sum([res[sitenames[i][1]] for res in stat])}}</td>
			%else:
				<td>0</td>
			%end
			%if percent.has_key(sitenames[i][1]):
				<td>{{sum(percent[sitenames[i][1]])}}</td>
			%else:
				<td>0</td>
			%end
		  </tr>
		%end
	</tbody>
  </table>
  %end
</div>