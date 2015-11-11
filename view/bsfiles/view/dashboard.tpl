%include ('./view/bsfiles/view/html_hdr.tpl')

%include ('./view/bsfiles/view/navbar.tpl')

    <div class="container-fluid">
      <div class="row">
        %include ('./view/bsfiles/view/nav_sidebar.tpl')
        <div class="col-xs-8 col-xs-offset-4 col-sm-8 col-sm-offset-4 
                    col-md-10 col-md-offset-2 col-lg-10 col-lg-offset-2 main">
          <h3 class="page-header">数据统计</h3>
          <table class="table table-striped">
            <tbody>
            <form action="/statdata" method="POST">
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
                  <label class="col-xs-4 col-sm-4 col-md-4 col-lg-4 control-label">站点</label>
                  <div class="col-xs-5 col-sm-5 col-md-6 col-lg-6">
                  <select class="form-control input-sm" name="SiteID" id="siteid">
                    %for site in sitenames:
                    <option value={{site[0]}}>{{site[1]}}</option>
                    %end
                  </select>
                  </div>
                </td>
            </tr>
            <tr>
              <td>
                <button type="submit" class="btn btn-md btn-primary" name="query" value="show">
                  查询
                </button>
                <button type="submit" class="btn btn-md btn-success" name="export" value="export">
                  导出
                </button>
              </td>
            </tr>
          </form>
          </tbody>
        </table>

          <!--div class="row placeholders placeholder">
            <div class="col-xs-3 col-sm-3 placeholder">
              <h4>今日超限违章</h4>
              <button class="btn btn-primary" type="button">
                今日违章个数 <span class="badge">0</span>
              </button>
            </div>
            <div class="col-xs-3 col-sm-3 col-md-3 col-lg-3 placeholder">
              <h4>本周超限违章</h4>
              <button class="btn btn-primary" type="button">
                违章个数 <span class="badge">0</span>
              </button>
            </div>
            <div class="col-xs-3 col-sm-3 col-md-3 col-lg-3 placeholder">
              <h4>本月超限违章</h4>
              <button class="btn btn-primary" type="button">
                违章个数 <span class="badge">0</span>
              </button>
            </div>
            <div class="col-xs-3 col-sm-3 col-md-3 col-lg-3 placeholder">
              <h4>黑名单</h4>
              <button class="btn btn-primary" type="button">
                黑名单个数 <span class="badge">0</span>
              </button>
            </div>
          </div-->
          %if query_results:
            %include (query_results)
          %end
          <!--div class="panel panel-info">
            <div class="panel-heading">站点今日各时段违章</div>
              <div class="panel-body">
                <div id="line-stat"></div>
              </div>
          </div-->
        </div>
      </div>
    </div>

    <script src="/static/view/bsfiles/js/jquery.min.js"></script>
    <script src="/static/view/bsfiles/js/bootstrap.min.js"></script>

%include ('./view/bsfiles/view/html_footer.tpl')
