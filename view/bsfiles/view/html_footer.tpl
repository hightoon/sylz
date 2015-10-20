<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
	
    <!--script src="/static/view/bsfiles/js/jquery.min.js"></script-->
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <!--script src="/static/view/bsfiles/js/bootstrap.min.js"></script-->
    <script src="/static/view/bsfiles/js/jquery-ui-1.11.4.custom/jquery-ui.js"></script>
    <script type="text/javascript">
    	function open_window(url) {
    		window.open(url, "_blank", "toolbar=yes, scrollbars=yes, resizable=yes, top=500, left=500, width=600, height=500");
    	}

    	//send asynchronous http request
    	function httpGetAsync(theUrl, callback)
		{
		    var xmlHttp = new XMLHttpRequest();
		    xmlHttp.onreadystatechange = function() { 
		        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
		            callback(xmlHttp.responseText);
		    }
		    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
		    xmlHttp.send(null);
		}

    	$( "#startdate" ).datepicker();
      	$( "#enddate" ).datepicker();

      	/*$(function () {
		    $('body').on('click', '.regform-sub', function (e) {
		        document.forms["regform"].submit();
		        $('#register-modula').modal('hide');
		    });
		});*/
		$('#regform-sub').click(function(e){
      		e.preventDefault();
      		//document.forms["regform"].submit();
      		//alert($('#regtime').val());
	      	$.post(document.getElementById("regform").action, 
	         	$('#regform').serialize(), 
	         	function(data, status, xhr){
	           // do something here with response;
	           		alert("处理登记已提交，请等待审核!");
	           		$('#register-modula').modal('hide');
	        });
		});
      	
    </script>
  </body>
</html>
