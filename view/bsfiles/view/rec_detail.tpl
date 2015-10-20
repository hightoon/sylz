%include ('./view/bsfiles/view/html_hdr.tpl')
<div class="panel {{panel_type}}">
  <div class="panel-heading">
    <h3 class="panel-title">记录详情</h3>
  </div>
  <div class="panel-body">
  </div>
  <table class="table table-bordered">
  	%for i in xrange(0, length, 2):
  		<tr>
    	%if (i==4 or i==10) and "danger" in panel_type:
    		<td class="danger">
    			<label>{{detail[0][i]}}:&nbsp</label>
		    		<span>{{detail[1][i]}}</span>
		    </td>
    	%else:
    		<td>
    			<label>{{detail[0][i]}}:&nbsp</label>
		    		<span>{{detail[1][i]}}</span>
		    </td>
    	%end
			<td>
				<label>{{detail[0][i+1]}}:&nbsp</label>
	    		<span>{{detail[1][i+1]}}</span>
			</td>
    	</tr>
	%end
	<tr>
	    <td>
	    	<label>车头照片:&nbsp</label>
  			<img src="{{imgpath}}{{detail[1][-3]}}" alt="{{imgpath}}{{detail[1][-3]}}">
	    </td>
	</tr>
	<tr>
	    <td>
	    	<label>车尾照片:&nbsp</label>
  			<img src="{{imgpath}}{{detail[1][-2]}}" alt="{{imgpath}}{{detail[1][-2]}}">
	    </td>
	<tr>
  </table>
  <div class="panel-heading panel-warning">
    <h4 class="panel-title">历史信息</h4>
  </div>
  <div class="panel-body">
  </div>
  <table class="table table-bordered">
  	<tr>
  		%for item in history_recs[0]:
  			<th>{{item}}</th>
  		%end
  		<th>车头图</th>
  		<th>车尾图</th>
  	</tr>
  	%for rec in history_recs[1:]:
  		<tr>
  		%for i in xrange(0, len(history_recs[0])):
  			%if (i==3) and isblack:
		    	<td class="danger">{{rec[i]}}</td>
		    %elif (i==0) and rec[-1]=="未处理":
		    	<td class="danger">{{rec[i]}}</td>
		    %else:
		    	<td>{{rec[i]}}</td>
		    %end
  		%end
  		<td><a href="{{imgpath}}{{rec[-3]}}">点击查看</a></td>
  		<td><a href="{{imgpath}}{{rec[-2]}}">点击查看</a></td>
  		</tr>
  	%end
  </table>
</div>


%include ('./view/bsfiles/view/html_footer.tpl')