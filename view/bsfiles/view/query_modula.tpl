<div class="modal fade" tabindex="-1" role="document" id="rec-modula-{{res[1][0]}}">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <h3 class="sub-header">纪录详情</h3>
	  <table class="table" id="query-table">  
	    <thead>
	        <tr>
	      	  %for col in details[0]:
	      	    <th class="rotate"><div><span>{{col}}</span></div></th>
	      	  %end
	      	</tr>
	    </thead>
	    <tbody>
	      	<tr>
	      	  %for col in res[1][:-3]:
	      	    <td>{{col}}</td>
	      	  %end
	      	</tr>
	    </tbody>
	  </table>
	    <!--div id="carousel-example-generic" class="carousel slide" data-ride="carousel">
		  <ol class="carousel-indicators">
		    <li data-target="#carousel-example-generic" data-slide-to="0"></li>
		    <li data-target="#carousel-example-generic" data-slide-to="1"></li>
		  </ol>

		  <h4>车辆照片</h4>
		  <div class="carousel-inner" role="listbox">
		    <div class="item active">
		      <img src="{{imgpath}}{{res[1][-3]}}" alt="车头照片">
		      <div class="carousel-caption">
		        车头照片
		      </div>
		    </div>
		    <div class="item">
		      <img src="{{imgpath}}{{res[1][-2]}}" alt="车尾照片">
		      <div class="carousel-caption">
		        车尾照片
		      </div>
		    </div>
		  </div>

		  <a class="left carousel-control" href="#carousel-example-generic" role="button" data-slide="prev">
		    <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
		    <span class="sr-only">Previous</span>
		  </a>
		  <a class="right carousel-control" href="#carousel-example-generic" role="button" data-slide="next">
		    <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
		    <span class="sr-only">Next</span>
		  </a>
		</div-->
		<div class="item">
	      <img src="/static/{{res[1][-3]}}" alt="车头照片" width="860px" height="600px">
	      <div class="carousel-caption">
	        车头照片
	      </div>
	    </div>
	    <br>
	    <div class="item">
	      <img src="/static/{{res[1][-2]}}" alt="车尾照片" width="860px" height="600px">
	      <div class="carousel-caption">
	        车尾照片
	      </div>
	    </div>
		<a class="link printbut" href="javascript:window.print();">打印</a>
    </div>
  </div>
</div>