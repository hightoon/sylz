%include ('./view/bsfiles/view/html_hdr.tpl')

    <!--div class="container"-->

      <form class="form-signin" action="/login" method="POST">
        <!--h2 class="form-signin-heading" class="sr-only">登录信息管理系统</h2-->
        <label for="inputEmail" class="sr-only">用户名</label>
        <input type="text" id="inputEmail" name="usrname" class="form-control" placeholder="用户名" required autofocus>
        <label for="inputPassword" class="sr-only">密码</label>
        <input type="password" id="inputPassword" name="passwd" class="form-control" placeholder="密码" required>
        <div class="checkbox">
          <label class="sr-only">
            <input type="checkbox" name="rememberme" value="remember-me"> 记住我
          </label>
        </div>
        <button class="btn btn-sm btn-primary btn-block" type="submit">登录</button>
      </form>
      <!--span class="compinfo">Powered By Sifang</span><br>
      <span class="verinfo">版本: 0.0.1</span-->
    <!--/div--> <!-- /container -->

%include ('./view/bsfiles/view/html_footer.tpl')
