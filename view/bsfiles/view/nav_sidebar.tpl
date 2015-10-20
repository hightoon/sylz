        <div class="col-xs-3 col-sm-3 col-md-2 col-lg-2 sidebar">
          <ul class="nav nav-sidebar">
            <li>
              <span class="glyphicon glyphicon-hand-right" aria-hidden="true">
                <a href="/index" class="fst-level-side-menu">数据统计</a>
              </span>
            </li>
          </ul>
          <ul class="nav nav-sidebar">
            <li><span class="glyphicon glyphicon-hand-right" aria-hidden="true">
              <a href="/query" class="fst-level-side-menu">数据查询</a>
            </span>
            </li>
          </ul>
          <ul class="nav nav-sidebar">
            <li><span class="glyphicon glyphicon-hand-down" aria-hidden="true">
              <a href="#" class="fst-level-side-menu">超限纪录审核</a></span>
            </li>
            %if "超限处理" in privs:
              <li><span><a href="/proceed" class="subsidebar">超限处理</a></span></li>
            %end
            %if "处理审核" in privs:
              <li><span><a href="/proceed_approval" class="subsidebar">处理审核</a></span></li>
            %end
          </ul>
          <ul class="nav nav-sidebar">
            <li><span class="glyphicon glyphicon-hand-down" aria-hidden="true">
              <a href="#" class="fst-level-side-menu">超限处理登记</a>
            </span></li>
            %if "超限处理登记" in privs:
              <li><span><a href="/register" class="subsidebar">增删纪录</a></span></li>
            %end
            %if "超限处理登记审核" in privs:
              <li><span><a href="/reg_approval" class="subsidebar">登记审核</a></span></li>
            %end
          </ul>
          <ul class="nav nav-sidebar">
            <li><span class="glyphicon glyphicon-hand-down" aria-hidden="true">
              <a href="#" class="fst-level-side-menu">黑名单管理</a>
            </span></li>
            <li><span><a href="/blacklist_query" class="subsidebar">查询</a></span></li>
            %if "黑名单增删" in privs:
              <li><span><a href="/blacklist_mng" class="subsidebar">添加删除</a></span></li>
            %end
            %if "黑名单审核" in privs:
              <li><span><a href="/blacklist_approval" class="subsidebar">审核</a></span></li>
            %end
          </ul>
          <ul class="nav nav-sidebar">
            %if "用户增删" in privs:
              <li><span class="glyphicon glyphicon-hand-right" aria-hidden="false">
                <a href="/account_mngn">用户管理</a>
              </span></li>
              <!--li><a href="/account_mngn">添加删除</a></li-->
            %end
          </ul>
        </div>